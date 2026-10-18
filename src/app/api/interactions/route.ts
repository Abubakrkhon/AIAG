import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { ingredientIds, drugIds } = body;

    let targetIngredientIds: string[] = ingredientIds || [];

    // If drug IDs provided, gather all associated ingredient IDs
    if (drugIds && drugIds.length > 0) {
      const drugsWithIngredients = await prisma.drugActiveIngredient.findMany({
        where: { drugId: { in: drugIds } },
        select: { ingredientId: true },
      });
      const extractedIds = drugsWithIngredients.map((d) => d.ingredientId);
      targetIngredientIds = Array.from(new Set([...targetIngredientIds, ...extractedIds]));
    }

    if (targetIngredientIds.length < 2) {
      return NextResponse.json({
        success: true,
        message: 'Укажите минимум 2 действующее вещества или препарата для проверки взаимодействий.',
        interactions: [],
      });
    }

    const interactions = await prisma.drugInteraction.findMany({
      where: {
        OR: [
          {
            ingredientAId: { in: targetIngredientIds },
            ingredientBId: { in: targetIngredientIds },
          },
          {
            ingredientAId: { in: targetIngredientIds },
            ingredientBId: { in: targetIngredientIds },
          },
        ],
      },
      include: {
        ingredientA: true,
        ingredientB: true,
      },
    });

    return NextResponse.json({
      success: true,
      checkedIngredientsCount: targetIngredientIds.length,
      interactionsFound: interactions.length,
      interactions,
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
