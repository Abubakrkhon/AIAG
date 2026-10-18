export const dynamic = 'force-dynamic';

import Link from 'next/link';
import { prisma } from '@/lib/prisma';
import { Layers, BookOpen, Pill, ChevronRight, Hash } from 'lucide-react';

export default async function ClassificationsPage() {
  const [classes, atcCodes] = await Promise.all([
    prisma.pharmacologicalClass.findMany({
      include: {
        drugs: true,
        ingredients: true,
      },
      orderBy: { nameRu: 'asc' },
    }),
    prisma.aTCCode.findMany({
      include: {
        drugs: true,
        ingredients: true,
      },
      orderBy: { code: 'asc' },
    }),
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <Layers className="w-8 h-8 text-teal-400" />
          Иерархическая классификация фармакологии
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-3xl">
          Классификация лекарственных средств по фармакологическому действию, механизмам, терапевтическому применению и кодам анатомо-терапевтическо-химической систем (ATC).
        </p>
      </div>

      {/* Pharmacological Classes */}
      <section className="space-y-6">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2 border-b border-slate-800 pb-3">
          <BookOpen className="w-5 h-5 text-emerald-400" />
          Фармакологические группы
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {classes.map((cls) => (
            <div
              key={cls.id}
              id={cls.code || undefined}
              className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4 shadow-xl"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                    {cls.nameRu}
                  </h3>
                  {cls.nameEn && <p className="text-xs text-slate-400 italic">{cls.nameEn}</p>}
                </div>
                {cls.code && (
                  <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-lg bg-teal-500/10 text-teal-300 border border-teal-500/20 shrink-0">
                    {cls.code}
                  </span>
                )}
              </div>

              {cls.description && (
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
                  {cls.description}
                </p>
              )}

              {cls.drugs.length > 0 && (
                <div className="space-y-2 pt-2">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
                    Представители группы:
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {cls.drugs.map((d) => (
                      <Link
                        key={d.id}
                        href={`/drugs/${d.id}`}
                        className="text-xs px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-emerald-500 hover:text-slate-950 text-emerald-400 font-semibold transition-all flex items-center gap-1.5 border border-slate-700/60"
                      >
                        <Pill className="w-3.5 h-3.5" />
                        {d.tradeNameRu} ({d.dosageStrength})
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* ATC Codes Classification */}
      <section className="space-y-6">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2 border-b border-slate-800 pb-3">
          <Hash className="w-5 h-5 text-cyan-400" />
          Анатомо-терапевтически-химическая классификация (ATC / АТХ)
        </h2>

        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {atcCodes.map((atc) => (
              <div
                key={atc.id}
                className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                      {atc.code}
                    </span>
                    <span className="text-sm font-semibold text-slate-200">{atc.nameRu}</span>
                  </div>
                  {atc.nameEn && <p className="text-xs text-slate-400 mt-0.5">{atc.nameEn}</p>}
                </div>
                <span className="text-xs text-slate-500">Уровень {atc.level}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
