-- CreateEnum
CREATE TYPE "AuthProvider" AS ENUM ('manual', 'google', 'discord');

-- CreateEnum
CREATE TYPE "AbilityEnum" AS ENUM ('STRENGTH', 'DEXTERITY', 'CONSTITUTION', 'INTELLIGENCE', 'WISDOM', 'CHARISMA');

-- CreateEnum
CREATE TYPE "AlignmentEnum" AS ENUM ('LAWFUL_GOOD', 'NEUTRAL_GOOD', 'CHAOTIC_GOOD', 'LAWFUL_NEUTRAL', 'TRUE_NEUTRAL', 'CHAOTIC_NEUTRAL', 'LAWFUL_EVIL', 'NEUTRAL_EVIL', 'CHAOTIC_EVIL');

-- CreateEnum
CREATE TYPE "SizeEnum" AS ENUM ('GIANT', 'LARGE', 'MEDIUM', 'SMALL', 'TINY');

-- CreateTable
CREATE TABLE "User" (
    "id" UUID NOT NULL,
    "username" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT,
    "oauth_provider" "AuthProvider" NOT NULL,
    "oauth_id" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Character" (
    "id" UUID NOT NULL,
    "userId" UUID NOT NULL,
    "characterName" TEXT NOT NULL,
    "alignment" "AlignmentEnum" NOT NULL DEFAULT 'TRUE_NEUTRAL',
    "deity" TEXT,
    "size" "SizeEnum" NOT NULL DEFAULT 'MEDIUM',
    "age" INTEGER NOT NULL,
    "sex" TEXT NOT NULL,
    "height" INTEGER NOT NULL,
    "weight" INTEGER NOT NULL,
    "eyes" TEXT NOT NULL,
    "hair" TEXT NOT NULL,
    "class" TEXT NOT NULL,
    "race" TEXT NOT NULL,
    "level" INTEGER NOT NULL DEFAULT 0,
    "statsId" UUID NOT NULL,
    "inventory" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Character_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Stat" (
    "id" UUID NOT NULL,
    "strength" INTEGER NOT NULL,
    "dexterity" INTEGER NOT NULL,
    "constitution" INTEGER NOT NULL,
    "intelligence" INTEGER NOT NULL,
    "wisdom" INTEGER NOT NULL,
    "charisma" INTEGER NOT NULL,
    "tempStrength" INTEGER,
    "tempDexterity" INTEGER,
    "tempConstitution" INTEGER,
    "tempIntelligence" INTEGER,
    "tempWisdom" INTEGER,
    "tempCharisma" INTEGER,

    CONSTRAINT "Stat_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Skill" (
    "id" UUID NOT NULL,
    "characterId" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "ability" "AbilityEnum" NOT NULL,
    "ranks" INTEGER NOT NULL,
    "miscMod" INTEGER,
    "isLearned" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "Skill_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SkillPoints" (
    "id" UUID NOT NULL,
    "characterId" UUID NOT NULL,
    "max" INTEGER NOT NULL,
    "current" INTEGER NOT NULL,

    CONSTRAINT "SkillPoints_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "User_oauth_id_key" ON "User"("oauth_id");

-- CreateIndex
CREATE UNIQUE INDEX "Character_statsId_key" ON "Character"("statsId");

-- CreateIndex
CREATE UNIQUE INDEX "Skill_characterId_key" ON "Skill"("characterId");

-- CreateIndex
CREATE UNIQUE INDEX "SkillPoints_characterId_key" ON "SkillPoints"("characterId");

-- AddForeignKey
ALTER TABLE "Character" ADD CONSTRAINT "Character_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Character" ADD CONSTRAINT "Character_statsId_fkey" FOREIGN KEY ("statsId") REFERENCES "Stat"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Skill" ADD CONSTRAINT "Skill_characterId_fkey" FOREIGN KEY ("characterId") REFERENCES "Character"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SkillPoints" ADD CONSTRAINT "SkillPoints_characterId_fkey" FOREIGN KEY ("characterId") REFERENCES "Character"("id") ON DELETE CASCADE ON UPDATE CASCADE;
