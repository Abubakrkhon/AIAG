'use client';

import { useState, useEffect } from 'react';
import { BookOpen, CheckCircle2, HelpCircle, RotateCcw, Award, Layers, Sparkles } from 'lucide-react';

export default function StudyPage() {
  const [studyMaterials, setStudyMaterials] = useState<any[]>([]);
  const [selectedMaterial, setSelectedMaterial] = useState<any>(null);
  const [explanationLevel, setExplanationLevel] = useState<'BRIEF' | 'STANDARD' | 'DETAILED' | 'ADVANCED'>('STANDARD');

  // Quiz state
  const [activeQuizIndex, setActiveQuizIndex] = useState<number | null>(null);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [score, setScore] = useState(0);

  useEffect(() => {
    async function loadStudyData() {
      try {
        const res = await fetch('/api/study');
        const data = await res.json();
        if (data.success && data.studyMaterials.length > 0) {
          setStudyMaterials(data.studyMaterials);
          setSelectedMaterial(data.studyMaterials[0]);
        }
      } catch (e) {
        console.error('Failed to load study materials', e);
      }
    }
    loadStudyData();
  }, []);

  const handleSelectOption = (index: number) => {
    if (isAnswered) return;
    setSelectedOption(index);
    setIsAnswered(true);

    if (selectedMaterial && activeQuizIndex !== null) {
      const quiz = selectedMaterial.quizzes[activeQuizIndex];
      if (index === quiz.correctOptionIndex) {
        setScore((prev) => prev + 1);
      }
    }
  };

  const nextQuestion = () => {
    if (!selectedMaterial) return;
    if (activeQuizIndex !== null && activeQuizIndex < selectedMaterial.quizzes.length - 1) {
      setActiveQuizIndex(activeQuizIndex + 1);
      setSelectedOption(null);
      setIsAnswered(false);
    }
  };

  const startQuiz = () => {
    setActiveQuizIndex(0);
    setSelectedOption(null);
    setIsAnswered(false);
    setScore(0);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-100 tracking-tight flex items-center gap-3">
          <BookOpen className="w-8 h-8 text-indigo-400" />
          Учебный центр для студентов и врачей
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-3xl">
          Адаптивная обучающая система: структурированные конспекты, разноуровневые объяснения фармакодинамики и интерактивные тесты с пояснениями.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Topic Selector Sidebar */}
        <div className="space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            Темы занятий ({studyMaterials.length})
          </h2>

          <div className="space-y-2">
            {studyMaterials.map((mat) => (
              <button
                key={mat.id}
                onClick={() => {
                  setSelectedMaterial(mat);
                  setActiveQuizIndex(null);
                }}
                className={`w-full text-left p-4 rounded-2xl border transition-all ${
                  selectedMaterial?.id === mat.id
                    ? 'bg-indigo-600/10 border-indigo-500/50 text-indigo-300 font-bold shadow-lg'
                    : 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <div className="text-xs text-indigo-400 font-semibold mb-1">{mat.category}</div>
                <div className="text-sm font-extrabold">{mat.topic}</div>
                <div className="text-xs text-slate-400 mt-2 flex items-center gap-2">
                  <span>{mat.quizzes?.length || 0} вопросов</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Right Main Content Panel */}
        <div className="lg:col-span-2 space-y-6">
          {selectedMaterial && (
            <>
              {/* Level Switcher */}
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex flex-wrap items-center justify-between gap-3 shadow-xl">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Уровень детальности:
                </span>
                <div className="flex items-center gap-1.5 overflow-x-auto text-xs font-bold">
                  {[
                    { id: 'BRIEF', label: '1. Кратко' },
                    { id: 'STANDARD', label: '2. Стандартно' },
                    { id: 'DETAILED', label: '3. Подробно' },
                    { id: 'ADVANCED', label: '4. Углубленно' },
                  ].map((lvl) => (
                    <button
                      key={lvl.id}
                      onClick={() => setExplanationLevel(lvl.id as any)}
                      className={`px-3 py-1.5 rounded-xl transition-all ${
                        explanationLevel === lvl.id
                          ? 'bg-indigo-500 text-slate-950 shadow-md shadow-indigo-500/20'
                          : 'bg-slate-950 text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      {lvl.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Study Text Content */}
              <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
                <h2 className="text-2xl font-black text-slate-100 flex items-center gap-2">
                  <Sparkles className="w-6 h-6 text-indigo-400" />
                  {selectedMaterial.topic}
                </h2>

                <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800 text-sm text-slate-200 leading-relaxed space-y-4">
                  {explanationLevel === 'BRIEF' && (
                    <p className="font-medium text-emerald-300">{selectedMaterial.briefText}</p>
                  )}
                  {explanationLevel === 'STANDARD' && (
                    <p>{selectedMaterial.standardText}</p>
                  )}
                  {explanationLevel === 'DETAILED' && (
                    <p>{selectedMaterial.detailedText}</p>
                  )}
                  {explanationLevel === 'ADVANCED' && (
                    <p>{selectedMaterial.advancedText}</p>
                  )}
                </div>

                {/* Key Takeaways */}
                {selectedMaterial.keyTakeways && (
                  <div className="p-5 rounded-2xl bg-indigo-950/20 border border-indigo-800/40 space-y-3">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                      Ключевые моменты для запоминания:
                    </h3>
                    <ul className="list-disc list-inside text-xs text-indigo-200 space-y-1">
                      {JSON.parse(selectedMaterial.keyTakeways).map((item: string, idx: number) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Quiz Module */}
              <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
                <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                  <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                    <HelpCircle className="w-5 h-5 text-indigo-400" />
                    Проверка знаний по теме
                  </h3>
                  {activeQuizIndex === null ? (
                    <button
                      onClick={startQuiz}
                      className="px-4 py-2 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-bold text-xs shadow-lg shadow-indigo-500/20 transition-all"
                    >
                      Начать тест
                    </button>
                  ) : (
                    <span className="text-xs font-bold text-indigo-400">
                      Вопрос {activeQuizIndex + 1} из {selectedMaterial.quizzes.length}
                    </span>
                  )}
                </div>

                {activeQuizIndex !== null && selectedMaterial.quizzes[activeQuizIndex] && (
                  <div className="space-y-6">
                    <p className="text-sm font-bold text-slate-100">
                      {selectedMaterial.quizzes[activeQuizIndex].question}
                    </p>

                    <div className="space-y-2">
                      {JSON.parse(selectedMaterial.quizzes[activeQuizIndex].optionsJson).map(
                        (opt: string, optIdx: number) => {
                          const isCorrect = optIdx === selectedMaterial.quizzes[activeQuizIndex].correctOptionIndex;
                          const isSelected = selectedOption === optIdx;

                          let btnStyle = 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800';
                          if (isAnswered) {
                            if (isCorrect) btnStyle = 'bg-emerald-500/20 border-emerald-500 text-emerald-300 font-bold';
                            else if (isSelected) btnStyle = 'bg-rose-500/20 border-rose-500 text-rose-300 font-bold';
                          }

                          return (
                            <button
                              key={optIdx}
                              onClick={() => handleSelectOption(optIdx)}
                              className={`w-full text-left p-4 rounded-xl border text-xs transition-all ${btnStyle}`}
                            >
                              {opt}
                            </button>
                          );
                        }
                      )}
                    </div>

                    {isAnswered && (
                      <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-800/40 space-y-2 text-xs">
                        <p className="font-bold text-indigo-300">Пояснение ответа:</p>
                        <p className="text-slate-300 leading-relaxed">
                          {selectedMaterial.quizzes[activeQuizIndex].explanation}
                        </p>

                        {activeQuizIndex < selectedMaterial.quizzes.length - 1 ? (
                          <button
                            onClick={nextQuestion}
                            className="mt-3 px-4 py-2 rounded-xl bg-indigo-500 text-slate-950 font-bold text-xs shadow-md shadow-indigo-500/20"
                          >
                            Следующий вопрос
                          </button>
                        ) : (
                          <div className="pt-2 text-emerald-400 font-bold flex items-center gap-2">
                            <Award className="w-5 h-5" />
                            Тест завершен! Итоговый счет: {score} из {selectedMaterial.quizzes.length}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
