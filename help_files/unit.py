from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional
from skills import Skill, ShieldSlam

class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = None
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Weapon
        self.armor = Armor
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp)# TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return  round(self.stamina)# TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        self.armor = armor
    

    def _count_damage(self, target: BaseUnit) -> int:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage = round(damage - target.armor.defence * target.unit_class.armor)
        else:
            damage = damage - target.armor.defence
        get_damage = target.get_damage(damage)
        return get_damage

    def get_damage(self, damage: int) -> Optional[int]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        health = self.hp - damage 
        self.hp = health
        return damage
        

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернет нам строку которая характеризует выполнение умения
        """

        if self._is_skill_used:
            return "Навык использован"
        else:
            self._is_skill_used = True
            use_skill = self.unit_class.skill.use(user=self, target=target)
            return use_skill

class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        elif self.weapon.stamina_per_hit < self.armor.stamina_per_turn:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        # TODO результат функции должен возвращать следующие строки:
        
        
        

class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if self._is_skill_used == True:    
            if self.stamina >= self.weapon.stamina_per_hit:
                damage = self._count_damage(target)
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
            elif self.weapon.stamina_per_hit < self.armor.stamina_per_turn:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
            else:
                return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if self._is_skill_used == False:
            self._is_skill_used = True
            self.unit_class.skill.use(user=self, target=target)
            return  f"{self.name} исользовал умение {self.unit_class.skill.name} и нанёс {self.unit_class.skill.damage} урона"
        
        # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
        
        
        


