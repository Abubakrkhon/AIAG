'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { GitCompare, Pill, Plus, X, ArrowRight, Activity, Zap, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function ComparePage() {
  const [allDrugs, setAllDrugs] = useState<any[]>([]);
  const [selectedDrugIds, setSelectedDrugIds] = useState<string[]>([]);
  const [comparedDrugs, setComparedDrugs] = useState<any[]>([]);

  useEffect(() => {
    async function loadDrugs() {
      try {
        const res = await fetch('/api/drugs');
        const data = await res.json();
        if (data.success && data.data.length > 0) {
          setAllDrugs(data.data);
          // Pre-select first 2 drugs for comparison demo
          const initialIds = data.data.slice(0, 2).map((d: any) => d.id);
          setSelectedDrugIds(initialIds);
        }
      } catch (e) {
        console.error('Failed to load drugs', e);
      }
    }
    loadDrugs();
  }, []);

  useEffect(() => {
    async function fetchDetailedDrugs() {
      if (selectedDrugIds.length === 0) {
        setComparedDrugs([]);
        return;
      }

      const promises = selectedDrugIds.map((id) =>
        fetch(`/api/drugs/${id}`).then((res) => res.json())
      );

      const results = await Promise.all(promises);
      const valid = results.filter((r) => r.success).map((r) => r.data);
      setComparedDrugs(valid);
    }

    fetchDetailedDrugs();
  }, [selectedDrugIds]);

  const toggleDrug = (id: string) => {
    if (selectedDrugIds.includes(id)) {
      setSelectedDrugIds(selectedDrugIds.filter((d) => d !== id));
    } else {
      if (selectedDrugIds.length >= 3) {
        alert('Максимум 3 препарата для одноновременного сравнения.');
        return;
      }
      setSelectedDrugIds([...selectedDrugIds, id]);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <GitCompare className="w-8 h-8 text-blue-400" />
          Сравнение лекарственных препаратов
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-3xl">
          Сравнительный анализ показателей фармакодинамики, кинетики, показаний, дозировок и безопасности двух или трех препаратов.
        </p>
      </div>

      {/* Drug Selector */}
      <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 space-y-4 shadow-xl">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-300">
          Выберите препараты для сравнения (до 3-х):
        </h2>

        <div className="flex flex-wrap gap-2">
          {allDrugs.map((drug) => {
            const isSelected = selectedDrugIds.includes(drug.id);
            return (
              <button
                key={drug.id}
                onClick={() => toggleDrug(drug.id)}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 border ${
                  isSelected
                    ? 'bg-blue-500 text-slate-950 border-blue-400 shadow-lg shadow-blue-500/20'
                    : 'bg-slate-950 text-slate-300 border-slate-800 hover:bg-slate-800'
                }`}
              >
                <Pill className="w-3.5 h-3.5" />
                {drug.tradeNameRu} ({drug.dosageStrength})
                {isSelected ? <X className="w-3.5 h-3.5" /> : <Plus className="w-3.5 h-3.5 text-slate-500" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Comparison Matrix Table */}
      {comparedDrugs.length > 0 ? (
        <div className="overflow-x-auto rounded-3xl border border-slate-800 bg-slate-900 shadow-2xl">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/80">
                <th className="p-4 sm:p-6 w-1/4 text-slate-400 uppercase tracking-wider font-bold">Характеристика</th>
                {comparedDrugs.map((drug) => (
                  <th key={drug.id} className="p-4 sm:p-6 text-slate-100 font-extrabold text-sm border-l border-slate-800">
                    <div className="flex items-center justify-between">
                      <Link href={`/drugs/${drug.id}`} className="hover:text-emerald-400 transition-colors">
                        {drug.tradeNameRu}
                      </Link>
                      <button onClick={() => toggleDrug(drug.id)} className="text-slate-500 hover:text-rose-400">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                    <span className="text-xs font-normal text-emerald-400 block mt-1">
                      {drug.ingredients.map((i: any) => i.ingredient.innRu).join(', ')}
                    </span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Лекарственная форма</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800">{d.form} ({d.dosageStrength})</td>
                ))}
              </tr>
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Фармакологическая группа</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800 text-teal-300">{d.pharmClass?.nameRu || 'Н/Д'}</td>
                ))}
              </tr>
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Молекулярная мишень</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800">
                    {d.ingredients[0]?.ingredient?.mechanisms[0]?.target || 'Н/Д'}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Период полувыведения (T1/2)</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800 font-semibold text-emerald-400">
                    {d.ingredients[0]?.ingredient?.kinetics[0]?.halfLife || 'Н/Д'}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Биодоступность</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800">
                    {d.ingredients[0]?.ingredient?.kinetics[0]?.bioavailability || 'Н/Д'}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Основные показания</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800">
                    <ul className="list-disc list-inside space-y-1">
                      {d.indications?.map((ind: any) => (
                        <li key={ind.id}>{ind.title}</li>
                      ))}
                    </ul>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-4 sm:p-6 font-bold text-slate-400">Ключевые противопоказания</td>
                {comparedDrugs.map((d) => (
                  <td key={d.id} className="p-4 sm:p-6 border-l border-slate-800 text-rose-300">
                    <ul className="list-disc list-inside space-y-1">
                      {d.contraindications?.map((ci: any) => (
                        <li key={ci.id}>{ci.title}</li>
                      ))}
                    </ul>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <div className="p-12 text-center text-slate-400 bg-slate-900 border border-slate-800 rounded-3xl">
          Выберите хотя бы один препарат для отображения таблицы сравнения.
        </div>
      )}
    </div>
  );
}
