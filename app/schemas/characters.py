from pydantic import BaseModel, Field
from typing import Dict, Set, Optional
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
    spellsPerDay: Dict[int, int]
    spellsKnown: Dict[int, int]


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


class ModifiersShape(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Stats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    modifiers: Dict[str, int]
    tempScores: Dict[str, int]
    tempModifiers: Dict[str, int]


class SaveThrow(BaseModel):
    magicMod: int
    miscMod: int
    tempMod: int
    total: Optional[int] = None


class SavingThrows(BaseModel):
    fortitude: SaveThrow
    reflex: SaveThrow
    will: SaveThrow


class ArmorClassType(BaseModel):
    aBonus: int
    naturalArmor: int
    miscModifier: int


class HealthStatus(BaseModel):
    maxHealth: int
    currentHealth: int
    damage: int
    hitDie: int


class SpeedType(BaseModel):
    speed: int


class Status(BaseModel):
    armorClass: ArmorClassType
    health: HealthStatus
    speed: SpeedType


class Bonus(BaseModel):
    baseAttackBonus: int
    initiative: int


class Skill(BaseModel):
    learned: bool
    abilityName: str
    ranks: int
    miscMod: int
    skillMod: int


class SkillPoints(BaseModel):
    max: int
    current: int


class Skills(BaseModel):
    skillPoints: SkillPoints
    skills: Dict[str, Skill]


class State(BaseModel):
    CharacterDetails: CharacterDetails
    stats: Stats
    status: Status
    bonus: Bonus
    SavingThrows: SavingThrows
    skills: Skills
