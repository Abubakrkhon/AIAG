export const dynamic = 'force-dynamic';

import Link from 'next/link';
import { prisma } from '@/lib/prisma';
import { Pill, ExternalLink } from 'lucide-react';

export default async function DrugsCatalogPage() {
  const drugs = await prisma.drug.findMany({
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

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <Pill className="w-8 h-8 text-emerald-400" />
          Энциклопедия лекарственных средств
        </h1>
        <p className="text-sm text-slate-400 mt-2">
          Полный каталог зарегистрированных препаратов с проверенной инструкцией по медицинскому применению.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {drugs.map((drug) => (
          <Link
            key={drug.id}
            href={`/drugs/${drug.id}`}
            className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800/80 transition-all flex flex-col justify-between group shadow-xl"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-3">
                <div>
                  <h2 className="text-xl font-extrabold text-slate-100 group-hover:text-emerald-400 transition-colors">
                    {drug.tradeNameRu}
                  </h2>
                  {drug.tradeNameEn && (
                    <p className="text-xs text-slate-400 italic">{drug.tradeNameEn}</p>
                  )}
                </div>
                <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold shrink-0">
                  {drug.dosageStrength}
                </span>
              </div>

              <div className="space-y-2 text-xs text-slate-300">
                <p>
                  <strong className="text-slate-400">МНН:</strong>{' '}
                  <span className="text-emerald-300 font-medium">
                    {drug.ingredients.map((i) => i.ingredient.innRu).join(', ')}
                  </span>
                </p>
                <p>
                  <strong className="text-slate-400">Форма:</strong> {drug.form}
                </p>
                {drug.pharmClass && (
                  <p>
                    <strong className="text-slate-400">Фармгруппа:</strong> {drug.pharmClass.nameRu}
                  </p>
                )}
                {drug.manufacturer && (
                  <p>
                    <strong className="text-slate-400">Производитель:</strong> {drug.manufacturer.name} ({drug.manufacturer.country})
                  </p>
                )}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-emerald-400 font-semibold group-hover:translate-x-1 transition-transform">
              <span>Открыть карточку препарата</span>
              <ExternalLink className="w-4 h-4" />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
