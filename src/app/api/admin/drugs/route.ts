import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const {
      tradeNameRu,
      tradeNameEn,
      synonyms,
      form,
      dosageStrength,
      packaging,
      isPrescription,
      compositionExcipients,
      pharmClassId,
      atcCodeId,
      manufacturerId,
      ingredientId,
      ingredientAmount,
    } = body;

    if (!tradeNameRu || !form || !dosageStrength) {
      return NextResponse.json(
        { success: false, error: 'Обязательные поля: tradeNameRu, form, dosageStrength' },
        { status: 400 }
      );
    }

    const drug = await prisma.drug.create({
      data: {
        tradeNameRu,
        tradeNameEn,
        synonyms,
        form,
        dosageStrength,
        packaging,
        isPrescription: Boolean(isPrescription),
        compositionExcipients,
        pharmClassId: pharmClassId || null,
        atcCodeId: atcCodeId || null,
        manufacturerId: manufacturerId || null,
        ingredients: ingredientId
          ? {
              create: [
                {
                  ingredientId,
                  amount: ingredientAmount || dosageStrength,
                },
              ],
            }
          : undefined,
      },
    });

    return NextResponse.json({ success: true, data: drug });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
