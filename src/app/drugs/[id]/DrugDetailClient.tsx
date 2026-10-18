'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
  Pill,
  Activity,
  Layers,
  ShieldAlert,
  FileText,
  AlertTriangle,
  Clock,
  CheckCircle2,
  ExternalLink,
  ChevronRight,
  Zap,
  Info,
  BookOpen,
} from 'lucide-react';

export function DrugDetailClient({ drug }: { drug: any }) {
  const [activeTab, setActiveTab] = useState<
    | 'OVERVIEW'
    | 'COMPOSITION'
    | 'PHARMACODYNAMICS'
    | 'PHARMACOKINETICS'
    | 'INDICATIONS'
    | 'DOSAGE'
    | 'CONTRAINDICATIONS'
    | 'SIDE_EFFECTS'
    | 'INTERACTIONS'
    | 'SOURCES'
  >('OVERVIEW');

  const mainIngredient = drug.ingredients[0]?.ingredient;
  const mechanism = mainIngredient?.mechanisms[0];
  const kinetics = mainIngredient?.kinetics[0];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Breadcrumb Navigation */}
      <nav className="flex items-center gap-2 text-xs text-slate-400 mb-6 overflow-x-auto">
        <Link href="/" className="hover:text-emerald-400 transition-colors">
          Главная
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
        <Link href="/drugs" className="hover:text-emerald-400 transition-colors">
          Лекарства
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
        <span className="text-slate-200 font-semibold">{drug.tradeNameRu}</span>
      </nav>

      {/* Drug Card Main Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5 text-emerald-400 pointer-events-none">
          <Pill className="w-64 h-64" />
        </div>

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {drug.dosageStrength}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                {drug.form}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                {drug.isPrescription ? 'Рецептурный препарат' : 'Без рецепта'}
              </span>
            </div>

            <h1 className="text-3xl sm:text-4xl font-black text-slate-100 tracking-tight">
              {drug.tradeNameRu}
              {drug.tradeNameEn && (
                <span className="text-lg sm:text-xl text-slate-400 font-normal ml-3">
                  ({drug.tradeNameEn})
                </span>
              )}
            </h1>

            <p className="text-sm text-slate-300 mt-2">
              <strong className="text-slate-400">МНН / Действующее вещество:</strong>{' '}
              <span className="text-emerald-400 font-bold">
                {drug.ingredients.map((i: any) => i.ingredient.innRu).join(', ')}
              </span>{' '}
              {mainIngredient?.latinName && (
                <span className="text-slate-400 italic">({mainIngredient.latinName})</span>
              )}
            </p>

            {drug.pharmClass && (
              <p className="text-xs text-slate-400 mt-1">
                Фармакологическая группа: <span className="text-cyan-300">{drug.pharmClass.nameRu}</span>
              </p>
            )}
          </div>

          <div className="shrink-0 space-y-2 text-right md:text-right text-xs text-slate-400 bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
            <p>
              <strong>Статус:</strong>{' '}
              <span className="text-emerald-400 font-semibold">{drug.registrationStatus}</span>
            </p>
            {drug.manufacturer && (
              <p>
                <strong>Производитель:</strong> {drug.manufacturer.name} ({drug.manufacturer.country})
              </p>
            )}
            {drug.atcCode && (
              <p>
                <strong>Код ATC:</strong>{' '}
                <span className="font-mono text-cyan-400">{drug.atcCode.code}</span>
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Structured Navigation Tabs */}
      <div className="flex items-center gap-1 overflow-x-auto pb-3 mb-8 border-b border-slate-800 text-xs font-semibold scrollbar-none">
        {[
          { id: 'OVERVIEW', label: 'Обзор', icon: Info },
          { id: 'COMPOSITION', label: 'Состав', icon: Pill },
          { id: 'PHARMACODYNAMICS', label: 'Фармакодинамика', icon: Zap },
          { id: 'PHARMACOKINETICS', label: 'Фармакокинетика', icon: Activity },
          { id: 'INDICATIONS', label: 'Показания', icon: CheckCircle2 },
          { id: 'DOSAGE', label: 'Дозировки', icon: Clock },
          { id: 'CONTRAINDICATIONS', label: 'Противопоказания', icon: AlertTriangle },
          { id: 'SIDE_EFFECTS', label: 'Побочные эффекты', icon: ShieldAlert },
          { id: 'INTERACTIONS', label: 'Взаимодействия', icon: Layers },
          { id: 'SOURCES', label: 'Источники', icon: BookOpen },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-emerald-500 text-slate-950 font-extrabold shadow-lg shadow-emerald-500/20'
                  : 'bg-slate-900 text-slate-300 hover:bg-slate-800 hover:text-white border border-slate-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Content Display */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl min-h-[400px]">
        {/* TAB 1: OVERVIEW */}
        {activeTab === 'OVERVIEW' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <Info className="w-5 h-5 text-emerald-400" />
              Краткий обзор препарата
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                <h3 className="text-sm font-bold text-slate-200">Основная информация</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  <strong>Синонимы:</strong> {drug.synonyms || 'Не указаны'}
                </p>
                <p className="text-xs text-slate-300 leading-relaxed">
                  <strong>Форма выпуска:</strong> {drug.form}
                </p>
                <p className="text-xs text-slate-300 leading-relaxed">
                  <strong>Упаковка:</strong> {drug.packaging || 'Официальная упаковка производителя'}
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                <h3 className="text-sm font-bold text-slate-200">Изображение и упаковка</h3>
                <div className="w-full h-32 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-500 text-xs text-center p-4">
                  {drug.images && drug.images.length > 0 ? (
                    <span>Упаковка: {drug.images[0].caption}</span>
                  ) : (
                    <span>Фотография упаковки {drug.tradeNameRu} ({drug.dosageStrength})</span>
                  )}
                </div>
              </div>
            </div>

            {/* Warnings Section */}
            {drug.warnings && drug.warnings.length > 0 && (
              <div className="p-5 rounded-2xl bg-amber-950/30 border border-amber-800/40 space-y-2">
                <h3 className="text-sm font-bold text-amber-300 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4" />
                  Важные предупреждения безопасности
                </h3>
                {drug.warnings.map((w: any) => (
                  <p key={w.id} className="text-xs text-amber-200/90 leading-relaxed">
                    <strong>{w.title}:</strong> {w.content}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 2: COMPOSITION */}
        {activeTab === 'COMPOSITION' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <Pill className="w-5 h-5 text-emerald-400" />
              Полный химический состав
            </h2>

            <div className="space-y-4">
              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800">
                <h3 className="text-sm font-bold text-emerald-400 mb-3">
                  Действующие вещества (МНН)
                </h3>
                <div className="space-y-2">
                  {drug.ingredients.map((item: any) => (
                    <div
                      key={item.ingredient.id}
                      className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between"
                    >
                      <div>
                        <p className="text-sm font-semibold text-slate-200">
                          {item.ingredient.innRu} ({item.ingredient.innEn})
                        </p>
                        {item.ingredient.chemicalName && (
                          <p className="text-xs text-slate-400">{item.ingredient.chemicalName}</p>
                        )}
                      </div>
                      <span className="text-xs font-bold px-3 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {item.amount}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800">
                <h3 className="text-sm font-bold text-slate-200 mb-2">Вспомогательные вещества</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {drug.compositionExcipients || 'Данные о вспомогательных веществах содержатся в официальном вкладыше.'}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: PHARMACODYNAMICS */}
        {activeTab === 'PHARMACODYNAMICS' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <Zap className="w-5 h-5 text-emerald-400" />
              Фармакодинамика и молекулярный механизм
            </h2>

            {mechanism ? (
              <div className="space-y-6">
                {/* Visual Causal Chain Diagram */}
                <div className="p-6 rounded-2xl bg-slate-950 border border-emerald-500/30 space-y-4">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                    Причинно-следственная цепочка действия
                  </h3>
                  <div className="p-4 rounded-xl bg-slate-900 font-mono text-xs text-emerald-300 leading-relaxed border border-slate-800 overflow-x-auto">
                    {mechanism.causalChain}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <h4 className="text-xs font-bold text-slate-400 uppercase">Молекулярная мишень</h4>
                    <p className="text-sm font-semibold text-slate-100">{mechanism.target}</p>
                    <p className="text-xs text-slate-400">Тип: {mechanism.targetType}</p>
                  </div>

                  <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <h4 className="text-xs font-bold text-slate-400 uppercase">Тип взаимодействия</h4>
                    <p className="text-sm font-semibold text-slate-100">{mechanism.interactionType}</p>
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                  <h4 className="text-sm font-bold text-slate-200">Подробный молекулярный механизм</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{mechanism.molecularMechanism}</p>
                </div>

                <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                  <h4 className="text-sm font-bold text-slate-200">Клеточный и физиологический эффект</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{mechanism.cellularEffect}</p>
                  <p className="text-xs text-emerald-300 leading-relaxed font-medium">
                    {mechanism.physiologicalEffect}
                  </p>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400">Данные по фармакодинамике проверяются.</p>
            )}
          </div>
        )}

        {/* TAB 4: PHARMACOKINETICS */}
        {activeTab === 'PHARMACOKINETICS' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              Фармакокинетика (ADME)
            </h2>

            {kinetics ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs text-slate-400 font-bold block">Биодоступность</span>
                  <span className="text-sm text-slate-100 font-semibold">{kinetics.bioavailability || 'Н/Д'}</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs text-slate-400 font-bold block">Tmax (Время Cmax)</span>
                  <span className="text-sm text-slate-100 font-semibold">{kinetics.tMax || 'Н/Д'}</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs text-slate-400 font-bold block">Связывание с белками</span>
                  <span className="text-sm text-slate-100 font-semibold">{kinetics.proteinBinding || 'Н/Д'}</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <span className="text-xs text-slate-400 font-bold block">Период полувыведения (T1/2)</span>
                  <span className="text-sm text-emerald-400 font-semibold">{kinetics.halfLife || 'Н/Д'}</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 md:col-span-2">
                  <span className="text-xs text-slate-400 font-bold block mb-1">Метаболизм (CYP450)</span>
                  <p className="text-xs text-slate-300 leading-relaxed">{kinetics.metabolism || 'Н/Д'}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 md:col-span-2">
                  <span className="text-xs text-slate-400 font-bold block mb-1">Пути выведения</span>
                  <p className="text-xs text-slate-300 leading-relaxed">{kinetics.excretion || 'Н/Д'}</p>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400">Фармакокинетические параметры уточняются.</p>
            )}
          </div>
        )}

        {/* TAB 5: INDICATIONS */}
        {activeTab === 'INDICATIONS' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              Показания к применению
            </h2>

            <div className="space-y-3">
              {drug.indications?.map((ind: any) => (
                <div key={ind.id} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800">
                  <h3 className="text-sm font-bold text-emerald-300 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    {ind.title}
                  </h3>
                  {ind.description && (
                    <p className="text-xs text-slate-300 mt-1 leading-relaxed">{ind.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 6: DOSAGE */}
        {activeTab === 'DOSAGE' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <Clock className="w-5 h-5 text-emerald-400" />
              Режим дозирования и способ применения
            </h2>

            <div className="space-y-4">
              {drug.dosages?.map((dos: any) => (
                <div key={dos.id} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                      Категория: {dos.patientGroup}
                    </span>
                    {dos.maxDailyDose && (
                      <span className="text-xs font-semibold px-2.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">
                        Макс. суточная: {dos.maxDailyDose}
                      </span>
                    )}
                  </div>
                  <p className="text-sm font-bold text-slate-100">{dos.dose}</p>
                  {dos.instructions && (
                    <p className="text-xs text-slate-300 leading-relaxed">
                      <strong>Инструкция:</strong> {dos.instructions}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 7: CONTRAINDICATIONS */}
        {activeTab === 'CONTRAINDICATIONS' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-400" />
              Противопоказания
            </h2>

            <div className="space-y-3">
              {drug.contraindications?.map((ci: any) => (
                <div
                  key={ci.id}
                  className={`p-5 rounded-2xl border ${
                    ci.type === 'ABSOLUTE'
                      ? 'bg-rose-950/20 border-rose-800/40'
                      : 'bg-amber-950/20 border-amber-800/40'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-xs font-bold px-2.5 py-0.5 rounded ${
                        ci.type === 'ABSOLUTE'
                          ? 'bg-rose-500/20 text-rose-300'
                          : 'bg-amber-500/20 text-amber-300'
                      }`}
                    >
                      {ci.type === 'ABSOLUTE' ? 'Абсолютное' : 'Относительное'}
                    </span>
                  </div>
                  <p className="text-sm font-semibold text-slate-100 mt-2">{ci.title}</p>
                  {ci.description && (
                    <p className="text-xs text-slate-300 mt-1 leading-relaxed">{ci.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 8: SIDE_EFFECTS */}
        {activeTab === 'SIDE_EFFECTS' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-amber-400" />
              Побочные действия и нежелательные реакции
            </h2>

            <div className="space-y-3">
              {drug.adverseReactions?.map((ar: any) => (
                <div key={ar.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center justify-between">
                  <div>
                    <span className="text-xs text-slate-400 font-bold block">{ar.systemOrganClass}</span>
                    <span className="text-sm font-semibold text-slate-200">{ar.reaction}</span>
                  </div>
                  <span className="text-xs px-2.5 py-1 rounded bg-slate-800 text-slate-300 font-mono">
                    {ar.frequencyDescription || ar.frequency}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 9: INTERACTIONS */}
        {activeTab === 'INTERACTIONS' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <Layers className="w-5 h-5 text-emerald-400" />
              Лекарственные взаимодействия
            </h2>

            <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 leading-relaxed">
              Для проверки совпадения несколько препаратов перейдите в интерактивный раздел{' '}
              <Link href="/interactions" className="text-emerald-400 underline font-bold">
                Проверка взаимодействий
              </Link>
              .
            </div>
          </div>
        )}

        {/* TAB 10: SOURCES */}
        {activeTab === 'SOURCES' && (
          <div className="space-y-6">
            <h2 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-emerald-400" />
              Проверенные медицинские источники
            </h2>

            <div className="space-y-3">
              {drug.sources?.map((src: any) => (
                <div key={src.id} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-slate-200">{src.title}</h3>
                    <p className="text-xs text-slate-400">
                      Издатель: {src.publisher || 'Официальный регулятор'} • Юрисдикция: {src.jurisdiction}
                    </p>
                  </div>
                  {src.url && (
                    <a
                      href={src.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/20 transition-colors flex items-center gap-1 shrink-0"
                    >
                      Источник <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
