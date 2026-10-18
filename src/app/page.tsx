'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { Search, Pill, Layers, Activity, ShieldAlert, CheckCircle2, ChevronRight, Sparkles, BookOpen } from 'lucide-react';

interface SearchResult {
  drugs: any[];
  ingredients: any[];
  pharmClasses: any[];
  atcCodes: any[];
}

export function SearchSection() {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('ALL');
  const [results, setResults] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (!query.trim()) {
      setResults(null);
      setIsOpen(false);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&type=${searchType}`);
        const data = await res.json();
        if (data.success) {
          setResults(data.results);
          setIsOpen(true);
        }
      } catch (e) {
        console.error('Search error', e);
      } finally {
        setLoading(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [query, searchType]);

  const hasResults =
    results &&
    (results.drugs.length > 0 ||
      results.ingredients.length > 0 ||
      results.pharmClasses.length > 0 ||
      results.atcCodes.length > 0);

  return (
    <div className="relative w-full max-w-4xl mx-auto" ref={dropdownRef}>
      {/* Filter Tabs */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 text-xs font-medium scrollbar-none">
        {[
          { id: 'ALL', label: 'Всё' },
          { id: 'TRADE_NAME', label: 'Торговое название' },
          { id: 'INN', label: 'МНН' },
          { id: 'PHARM_CLASS', label: 'Фармгруппа' },
          { id: 'ATC', label: 'ATC-код' },
          { id: 'MECHANISM', label: 'Механизм действия' },
          { id: 'INDICATION', label: 'Показания' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSearchType(tab.id)}
            className={`px-3 py-1.5 rounded-full whitespace-nowrap transition-all ${
              searchType === tab.id
                ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Main Search Bar */}
      <div className="relative mt-2">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-emerald-400">
          <Search className="w-6 h-6" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.trim() && setIsOpen(true)}
          placeholder="Поиск по названию, МНН (Парацетамол), фармгруппе, ATC или показанию..."
          className="w-full pl-13 pr-12 py-4 text-base sm:text-lg bg-slate-900 border-2 border-emerald-500/30 focus:border-emerald-400 rounded-2xl text-slate-100 placeholder-slate-400 shadow-2xl focus:outline-none focus:ring-4 focus:ring-emerald-500/10 transition-all"
        />
        {loading && (
          <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
            <div className="w-5 h-5 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
      </div>

      {/* Autocomplete Dropdown */}
      {isOpen && (
        <div className="absolute left-0 right-0 mt-3 bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden z-50 max-h-[75vh] overflow-y-auto divide-y divide-slate-800">
          {!hasResults && !loading && (
            <div className="p-8 text-center text-slate-400">
              <p className="text-sm font-medium">По запросу «{query}» ничего не найдено.</p>
              <p className="text-xs text-slate-500 mt-1">
                Проверьте правильность написания или попробуйте изменить тип поиска.
              </p>
            </div>
          )}

          {/* Drugs */}
          {results?.drugs && results.drugs.length > 0 && (
            <div className="p-3">
              <div className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 px-3 flex items-center gap-1.5">
                <Pill className="w-3.5 h-3.5" />
                Препараты ({results.drugs.length})
              </div>
              <div className="space-y-1">
                {results.drugs.map((drug) => (
                  <Link
                    key={drug.id}
                    href={`/drugs/${drug.id}`}
                    onClick={() => setIsOpen(false)}
                    className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-800 transition-colors group"
                  >
                    <div>
                      <div className="font-semibold text-slate-100 group-hover:text-emerald-400 flex items-center gap-2">
                        {drug.tradeNameRu}
                        {drug.tradeNameEn && (
                          <span className="text-xs text-slate-400 font-normal">({drug.tradeNameEn})</span>
                        )}
                        <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {drug.dosageStrength}
                        </span>
                      </div>
                      <div className="text-xs text-slate-400 mt-0.5">
                        МНН: {drug.ingredients.map((i: any) => i.ingredient.innRu).join(', ')} • {drug.form}
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 group-hover:translate-x-1 transition-all" />
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* Active Ingredients */}
          {results?.ingredients && results.ingredients.length > 0 && (
            <div className="p-3">
              <div className="text-xs font-bold uppercase tracking-wider text-teal-400 mb-2 px-3 flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5" />
                Действующие вещества / МНН ({results.ingredients.length})
              </div>
              <div className="space-y-1">
                {results.ingredients.map((ing) => (
                  <div key={ing.id} className="p-3 rounded-xl bg-slate-800/40 border border-slate-800">
                    <div className="font-semibold text-slate-200 flex items-center gap-2">
                      {ing.innRu} ({ing.innEn})
                      {ing.latinName && <span className="text-xs text-slate-400 italic">{ing.latinName}</span>}
                    </div>
                    <p className="text-xs text-slate-400 mt-1 line-clamp-2">{ing.description}</p>
                    {ing.drugs.length > 0 && (
                      <div className="mt-2 flex items-center gap-1.5 flex-wrap">
                        <span className="text-[10px] text-slate-500 font-semibold">Торговые марки:</span>
                        {ing.drugs.map((d: any) => (
                          <Link
                            key={d.drug.id}
                            href={`/drugs/${d.drug.id}`}
                            onClick={() => setIsOpen(false)}
                            className="text-[11px] px-2 py-0.5 rounded bg-slate-700 hover:bg-emerald-600 hover:text-white text-emerald-300 transition-colors"
                          >
                            {d.drug.tradeNameRu}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Pharmacological Classes */}
          {results?.pharmClasses && results.pharmClasses.length > 0 && (
            <div className="p-3">
              <div className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-2 px-3 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5" />
                Фармакологические группы ({results.pharmClasses.length})
              </div>
              <div className="space-y-1">
                {results.pharmClasses.map((cls) => (
                  <Link
                    key={cls.id}
                    href={`/classifications#${cls.code}`}
                    onClick={() => setIsOpen(false)}
                    className="block p-2.5 rounded-xl hover:bg-slate-800 text-slate-200 transition-colors"
                  >
                    <div className="font-medium text-sm flex items-center justify-between">
                      <span>{cls.nameRu}</span>
                      <span className="text-xs font-mono text-cyan-400">{cls.code}</span>
                    </div>
                    {cls.description && (
                      <p className="text-xs text-slate-400 mt-0.5 line-clamp-1">{cls.description}</p>
                    )}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Hero Section */}
      <section className="relative pt-12 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-950 border-b border-slate-800/60 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-emerald-500/5 blur-3xl rounded-full pointer-events-none" />

        <div className="max-w-5xl mx-auto text-center space-y-6 relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            Цифровая энциклопедия нового поколения
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight bg-gradient-to-r from-white via-slate-100 to-emerald-300 bg-clip-text text-transparent">
            PHARMA ATLAS
          </h1>

          <p className="text-base sm:text-lg text-slate-300 max-w-3xl mx-auto leading-relaxed">
            Профессиональный справочник лекарств, доказательная фармакология, визуальный атлас молекулярных механизмов и интерактивная учебная система.
          </p>

          <SearchSection />
        </div>
      </section>

      {/* Quick Navigation Cards */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <h2 className="text-xl font-extrabold text-slate-100 mb-6 flex items-center gap-2">
          <Layers className="w-5 h-5 text-emerald-400" />
          Основные разделы платформы
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <Link
            href="/drugs"
            className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800/80 transition-all group shadow-xl"
          >
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-110 transition-transform">
              <Pill className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 group-hover:text-emerald-400 transition-colors">
              Лекарства
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Карточки препаратов с доказанной базой, составом, дозировками и инструкциями.
            </p>
          </Link>

          <Link
            href="/classifications"
            className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-teal-500/50 hover:bg-slate-800/80 transition-all group shadow-xl"
          >
            <div className="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 mb-4 group-hover:scale-110 transition-transform">
              <Layers className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 group-hover:text-teal-400 transition-colors">
              Классификации
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Иерархия по фармакологическому действию, мишеням и кодам ATC.
            </p>
          </Link>

          <Link
            href="/atlas"
            className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-800/80 transition-all group shadow-xl"
          >
            <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-110 transition-transform">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 group-hover:text-cyan-400 transition-colors">
              Атлас механизмов
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Интерактивные визуальные схемы рецепторов, ионных каналов и сигнальных путей.
            </p>
          </Link>

          <Link
            href="/interactions"
            className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800/80 transition-all group shadow-xl"
          >
            <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4 group-hover:scale-110 transition-transform">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100 group-hover:text-amber-400 transition-colors">
              Взаимодействия
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Матрица проверки опасных комбинаций и клинические рекомендации.
            </p>
          </Link>
        </div>
      </section>

      {/* Featured Medical Standards Banner */}
      <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 border border-emerald-500/20 flex flex-col md:flex-row items-center justify-between gap-6 shadow-2xl">
          <div className="space-y-2 text-center md:text-left">
            <h3 className="text-xl font-bold text-slate-100 flex items-center justify-center md:justify-start gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              Научная достоверность и проверяемость
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 max-w-2xl leading-relaxed">
              Все данные сопоставлены с официальными инструкциями ГРЛС Минздрава РФ, классификацией ВОЗ ATC/DDD и доказательными клиническими источниками.
            </p>
          </div>
          <Link
            href="/study"
            className="shrink-0 px-5 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 transition-colors flex items-center gap-2"
          >
            <BookOpen className="w-4 h-4" />
            Перейти в Учебный центр
          </Link>
        </div>
      </section>
    </div>
  );
}
