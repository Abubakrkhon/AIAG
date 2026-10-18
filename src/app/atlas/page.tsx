'use client';

import { useState } from 'react';
import { Activity, ShieldAlert, Zap, Layers, Info } from 'lucide-react';

export default function AtlasPage() {
  const [selectedDiagram, setSelectedDiagram] = useState<'GPCR' | 'COX' | 'CCB' | 'SYNAPSE'>('GPCR');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <Activity className="w-8 h-8 text-cyan-400" />
          Интерактивный атлас механизмов действия
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-3xl">
          Наглядная визуализация взаимодействия лекарств с мембранными и внутриклеточными мишенями: GPCR-рецепторы, ионные каналы, ферменты и синаптическая передача.
        </p>
      </div>

      {/* Diagram Selector */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800 text-xs font-semibold">
        {[
          { id: 'GPCR', label: 'G-белок сопряженные рецепторы (GPCR)' },
          { id: 'COX', label: 'Ингибирование ЦОГ-1 / ЦОГ-2 (НПВП)' },
          { id: 'CCB', label: 'Блокада кальциевых каналов (L-тип)' },
          { id: 'SYNAPSE', label: 'Синаптическая передача (Холинергический/Адренергический)' },
        ].map((item) => (
          <button
            key={item.id}
            onClick={() => setSelectedDiagram(item.id as any)}
            className={`px-4 py-2.5 rounded-xl whitespace-nowrap transition-all ${
              selectedDiagram === item.id
                ? 'bg-cyan-500 text-slate-950 font-bold shadow-lg shadow-cyan-500/20'
                : 'bg-slate-900 text-slate-300 hover:bg-slate-800 border border-slate-800'
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {/* SVG Interactive Visualizer */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
        {selectedDiagram === 'GPCR' && (
          <div className="space-y-6">
            <h2 className="text-lg font-extrabold text-cyan-300">
              Схема GPCR-сигнализации (Gs-каскад / цАМФ)
            </h2>

            {/* Interactive SVG Diagram */}
            <div className="w-full overflow-x-auto bg-slate-950 p-6 rounded-2xl border border-slate-800 flex justify-center">
              <svg width="650" height="320" viewBox="0 0 650 320" className="max-w-full">
                {/* Cell Membrane */}
                <rect x="50" y="120" width="550" height="40" fill="#1e293b" rx="8" stroke="#334155" strokeWidth="2" />
                <text x="60" y="145" fill="#94a3b8" fontSize="12" fontFamily="sans-serif" fontWeight="bold">Клеточная мембрана (Липидный бислой)</text>

                {/* Receptor */}
                <path d="M 150 70 L 190 70 L 190 170 L 150 170 Z" fill="#06b6d4" rx="10" opacity="0.9" />
                <text x="170" y="125" fill="#0284c7" fontSize="11" textAnchor="middle" fontWeight="bold">GPCR</text>

                {/* Agonist/Drug */}
                <circle cx="170" cy="50" r="14" fill="#10b981" />
                <text x="170" y="54" fill="#022c22" fontSize="10" textAnchor="middle" fontWeight="bold">Агонист</text>

                {/* Arrow Agonist -> Receptor */}
                <path d="M 170 65 L 170 70" stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow)" />

                {/* G-Protein Complex */}
                <rect x="220" y="165" width="80" height="35" fill="#f59e0b" rx="6" />
                <text x="260" y="186" fill="#451a03" fontSize="11" textAnchor="middle" fontWeight="bold">G-белок (Gs)</text>

                {/* Enzyme (Adenylate Cyclase) */}
                <rect x="360" y="100" width="90" height="80" fill="#8b5cf6" rx="10" />
                <text x="405" y="145" fill="#ffffff" fontSize="11" textAnchor="middle" fontWeight="bold">Аденилатциклаза</text>

                {/* ATP to cAMP */}
                <path d="M 405 185 L 405 230" stroke="#ec4899" strokeWidth="3" strokeDasharray="4" />
                <text x="415" y="210" fill="#f472b6" fontSize="10" fontWeight="bold">АТФ → цАМФ</text>

                {/* Effect */}
                <rect x="340" y="240" width="130" height="40" fill="#10b981" rx="8" />
                <text x="405" y="264" fill="#022c22" fontSize="11" textAnchor="middle" fontWeight="bold">Протеинкиназа A (PKA)</text>
              </svg>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 leading-relaxed space-y-2">
              <p><strong>Последовательность каскада:</strong></p>
              <p>1. Связывание лекарственного вещества (агониста) с конформационным доменом GPCR.</p>
              <p>2. Активация гетеротримерного Gs-белка и обмен ГДФ на ГТФ на α-субъединице.</p>
              <p>3. Стимуляция фермента Аденилатциклазы и превращение АТФ в вторичный посредник цАМФ.</p>
              <p>4. Активация Протеинкиназы A (PKA) и фосфорилирование целевых белков клетки.</p>
            </div>
          </div>
        )}

        {selectedDiagram === 'COX' && (
          <div className="space-y-4">
            <h2 className="text-lg font-extrabold text-cyan-300">
              Механизм действия НПВП (Блокада ЦОГ-1 / ЦОГ-2)
            </h2>
            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 text-xs font-mono text-emerald-300 space-y-3">
              <p>Фосфолипиды клеточных мембран</p>
              <p className="text-slate-500">↓ (Фосфолипаза A2)</p>
              <p>Арахидоновая кислота</p>
              <p className="text-rose-400 font-bold">
                ↓ [X БЛОКИРУЕТСЯ НПВП (Ибупрофен, Парацетамол)]
              </p>
              <p>Циклооксигеназа (ЦОГ-1 / ЦОГ-2)</p>
              <p className="text-slate-500">↓</p>
              <p>Простагландины (PGE2, PGI2) & Тромбоксан A2</p>
            </div>
          </div>
        )}

        {selectedDiagram === 'CCB' && (
          <div className="space-y-4">
            <h2 className="text-lg font-extrabold text-cyan-300">
              Блокада потенциалзависимых Ca2+ каналов L-типа (Амлодипин)
            </h2>
            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed space-y-3">
              <p className="font-semibold text-emerald-400">
                Мишень: Кальциевые каналы L-типа гладкой мускулатуры сосудов.
              </p>
              <p>
                1. Амлодипин связывается с дигидропиридиновыми рецепторами каналов L-типа.
              </p>
              <p>
                2. Препятствует входу ионов Ca2+ внутрь гладкомышечных клеток артериол.
              </p>
              <p>
                3. Снижает связывание Ca2+ с кальмодулином и предотвращает активацию киназы легких цепей миозина.
              </p>
              <p>
                4. Результат: Выраженная вазодилатация, снижение ОПСС и артериального давления.
              </p>
            </div>
          </div>
        )}

        {selectedDiagram === 'SYNAPSE' && (
          <div className="space-y-4">
            <h2 className="text-lg font-extrabold text-cyan-300">
              Синаптическая передача и нейромедиаторы
            </h2>
            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed space-y-3">
              <p>
                <strong>Пресинаптическая мембрана:</strong> Синтез и депонирование нейромедиатора в везикулах.
              </p>
              <p>
                <strong>Синаптическая щель:</strong> Высвобождение медиатора, его инактивация ферментами или обратный захват.
              </p>
              <p>
                <strong>Постсинаптическая мембрана:</strong> Связывание с рецепторами (M/N-холинорецепторы, α/β-адренорецепторы) и изменение мембранного потенциала.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
