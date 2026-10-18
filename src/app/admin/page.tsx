'use client';

import { useState } from 'react';
import { Settings, Plus, Upload, Download, CheckCircle2, AlertCircle, FileText, Database } from 'lucide-react';

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<'ADD_DRUG' | 'IMPORT_EXPORT' | 'LOGS'>('ADD_DRUG');

  // Form State
  const [tradeNameRu, setTradeNameRu] = useState('');
  const [tradeNameEn, setTradeNameEn] = useState('');
  const [synonyms, setSynonyms] = useState('');
  const [form, setForm] = useState('Таблетки');
  const [dosageStrength, setDosageStrength] = useState('');
  const [packaging, setPackaging] = useState('');
  const [isPrescription, setIsPrescription] = useState(false);
  const [compositionExcipients, setCompositionExcipients] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  // Import State
  const [jsonInput, setJsonInput] = useState('');

  const handleAddDrug = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusMessage('');
    try {
      const res = await fetch('/api/admin/drugs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tradeNameRu,
          tradeNameEn,
          synonyms,
          form,
          dosageStrength,
          packaging,
          isPrescription,
          compositionExcipients,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setStatusMessage(`Успешно создан препарат: ${data.data.tradeNameRu}`);
        setTradeNameRu('');
        setTradeNameEn('');
        setDosageStrength('');
      } else {
        setStatusMessage(`Ошибка: ${data.error}`);
      }
    } catch (e: any) {
      setStatusMessage(`Ошибка запроса: ${e.message}`);
    }
  };

  const handleImportJson = async () => {
    setStatusMessage('');
    try {
      const parsed = JSON.parse(jsonInput);
      const res = await fetch('/api/admin/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(parsed),
      });
      const data = await res.json();
      if (data.success) {
        setStatusMessage(data.message || 'Импорт успешно завершен!');
        setJsonInput('');
      } else {
        setStatusMessage(`Ошибка импорта: ${data.error}`);
      }
    } catch (e: any) {
      setStatusMessage(`Неверный формат JSON: ${e.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <Settings className="w-8 h-8 text-emerald-400" />
          Панель администратора и редактора медицинских данных
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-3xl">
          Управление карточками лекарственных средств, добавление новых торговых марок, пакетный импорт JSON/CSV и проверка медицинских источников.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800 text-xs font-semibold">
        {[
          { id: 'ADD_DRUG', label: 'Добавить препарат', icon: Plus },
          { id: 'IMPORT_EXPORT', label: 'Импорт / Экспорт JSON', icon: Upload },
          { id: 'LOGS', label: 'Журнал изменений', icon: Database },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl transition-all ${
                activeTab === tab.id
                  ? 'bg-emerald-500 text-slate-950 font-bold shadow-lg shadow-emerald-500/20'
                  : 'bg-slate-900 text-slate-300 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Status Message */}
      {statusMessage && (
        <div className="p-4 rounded-xl bg-slate-900 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          {statusMessage}
        </div>
      )}

      {/* Tab 1: Add Drug Form */}
      {activeTab === 'ADD_DRUG' && (
        <form onSubmit={handleAddDrug} className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6 max-w-3xl">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Plus className="w-5 h-5 text-emerald-400" />
            Создание карточки нового препарата
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Торговое название (RU) *
              </label>
              <input
                type="text"
                required
                value={tradeNameRu}
                onChange={(e) => setTradeNameRu(e.target.value)}
                placeholder="Например: Ибупрофен-Акос"
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 focus:border-emerald-400 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Торговое название (EN)
              </label>
              <input
                type="text"
                value={tradeNameEn}
                onChange={(e) => setTradeNameEn(e.target.value)}
                placeholder="Например: Ibuprofen-Akos"
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 focus:border-emerald-400 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Дозировка / Концентрация *
              </label>
              <input
                type="text"
                required
                value={dosageStrength}
                onChange={(e) => setDosageStrength(e.target.value)}
                placeholder="Например: 400 мг"
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 focus:border-emerald-400 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Лекарственная форма *
              </label>
              <select
                value={form}
                onChange={(e) => setForm(e.target.value)}
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 focus:border-emerald-400 focus:outline-none"
              >
                <option value="Таблетки">Таблетки</option>
                <option value="Капсулы">Капсулы</option>
                <option value="Раствор для инъекций">Раствор для инъекций</option>
                <option value="Суспензия">Суспензия</option>
                <option value="Мазь / Гель">Мазь / Гель</option>
              </select>
            </div>

            <div className="sm:col-span-2">
              <label className="block text-slate-300 font-bold mb-1">Синонимы</label>
              <input
                type="text"
                value={synonyms}
                onChange={(e) => setSynonyms(e.target.value)}
                placeholder="Через запятую"
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 focus:border-emerald-400 focus:outline-none"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block text-slate-300 font-bold mb-1">Вспомогательные вещества</label>
              <textarea
                value={compositionExcipients}
                onChange={(e) => setCompositionExcipients(e.target.value)}
                placeholder="Описание состава и аллергенов..."
                rows={3}
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 focus:border-emerald-400 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all"
          >
            Сохранить препарат
          </button>
        </form>
      )}

      {/* Tab 2: Import / Export */}
      {activeTab === 'IMPORT_EXPORT' && (
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6 max-w-3xl">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Upload className="w-5 h-5 text-emerald-400" />
            Пакетный импорт данных (JSON)
          </h2>

          <div className="space-y-3">
            <label className="block text-xs font-bold text-slate-300">
              Вставьте массив объектов JSON с данными препаратов:
            </label>
            <textarea
              value={jsonInput}
              onChange={(e) => setJsonInput(e.target.value)}
              placeholder={`[\n  {\n    "tradeNameRu": "Аспирин",\n    "form": "Таблетки",\n    "dosageStrength": "500 мг"\n  }\n]`}
              rows={10}
              className="w-full p-4 rounded-xl bg-slate-950 font-mono text-xs text-emerald-300 border border-slate-800 focus:border-emerald-400 focus:outline-none"
            />
          </div>

          <button
            onClick={handleImportJson}
            className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all"
          >
            Запустить импорт
          </button>
        </div>
      )}

      {/* Tab 3: Logs */}
      {activeTab === 'LOGS' && (
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-4 max-w-3xl">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-5 h-5 text-emerald-400" />
            Журнал действий и аудита источников
          </h2>
          <p className="text-xs text-slate-400">
            История верификации карточек медицинскими специалистами. Все записи имеют привязку к авторитетным источникам ГРЛС / WHO ATC.
          </p>
        </div>
      )}
    </div>
  );
}
