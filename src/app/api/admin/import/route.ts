import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(request: Request) {
  try {
    const data = await request.json();

    if (Array.isArray(data)) {
      let importedCount = 0;
      for (const item of data) {
        if (item.tradeNameRu) {
          await prisma.drug.create({
            data: {
              tradeNameRu: item.tradeNameRu,
              tradeNameEn: item.tradeNameEn || null,
              synonyms: item.synonyms || null,
              form: item.form || 'Таблетки',
              dosageStrength: item.dosageStrength || '100 мг',
              packaging: item.packaging || null,
              compositionExcipients: item.compositionExcipients || null,
              isPrescription: Boolean(item.isPrescription),
            },
          });
          importedCount++;
        }
      }
      return NextResponse.json({ success: true, count: importedCount, message: `Успешно импортировано ${importedCount} препаратов.` });
    } else if (data.tradeNameRu) {
      const drug = await prisma.drug.create({
        data: {
          tradeNameRu: data.tradeNameRu,
          tradeNameEn: data.tradeNameEn || null,
          synonyms: data.synonyms || null,
          form: data.form || 'Таблетки',
          dosageStrength: data.dosageStrength || '100 мг',
          packaging: data.packaging || null,
          compositionExcipients: data.compositionExcipients || null,
          isPrescription: Boolean(data.isPrescription),
        },
      });
      return NextResponse.json({ success: true, count: 1, data: drug });
    }

    return NextResponse.json({ success: false, error: 'Неверный формат данных JSON' }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
