from flask import Flask, render_template, redirect, request

import re

from unit import PlayerUnit, EnemyUnit, BaseUnit
from classes import unit_classes
from equipment import Equipment

from base import Arena

app = Flask(__name__, template_folder="R:\Python\coursework_5\\templates")

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

header = ['Выберите героя', 'Выберите врага']

arena =  Arena()


@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    arena = Arena()
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template("fight.html", heroes=heroes)

@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if arena.game_is_running == True:
        results = arena.player_hit()
        return render_template("fight.html", heroes=heroes, results=results)
    else:
        return render_template("fight.html", heroes=heroes)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running == True:
        results = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, results=results)
    else:
        return render_template("fight.html", heroes=heroes)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running == True:
        results = arena.next_turn()
        return render_template("fight.html", heroes=heroes, results=results)
    else:
        return render_template("fight.html", heroes=heroes)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == 'GET':
        equipment = Equipment()
        result = {
            "header": header[0],    # для названия страниц
            "classes": unit_classes,    # для названия классов
            "weapons": equipment.get_weapons_names(), # для названия оружия
            "armors": equipment.get_armors_names()     # для названия брони
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        equipment = Equipment()
        data = request.form
        hero = request.form.get('unit_class')
        unit = PlayerUnit(unit_classes[hero])
        unit.name = data['name']

        
        weapon_name = equipment.get_equipment_names(data['weapon'])
        unit.weapon = equipment.get_weapon(weapon_name)
        unit.equip_weapon(unit.weapon)

       
        armor_name = equipment.get_equipment_names(data['armor'])
        unit.armor = equipment.get_armor(armor_name)
        unit.equip_armor(unit.armor)

        heroes['player'] = unit
        return redirect('/choose-enemy/')

@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        equipment = Equipment()
        result = {
            "header": header[1],      # для названия страниц
            "classes": unit_classes,    # для названия классов
            "weapons": equipment.get_weapons_names(), # для названия оружия
            "armors": equipment.get_armors_names()     # для названия брони
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        equipment = Equipment()
        data = request.form
        hero = request.form.get('unit_class')
        unit = EnemyUnit(unit_classes[hero])
        unit.name = data['name']

        
        weapon_name = equipment.get_equipment_names(data['weapon'])
        unit.weapon = equipment.get_weapon(weapon_name)
        unit.equip_weapon(unit.weapon)

        
        armor_name = equipment.get_equipment_names(data['armor'])
        unit.armor = equipment.get_armor(armor_name)
        unit.equip_armor(unit.armor)

        heroes['enemy'] = unit
        return redirect('/fight/')
if __name__ == "__main__":
    app.run()
