from dataclasses import dataclass

from skills import Skill, ShieldSlam, FuryPunch

@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    armor: float
    stamina: float
    skill: Skill


WarriorClass =  UnitClass('Alesha', 50.0, 40.0, 7.0, 1.3, 1.1, ShieldSlam()) # TODO Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов

ThiefClass = UnitClass('Oleg', 40.0, 30.0, 19.5, 1.1, 1.3 , FuryPunch()) # TODO действуем так же как и с войном

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}

