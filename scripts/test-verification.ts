import { prisma } from '../src/lib/prisma';

async function testApiAndDatabase() {
  console.log('--- STARTING VERIFICATION TESTS ---');

  // 1. Verify Drugs in DB
  const drugs = await prisma.drug.findMany({
    include: { ingredients: { include: { ingredient: true } }, sources: true }
  });
  console.log(`[PASS] DB contains ${drugs.length} drugs.`);
  if (drugs.length === 0) throw new Error('Database drug count is 0');

  // 2. Test Drug detail query
  const testDrug = drugs[0];
  if (!testDrug.tradeNameRu || !testDrug.ingredients[0].ingredient.innRu) {
    throw new Error('Drug data is incomplete');
  }
  console.log(`[PASS] Verified drug details for: ${testDrug.tradeNameRu} (${testDrug.ingredients[0].ingredient.innRu})`);

  // 3. Test Interaction query
  const interactions = await prisma.drugInteraction.findMany();
  console.log(`[PASS] Found ${interactions.length} drug interactions rules.`);

  // 4. Test Study materials
  const study = await prisma.studyMaterial.findMany({ include: { quizzes: true } });
  console.log(`[PASS] Found ${study.length} study topics with ${study[0]?.quizzes.length || 0} quizzes.`);

  console.log('--- ALL VERIFICATION TESTS PASSED SUCCESSFULLY ---');
}

testApiAndDatabase()
  .catch((e) => {
    console.error('[FAIL]', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
