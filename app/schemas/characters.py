from pydantic import BaseModel, Field
from typing import Dict, Set, Optional
from typing_extensions import Literal
from enum import Enum


# Pydantic model reflecting central state object on frontend typescript


## Character Details section
class AlignmentEnum(str, Enum):
    LAWFUL_GOOD = "LAWFUL_GOOD"
    NEUTRAL_GOOD = "NEUTRAL_GOOD"
    CHAOTIC_GOOD = "CHAOTIC_GOOD"
    LAWFUL_NEUTRAL = "LAWFUL_NEUTRAL"
    TRUE_NEUTRAL = "TRUE_NEUTRAL"
    CHAOTIC_NEUTRAL = "CHAOTIC_NEUTRAL"
    LAWFUL_EVIL = "LAWFUL_EVIL"
    NEUTRAL_EVIL = "NEUTRAL_EVIL"
    CHAOTIC_EVIL = "CHAOTIC_EVIL"


class SizeEnum(str, Enum):
    GIANT = "GIANT"
    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"
    TINY = "TINY"


class ClassBaseSaves(BaseModel):
    fortitudeBase: int
    reflexBase: int
    willBase: int


class ClassSpellShape(BaseModel):
    spellsPerDay: Dict[Literal[0, 1, 2, 3, 4, 5, 6], int]  # No more lv 10 spells!
    spellsKnown: Dict[Literal[0, 1, 2, 3, 4, 5, 6], int]


class ClassShape(BaseModel):
    className: str
    baseAttack: int
    baseSkill: int
    classSkills: Set[str] = set()
    specials: list[str] = []
    spells: Optional[ClassSpellShape] = None
    baseSave: ClassBaseSaves


class RaceShape(BaseModel):
    raceName: str
    raceBase: int
    raceBonus: int


class SizeShape(BaseModel):
    sizeName: SizeEnum
    ACMod: int


class CharacterDetails(BaseModel):
    characterName: str
    playerName: str

    characterClass: ClassShape

    baseAttack: int
    baseSkill: int

    race: RaceShape

    alignment: AlignmentEnum

    deity: str
    level: int

    size: SizeShape

    ACMod: int
    age: int
    sex: str
    height: int
    weight: int
    eyes: str
    hair: str


## Stats section


class ScoresModifiersShape(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Stats(BaseModel):
    scores: ScoresModifiersShape
    modifiers: ScoresModifiersShape
    tempScores: Optional[ScoresModifiersShape]
    tempModifiers: Optional[ScoresModifiersShape]


## Status section


class ArmorClassShape(BaseModel):
    aBonus: int
    naturalArmor: int
    miscModifier: int


class HealthShape(BaseModel):
    maxHealth: int
    currentHealth: int
    damage: int
    hitDie: int


class SpeedShape(BaseModel):
    speed: int


class Status(BaseModel):
    armorClass: ArmorClassShape
    health: HealthShape
    speed: SpeedShape


## bonus section


class InitiativeShape(BaseModel):
    initiativeTotal: int
    miscModifier: int


class Bonus(BaseModel):
    baseAttackBonus: int
    initiative: InitiativeShape


## savingThrows section


class SavingThrowsShape(BaseModel):
    miscMod: int
    magicMod: int
    tempMod: int
    total: int


class SavingThrows(BaseModel):
    fortitude: SavingThrowsShape
    reflex: SavingThrowsShape
    will: SavingThrowsShape


## skills section


class AbilityNameEnum(str, Enum):
    strength = "strength"
    dexterity = "dexterity"
    constitution = "constitution"
    wisdom = "wisdom"
    intelligence = "intelligence"
    charisma = "charisma"


class SkillPointsShape(BaseModel):
    maximum: int
    current: int


class SkillsShape(BaseModel):
    learned: bool
    abilityName: AbilityNameEnum
    ranks: int
    miscMod: int
    skillMod: int


class Skills(BaseModel):
    skillPoints: SkillPointsShape
    skills: Dict[str, SkillsShape]


## Finally, assemble to State object


class State(BaseModel):
    characterDetails: CharacterDetails
    stats: Stats
    status: Status
    bonus: Bonus
    savingThrows: SavingThrows
    skills: Skills
