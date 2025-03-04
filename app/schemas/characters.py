from pydantic import BaseModel, Field
from typing import Dict, Set, Optional


# Pydantic model reflecting central state object on frontend typescript


class ClassBaseSaves(BaseModel):
    fortitudeBase: int
    reflexBase: int
    willBase: int


class ClassSpellShape(BaseModel):
    spellsPerDay: Dict[int, int]
    spellsKnown: Dict[int, int]


class CharacterDetails(BaseModel):
    characterName: str
    playerName: str
    className: str
    baseAttack: int
    baseSkill: int
    classSkills: Optional[Set[str]] = None
    specials: Optional[list[str]] = None
    spells: Optional[ClassSpellShape] = None
    baseSave: ClassBaseSaves
    raceName: str
    raceBase: int
    raceBonus: int
    alignment: str
    deity: str
    level: int
    sizeName: str
    ACMod: int
    age: int
    sex: str
    height: int
    weight: int
    eyes: str
    hair: str


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
