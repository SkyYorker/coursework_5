from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json
import re

@dataclass
class Armor:
     id : int
     name : str
     defence : float
     stamina_per_turn : float


@dataclass
class Weapon:
    id : int
    name : str
    min_damage : float
    max_damage : float
    stamina_per_hit : float

    # @property
    # def damage(self):
    #     return self.damage
    
    @property
    def damage(self):
        data = Equipment()
        for i in data.get_weapons_names():
            if self.name == i.name:
                damage = uniform(i.min_damage, i.max_damage)
                return damage

@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    weapons: List[Weapon] 
    armors: List[Armor]



class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # TODO возвращает объект оружия по имени
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        return self.equipment.weapons

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        return self.equipment.armors

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        
        
        equipment_file = open("R:\Python\coursework_5\data\equipment.json", encoding='utf8')
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError


    def get_equipment_names(*args):
        reg_equipment = re.search(r"\'(\w+\s\w+)\'|\'(\w+)\'", args[1])
        new_str = reg_equipment[0].replace("'", '')
        return new_str
