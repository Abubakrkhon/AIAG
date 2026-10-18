import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('q') || '';
    const category = searchParams.get('category');
    const limit = parseInt(searchParams.get('limit') || '50', 10);

    const whereCondition: any = {};

    if (search) {
      whereCondition.OR = [
        { tradeNameRu: { contains: search } },
        { tradeNameEn: { contains: search } },
        { synonyms: { contains: search } },
        {
          ingredients: {
            some: {
              ingredient: {
                OR: [
                  { innRu: { contains: search } },
                  { innEn: { contains: search } },
                  { latinName: { contains: search } },
                ],
              },
            },
          },
        },
      ];
    }

    if (category) {
      whereCondition.pharmClass = {
        code: category,
      };
    }

    const drugs = await prisma.drug.findMany({
      where: whereCondition,
      take: limit,
      include: {
        pharmClass: true,
        atcCode: true,
        manufacturer: true,
        ingredients: {
          include: {
            ingredient: true,
          },
        },
        images: true,
      },
      orderBy: { tradeNameRu: 'asc' },
    });

    return NextResponse.json({ success: true, count: drugs.length, data: drugs });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
