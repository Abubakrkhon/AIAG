import Link from 'next/link';
import { Shield, ExternalLink } from 'lucide-react';

export function Footer() {
  const currentYear = 2026;

  return (
    <footer className="bg-slate-950 border-t border-slate-800 text-slate-400 text-sm mt-auto">
      {/* Medical Disclaimer Banner */}
      <div className="bg-amber-950/40 border-b border-amber-800/30 py-3 px-4 text-center">
        <div className="max-w-7xl mx-auto flex items-center justify-center gap-2 text-amber-300 text-xs sm:text-sm font-medium">
          <Shield className="w-4 h-4 shrink-0" />
          <span>
            <strong>Медицинский дисклеймер:</strong> Информация на платформе носит исключительно справочно-образовательный характер и не является инструкцией по самолечению. Перед применением препаратов проконсультируйтесь с врачом.
          </span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-3 md:col-span-1">
            <h3 className="text-slate-100 font-bold text-base tracking-wide bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">
              PHARMA ATLAS
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Единая медицинская веб-платформа по фармакологии. Профессиональный лекарственный справочник, атлас механизмов действия и учебный центр.
            </p>
            <p className="text-xs text-emerald-400/90 font-medium">
              Проверено по источникам: ГРЛС, WHO ATC, FDA, EMA.
            </p>
          </div>

          <div>
            <h4 className="text-slate-200 font-semibold text-xs uppercase tracking-wider mb-3">
              Навигация
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/drugs" className="hover:text-emerald-400 transition-colors">
                  Энциклопедия лекарств
                </Link>
              </li>
              <li>
                <Link href="/classifications" className="hover:text-emerald-400 transition-colors">
                  Фармакологические группы
                </Link>
              </li>
              <li>
                <Link href="/atlas" className="hover:text-emerald-400 transition-colors">
                  Атлас механизмов
                </Link>
              </li>
              <li>
                <Link href="/interactions" className="hover:text-emerald-400 transition-colors">
                  Проверка взаимодействий
                </Link>
              </li>
              <li>
                <Link href="/compare" className="hover:text-emerald-400 transition-colors">
                  Сравнение препаратов
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-slate-200 font-semibold text-xs uppercase tracking-wider mb-3">
              Студентам и Врачам
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/study" className="hover:text-emerald-400 transition-colors">
                  Общая фармакология
                </Link>
              </li>
              <li>
                <Link href="/study" className="hover:text-emerald-400 transition-colors">
                  Частная фармакология
                </Link>
              </li>
              <li>
                <Link href="/study" className="hover:text-emerald-400 transition-colors">
                  Тесты и карточки запоминания
                </Link>
              </li>
              <li>
                <Link href="/admin" className="hover:text-emerald-400 transition-colors">
                  Импорт и управление данными
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-slate-200 font-semibold text-xs uppercase tracking-wider mb-3">
              Источники данных
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <a
                  href="https://grls.rosminzdrav.ru"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-emerald-400 flex items-center gap-1 transition-colors"
                >
                  ГРЛС Минздрава РФ <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://www.whocc.no"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-emerald-400 flex items-center gap-1 transition-colors"
                >
                  WHO ATC/DDD Index <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://dailymed.nlm.nih.gov"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-emerald-400 flex items-center gap-1 transition-colors"
                >
                  DailyMed (FDA) <ExternalLink className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {currentYear} PHARMA ATLAS — Цифровая медицинская энциклопедия. Все права защищены.</p>
          <div className="flex items-center gap-4">
            <span>Язык: Русский (Таджикский / English — планируется)</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
