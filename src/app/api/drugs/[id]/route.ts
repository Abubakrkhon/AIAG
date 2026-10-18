import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    const drug = await prisma.drug.findUnique({
      where: { id },
      include: {
        pharmClass: {
          include: {
            parent: true,
          },
        },
        atcCode: true,
        manufacturer: true,
        ingredients: {
          include: {
            ingredient: {
              include: {
                mechanisms: true,
                kinetics: true,
              },
            },
          },
        },
        indications: true,
        contraindications: true,
        adverseReactions: true,
        dosages: true,
        warnings: true,
        images: true,
        registrations: true,
        sources: true,
      },
    });

    if (!drug) {
      return NextResponse.json({ success: false, error: 'Drug not found' }, { status: 404 });
    }

    return NextResponse.json({ success: true, data: drug });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
