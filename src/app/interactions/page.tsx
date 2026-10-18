'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ShieldAlert, AlertTriangle, CheckCircle2, Pill, Plus, X } from 'lucide-react';

export default function InteractionsPage() {
  const [allDrugs, setAllDrugs] = useState<any[]>([]);
  const [selectedDrugIds, setSelectedDrugIds] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadDrugs() {
      try {
        const res = await fetch('/api/drugs');
        const data = await res.json();
        if (data.success) {
          setAllDrugs(data.data);
          // Preselect first two if available
          if (data.data.length >= 2) {
            setSelectedDrugIds([data.data[0].id, data.data[1].id]);
          }
        }
      } catch (e) {
        console.error('Failed to load drugs', e);
      }
    }
    loadDrugs();
  }, []);

  const handleCheck = async () => {
    if (selectedDrugIds.length < 2) return;
    setLoading(true);
    try {
      const res = await fetch('/api/interactions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ drugIds: selectedDrugIds }),
      });
      const data = await res.json();
      if (data.success) {
        setResult(data);
      }
    } catch (e) {
      console.error('Interaction check failed', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedDrugIds.length >= 2) {
      handleCheck();
    } else {
      setResult(null);
    }
  }, [selectedDrugIds]);

  const toggleDrug = (id: string) => {
    if (selectedDrugIds.includes(id)) {
      setSelectedDrugIds(selectedDrugIds.filter((d) => d !== id));
    } else {
      setSelectedDrugIds([...selectedDrugIds, id]);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <ShieldAlert className="w-8 h-8 text-amber-400" />
          Система проверки лекарственных взаимодействий
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-3xl">
          Выберите два или более препарата для анализа фармакодинамических и фармакокинетических взаимодействий, потенциальных рисков и клинических рекомендаций.
        </p>
      </div>

      {/* Selector Box */}
      <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 space-y-4 shadow-xl">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">
          Выберите препараты для проверки:
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
                    ? 'bg-emerald-500 text-slate-950 border-emerald-400 shadow-lg shadow-emerald-500/20'
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

      {/* Results Display */}
      {result && (
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              Результаты анализа комбинированного приема ({result.interactionsFound} обнаружено)
            </h3>
            {loading && <span className="text-xs text-amber-400 animate-pulse">Анализ...</span>}
          </div>

          {result.interactionsFound === 0 ? (
            <div className="p-6 rounded-2xl bg-emerald-950/20 border border-emerald-800/40 text-center space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
              <p className="text-sm font-bold text-emerald-300">
                Клинически значимых опасных взаимодействий между выбранными препаратами не выявлено.
              </p>
              <p className="text-xs text-slate-400">
                Тем не менее всегда соблюдайте интервалы приема и назначения лечащего врача.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {result.interactions.map((item: any) => (
                <div
                  key={item.id}
                  className={`p-6 rounded-2xl border space-y-3 ${
                    item.severity === 'HIGH' || item.severity === 'CONTRAINDICATED'
                      ? 'bg-rose-950/20 border-rose-800/50'
                      : 'bg-amber-950/20 border-amber-800/50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200">
                      Взаимодействие: {item.ingredientA.innRu} + {item.ingredientB.innRu}
                    </span>
                    <span
                      className={`text-xs font-bold px-2.5 py-1 rounded ${
                        item.severity === 'HIGH' ? 'bg-rose-500 text-slate-950' : 'bg-amber-500 text-slate-950'
                      }`}
                    >
                      Степень риска: {item.severity}
                    </span>
                  </div>

                  <div className="space-y-2 text-xs">
                    <p className="text-slate-200">
                      <strong>Механизм:</strong> {item.mechanism}
                    </p>
                    <p className="text-slate-300">
                      <strong>Клиническое последствие:</strong> {item.clinicalConsequence}
                    </p>
                    <p className="text-amber-300 font-semibold bg-amber-950/40 p-3 rounded-xl border border-amber-800/30">
                      <strong>Рекомендации:</strong> {item.recommendation}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
