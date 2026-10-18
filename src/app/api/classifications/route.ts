import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    const classes = await prisma.pharmacologicalClass.findMany({
      include: {
        children: {
          include: {
            drugs: true,
            ingredients: true,
          },
        },
        drugs: {
          include: {
            ingredients: {
              include: {
                ingredient: true,
              },
            },
          },
        },
        ingredients: true,
      },
      orderBy: { nameRu: 'asc' },
    });

    const atcCodes = await prisma.aTCCode.findMany({
      include: {
        children: true,
        drugs: true,
        ingredients: true,
      },
      orderBy: { code: 'asc' },
    });

    return NextResponse.json({
      success: true,
      pharmacologicalClasses: classes,
      atcCodes: atcCodes,
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
