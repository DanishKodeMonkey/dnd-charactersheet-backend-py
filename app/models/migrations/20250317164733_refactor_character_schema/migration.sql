/*
  Warnings:

  - You are about to drop the column `age` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `alignment` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `deity` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `eyes` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `hair` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `height` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `sex` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `size` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `statsId` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the column `weight` on the `Character` table. All the data in the column will be lost.
  - You are about to drop the `Skill` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `SkillPoints` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Stat` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `bonuses` to the `Character` table without a default value. This is not possible if the table is not empty.
  - Added the required column `characterDetails` to the `Character` table without a default value. This is not possible if the table is not empty.
  - Added the required column `savingThrows` to the `Character` table without a default value. This is not possible if the table is not empty.
  - Added the required column `skills` to the `Character` table without a default value. This is not possible if the table is not empty.
  - Added the required column `stats` to the `Character` table without a default value. This is not possible if the table is not empty.
  - Added the required column `status` to the `Character` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "Character" DROP CONSTRAINT "Character_statsId_fkey";

-- DropForeignKey
ALTER TABLE "Skill" DROP CONSTRAINT "Skill_characterId_fkey";

-- DropForeignKey
ALTER TABLE "SkillPoints" DROP CONSTRAINT "SkillPoints_characterId_fkey";

-- DropIndex
DROP INDEX "Character_statsId_key";

-- AlterTable
ALTER TABLE "Character" DROP COLUMN "age",
DROP COLUMN "alignment",
DROP COLUMN "deity",
DROP COLUMN "eyes",
DROP COLUMN "hair",
DROP COLUMN "height",
DROP COLUMN "sex",
DROP COLUMN "size",
DROP COLUMN "statsId",
DROP COLUMN "weight",
ADD COLUMN     "bonuses" JSONB NOT NULL,
ADD COLUMN     "characterDetails" JSONB NOT NULL,
ADD COLUMN     "savingThrows" JSONB NOT NULL,
ADD COLUMN     "skills" JSONB NOT NULL,
ADD COLUMN     "stats" JSONB NOT NULL,
ADD COLUMN     "status" JSONB NOT NULL;

-- DropTable
DROP TABLE "Skill";

-- DropTable
DROP TABLE "SkillPoints";

-- DropTable
DROP TABLE "Stat";

-- DropEnum
DROP TYPE "AbilityEnum";

-- DropEnum
DROP TYPE "AlignmentEnum";

-- DropEnum
DROP TYPE "SizeEnum";
