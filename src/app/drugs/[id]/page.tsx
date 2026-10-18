export const dynamic = 'force-dynamic';

import { notFound } from 'next/navigation';
import { prisma } from '@/lib/prisma';
import { DrugDetailClient } from './DrugDetailClient';

export default async function DrugDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const drug = await prisma.drug.findUnique({
    where: { id },
    include: {
      pharmClass: {
        include: {
          parent: true,
        },
      },
      atcCode: true,
      manufacturer: true,
      ingredients: {
        include: {
          ingredient: {
            include: {
              mechanisms: true,
              kinetics: true,
            },
          },
        },
      },
      indications: true,
      contraindications: true,
      adverseReactions: true,
      dosages: true,
      warnings: true,
      images: true,
      registrations: true,
      sources: true,
    },
  });

  if (!drug) {
    notFound();
  }

  return <DrugDetailClient drug={drug} />;
}
