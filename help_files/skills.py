from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Яростный удар"
    stamina = 4.0
    damage = 6.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использовал {self.stamina} стамины и нанёс {self.damage} урона"

class HardShot(Skill):
    name = ...
    stamina = ...
    damage = ...

    def skill_effect(self):
        pass


class ShieldSlam(Skill):
    name = "Удар Щитом"
    stamina = 5.0
    damage = 5.5

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использовал {self.name} и нанёс {self.damage} урона"