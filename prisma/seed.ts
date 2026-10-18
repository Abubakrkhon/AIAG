import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('Seeding medical database...');

  // 1. Create ATC Codes
  const atcN02BE01 = await prisma.aTCCode.upsert({
    where: { code: 'N02BE01' },
    update: {},
    create: {
      code: 'N02BE01',
      nameRu: 'Парацетамол',
      nameEn: 'Paracetamol',
      level: 5,
    },
  });

  const atcM01AE01 = await prisma.aTCCode.upsert({
    where: { code: 'M01AE01' },
    update: {},
    create: {
      code: 'M01AE01',
      nameRu: 'Ибупрофен',
      nameEn: 'Ibuprofen',
      level: 5,
    },
  });

  const atcA02BC01 = await prisma.aTCCode.upsert({
    where: { code: 'A02BC01' },
    update: {},
    create: {
      code: 'A02BC01',
      nameRu: 'Омепразол',
      nameEn: 'Omeprazole',
      level: 5,
    },
  });

  const atcC08CA01 = await prisma.aTCCode.upsert({
    where: { code: 'C08CA01' },
    update: {},
    create: {
      code: 'C08CA01',
      nameRu: 'Амлодипин',
      nameEn: 'Amlodipine',
      level: 5,
    },
  });

  const atcJ01CA04 = await prisma.aTCCode.upsert({
    where: { code: 'J01CA04' },
    update: {},
    create: {
      code: 'J01CA04',
      nameRu: 'Амоксициллин',
      nameEn: 'Amoxicillin',
      level: 5,
    },
  });

  // 2. Create Pharmacological Classes
  const classAnalgesics = await prisma.pharmacologicalClass.create({
    data: {
      nameRu: 'Анальгетики и антипиретики',
      nameEn: 'Analgesics and Antipyretics',
      code: 'ANALG-01',
      category: 'SPECIAL',
      description: 'Лекарственные средства, оказывающие обезболивающее и жаропонижающее действие.',
    },
  });

  const classNSAID = await prisma.pharmacologicalClass.create({
    data: {
      nameRu: 'Нестероидные противовоспалительные препараты (НПВП)',
      nameEn: 'Nonsteroidal Anti-inflammatory Drugs (NSAIDs)',
      code: 'NSAID-01',
      category: 'SPECIAL',
      description: 'Группа лекарственных средств, обладающих обезболивающим, жаропонижающим и противовоспалительным эффектами.',
    },
  });

  const classPPI = await prisma.pharmacologicalClass.create({
    data: {
      nameRu: 'Ингибиторы протонной помпы (ИПП)',
      nameEn: 'Proton Pump Inhibitors',
      code: 'PPI-01',
      category: 'SPECIAL',
      description: 'Препараты, снижающие секрецию соляной кислоты в желудке путем блокирования H+/K+-АФАзы.',
    },
  });

  const classCCB = await prisma.pharmacologicalClass.create({
    data: {
      nameRu: 'Блокаторы медленных кальциевых каналов (БМКК)',
      nameEn: 'Calcium Channel Blockers',
      code: 'CCB-01',
      category: 'SPECIAL',
      description: 'Препараты, селективно блокирующие кальциевые каналы L-типа в гладкомышечных клетках сосудов и миокарде.',
    },
  });

  const classPenicillins = await prisma.pharmacologicalClass.create({
    data: {
      nameRu: 'Пенициллины широкого спектра действия',
      nameEn: 'Broad-spectrum Penicillins',
      code: 'AB-PEN-01',
      category: 'SPECIAL',
      description: 'Бета-лактамные антибиотики, ингибирующие синтез клеточной стенки бактерий.',
    },
  });

  // 3. Create Active Ingredients
  const ingParacetamol = await prisma.activeIngredient.create({
    data: {
      innRu: 'Парацетамол',
      innEn: 'Paracetamol',
      latinName: 'Paracetamolum',
      chemicalName: 'N-(4-Гидроксифенил)ацетамид',
      casNumber: '103-90-2',
      description: 'Анальгетик-антипиретик из группы анилидов. Блокирует ЦОГ-1 и ЦОГ-2 преимущественно в ЦНС.',
      atcCodeId: atcN02BE01.id,
      pharmClassId: classAnalgesics.id,
      mechanisms: {
        create: [
          {
            target: 'Циклооксигеназа (ЦОГ-1 и ЦОГ-2 в ЦНС)',
            targetType: 'ENZYME',
            interactionType: 'INHIBITOR',
            molecularMechanism: 'Обратимое ингибирование фермента циклооксигеназы в центральной нервной системе, что приводит к угнетению синтеза простагландинов E2.',
            cellularEffect: 'Снижение возбудимости центров терморегуляции и ноцицепции в гипоталамусе.',
            physiologicalEffect: 'Снижение повышенной температуры тела до нормальных значений и повышение порога болевой чувствительности.',
            causalChain: 'Парацетамол -> Ингибирование ЦОГ в ЦНС -> Снижение простагландинов E2 -> Воздействие на гипоталамус -> Анальгезия и антипирез',
          },
        ],
      },
      kinetics: {
        create: [
          {
            bioavailability: '70–90%',
            tMax: '0.5–2 часа',
            cMax: '5–20 мкг/мл',
            proteinBinding: '10–25%',
            volumeOfDistribution: '0.95 Л/кг',
            bbbPenetration: 'Хорошо проникает через ГЭБ',
            placentalPenetration: 'Проникает через плаценту и в грудное молоко в небольших количествах',
            metabolism: 'Печеночный метаболизм (глюкуронидация 60%, сульфатирование 35%, CYP2E1 5% с образованием NAPQI)',
            activeMetabolites: 'N-ацетил-p-бензохинонимин (NAPQI) - токсичный метаболит, обезвреживаемый глутатионом',
            halfLife: '1.5–3 часа',
            clearance: '5 мл/мин/кг',
            excretion: 'Почками (90% в виде конъюгатов, 3% в неизмененном виде)',
            renalHepaticAdjust: 'При выраженной почечной или печеночной недостаточности интервал между приемами увеличивается до 8 часов.',
          },
        ],
      },
    },
  });

  const ingIbuprofen = await prisma.activeIngredient.create({
    data: {
      innRu: 'Ибупрофен',
      innEn: 'Ibuprofen',
      latinName: 'Ibuprofenum',
      chemicalName: '(RS)-2-(4-изобутилфенил)пропановая кислота',
      casNumber: '15687-27-1',
      description: 'НПВП, производное пропионовой кислоты. Оказывает обезболивающее, противовоспалительное и жаропонижающее действие.',
      atcCodeId: atcM01AE01.id,
      pharmClassId: classNSAID.id,
      mechanisms: {
        create: [
          {
            target: 'Циклооксигеназа-1 и Циклооксигеназа-2 (ЦОГ-1 / ЦОГ-2)',
            targetType: 'ENZYME',
            interactionType: 'INHIBITOR',
            molecularMechanism: 'Неселективное неконкурентное блокирование ЦОГ-1 и ЦОГ-2, тормозящее превращение арахидоновой кислоты в простагландины и тромбоксан A2.',
            cellularEffect: 'Угнетение экссудативной и пролиферативной фаз воспаления, торможение агрегации тромбоцитов.',
            physiologicalEffect: 'Выраженное уменьшение боли, отека, гиперемии при воспалительных процессах и снижение температуры.',
            causalChain: 'Ибупрофен -> Блокада ЦОГ-1/ЦОГ-2 -> Торможение арахидонового каскада -> Снижение медиаторов воспаления -> Анальгезия + Противовоспалительный эффект',
          },
        ],
      },
      kinetics: {
        create: [
          {
            bioavailability: '80–90%',
            tMax: '1–2 часа (натощак)',
            cMax: '25–50 мкг/мл',
            proteinBinding: '99% (связывание с альбумином)',
            volumeOfDistribution: '0.12 Л/кг',
            bbbPenetration: 'Проникает в синовиальную жидкость и ЦНС',
            placentalPenetration: 'Проникает через плацентарный барьер. Противопоказан в III триместре.',
            metabolism: 'Метаболизируется в печени (CYP2C9, CYP2C8)',
            activeMetabolites: 'Неактивные гидроксилированные и карбоксилированные метаболиты',
            halfLife: '2–2.5 часа',
            clearance: '3.5 Л/ч',
            excretion: 'Почками (80%) и с желчью (20%)',
            renalHepaticAdjust: 'При тяжелой почечной/печеночной недостаточности применение противопоказано.',
          },
        ],
      },
    },
  });

  const ingOmeprazole = await prisma.activeIngredient.create({
    data: {
      innRu: 'Омепразол',
      innEn: 'Omeprazole',
      latinName: 'Omeprazolum',
      casNumber: '73590-58-6',
      description: 'Ингибитор H+/K+-Атфазы (протонной помпы). Подавляет базальную и стимулированную секрецию соляной кислоты.',
      atcCodeId: atcA02BC01.id,
      pharmClassId: classPPI.id,
      mechanisms: {
        create: [
          {
            target: 'H+/K+-АТФаза (протонный насос париетальных клеток)',
            targetType: 'ENZYME',
            interactionType: 'INHIBITOR',
            molecularMechanism: 'Накапливается в канальцах париетальных клеток, превращается в сульфенамид и ковалентно связывается с дисульфидными группами H+/K+-АТФазы.',
            cellularEffect: 'Необратимое блокирование конечного этапа гидрохлоридогенеза в желудке.',
            physiologicalEffect: 'Быстрое и продолжительное снижение уровня кислотности желудочного сока.',
            causalChain: 'Омепразол -> Активация в кислой среде париетальных клеток -> Ингибирование H+/K+-АТФазы -> Прекращение секреции H+ -> Заживление язв и эррозий',
          },
        ],
      },
      kinetics: {
        create: [
          {
            bioavailability: '30–40% (увеличивается при повторном приеме до 60%)',
            tMax: '0.5–3.5 часа',
            proteinBinding: '95%',
            volumeOfDistribution: '0.3 Л/кг',
            metabolism: 'Полностью метаболизируется в печени ферментами CYP2C19 и CYP3A4',
            halfLife: '0.5–1 час (но действие сохраняется до 24 часов за счет ковалентной связи)',
            excretion: '80% почками, 20% через кишечник',
          },
        ],
      },
    },
  });

  const ingAmlodipine = await prisma.activeIngredient.create({
    data: {
      innRu: 'Амлодипин',
      innEn: 'Amlodipine',
      latinName: 'Amlodipinum',
      casNumber: '88150-42-9',
      description: 'Блокатор медленных кальциевых каналов II поколения, производное дигидропиридина.',
      atcCodeId: atcC08CA01.id,
      pharmClassId: classCCB.id,
      mechanisms: {
        create: [
          {
            target: 'Кальциевые каналы L-типа гладкой мускулатуры сосудов',
            targetType: 'ION_CHANNEL',
            interactionType: 'ANTAGONIST',
            molecularMechanism: 'Селективно ингибирует трансмембранный ток ионов кальция в гладкомышечные клетки сосудов и миокарда.',
            cellularEffect: 'Снижение тонуса гладких мышц артериол и периферического сосудистого сопротивления (ОПСС).',
            physiologicalEffect: 'Снижение систолического и диастолического артериального давления, уменьшение постнагрузки на сердце.',
            causalChain: 'Амлодипин -> Блокада L-каналов Ca2+ -> Снижение внутриклеточного Ca2+ -> Вазодилатация артериол -> Снижение АД и постнагрузки',
          },
        ],
      },
      kinetics: {
        create: [
          {
            bioavailability: '64–80%',
            tMax: '6–12 часов',
            proteinBinding: '97.5%',
            volumeOfDistribution: '21 Л/кг',
            metabolism: 'Медленно и интенсивно метаболизируется в печени (CYP3A4)',
            halfLife: '35–50 часов (подходит для приема 1 раз в сутки)',
            excretion: '60% почками в виде метаболитов, 10% в неизмененном виде',
          },
        ],
      },
    },
  });

  // 4. Create Manufacturers
  const manBayer = await prisma.manufacturer.create({
    data: { name: 'Bayer AG', country: 'Германия', website: 'https://www.bayer.com' },
  });

  const manOTC = await prisma.manufacturer.create({
    data: { name: 'Pharmstandard', country: 'Россия', website: 'https://pharmstd.ru' },
  });

  const manSandoz = await prisma.manufacturer.create({
    data: { name: 'Sandoz / Novartis', country: 'Швейцария', website: 'https://www.sandoz.com' },
  });

  // 5. Create Drugs (Trade Brands)
  const drugParacetamol = await prisma.drug.create({
    data: {
      tradeNameRu: 'Парацетамол Таблетки',
      tradeNameEn: 'Paracetamol Tablets',
      synonyms: 'Панадол, Эффералган, Тайленол',
      form: 'Таблетки',
      dosageStrength: '500 мг',
      packaging: 'Блистер 10 или 20 таблеток',
      registrationStatus: 'Зарегистрировано в ГРЛС',
      isPrescription: false,
      compositionExcipients: 'Крахмал картофельный, стеариновая кислота, желатин.',
      pharmClassId: classAnalgesics.id,
      atcCodeId: atcN02BE01.id,
      manufacturerId: manOTC.id,
      ingredients: {
        create: [{ ingredientId: ingParacetamol.id, amount: '500 мг' }],
      },
      indications: {
        create: [
          { title: 'Болевой синдром слабой и умеренной интенсивности', description: 'Головная боль, зубная боль, миалгия, невралгия, альгодисменорея.' },
          { title: 'Лихорадочный синдром', description: 'Повышенная температура тела при инфекционно-воспалительных заболеваниях.' },
        ],
      },
      contraindications: {
        create: [
          { title: 'Повышенная чувствительность к парацетамолу', type: 'ABSOLUTE' },
          { title: 'Тяжелые нарушения функции печени или почек', type: 'ABSOLUTE' },
          { title: 'Дефицит глюкозо-6-фосфатдегидрогеназы', type: 'RELATIVE' },
          { title: 'Детский возраст до 6 лет', type: 'ABSOLUTE', appliesToPediatric: true },
        ],
      },
      adverseReactions: {
        create: [
          { systemOrganClass: 'Желудочно-кишечный тракт', reaction: 'Тошнота, боль в эпигастрии', frequency: 'UNCOMMON', frequencyDescription: '0.1-1%' },
          { systemOrganClass: 'Аллергические реакции', reaction: 'Кожная сыпь, зуд, крапивница, ангионевротический отек', frequency: 'RARE', frequencyDescription: '<0.1%' },
          { systemOrganClass: 'Кроветворение', reaction: 'Тромбоцитопения, анемия, агранулоцитоз (при длительном приеме)', frequency: 'RARE' },
        ],
      },
      dosages: {
        create: [
          { patientGroup: 'ADULT', route: 'ORAL', dose: '500–1000 мг до 4 раз в сутки', maxDailyDose: '4000 мг (4 г)', instructions: 'Принимать через 1-2 часа после еды, запивая достаточным количеством воды.' },
          { patientGroup: 'PEDIATRIC', route: 'ORAL', dose: '10–15 мг/кг массы тела 3-4 раза в сутки', maxDailyDose: '60 мг/кг', instructions: 'Для детей от 6 до 12 лет.' },
        ],
      },
      warnings: {
        create: [
          { level: 'WARNING', title: 'Риск гепатотоксичности', content: 'Не превышать максимальную суточную дозу (4 г). Совместный прием с алкоголем значительно повышает риск поражения печени.' },
        ],
      },
      images: {
        create: [
          { url: '/images/placeholder-paracetamol.webp', caption: 'Упаковка Парацетамол 500 мг', imageType: 'PACKAGING' },
        ],
      },
      registrations: {
        create: [
          { regNumber: 'ЛС-001402', country: 'РФ', status: 'ACTIVE' },
        ],
      },
      sources: {
        create: [
          { title: 'Государственный реестр лекарственных средств (ГРЛС)', publisher: 'Минздрав РФ', url: 'https://grls.rosminzdrav.ru', jurisdiction: 'РФ', sourceType: 'OFFICIAL_INSTRUCTION' },
          { title: 'WHO ATC/DDD Index - Paracetamol', publisher: 'World Health Organization', url: 'https://www.whocc.no', jurisdiction: 'ВОЗ', sourceType: 'REGISTER' },
        ],
      },
    },
  });

  const drugIbuprofen = await prisma.drug.create({
    data: {
      tradeNameRu: 'Нурофен Экспресс',
      tradeNameEn: 'Nurofen Express',
      synonyms: 'Ибупрофен, МИГ 400, Фаспик',
      form: 'Капсулы мягкие',
      dosageStrength: '200 мг',
      packaging: 'Блистер 10 капсул',
      registrationStatus: 'Зарегистрировано в ГРЛС',
      isPrescription: false,
      compositionExcipients: 'Макрогол 600, калия гидроксид, желатин, сорбитол.',
      pharmClassId: classNSAID.id,
      atcCodeId: atcM01AE01.id,
      manufacturerId: manBayer.id,
      ingredients: {
        create: [{ ingredientId: ingIbuprofen.id, amount: '200 мг' }],
      },
      indications: {
        create: [
          { title: 'Головная и зубная боль', description: 'Быстрое купирование острой боли.' },
          { title: 'Суставные и мышечные боли', description: 'Ревматоидный артрит, остеоартроз, миалгия.' },
          { title: 'Лихорадочные состояния', description: 'При ОРВИ и гриппе.' },
        ],
      },
      contraindications: {
        create: [
          { title: 'Эрозивно-язвенные поражения ЖКТ в фазе обострения', type: 'ABSOLUTE' },
          { title: ' Полное или неполное сочетание бронхиальной астмы и полипоза носа (Аспириновая триада)', type: 'ABSOLUTE' },
          { title: 'Беременность (III триместр)', type: 'ABSOLUTE', appliesToPregnancy: true },
        ],
      },
      adverseReactions: {
        create: [
          { systemOrganClass: 'ЖКТ', reaction: 'НПВП-гастропатия, абдоминальная боль, изжога', frequency: 'COMMON', frequencyDescription: '1-10%' },
          { systemOrganClass: 'Нервная система', reaction: 'Головная боль, головокружение, бессонница', frequency: 'UNCOMMON' },
        ],
      },
      dosages: {
        create: [
          { patientGroup: 'ADULT', route: 'ORAL', dose: '200–400 мг 3–4 раза в сутки', maxDailyDose: '1200 мг', instructions: 'Принимать во время или после еды.' },
        ],
      },
      warnings: {
        create: [
          { level: 'WARNING', title: 'Гастроинтестинальный риск', content: 'Длительное применение может вызывать язвы и кровотечения ЖКТ. Рекомендуется совместный прием с ИПП (омепразол) у пациентов группы риска.' },
        ],
      },
      sources: {
        create: [
          { title: 'Официальная инструкция Нурофен Экспресс', publisher: 'ГРЛС', url: 'https://grls.rosminzdrav.ru', jurisdiction: 'РФ', sourceType: 'OFFICIAL_INSTRUCTION' },
        ],
      },
    },
  });

  const drugOmeprazole = await prisma.drug.create({
    data: {
      tradeNameRu: 'Омез',
      tradeNameEn: 'Omez',
      synonyms: 'Омепразол, Лосек, Ультоп',
      form: 'Капсулы кишечнорастворимые',
      dosageStrength: '20 мг',
      packaging: '30 капсул в упаковке',
      registrationStatus: 'Зарегистрировано',
      isPrescription: false,
      compositionExcipients: 'Сахароза, лактоза, гипромеллоза, титана диоксид.',
      pharmClassId: classPPI.id,
      atcCodeId: atcA02BC01.id,
      manufacturerId: manSandoz.id,
      ingredients: {
        create: [{ ingredientId: ingOmeprazole.id, amount: '20 мг' }],
      },
      indications: {
        create: [
          { title: 'Язвенная болезнь желудка и 12-перстной кишки', description: 'Лечение и профилактика рецидивов.' },
          { title: 'ГЭРБ (Гастроэзофагеальная рефлюксная болезнь)', description: 'Симптоматическое лечение изжоги и кислый рефлюкс.' },
          { title: 'Эрадикация Helicobacter pylori', description: 'В составе комбинированной антибактериальной терапии.' },
        ],
      },
      contraindications: {
        create: [
          { title: 'Повышенная чувствительность к замещенным бензимидазолам', type: 'ABSOLUTE' },
          { title: 'Одновременный прием с нелфинавиром', type: 'ABSOLUTE' },
        ],
      },
      adverseReactions: {
        create: [
          { systemOrganClass: 'ЖКТ', reaction: 'Диарея, запор, метеоризм, боль в животе', frequency: 'COMMON' },
        ],
      },
      dosages: {
        create: [
          { patientGroup: 'ADULT', route: 'ORAL', dose: '20 мг 1 раз в сутки утром', maxDailyDose: '40 мг', instructions: 'Проглатывать целиком за 30 минут до еды, запивая половиной стакана воды.' },
        ],
      },
      sources: {
        create: [
          { title: 'Инструкция по медицинскому применению препарата Омез', publisher: 'ГРЛС', jurisdiction: 'РФ', sourceType: 'OFFICIAL_INSTRUCTION' },
        ],
      },
    },
  });

  // 6. Create Drug Interactions
  await prisma.drugInteraction.create({
    data: {
      ingredientAId: ingParacetamol.id,
      ingredientBId: ingIbuprofen.id,
      severity: 'LOW',
      mechanism: 'Комбинированная анальгезия через центральный (парацетамол) и периферический (ибупрофен) механизмы.',
      clinicalConsequence: 'Усиление обезболивающего и жаропонижающего эффекта без взаимного повышения токсичности при соблюдении доз.',
      recommendation: 'Допускается краткосрочный чередующийся или комбинированный прием по рекомендации врача.',
    },
  });

  await prisma.drugInteraction.create({
    data: {
      ingredientAId: ingIbuprofen.id,
      ingredientBId: ingAmlodipine.id,
      severity: 'MODERATE',
      mechanism: 'НПВП ингибируют почечные простагландины, вызывают задержку натрия и воды и ослабляют гипотензивное действие БМКК.',
      clinicalConsequence: 'Возможно снижение эффективного контроля артериального давления.',
      recommendation: 'Контролировать артериальное давление при совместном назначении.',
    },
  });

  // 7. Create Study Materials & Quizzes
  const studyNSAID = await prisma.studyMaterial.create({
    data: {
      topic: 'Нестероидные противовоспалительные препараты (НПВП)',
      category: 'SPECIAL_PHARMACOLOGY',
      briefText: 'НПВП блокируют ЦОГ-1 и ЦОГ-2, уменьшая синтез простагландинов. Обладают 3 эффектами: анальгезирующим, жаропонижающим и противовоспалительным.',
      standardText: 'Механизм действия НПВП связан с ингибированием фермента циклооксигеназы (ЦОГ). ЦОГ-1 является конститутивной и защищает слизистую ЖКТ, а ЦОГ-2 индуцируется при воспалении. Блокада ЦОГ-1 обусловливает побочные эффекты (язвы, кровотечения), а ЦОГ-2 — терапевтический эффект.',
      detailedText: 'Арахидоновый каскад: Фосфолипиды мембран под действием Фосфолипазы А2 превращаются в Арахидоновую кислоту. ЦОГ метаболизирует её в Простагландин H2, из которого синтезируются PGE2, PGI2 (простациклин) и TXA2 (тромбоксан). НПВП конкурируют за активный центр ЦОГ.',
      advancedText: 'Селективность НПВП: Селективные ингибиторы ЦОГ-2 (целекоксиб) минимально повреждают ЖКТ, однако повышают риск тромбоэмболических осложнений за счет дисбаланса PGI2/TXA2. Неселективные (ибупрофен, диклофенак) имеют более высокий гастроинтестинальный риск.',
      keyTakeways: JSON.stringify([
        'Триада эффектов: Обезболивание, Жаропонижение, Противовоспалительное действие.',
        'ЦОГ-1 = Защита желудка и тромбоциты.',
        'ЦОГ-2 = Воспаление и боль.',
      ]),
      quizzes: {
        create: [
          {
            question: 'Какая изоформа циклооксигеназы отвечает за синтез простагландинов, защищающих слизистую оболочку желудка?',
            optionsJson: JSON.stringify(['ЦОГ-1', 'ЦОГ-2', 'ЦОГ-3', '5-ЛОГ']),
            correctOptionIndex: 0,
            explanation: 'ЦОГ-1 является физиологической (конститутивной) изоформой, обеспечивающей синтез защитных простагландинов E2 и I2 в слизистой желудка.',
          },
          {
            question: 'Какой основной побочный эффект характерен для неселективных НПВП?',
            optionsJson: JSON.stringify(['НПВП-гастропатия (язвы ЖКТ)', 'Атриовентрикулярная блокада', 'Гипогликемия', 'Остеопороз']),
            correctOptionIndex: 0,
            explanation: 'Ингибирование ЦОГ-1 приводит к снижению выработки защитной слизи и гидрокарбонатов в желудке, вызывая НПВП-гастропатию.',
          },
        ],
      },
    },
  });

  console.log('Database seeded successfully!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
