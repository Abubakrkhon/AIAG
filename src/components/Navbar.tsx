import Link from 'next/link';
import { Pill, Search, Layers, GitCompare, ShieldAlert, BookOpen, Settings, Heart } from 'lucide-react';

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-emerald-900/10 bg-slate-900/95 backdrop-blur text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-slate-950 font-black shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <Pill className="w-6 h-6 stroke-[2.5]" />
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-300 bg-clip-text text-transparent">
              PHARMA ATLAS
            </span>
            <span className="text-[10px] text-emerald-400/80 uppercase tracking-widest font-medium -mt-1">
              Энциклопедия лекарственных средств
            </span>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-1 text-sm font-medium text-slate-300">
          <Link
            href="/drugs"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
          >
            <Pill className="w-4 h-4 text-emerald-400" />
            Лекарства
          </Link>

          <Link
            href="/classifications"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
          >
            <Layers className="w-4 h-4 text-teal-400" />
            Классификации
          </Link>

          <Link
            href="/atlas"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
          >
            <BookOpen className="w-4 h-4 text-cyan-400" />
            Атлас механизмов
          </Link>

          <Link
            href="/interactions"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
          >
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            Взаимодействия
          </Link>

          <Link
            href="/compare"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
          >
            <GitCompare className="w-4 h-4 text-blue-400" />
            Сравнение
          </Link>

          <Link
            href="/study"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
          >
            <BookOpen className="w-4 h-4 text-indigo-400" />
            Учебный центр
          </Link>
        </nav>

        <div className="flex items-center gap-3">
          <Link
            href="/admin"
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 border border-slate-700 hover:border-emerald-500/50 hover:bg-slate-700 text-slate-200 transition-all"
          >
            <Settings className="w-3.5 h-3.5 text-slate-400" />
            Админ-панель
          </Link>
        </div>
      </div>
    </header>
  );
}
