/*
  Warnings:

  - You are about to drop the `Atendimento` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Atendimento" DROP CONSTRAINT "Atendimento_profissionalId_fkey";

-- DropForeignKey
ALTER TABLE "Atendimento" DROP CONSTRAINT "Atendimento_usuarioId_fkey";

-- DropTable
DROP TABLE "Atendimento";
