import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('q') || '';
    const type = searchParams.get('type') || 'ALL'; // TRADE_NAME, INN, PHARM_CLASS, ATC, MECHANISM, INDICATION, ALL

    if (!query || query.trim().length === 0) {
      return NextResponse.json({ success: true, results: [] });
    }

    const q = query.trim();

    const [drugs, ingredients, pharmClasses, atcCodes] = await Promise.all([
      // 1. Search Drugs by Trade Name, Synonyms, Indications
      prisma.drug.findMany({
        where: {
          OR: [
            { tradeNameRu: { contains: q } },
            { tradeNameEn: { contains: q } },
            { synonyms: { contains: q } },
            { indications: { some: { title: { contains: q } } } },
          ],
        },
        include: {
          pharmClass: true,
          ingredients: {
            include: {
              ingredient: true,
            },
          },
          images: true,
        },
        take: 10,
      }),

      // 2. Search Active Ingredients by INN, Mechanism
      prisma.activeIngredient.findMany({
        where: {
          OR: [
            { innRu: { contains: q } },
            { innEn: { contains: q } },
            { latinName: { contains: q } },
            { mechanisms: { some: { target: { contains: q } } } },
            { mechanisms: { some: { molecularMechanism: { contains: q } } } },
          ],
        },
        include: {
          drugs: {
            include: {
              drug: true,
            },
          },
          mechanisms: true,
        },
        take: 10,
      }),

      // 3. Search Pharm Classes
      prisma.pharmacologicalClass.findMany({
        where: {
          OR: [
            { nameRu: { contains: q } },
            { nameEn: { contains: q } },
            { code: { contains: q } },
          ],
        },
        take: 5,
      }),

      // 4. Search ATC Codes
      prisma.aTCCode.findMany({
        where: {
          OR: [
            { code: { contains: q } },
            { nameRu: { contains: q } },
            { nameEn: { contains: q } },
          ],
        },
        take: 5,
      }),
    ]);

    return NextResponse.json({
      success: true,
      query: q,
      results: {
        drugs,
        ingredients,
        pharmClasses,
        atcCodes,
      },
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
