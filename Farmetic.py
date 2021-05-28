import pygame
import random

from My_classes.Farmetic_classes import AggressiveMobs, Mob, PeacefulMobs, Heretic, heretic, current_interface, \
    mobs_directions, mobs_list, bushes_list, trails_list, drops_list, trees_list, leftside_drops_list, home_drops_list, \
    decors_list, leftside_decors_list, crates_list, regrowing_list, \
    leftside_stones_list, leftside_mobs_list, menu_decors_list, \
    produce_new_peaceful_mob, produce_new_aggressive_mob, print_for_mob, print_on_screen, \
    Trail, Bush, Tree, Stump, Sapling, HighGrass, Rock, Drop, Fuel, Meltable, Eatable, Log, Stone, Coal, IronOre, IronIngot, Pine, \
    Berry, DroppedBerry, Juice, RawMeat, Meat, \
    House, Decor, Stones, Fog, Blood, Smoke, Steps, Torch, Particles, Flashes, FallingBlood, FallingLeaves, Powder, Bed, \
    WorkBenches, \
    JuiceMaker, GridStone, Furnace, Weapon, Sword, Stick, PickAxe, SharpenedStone, Shovel, Storage, Chest, Crate, \
    BackPack, Bag, Sign, \
    blood_setting, tick, day_tick, sleeping, home, x_home, y_home, h_length, h_width
import My_classes.Farmetic_classes

'''
TODO:
Доработать режим Бога
Добавить ящики, которые можно создавать и ставить !!

'''
pygame.init()
pygame.mixer.init()

display = pygame.display.set_mode((1440, 900), pygame.FULLSCREEN)
sign_surf = pygame.Surface((1440, 900))
bloor_surf = pygame.Surface((1440, 900))
bloor_surf.set_alpha(15)
sign_surf.set_alpha(150)
pygame.display.set_caption('Farmetic')

'''
Настройки
'''

game = True
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


def put_item_in_the_storage(storage, i):
    if len(storage.storage) < storage.max_capability and len(heretic.inventory) > i:
        storage.storage.append(heretic.inventory[i])
        heretic.inventory.pop(i)


def open(bench):
    global current_interface

    current_interface = bench


def close():
    global current_interface
    current_interface = 'none'


volume = 80
pygame.mixer.music.load(r'C:\Users\User\Desktop\Farmetic-master\Home track.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)
chopping_sound_1 = pygame.mixer.Sound(r'C:\Users\User\Desktop\Farmetic-master\chopping sound 1.wav')
sword_image = pygame.image.load(r"C:\Users\User\Desktop\Farmetic-master\sword.png")
crate_image = pygame.image.load(r"C:\Users\User\Desktop\Farmetic-master\crate.png").convert_alpha()
crate_image = pygame.transform.scale(crate_image, (crate_image.get_width() * 2, crate_image.get_height() * 2))

directions = ['vert', 'gor']
drop_type = ['Аптечка', 'Броня', 'Оружие']

sign_to_leftside = Sign(100, 400, "left",
                        ["Лефт-Сайд", "Лефт-Сайд - тихая пустынная долина", "Ее особенность - каменные глыбы,",
                         "являющиеся источниками камня и руд", "Из-за подземных вод они",
                         "постепенно восстанавливаются"],
                        [list(range(10, 170)), list(range(350, 500))])

sign_to_home = Sign(1300, 400, "right", ["Поляна", "Место, где находится ваш дом.",
                                         "Когда вы впервые здесь очутились,", "то решили тут обосноваться, так как",
                                         "это место богато разными ягодами,", "животными и деревьями"],
                    [list(range(1210, 1370)), list(range(350, 500))])

'''
Локации
'''

'''
Блок создания уникальных объектов
'''

bed = Bed(310, 160, [[i for i in range(300, 400)], [j for j in range(160, 270)]])
juicemaker = JuiceMaker(550, 160, [[i for i in range(500, 650)], [j for j in range(160, 240)]], -1, 'none')
furnace = Furnace(700, 160, [[i for i in range(700, 800)], [j for j in range(160, 260)]], -1, 'off')
torch = Torch(1200, 350, 0, 0, [list(range(1100, 1300)), list(range(290, 400))])
chest = Chest(850, 160, 120, 100, [], 20, [list(range(840, 980)), list(range(150, 260))],
              [list(range(850, 970)), list(range(160, 260))], 'Сундук')
gridstone = GridStone(980, 330, [list(range(940, 1050)), list(range(300, 420))], -1, 'off')

gridstone_recipes = ['Заточ. камень', "Копье", "Топор", "Кирка", "Лопата", 'Ящик', 'Сумка', "Щипцы", "Пластина"]

clock = pygame.time.Clock()
active_font = pygame.font.Font(None, 60)
inventory_font = pygame.font.SysFont('Cambria', 75)
title_font = pygame.font.SysFont('Cambria', 125)
title = ''
FARMETIC = 'FARMETIC'
going_to_menu = 0

active = False
collect_berry = active_font.render('Собрать ягоды', True, (0, 0, 0))
pick_up = active_font.render('Подобрать', True, (0, 0, 0))
enter = active_font.render('Войти', True, (0, 0, 0))
exit_home = active_font.render('Выйти', True, (0, 0, 0))
inactive = active_font.render('Нечего использовать', True, (0, 0, 0))
chopping = active_font.render('Рубить', True, (0, 0, 0))
leftside_tp = active_font.render('К Лефт-Саид', True, (0, 0, 0))
home_tp = active_font.render('К дому', True, (0, 0, 0))
sleep = active_font.render('Спать', True, (0, 0, 200))
juicemaker_sign = active_font.render('Соковыжималка', True, (200, 0, 0))

picked_up = None
chosen_item = None
inactive_time = 0
picked_up_time = 0
eat_time = 0
energy_boost = ''
drop_active = False
home_active = False
chopping_active = False
on_path = False
tp_to_left_side = False
tp_to_home = False
go_to_bed = False
b_owner = None
d_owner = None
t_owner = None
m_owner = None
rock_owner = None
crate_owner = None
menu_tick = 0
day_return = False
drop_appear_tick = 500
z_z_Z = ''
main_mob = Mob(0, 0, 'left', [0, 2], [3, 3], 0, 0, True, 5, 0, 0, 0, '', 0, 0, 0, 'none', 'none')
current_attached = None
current_mean = 0
heretic.x = x_home + 155
heretic.y = y_home + 50
settings = {"Кровь": blood_setting, "Режим Бога": My_classes.Farmetic_classes.god_mode,
            "Спавн гоблинов": My_classes.Farmetic_classes.goblins_spawn}

'''
Создание троп
'''
for i in range(random.randint(4, 6)):
    trails_direction = random.choice(directions)
    if trails_direction == 'vert':
        x = random.randint(100, 1300)
        y = random.randint(100, 900)
        length = random.choice([j for j in range(50, 76) if not j % 10])
        width = random.choice([j for j in range(300, 901) if not j % 10])

    else:
        x = random.randint(100, 1300)
        y = random.randint(100, 900)
        length = random.choice([j for j in range(300, 901) if not j % 10])
        width = random.choice([j for j in range(50, 76) if not j % 10])
    trails_list.append(Trail(x, y, trails_direction, length, width, [[j for j in range(x, x + length)],
                                                                     [k for k in range(y, y + width)]],
                             [[j for j in range(x, x + length)], [k for k in range(y, y + width)]],
                             [[str(j) + " " + str(k) for j in range(x, x + length, 10)] for k in range(y, y + width,
                                                                                                       10)], []))
'''
Создание кустов
'''
for i in range(random.randint(3, 5)):
    x = random.randint(100, 1200)
    y = random.randint(100, 800)
    berries_list = [Berry(random.randint(x, x + 90),
                          random.randint(y, y + 90), 'Ягода',
                          ['Спелая сочная ягода', 'Восстанавливает энергию']) for j in range(random.randint(2, 3))]
    bushes_list.append(Bush(x, y, 450, berries_list, [[k for k in range(x - 120, x + 130)],
                                                      [j for j in range(y - 120, y + 140)]],
                            [[k for k in range(x, x + 100)], [j for j in range(y, y + 100)]]))

for i in range(random.randint(3, 5)):
    x = random.randint(100, 1200)
    y = random.randint(100, 800)
    trees_list.append(Tree(x, y, random.randint(10, 15), [[j for j in range(x - 120, x + 70)],
                                                          [k for k in range(y - 70, y + 100)]]))

for tree in range(len(trees_list)):
    for tree2 in range(tree, len(trees_list)):
        if trees_list[tree2].y < trees_list[tree].y:
            trees_list[tree], trees_list[tree2] = trees_list[tree2], trees_list[tree]

'''
Создание камешков
'''
for i in range(random.randint(7, 12)):
    leftside_decors_list.append(Stones(random.randint(100, 1300), random.randint(100, 800), random.randint(10, 40),
                                       random.randint(10, 40), -1))

'''
Создание животных
'''
for i in range(random.randint(5, 7)):
    produce_new_peaceful_mob()

"""
Создание булыжников
"""
for i in range(random.randint(7, 10)):
    x = random.randint(100, 1300)
    y = random.randint(100, 800)
    leftside_stones_list.append(Rock(x, y, 10, [list(range(x - 50, x + 150)), list(range(y - 50, y + 150))],
                                     [list(range(x - 30, x + 100)), list(range(y, y + 100))], 900,
                                     random.choice(['general', 'general', 'coal', 'coal', 'iron'])))

'''
Создание трав и других растущих структур(в разработке)
'''
for i in range(random.randint(5, 7)):
    x = random.randint(100, 1300)
    y = random.randint(100, 800)
    regrowing_list.append(HighGrass(x, y, [list(range(x - 50, x + 150)), list(range(y - 50, y + 150))],
                                    [list(range(x, x + 60)), list(range(y, y + 60))], 'uncut', 0, 0))

while game:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            '''
            Повторная генерация
            '''

            if event.button == 2:
                if not My_classes.Farmetic_classes.inventory_mode:
                    trails_list = []
                    for i in range(random.randint(4, 6)):
                        trails_direction = random.choice(directions)
                        if trails_direction == 'vert':
                            x = random.randint(100, 1300)
                            y = random.randint(100, 900)
                            length = random.choice([j for j in range(50, 76) if not j % 25])
                            width = random.choice([j for j in range(300, 901) if not j % 25])

                        else:
                            x = random.randint(100, 1300)
                            y = random.randint(100, 900)
                            length = random.choice([j for j in range(300, 901) if not j % 25])
                            width = random.choice([j for j in range(50, 76) if not j % 25])
                        trails_list.append(Trail(x, y, trails_direction,
                                                 length, width,
                                                 [[j for j in range(x, x + length)], [k for k in range(y, y + width)]],
                                                 [[j for j in range(x, x + length)], [k for k in range(y, y + width)]],
                                                 [[str(j) + " " + str(k) for j in range(x, x + length, 10)]
                                                  for k in range(y, y + width, 10)], []))

                    bushes_list = []
                    for i in range(random.randint(3, 5)):
                        x = random.randint(100, 1200)
                        y = random.randint(100, 800)
                        berries_list = [Berry(random.randint(x, x + 90), random.randint(y, y + 90), 'Ягода',
                                              ['Спелая сочная ягода', 'Восстанавливает энергию']) for j in
                                        range(random.randint(2, 3))]
                        bushes_list.append(Bush(x, y, 450, berries_list, [[k for k in range(x - 120, x + 130)],
                                                                          [j for j in range(y - 120, y + 130)]],
                                                [[k for k in range(x, x + 100)], [j for j in range(y, y + 100)]]))

                    trees_list = []
                    for i in range(random.randint(3, 5)):
                        x = random.randint(100, 1200)
                        y = random.randint(100, 800)
                        trees_list.append(Tree(x, y, random.randint(10, 15),
                                               [[j for j in range(x - 120, x + 80)],
                                                [k for k in range(y - 70, y + 100)]]))

                    for tree in range(len(trees_list)):
                        for tree2 in range(tree, len(trees_list)):
                            if trees_list[tree2].y < trees_list[tree].y:
                                trees_list[tree], trees_list[tree2] = trees_list[tree2], trees_list[tree]
            elif event.button == 1:

                if My_classes.Farmetic_classes.current_location == 'menu':
                    if 450 <= event.pos[0] <= 950 and menu_tick > 600:
                        if 290 <= event.pos[1] <= 400:
                            My_classes.Farmetic_classes.current_location = 'home'
                        elif 570 <= event.pos[1] <= 680:
                            pygame.quit()
                        elif 430 <= event.pos[1] <= 540:
                            My_classes.Farmetic_classes.current_location = 'settings'

                elif My_classes.Farmetic_classes.current_location == 'settings':
                    if 600 <= event.pos[0] <= 750:
                        if 250 <= event.pos[1] <= 300:
                            settings["Кровь"] = not settings["Кровь"]
                            blood_setting = not blood_setting
                        elif 380 <= event.pos[1] <= 430:
                            My_classes.Farmetic_classes.god_mode = not My_classes.Farmetic_classes.god_mode
                            settings["Режим Бога"] = not settings["Режим Бога"]

                        elif 460 <= event.pos[1] <= 510:
                            My_classes.Farmetic_classes.goblins_spawn = not My_classes.Farmetic_classes.goblins_spawn
                            settings["Спавн гоблинов"] = not settings["Спавн гоблинов"]

                if isinstance(m_owner, Mob) and event.pos[0] in m_owner.visible_zone[0] and event.pos[1] in \
                        m_owner.visible_zone[
                            1] and not heretic.is_tired and not My_classes.Farmetic_classes.inventory_mode and not heretic.attack_time:
                    heretic.attack_mob(m_owner)

                elif drop_active and len(heretic.inventory) < 20 and not My_classes.Farmetic_classes.at_home:
                    picked_up_time = 60
                    if My_classes.Farmetic_classes.current_location == 'home':
                        if isinstance(drops_list[d_owner], BackPack):
                            drops_list[d_owner].equip()
                        else:
                            heretic.inventory.append(drops_list[d_owner])
                        picked_up = active_font.render('Я подобрал ' + drops_list[d_owner].type, True, (0, 0, 0))
                        drops_list.pop(d_owner)
                    elif My_classes.Farmetic_classes.current_location == 'leftside':
                        if isinstance(leftside_drops_list[d_owner], BackPack):
                            leftside_drops_list[d_owner].equip()
                        else:
                            heretic.inventory.append(leftside_drops_list[d_owner])
                        picked_up = active_font.render('Я подобрал ' + leftside_drops_list[d_owner].type, True,
                                                       (0, 0, 0))
                        leftside_drops_list.pop(d_owner)
                    drop_active = None

                elif current_interface != 'none':
                    if isinstance(current_interface, Storage):
                        if event.pos[0] < 600:
                            index = (event.pos[0] - 50) // 150 + (event.pos[1] - 100) // 150 * 4
                            if current_interface.description[-1] == 'Пусто':
                                current_interface.description.pop()
                            if len(current_interface.storage) < current_interface.max_capability and index < len(heretic.inventory):
                                current_interface.description.append(heretic.inventory[index].type + ';')
                            put_item_in_the_storage(current_interface, index)

                        elif event.pos[0] > 820:
                            index = (event.pos[0] - 820) // 150 + (event.pos[1] - 100) // 150 * 4
                            current_interface.take_from_storage(index)
                            current_interface.description.pop()
                            if len(current_interface.description) < 3:
                                current_interface.description.append('Пусто')
                    elif current_interface == 'furnace':
                        index = (event.pos[0] - 50) // 150 + ((event.pos[1] - 100) // 150 * 4)
                        if not current_attached and index < len(heretic.inventory):
                            current_attached = heretic.inventory.pop(index)
                        elif isinstance(current_attached, Fuel) and 800 <= event.pos[0] <= 930 and 530 <= event.pos[1] <= 660:
                            furnace.fuel += current_attached.energy
                            current_attached = None
                        elif isinstance(current_attached, Meltable) and 800 <= event.pos[0] <= 930 and 380 <= event.pos[1] <= 530:
                            furnace.melt_something(current_attached.type)
                            current_attached = None
                        elif not current_attached and 1100 <= event.pos[0] <= 1230 and 380 <= event.pos[1] <= 510 \
                                and len(heretic.inventory) < 20:
                            heretic.inventory.append(furnace.product)
                            furnace.product = None
                        elif current_attached:
                            heretic.inventory.append(current_attached)
                            current_attached = None

                    elif current_interface == 'gridstone':
                        if 10 <= event.pos[0] <= 310:
                            recipy = (event.pos[1] - 10) // 110 + current_mean
                            if recipy == 0:
                                gridstone.status = 'sharpened stone'
                                gridstone.product = SharpenedStone(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)
                            elif recipy == 3:
                                gridstone.status = 'pickaxe'
                                gridstone.product = PickAxe(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)
                            elif recipy == 4:
                                gridstone.status = 'shovel'
                                gridstone.product = Shovel(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)
                            elif recipy == 5:
                                gridstone.status = 'crate'
                                gridstone.product = Crate(0, 0, 0, 0, 0, 0, 0, 0, 'Ящик')
                            elif recipy == 6:
                                gridstone.status = 'bag'
                                gridstone.product = Bag(0, 0, 0, 0, 0, 0, 0, 0, 'Сумка')
                        elif 720 <= event.pos[0] <= 970 and 700 <= event.pos[1] <= 800:
                            gridstone.produce_tools(gridstone.status)

                        elif 335 <= event.pos[0] <= 365:
                            if 20 <= event.pos[1] <= 50 and current_mean:
                                current_mean -= 1
                            if 850 <= event.pos[1] <= 880 and current_mean < len(gridstone_recipes) - 8:
                                current_mean += 1

                if 990 <= event.pos[0] <= 1090 and 245 <= event.pos[1] <= 345 and heretic.backpack and My_classes.Farmetic_classes.inventory_mode:
                    current_interface = heretic.backpack

                elif My_classes.Farmetic_classes.inventory_mode and len(heretic.inventory):

                    x = random.randint(heretic.x - 50, heretic.x + 100)
                    y = random.randint(heretic.y + 10, heretic.y + 120)
                    index = (event.pos[0] - 50) // 150 + ((event.pos[1] - 100) // 150 * 4)
                    try:
                        if isinstance(heretic.inventory[index], Drop):
                            heretic.inventory[index].x = x
                            heretic.inventory[index].y = y
                            heretic.inventory[index].active_zone = [list(range(x - 150, x + 150)),
                                                                    list(range(y - 150, y + 150))]

                            if isinstance(heretic.inventory[index], DroppedBerry):
                                heretic.inventory[index].visible_zone = [list(range(x - 3, x + 50)),
                                                                         list(range(y - 3, y + 50))]
                            else:
                                heretic.inventory[index].visible_zone = [list(range(x - 3, x +
                                                                                    len(heretic.inventory[index].visible_zone[0]))),
                                                                         list(range(y - 3, y +
                                                                                    len(heretic.inventory[
                                                                                            index].visible_zone[1])))]

                            if My_classes.Farmetic_classes.at_home:
                                home_drops_list.append(heretic.inventory[index])
                            elif My_classes.Farmetic_classes.current_location == 'leftside':
                                leftside_drops_list.append(heretic.inventory[index])
                            else:
                                drops_list.append(heretic.inventory[index])
                            if isinstance(heretic.inventory[index], Storage):
                                heretic.inventory[index].location = heretic.location

                            heretic.inventory.pop(index)
                    except IndexError:
                        print('IndexError has been caught!')

            elif event.button == 3:
                if 825 <= event.pos[0] <= 925 and 245 <= event.pos[1] <= 345 and heretic.weapon != 'none' and My_classes.Farmetic_classes.inventory_mode:
                    heretic.weapon.unequip()
                elif 990 <= event.pos[0] <= 1090 and 245 <= event.pos[1] <= 345 and heretic.backpack and My_classes.Farmetic_classes.inventory_mode:
                    x = random.randint(heretic.x - 50, heretic.x + 100)
                    y = random.randint(heretic.y + 10, heretic.y + 120)
                    heretic.backpack.x = x
                    heretic.backpack.y = y
                    heretic.backpack.active_zone = [list(range(x - 150, x + 150)),
                                                    list(range(y - 150, y + 150))]
                    heretic.backpack.visible_zone = [list(range(x, x + 50)),
                                                     list(range(y, y + 70))]
                    (drops_list if heretic.location == 'home' else leftside_drops_list).append(heretic.backpack)
                    heretic.backpack = None
                else:
                    x = random.randint(heretic.x - 50, heretic.x + 120)
                    y = random.randint(heretic.y + 50, heretic.y + 120)
                    index = (event.pos[0] - 50) // 150 + (event.pos[1] - 100) // 150 * 4
                    try:
                        if isinstance(heretic.inventory[index], Eatable) or isinstance(heretic.inventory[index], Berry):
                            heretic.inventory[index].eat()
                            My_classes.Farmetic_classes.remark_time = 90
                            My_classes.Farmetic_classes.current_string = random.choice(
                                ['Вкусно', heretic.inventory[index].type + '! М-м-м',
                                 "Объедение"])
                            eat_time = 90
                            if not isinstance(heretic.inventory[index], Berry):
                                energy_boost = '+ ' + str(heretic.inventory[index].energy)
                            else:
                                energy_boost = '+ 7'
                            heretic.inventory.pop(index)

                        elif isinstance(heretic.inventory[index], Pine):
                            if My_classes.Farmetic_classes.current_location == 'home':
                                trees_list.append(Sapling(x, y, 0, [[0], [0]]))
                                heretic.inventory.pop(index)
                            else:
                                My_classes.Farmetic_classes.current_string = "Почва не подходит"
                                My_classes.Farmetic_classes.remark_time = 100

                        elif isinstance(heretic.inventory[index], Weapon):
                            if heretic.weapon == 'none':
                                heretic.inventory[index].equip()

                        elif isinstance(heretic.inventory[index], Crate):
                            heretic.inventory[index].set()

                    except IndexError:
                        print('IndexError has been caught!')

            '''
Взаимодействие
            '''
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                try:
                    if home_active and not My_classes.Farmetic_classes.at_home:
                        My_classes.Farmetic_classes.at_home = True
                        heretic.direction = 'up'
                        heretic.x = 700
                        heretic.y = 500

                    elif current_interface != 'none':
                        close()

                    elif go_to_bed and not sleeping and heretic.health < 100:
                        sleeping = True
                        heretic.x = 315
                        heretic.y = 165
                        heretic.direction = 'up'

                    elif My_classes.Farmetic_classes.at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
                        My_classes.Farmetic_classes.at_home = False
                        heretic.direction = 'down'
                        heretic.x = home.x + 75
                        heretic.y = home.y + 60

                    elif My_classes.Farmetic_classes.current_location == 'home' and heretic.x in \
                            sign_to_leftside.active_zone[0] \
                            and heretic.y in sign_to_leftside.active_zone[1]:
                        current_interface = sign_to_leftside
                        sign_surf.fill((128, 128, 128))

                    elif My_classes.Farmetic_classes.current_location == 'leftside' and heretic.x in \
                            sign_to_home.active_zone[0] \
                            and heretic.y in sign_to_home.active_zone[1]:
                        current_interface = sign_to_home
                        sign_surf.fill((128, 128, 128))

                    elif My_classes.Farmetic_classes.current_location == 'leftside' and heretic.x in torch.active_zone[
                        0] \
                            and heretic.y in torch.active_zone[1]:
                        torch.light()

                    elif isinstance(heretic.weapon,
                                    Shovel) and heretic.health and not My_classes.Farmetic_classes.at_home:
                        heretic.weapon.dig()

                    elif active and len(bushes_list[b_owner].berries) > 0 and (
                            not heretic.is_tired or My_classes.Farmetic_classes.god_mode) \
                            and len(heretic.inventory) < 20 and not My_classes.Farmetic_classes.at_home:
                        bushes_list[b_owner].berries.pop(random.randint(0, len(bushes_list[b_owner].berries)))
                        heretic.inventory.append(DroppedBerry(0, 0, [[], []], [[], []], 'Ягода',
                                                              ['Вкусная спелая ягода'], random.randint(6, 8)))
                        heretic.health -= random.randint(1, 3)

                    elif My_classes.Farmetic_classes.at_home and drop_active and len(heretic.inventory) < 20 \
                            and not My_classes.Farmetic_classes.inventory_mode and \
                            current_interface == 'none':
                        My_classes.Farmetic_classes.remark_time = 60
                        My_classes.Farmetic_classes.current_string = 'Я подобрал ' + home_drops_list[d_owner].type
                        if isinstance(home_drops_list[d_owner], BackPack):
                            home_drops_list[d_owner].equip()
                            home_drops_list.pop(d_owner)
                        else:
                            heretic.inventory.append(home_drops_list.pop(d_owner))

                    elif (
                            active or chopping_active) and heretic.health <= 0 and My_classes.Farmetic_classes.remark_time <= 0:
                        My_classes.Farmetic_classes.remark_time = 60
                        My_classes.Farmetic_classes.current_string = random.choice(
                            ['Я очень устал', "Нет сил", "Нужно отдохнуть"])

                    elif My_classes.Farmetic_classes.at_home and heretic.x in juicemaker.active_zone[0] and heretic.y in \
                            juicemaker.active_zone[1] \
                            and juicemaker.work_time <= -1:
                        if len([i for i in heretic.inventory if
                                isinstance(i, Berry) or isinstance(i, DroppedBerry)]) >= 4:
                            My_classes.Farmetic_classes.current_string = 'Сок скоро будет готов'
                            My_classes.Farmetic_classes.remark_time = 60
                            juicemaker.make_juice()

                        else:
                            My_classes.Farmetic_classes.current_string = 'Нужно больше ягод'
                            My_classes.Farmetic_classes.remark_time = 60

                    elif My_classes.Farmetic_classes.at_home and heretic.x in furnace.active_zone[0] and heretic.y in \
                            furnace.active_zone[1]:
                        open('furnace')

                    elif My_classes.Farmetic_classes.at_home and heretic.x in chest.active_zone[0] and heretic.y in \
                            chest.active_zone[1] and \
                            current_interface == 'none':
                        open(chest)

                    elif crate_owner:
                        open(crate_owner)
                    elif My_classes.Farmetic_classes.at_home and heretic.x in gridstone.active_zone[0] and heretic.y in \
                            gridstone.active_zone[1] and \
                            current_interface == 'none':
                        open("gridstone")
                        gridstone.work()

                    elif chopping_active and inactive_time < 0 and (
                            0 < heretic.health or My_classes.Farmetic_classes.god_mode) \
                            and not heretic.attack_time and not My_classes.Farmetic_classes.at_home:
                        if heretic.x < trees_list[t_owner].x - 10:
                            heretic.direction = "right"
                        elif heretic.x > trees_list[t_owner].x + 50:
                            heretic.direction = 'left'
                        trees_list[t_owner].chop()
                        heretic.attack_time = 30
                        inactive_time = 5
                        if not My_classes.Farmetic_classes.god_mode:
                            heretic.health -= random.randint(2, 4)
                        chopping_sound_1.play()
                        if trees_list[t_owner].health <= 0:
                            trees_list.append(Stump(trees_list[t_owner].x, trees_list[t_owner].y, 1000, [[0], [2]]))
                            for i in range(random.randint(2, 3)):
                                x = random.choice(trees_list[t_owner].active_zone[0])
                                y = random.choice(trees_list[t_owner].active_zone[1])
                                drops_list.append(Log(x, y, [[j for j in range(x - 150, x + 150)],
                                                             [k for k in range(y - 120, y + 180)]],
                                                      [[k for k in range(x - 8, x + 85)],
                                                       [j for j in range(y, y + 50)]],
                                                      "Бревно", ['Необработанное бревно'], random.randint(5, 7)))
                            for i in range(random.randint(1, 2)):
                                x = random.choice(trees_list[t_owner].active_zone[0])
                                y = random.choice(trees_list[t_owner].active_zone[1])
                                drops_list.append(Pine(x, y, [[j for j in range(x - 150, x + 150)],
                                                              [k for k in range(y - 120, y + 180)]],
                                                       [[k for k in range(x - 8, x + 55)], [j for j in range(y - 5,
                                                                                                             y + 50)]],
                                                       "Желудь", ['Когда-то из него', "вырастет дерево"],
                                                       random.randint(1, 3)))
                            stick_chance = random.randint(0, 2)
                            if not stick_chance:
                                x = random.choice(trees_list[t_owner].active_zone[0])
                                y = random.choice(trees_list[t_owner].active_zone[1])
                                drops_list.append(Stick(x, y, [[j for j in range(x - 150, x + 150)],
                                                               [k for k in range(y - 120, y + 180)]],
                                                        [[k for k in range(x - 5, x + 32)], [j for j in range(y - 5,
                                                                                                              y + 50)]],
                                                        "Палка", ['Крепкая палка'], 2, 20, 20, 2))
                            trees_list.pop(t_owner)
                        for i in range(random.randint(3, 4)):
                            decors_list.append(FallingLeaves(random.choice(trees_list[t_owner].active_zone[0]),
                                                             random.randint(trees_list[t_owner].y - 200,
                                                                            trees_list[t_owner].y + 125), "down", 60))

                    elif rock_owner and rock_owner.health and heretic.health and not heretic.attack_time:
                        rock_owner.be_broken()
                        if not isinstance(heretic.weapon, PickAxe):
                            if not My_classes.Farmetic_classes.god_mode:
                                heretic.health -= random.randint(4, 6)
                        else:
                            heretic.weapon.mine(rock_owner)

                except IndexError:
                    print('IndexError is caught!')

                    '''
Открытие/закрытие инвентаря
            '''
            elif event.key == pygame.K_i and current_interface == 'none':
                if My_classes.Farmetic_classes.inventory_mode:
                    My_classes.Farmetic_classes.inventory_mode = False
                    chosen_item = None
                else:
                    My_classes.Farmetic_classes.inventory_mode = True

            elif event.key == pygame.K_d and My_classes.Farmetic_classes.inventory_mode:
                try:
                    if pos[0] < 650:
                        pos_index_d = (pos[0] - 50) // 150 + (pos[1] - 100) // 150 * 4
                        if pos_index_d < len(heretic.inventory):
                            chosen_item = heretic.inventory[pos_index_d]
                except IndexError:
                    print('IndexError has been caught!')

            elif event.key == pygame.K_ESCAPE and My_classes.Farmetic_classes.current_location != 'menu':
                going_to_menu += 1
                My_classes.Farmetic_classes.current_location = 'menu'

    '''
Движение
    '''
    keys = pygame.key.get_pressed()
    if not My_classes.Farmetic_classes.inventory_mode and not sleeping and My_classes.Farmetic_classes.current_location != 'menu' \
            and My_classes.Farmetic_classes.current_location != 'settings':
        if keys[pygame.K_a] and (heretic.x > -3 and not My_classes.Farmetic_classes.at_home or
                                 My_classes.Farmetic_classes.at_home and 300 <= heretic.x):
            if on_path:
                heretic.x -= 8
            elif heretic.is_tired:
                heretic.x -= 3
            else:
                heretic.x -= 5

            heretic.direction = 'left'
        elif keys[pygame.K_d] and (heretic.x < 1367 and not My_classes.Farmetic_classes.at_home or
                                   My_classes.Farmetic_classes.at_home and 1020 >= heretic.x):
            heretic.direction = 'right'
            if on_path:
                heretic.x += 7
            elif heretic.is_tired:
                heretic.x += 3
            else:
                heretic.x += 5

        if keys[pygame.K_w] and (heretic.y > 0 and not My_classes.Farmetic_classes.at_home or
                                 My_classes.Farmetic_classes.at_home and heretic.y > 150):
            if on_path:
                heretic.y -= 7
            elif heretic.is_tired:
                heretic.y -= 3
            else:
                heretic.y -= 4
            heretic.direction = 'up'

        elif keys[pygame.K_s] and (heretic.y < 800 and not My_classes.Farmetic_classes.at_home
                                   or My_classes.Farmetic_classes.at_home and heretic.y < 501):
            heretic.direction = 'down'
            if on_path:
                heretic.y += 5
            elif heretic.is_tired:
                heretic.y += 3
            else:
                heretic.y += 4

        if any([keys[pygame.K_a], keys[pygame.K_w], keys[pygame.K_a],
                keys[pygame.K_d]]) and not My_classes.Farmetic_classes.at_home:
            if not tick % 30:
                if heretic.direction in ['left', 'right']:
                    decors_list.append(Steps(random.randint(heretic.x + 10, heretic.x + 50), heretic.y + 80,
                                             random.randint(24, 30), random.randint(12, 16), random.randint(100, 120)))
                else:
                    decors_list.append(Steps(random.randint(heretic.x + 10, heretic.x + 50), heretic.y + 80,
                                             random.randint(12, 16), random.randint(24, 30), random.randint(100, 120)))
            if My_classes.Farmetic_classes.current_location == 'leftside':
                if not random.randint(0, 250):
                    for i in range(random.randint(2, 5)):
                        leftside_decors_list.append(Powder(random.randint(heretic.x, heretic.x + 50),
                                                           random.randint(heretic.y + 50, heretic.y + 120),
                                                           random.choice(['left', 'right']) + ' up', 70))

    """
    Перемещение
    """
    if My_classes.Farmetic_classes.current_location == 'home' and heretic.x < 10:
        My_classes.Farmetic_classes.current_location = 'leftside'
        active = False
        tp_to_left_side = False
        drop_active = False
        home_active = False
        inventory_mode = False
        chopping_active = False
        on_path = False
        tp_to_home = False
        heretic.x = 1350
        heretic.direction = 'left'
        volume = 0
    elif My_classes.Farmetic_classes.current_location == 'leftside' and heretic.x > 1350:
        My_classes.Farmetic_classes.current_location = 'home'
        active = False
        tp_to_left_side = False
        drop_active = False
        home_active = False
        inventory_mode = False
        chopping_active = False
        on_path = False
        tp_to_home = False
        heretic.x = 50
        heretic.direction = 'right'
        volume = 0

    if My_classes.Farmetic_classes.current_location == 'menu':
        display.fill((188, 252, 240))
        for i in menu_decors_list:
            pygame.draw.rect(display, (200, 200, 200), (i.x, i.y, i.width, i.height))
        pygame.draw.rect(display, (0, 0, 0), (330, 60, 740, 190))
        pygame.draw.rect(display, (126, 72, 32), (350, 80, 700, 150))
        display.blit(title_font.render(title, True, RED), (400, 80))
        if menu_tick > 210:
            if menu_tick < 398:
                pygame.draw.rect(display, (188 - menu_tick + 210, 252 - menu_tick + 168, 240 - menu_tick + 180),
                                 (450, 280, 500, 130))
                pygame.draw.rect(display, (188 - menu_tick + 210, 252 - menu_tick + 168, 240 - menu_tick + 180),
                                 (450, 420, 500, 130))
                pygame.draw.rect(display, (188 - menu_tick + 210, 252 - menu_tick + 168, 240 - menu_tick + 180),
                                 (450, 560, 500, 130))
            else:
                pygame.draw.rect(display, (0, 0, 0), (450, 280, 500, 130))
                pygame.draw.rect(display, (0, 0, 0), (450, 420, 500, 130))
                pygame.draw.rect(display, (0, 0, 0), (450, 560, 500, 130))
                if menu_tick < 598:
                    pygame.draw.rect(display, (0, menu_tick - 398, 0), (460, 290, 480, 110))
                    pygame.draw.rect(display, (0, 0, menu_tick - 398), (460, 430, 480, 110))
                    pygame.draw.rect(display, (menu_tick - 398, 0, 0), (460, 570, 480, 110))

                else:
                    pygame.draw.rect(display, GREEN, (460, 290, 480, 110))
                    pygame.draw.rect(display, BLUE, (460, 430, 480, 110))
                    pygame.draw.rect(display, RED, (460, 570, 480, 110))
                if not going_to_menu:
                    display.blit(inventory_font.render('Новая игра', True, (0, 0, 0)), (500, 310))
                else:
                    display.blit(inventory_font.render('Продолжить', True, (0, 0, 0)), (480, 310))
                display.blit(inventory_font.render('Настройки', True, (0, 0, 0)), (520, 440))
                display.blit(inventory_font.render('Выход', True, (0, 0, 0)), (595, 580))
        pygame.draw.rect(display, GREEN, (0, 700, 1440, 200))
        display.blit(inventory_font.render('Powered by PyGame', True, (0, 0, 0)), (10, 700))
        display.blit(inventory_font.render('Авторы: TecHeReTiC3141 и jedoron', True, (0, 0, 0)), (10, 780))
        if 700 >= menu_tick > 300:
            pygame.draw.rect(display, (0, 0, 0), (menu_tick - 600, 300, 300, 400))
            pygame.draw.rect(display, (255, 255, 255), (menu_tick - 420, 350, 50, 50))
            pygame.draw.rect(display, (0, 0, 0), (menu_tick - 390, 370, 10, 10))
            pygame.draw.rect(display, (255, 255, 255), (menu_tick - 490, 350, 50, 50))
            pygame.draw.rect(display, (0, 0, 0), (menu_tick - 460, 370, 10, 10))
        elif menu_tick > 700:
            pygame.draw.rect(display, (0, 0, 0), (100, 300, 300, 400))
            pygame.draw.rect(display, (255, 255, 255), (280, 350, 50, 50))
            pygame.draw.rect(display, (0, 0, 0), (300, 370, 10, 10))
            pygame.draw.rect(display, (255, 255, 255), (190, 350, 50, 50))
            pygame.draw.rect(display, (0, 0, 0), (210, 370, 10, 10))

    elif My_classes.Farmetic_classes.current_location == 'settings':
        display.fill((188, 252, 240))
        display.blit(title_font.render('Настройки', True, (0, 0, 0)), (350, 10))
        for i in range(len(settings.keys())):
            display.blit(inventory_font.render(list(settings.keys())[i], True, (0, 0, 0)), (100, 200 + i * 130))
            pygame.draw.rect(display, (0, 0, 0), (600, 230 + 125 * i, 150, 50))
            pygame.draw.rect(display, (0, 0, 0), (600, 230 + 125 * i, 150, 50))
            if settings.get(list(settings.keys())[i]):
                pygame.draw.rect(display, (0, 200, 0), (610, 230 + 130 * i, 40, 40))
            else:
                pygame.draw.rect(display, (200, 0, 0), (700, 230 + 130 * i, 40, 40))

    elif current_interface != 'none':
        if isinstance(current_interface, Storage):
            display.fill((184, 173, 118))
            display.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
            display.blit(inventory_font.render(current_interface.type, True, (0, 0, 0)), (1000, 10))
            for i in range(50, 601, 150):
                for j in range(100, 701, 150):
                    pygame.draw.rect(display, (0, 0, 200), (i, j, 130, 130))
                    pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))

            for i in range(len(heretic.inventory)):
                if isinstance(heretic.inventory[i], Berry) or isinstance(heretic.inventory[i], DroppedBerry):
                    heretic.inventory[i].draw_object(100 + 150 * (i % 4), 140 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Log):
                    heretic.inventory[i].draw_object(75 + 150 * (i % 4), 130 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Pine):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 130 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Juice):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], RawMeat):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Meat):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Stick):
                    heretic.inventory[i].draw_object(110 + 150 * (i % 4), 130 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Stone):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], SharpenedStone):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], PickAxe):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))
            for i in range(820, 1271, 150):
                for j in range(100, 101 + (current_interface.max_capability - 1) // 4 * 150, 150):
                    pygame.draw.rect(display, (0, 0, 200), (i, j, 130, 130))
                    pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))
            try:
                for i in range(len(current_interface.storage)):
                    if isinstance(current_interface.storage[i], DroppedBerry):
                        current_interface.storage[i].draw_object(870 + 150 * (i % 4), 140 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], Log):
                        current_interface.storage[i].draw_object(845 + 150 * (i % 4), 130 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], Pine):
                        current_interface.storage[i].draw_object(850 + 150 * (i % 4), 130 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], Juice):
                        current_interface.storage[i].draw_object(860 + 150 * (i % 4), 140 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], RawMeat):
                        current_interface.storage[i].draw_object(850 + 150 * (i % 4), 150 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], Meat):
                        current_interface.storage[i].draw_object(850 + 150 * (i % 4), 150 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], Stone):
                        current_interface.storage[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], SharpenedStone):
                        current_interface.storage[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], PickAxe):
                        current_interface.storage[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

                    elif isinstance(current_interface.storage[i], Drop):
                        current_interface.storage[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

            except IndexError as e:
                print(e)

            pygame.draw.line(display, (161, 96, 54), (700, 0), (700, 900), 100)

        elif isinstance(current_interface, Sign):

            bloor_surf.fill((128, 128, 128))
            pygame.draw.rect(display, (137, 99, 36), (600, 600, 200, 300))
            pygame.draw.rect(display, (137, 99, 36), (250, 150, 950, 550))
            pygame.draw.rect(display, (190, 190, 190), (290, 300, 845, 380))
            for i in range(360, 661, 60):
                pygame.draw.line(display, (0, 0, 0), (305, i), (1120, i), 10)
            for text in range(1, len(current_interface.description)):
                display.blit(active_font.render(current_interface.description[text], True, (0, 0, 0)),
                             (310, 314 + (text - 1) * 60))
            pygame.draw.line(display, (0, 0, 0), (450, 230), (950, 230), 90)
            display.blit(inventory_font.render(current_interface.description[0], True, (180, 0, 0)),
                         (560 - len(current_interface.description[0]) * 8, 180))
            display.blit(bloor_surf, (0, 0))

        elif current_interface == 'gridstone':
            display.fill((184, 173, 118))
            pygame.draw.line(display, (0, 0, 0), (350, 0), (350, 900), 40)
            if current_mean:
                pygame.draw.polygon(display, (150, 66, 45), ((335, 50), (350, 20), (365, 50)))
            if current_mean < len(gridstone_recipes) - 8:
                pygame.draw.polygon(display, (150, 66, 45), ((335, 850), (350, 880), (365, 850)))

            display.blit(title_font.render('Точило', True, (0, 0, 0)), (720, 40))
            for i in range(500, 781, 140):
                for j in range(250, 531, 140):
                    pygame.draw.rect(display, (0, 0, 0), (i, j, 130, 130))
                    pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))

            pygame.draw.line(display, (0, 0, 0), (940, 450), (990, 450), 10)
            pygame.draw.polygon(display, (0, 0, 0), ((990, 430), (1030, 450), (990, 470)))

            pygame.draw.rect(display, (0, 0, 0), (1040, 390, 130, 130))
            pygame.draw.rect(display, (190, 190, 190), (1055, 405, 100, 100))
            if gridstone.product:
                gridstone.product.draw_object(1100, 450)

            for i in range(10, 781, 110):
                pygame.draw.rect(display, (0, 0, 0), (10, i, 300, 100))
                pygame.draw.rect(display, (184, 173, 118), (15, i + 5, 290, 90))
                if i // 110 + current_mean < len(gridstone_recipes):
                    display.blit(active_font.render(gridstone_recipes[i // 110 + current_mean], True, (0, 0, 0)),
                                 (20, i + 30))
            if gridstone.status != 'off':
                if gridstone.status == 'not enough resources':
                    display.blit(active_font.render("Недостаточно ресурсов", True, (0, 0, 0)), (670, 720))
                else:
                    pygame.draw.rect(display, (0, 0, 0), (720, 700, 250, 100))
                    pygame.draw.rect(display, (200, 0, 0), (725, 705, 240, 90))
                    display.blit(active_font.render("Крафт", True, (0, 0, 0)), (760, 720))

        elif current_interface == 'furnace':
            display.fill((184, 173, 118))
            pygame.draw.line(display, (0, 0, 0), (680, 0), (680, 900), 40)
            display.blit(title_font.render('Печь', True, (0, 0, 0)), (920, 40))
            for i in range(50, 601, 150):
                for j in range(100, 801, 150):
                    pygame.draw.rect(display, (0, 0, 200), (i, j, 130, 130))
                    pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))
            for i in range(len(heretic.inventory)):
                if isinstance(heretic.inventory[i], Berry) or isinstance(heretic.inventory[i], DroppedBerry):
                    heretic.inventory[i].draw_object(100 + 150 * (i % 4), 160 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Log):
                    heretic.inventory[i].draw_object(75 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Pine):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Juice):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 160 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], RawMeat):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 170 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Meat):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 170 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Stick):
                    heretic.inventory[i].draw_object(110 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif any([isinstance(heretic.inventory[i], Stone), isinstance(heretic.inventory[i], IronOre),
                          isinstance(heretic.inventory[i], Coal)]):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], SharpenedStone):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], PickAxe) or isinstance(heretic.inventory[i], Shovel):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))
                elif isinstance(heretic.inventory[i], Storage) or isinstance(heretic.inventory[i], Drop):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))

            pygame.draw.rect(display, (0, 0, 200), (800, 380, 130, 130))
            pygame.draw.rect(display, (190, 190, 190), (815, 395, 100, 100))
            pygame.draw.rect(display, (0, 0, 200), (800, 530, 130, 130))
            pygame.draw.rect(display, (190, 190, 190), (815, 545, 100, 100))
            pygame.draw.rect(display, (184, 173, 118), (845, 570, 15, 10))
            pygame.draw.rect(display, (184, 173, 118), (850, 580, 40, 25))

            pygame.draw.rect(display, (0, 0, 200), (1100, 380, 130, 130))
            pygame.draw.rect(display, (190, 190, 190), (1115, 395, 100, 100))

            pygame.draw.rect(display, (200, 196, 193), (950, 425, 120, 40))
            if furnace.work_time:
                pygame.draw.rect(display, (220, 216, 213), (950, 425, (600 - furnace.work_time) // 5, 40))

            pygame.draw.rect(display, (10, 10, 10), (800, 700, 500, 80))
            pygame.draw.rect(display, (240, 240, 240), (810, 705, 480, 70))
            pygame.draw.rect(display, (125, 71, 43), (810, 705, furnace.fuel * 5, 70))
            display.blit(active_font.render("Топливо", True, (0, 0, 0)), (920, 790))

            if isinstance(current_attached, Drop):
                current_attached.draw_object(pos[0], pos[1])
            if isinstance(furnace.product, Drop):
                furnace.product.draw_object(1130, 410)
            for i in range(800, 1300, 50):
                if not i % 100 and i > 800:
                    pygame.draw.line(display, (0, 0, 0), (i - 5, 760), (i - 5, 775), 10)
                elif not i % 50 and i > 800:
                    pygame.draw.line(display, (0, 0, 0), (i - 4, 765), (i - 4, 775), 8)

    elif My_classes.Farmetic_classes.inventory_mode:

        display.fill((184, 173, 118))
        display.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
        display.blit(inventory_font.render('Часы: день/ночь', True, (0, 0, 0)), (800, 10))
        pygame.draw.rect(display, (0, 0, 0), (800, 150, 600, 60))
        pygame.draw.rect(display, (184, 173, 118), (1260, 155, 130, 50))
        pygame.draw.rect(display, (200, 0, 0), (810, 155, int(445 * heretic.health // 100), 50))
        pygame.draw.rect(display, (0, 0, 200), (810, 230, 130, 130))
        pygame.draw.rect(display, (190, 190, 190), (825, 245, 100, 100))
        pygame.draw.rect(display, (0, 0, 200), (970, 230, 130, 130))
        pygame.draw.rect(display, (190, 190, 190), (985, 245, 100, 100))
        if heretic.weapon != 'none':
            heretic.weapon.draw_object(865, 260)
            display.blit(active_font.render(heretic.weapon.type, True, (0, 0, 0)), (825, 365))
        else:
            pygame.draw.rect(display, (184, 173, 118), (860, 260, 20, 45))
            pygame.draw.polygon(display, (184, 173, 118), ((860, 260), (870, 252), (880, 260)))
            pygame.draw.rect(display, (184, 173, 118), (850, 300, 40, 6))
            pygame.draw.rect(display, (184, 173, 118), (864, 306, 12, 20))

        if heretic.backpack:
            heretic.backpack.draw_object(1000, 260)
            display.blit(active_font.render(heretic.backpack.type, True, (0, 0, 0)), (960, 365))
        else:
            pygame.draw.rect(display, (184, 173, 118), (1000, 260, 50, 70))
            pygame.draw.lines(display, (184, 173, 118), True, ((1000, 260), (1040, 245), (1060, 270)), 8)
            pygame.draw.polygon(display, (184, 173, 118),
                                ((998, 260), (998, 285), (1025, 295), (1052, 285), (1052, 260)))

            pygame.draw.circle(display, (184, 173, 118), (1035, 289), 3)

        pygame.draw.line(display, (161, 96, 54), (700, 0), (700, 900), 100)
        pygame.draw.line(display, (0, 0, 0), (1025 + 120 * day_tick // 550, 110), (1200 + 120 * day_tick // 550, 110),
                         10)
        if eat_time > 0:
            display.blit(active_font.render(energy_boost, True, (0, 0, 200)), (1260, 155))
        pygame.draw.rect(display, (240, 240, 240), (870, 450, 500, 450))

        for i in range(510, 871, 60):
            pygame.draw.line(display, (0, 0, 0), (880, i), (1350, i), 5)

        for i in range(50, 601, 150):
            for j in range(100, 801, 150):
                pygame.draw.rect(display, (0, 0, 200), (i, j, 130, 130))
                pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))
        try:
            for i in range(len(heretic.inventory)):
                if isinstance(heretic.inventory[i], Berry) or isinstance(heretic.inventory[i], DroppedBerry):
                    heretic.inventory[i].draw_object(100 + 150 * (i % 4), 160 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Log):
                    heretic.inventory[i].draw_object(75 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Pine):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Juice):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 160 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], RawMeat):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 170 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Meat):
                    heretic.inventory[i].draw_object(80 + 150 * (i % 4), 170 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Stick):
                    heretic.inventory[i].draw_object(110 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif any([isinstance(heretic.inventory[i], Stone), isinstance(heretic.inventory[i], IronOre),
                          isinstance(heretic.inventory[i], Coal)]):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], SharpenedStone):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], PickAxe) or isinstance(heretic.inventory[i], Shovel):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))
                else:
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))

            if 100 < pos[0] < 650 and pos[1] > 100:
                pos_index = (pos[0] - 50) // 150 + (pos[1] - 100) // 150 * 4
                if pos_index < len(heretic.inventory):
                    display.blit(inventory_font.render(heretic.inventory[pos_index].type, True,
                                                       (0, 0, 0)), (pos[0] - 100, pos[1] - 75))
            if isinstance(chosen_item, Drop) or isinstance(chosen_item, Berry) or isinstance(chosen_item, Weapon):
                for i in range(len(chosen_item.description)):
                    display.blit(active_font.render(chosen_item.description[i], True, (0, 0, 0)), (880, 465 + i * 60))

        except IndexError:
            print('IndexError has been caught!')

    elif My_classes.Farmetic_classes.at_home:
        display.fill((0, 0, 0))
        if not sleeping:

            pygame.draw.rect(display, (184, 173, 118), (300, 150, 800, 450))
            pygame.draw.rect(display, (160, 160, 160), (600, 480, 200, 110))
            display.blit(active_font.render('Welcome', True, (0, 0, 0)), (615, 515))
            for drop in range(len(home_drops_list)):
                if heretic.x in home_drops_list[drop].active_zone[0] \
                        and heretic.y in home_drops_list[drop].active_zone[1]:
                    drop_active = True
                    d_owner = drop
                    break
            else:
                drop_active = False
            '''
            Отрисовка соковыжималки 
            '''
            pygame.draw.rect(display, (121, 85, 61), (juicemaker.x, juicemaker.y, 100, 80))
            pygame.draw.rect(display, (200, 200, 200), (555, 180, 90, 20))
            pygame.draw.rect(display, (120, 120, 120), (650, 180, 35, 20))
            pygame.draw.rect(display, (120, 120, 120), (665, 180, 20, 30))
            if juicemaker.work_time > 0:
                pygame.draw.rect(display, (200, 0, 0), (555, 180, (600 - juicemaker.work_time) // 7, 20))
                pygame.draw.polygon(display, (171, 242, 242), ((660, 220), (665, 255), (685, 255), (690, 220)))
                pygame.draw.rect(display, (200, 0, 0), (670, 210, 10, 45))
                pygame.draw.rect(display, (200, 0, 0), (665, 225 + juicemaker.work_time // 20, 20,
                                                        (600 - juicemaker.work_time) // 20))

            '''
Отрисовка гриля
            
            '''
            furnace.draw_object(furnace.x, furnace.y)

            chest.draw_object()
            if heretic.y >= gridstone.y:
                gridstone.draw_object()

            for drop in home_drops_list:
                drop.draw_object(drop.x, drop.y)
                drop.up_down()

        pygame.draw.rect(display, (160, 73, 13), (310, 160, 90, 110))
        pygame.draw.rect(display, (239, 235, 230), (315, 165, 80, 30))

        heretic.draw_object()

        if not sleeping:
            if heretic.y < gridstone.y:
                gridstone.draw_object()

        if active and inactive_time < 0 and not My_classes.Farmetic_classes.at_home:
            display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))
        elif My_classes.Farmetic_classes.remark_time > 0:
            print_on_screen(My_classes.Farmetic_classes.current_string)
        elif 450 <= heretic.y < 600 <= heretic.x <= 750:
            display.blit(exit_home, (heretic.x - 25, heretic.y - 75))
        elif heretic.x in juicemaker.active_zone[0] and heretic.y in juicemaker.active_zone[1]:
            display.blit(juicemaker_sign, (heretic.x - 100, heretic.y - 75))
        elif drop_active and inactive_time < 0:
            display.blit(pick_up, (heretic.x - 60, heretic.y - 75))
        elif heretic.x in furnace.active_zone[0] and heretic.y in furnace.active_zone[1]:
            display.blit(active_font.render('Гриль', True, (200, 0, 0)), (heretic.x - 20, heretic.y - 75))
        elif heretic.x in chest.active_zone[0] and heretic.y in chest.active_zone[1]:
            display.blit(active_font.render('Сундук', True, (200, 0, 0)), (heretic.x - 35, heretic.y - 75))
        elif heretic.x in gridstone.active_zone[0] and heretic.y in gridstone.active_zone[1]:
            display.blit(active_font.render('Точило', True, (200, 0, 0)), (heretic.x - 35, heretic.y - 75))
        elif chopping_active and not My_classes.Farmetic_classes.at_home and len(trees_list) > 0:
            display.blit(chopping, (heretic.x - 40, heretic.y - 75))

        elif go_to_bed and not sleeping:
            display.blit(sleep, (heretic.x - 20, heretic.y - 75))
        elif picked_up_time > 0:
            display.blit(picked_up, (heretic.x - 100, heretic.y - 75))

        if heretic.x in bed.active_zone[0] and heretic.y in bed.active_zone[1]:
            go_to_bed = True
        else:
            go_to_bed = False

        if sleeping:
            display.blit(active_font.render(z_z_Z, True, (0, 0, 200)), (heretic.x + 110, heretic.y - 75))

        for drop in range(len(home_drops_list)):
            if heretic.x in home_drops_list[drop].active_zone[0] and heretic.y in home_drops_list[drop].active_zone[1]:
                drop_active = True
                d_owner = drop
                break
            else:
                drop_active = False

    elif My_classes.Farmetic_classes.current_location == 'home':
        display.fill((0, 200 - day_tick // 8, 0))
        '''
        for zone in ground_light_zone:
            for i in zone:
                coord = list(map(int, i.split()))
                x = coord[0]
                y = coord[1]
                if x in heretic.light_zone[0] and y in heretic.light_zone[1]:
                    pygame.draw.rect(display, (0, 150, 0), (x, y, 25, 25))

Отрисовка троп
        '''
        if day_tick > 450:  # ночной обзор
            pygame.draw.circle(display, (0, 150, 0), (heretic.x + 30, heretic.y + 50), 180 - (day_tick - 450) // 15)
        for trail in trails_list:
            if day_tick > 900:
                pygame.draw.rect(display, (69, 69, 69), (trail.x, trail.y, trail.length, trail.width))
            else:
                pygame.draw.rect(display, (219 - day_tick // 10, 168 - day_tick // 10, 31 - day_tick // 30),
                                 (trail.x, trail.y, trail.length, trail.width))
            for i in trail.light_zones:
                if heretic.y + 150 < trail.y or heretic.y - 150 > trail.y + trail.width:
                    continue
                for j in i:
                    x, y = (map(int, j.split()))
                    if x in heretic.light_zone[0] and y in heretic.light_zone[1]:
                        pygame.draw.rect(display, (219, 169, 31), (x, y, 10, 10))

        for blood in decors_list:
            if isinstance(blood, Steps):
                blood.draw_object(blood.x, blood.y)
            elif isinstance(blood, Blood) and blood_setting:
                pygame.draw.rect(display, (200 - (600 - blood.life_time) // 6, (600 - blood.life_time) // 10, 0),
                                 (blood.x, blood.y, blood.width, blood.height))

        '''
Отрисовка табличек
        '''
        sign_to_leftside.draw_object()
        '''
Отрисовка кустов и рост ягод
        '''
        for bush in bushes_list:
            if len(bush.berries) <= 4:
                bush.regrowth_time -= 1
                if bush.regrowth_time < 0:
                    bush.berries.append(Berry(random.randint(bush.x, bush.x + 90), random.randint(bush.y, bush.y + 90),
                                              'Ягода', ['Спелая сочная ягода']))
                    bush.regrowth_time = 450
            if bush.y > heretic.y + 40 and not My_classes.Farmetic_classes.at_home and My_classes.Farmetic_classes.current_location == 'home' \
                    and heretic.x in bush.active_zone[0]:
                continue
            if bush.x not in heretic.light_zone[0] or bush.y not in heretic.light_zone[1]:
                colour = (0, 100 - day_tick // 20, 0)
            else:
                colour = (0, 100, 0)
            pygame.draw.rect(display, colour, (bush.x, bush.y, 100, 100))
            for ber in bush.berries:
                pygame.draw.rect(display, (200, 0, 0), (ber.x, ber.y, 10, 10))

        for crate in crates_list:
            if crate.y < heretic.y + 40 and crate.location == heretic.location:
                crate.draw_object(crate.x, crate.y)

        for grass in regrowing_list:
            if grass.y <= 40 + heretic.y and grass.location == heretic.location:
                grass.draw_object(grass.x, grass.y)

        '''
Вход в зону куста
    '''

        for bush in range(len(bushes_list)):
            if heretic.x in bushes_list[bush].active_zone[0] and heretic.y in \
                    bushes_list[bush].active_zone[1] and bushes_list[bush].berries:
                active = True
                b_owner = bush
                break
        else:
            active = False
            '''
Вход в зону тропы
        '''
        for trail in range(len(trails_list)):
            if heretic.x in trails_list[trail].active_zone[0] and heretic.y + 80 in trails_list[trail].active_zone[1]:
                on_path = True
                current_trail = trails_list[trail]
                break
        else:
            on_path = False
            current_trail = None
            '''
Вход в зону предмета
        '''
        for drop in range(len(drops_list)):
            if heretic.x in drops_list[drop].active_zone[0] and heretic.y in drops_list[drop].active_zone[1] \
                    and pos[0] in drops_list[drop].visible_zone[0] and pos[1] in drops_list[drop].visible_zone[1]:
                drop_active = True
                d_owner = drop
                break
        else:
            drop_active = False

            '''
Вход в зону существа
        '''
        for mob in mobs_list:
            if mob.location == 'home':
                remark_chance = random.randint(0, 2000)
                if not remark_chance:
                    mob.remark_time = 60
                    if isinstance(mob, PeacefulMobs):
                        mob.remark = random.choice(['Бе-е-е', "Бе"])
                    elif isinstance(mob, AggressiveMobs):
                        mob.remark = random.choice(['Умри', "Убивать!"])
                if heretic.x in mob.active_zone[0] and heretic.y in mob.active_zone[1]:
                    m_owner = mob
                    break
        else:
            m_owner = None

        '''
Вход в зону ящика
        '''
        for crate in crates_list:
            if heretic.x in crate.active_zone[0] and heretic.y in crate.active_zone[1]:
                crate_owner = crate
                break
        else:
            crate_owner = None

            '''
Анимация предмета
        '''
        if drop_active:
            pygame.draw.rect(display, (213, 208, 11), (drops_list[d_owner].x - 3, drops_list[d_owner].y - 3,
                                                       len(drops_list[d_owner].visible_zone[0]),
                                                       len(drops_list[d_owner].visible_zone[1])))
        for drop in drops_list:
            drop.draw_object(drop.x, drop.y)
            drop.up_down()
            '''
Отрисовка дерева
            '''
        try:
            for tree in range(len(trees_list)):
                if isinstance(trees_list[tree], Stump):
                    pygame.draw.rect(display, (137, 99, 36), (trees_list[tree].x, trees_list[tree].y, 50, 50))
                    pygame.draw.ellipse(display, (155, 136, 70), (trees_list[tree].x, trees_list[tree].y - 10, 50, 20))
                    trees_list[tree].health -= 1
                    if trees_list[tree].health <= 0:
                        trees_list.pop(tree)

                elif isinstance(trees_list[tree], Sapling):
                    pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - trees_list[tree].health // 120,
                                                              trees_list[tree].y - trees_list[tree].health // 9, 20 +
                                                              trees_list[tree].health // 60,
                                                              60 + trees_list[tree].health // 130))
                    # pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - 30, trees_list[tree].y + 20, 30, 10))
                    '''if 1000 >= trees_list[tree].health >= 500:
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x, trees_list[tree].y - 60, 25, 120))
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - 40, trees_list[tree].y + 30, 40,
                                                                  15))
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - 40, trees_list[tree].y, 15, 30))
                        pygame.draw.ellipse(display, (40, 122, 36), (trees_list[tree].x - 60, trees_list[tree].y - 10,
                                                                     40, 40))'''
                    trees_list[tree].health += 1
                    if trees_list[tree].health >= 1800:
                        trees_list[tree].regrowth()
                        trees_list.pop(tree)

                else:
                    if trees_list[tree].y > heretic.y + 45 \
                            and not My_classes.Farmetic_classes.at_home and My_classes.Farmetic_classes.current_location == 'home':
                        continue
                    pygame.draw.rect(display, (137, 99, 36), (trees_list[tree].x, trees_list[tree].y - 150, 50, 200))
                    pygame.draw.circle(display, (40, 122, 36), (trees_list[tree].x + 25, trees_list[tree].y - 130), 75)

        except IndexError:
            print('IndexError has been caught!')

            '''
Вход в зону дерева
                 '''
        for tree in range(len(trees_list)):

            if not isinstance(trees_list[tree], Stump):
                if heretic.x in trees_list[tree].active_zone[0] and heretic.y in trees_list[tree].active_zone[1] \
                        and len(heretic.inventory) < 20:
                    chopping_active = True
                    t_owner = tree
                    break
                else:
                    chopping_active = False
                    t_owner = None

        pygame.draw.rect(display, (155 - day_tick // 10, 166 - day_tick // 10, 165 - day_tick // 10),
                         (x_home, y_home, h_length, h_width))
        for i in range(len(home.light_zones)):
            for j in home.light_zones[i]:
                x, y = map(int, j.split())
                if x in heretic.light_zone[0] and y in heretic.light_zone[1]:
                    pygame.draw.rect(display, (155, 166, 165), (x, y, 10, 10))
        pygame.draw.rect(display, (163, 121, 41), (x_home + 75, y_home + 50, 100, 130))

        if heretic.x in home.active_zone[0] and heretic.y in home.active_zone[1]:
            home_active = True
        else:
            home_active = False
        if not My_classes.Farmetic_classes.inventory_mode:

            '''
Отрисовка существ
            '''
            for mob in mobs_list:
                if mob.location == 'home':
                    if isinstance(mob, PeacefulMobs):
                        if mob.x in heretic.light_zone[0] and mob.y in heretic.light_zone[1]:
                            mob_head_colour = (255, 228, 196)
                        else:
                            mob_head_colour = (255 - day_tick // 10, 228 - day_tick // 10, 196 - day_tick // 10)
                        if mob.direction == 'up':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 15, mob.y - 10, 30, 30))
                        if mob.direction == 'left' or mob.direction == 'right':
                            if mob.x in heretic.light_zone[0] and mob.y in heretic.light_zone[1]:
                                mob_colour = (200, 200, 200)
                            else:
                                mob_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                            pygame.draw.rect(display, mob_colour, (mob.x, mob.y, 90, 60))
                            if heretic.x in mob.active_zone[0] and heretic.y in mob.active_zone[1]:
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + 5, mob.y - 30, 80, 20))
                                pygame.draw.rect(display, (200, 0, 0),
                                                 (mob.x + 7, mob.y - 28, int(76.0 * mob.health / 10.0), 16))
                        else:
                            if mob.x in heretic.light_zone[0] and mob.y in heretic.light_zone[1]:
                                mob_colour = (200, 200, 200)
                            else:
                                mob_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                            pygame.draw.rect(display, mob_colour, (mob.x, mob.y, 60, 90))
                            if heretic.x in mob.active_zone[0] and heretic.y in mob.active_zone[1]:
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + 5, mob.y - 30, 50, 20))
                                pygame.draw.rect(display, (200, 0, 0),
                                                 (mob.x + 7, mob.y - 28, int(46.0 * mob.health / 8.0), 16))

                        if mob.direction == 'down':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 15, mob.y + 50, 30, 30))
                            for i in range(22, 33, 10):
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + i, mob.y + 60, 5, 5))
                        elif mob.direction == 'left':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 10, mob.y + 15, 30, 30))
                            for i in range(17, 28, 10):
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + i, mob.y + 25, 5, 5))
                        elif mob.direction == 'right':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 50, mob.y + 15, 30, 30))
                            for i in range(57, 68, 10):
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + i, mob.y + 25, 5, 5))

                    elif isinstance(mob, AggressiveMobs):
                        mob.draw_object()

                    mob.bleed()

            for fog in decors_list:
                if isinstance(fog, Particles):
                    fog.fly()
                    fog.draw_object(fog.x, fog.y)
                    fog.life_time -= 1
                    if isinstance(fog, FallingBlood):
                        fog.fall()
                elif isinstance(fog, Fog) and fog.y < heretic.y - 40:
                    if fog.x in heretic.light_zone[0] and fog.y in heretic.light_zone[1]:
                        fog_colour = (200, 200, 200)
                    else:
                        fog_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                    fog_surf = pygame.Surface((fog.width, fog.height))
                    fog_surf.fill(fog_colour)
                    fog_surf.set_alpha(140)
                    display.blit(fog_surf, (fog.x, fog.y))
            '''
Отрисовка еретика
             '''
            heretic.draw_object()
            '''
Дополнительная прорисовка объектов перед еретиком:начало
            '''
            if heretic.y < 380:
                pygame.draw.rect(display, (137, 99, 36), (100, 400, 30, 80))
                pygame.draw.rect(display, (137, 99, 36), (60, 380, 90, 60))
                pygame.draw.rect(display, (0, 0, 0), (90, 395, 50, 30))
                pygame.draw.polygon(display, (0, 0, 0), ((70, 410), (90, 390), (90, 430)))
            for bush in bushes_list:
                if bush.y > heretic.y + 40 and not My_classes.Farmetic_classes.at_home \
                        and My_classes.Farmetic_classes.current_location == 'home' and heretic.x in \
                        bush.active_zone[0]:
                    if bush.x not in heretic.light_zone[0] or bush.y not in heretic.light_zone[1]:
                        colour = (0, 100 - day_tick // 20, 0)
                    else:
                        colour = (0, 100, 0)
                    pygame.draw.rect(display, colour, (bush.x, bush.y, 100, 100))
                    for ber in bush.berries:
                        pygame.draw.rect(display, (200, 0, 0), (ber.x, ber.y, 10, 10))

            for crate in crates_list:
                if crate.y > heretic.y + 40 and crate.location == heretic.location:
                    crate.draw_object(crate.x, crate.y)

            for grass in regrowing_list:
                if grass.y > 40 + heretic.y and grass.location == heretic.location:
                    grass.draw_object(grass.x, grass.y)

            if home.y > heretic.y and not My_classes.Farmetic_classes.at_home and My_classes.Farmetic_classes.current_location == 'home':
                pygame.draw.rect(display, (155 - day_tick // 10, 166 - day_tick // 10, 165 - day_tick // 10),
                                 (x_home, y_home, h_length, h_width))
                for i in range(len(home.light_zones)):
                    for j in home.light_zones[i]:
                        x, y = map(int, j.split())
                        if x in heretic.light_zone[0] and y in heretic.light_zone[1]:
                            pygame.draw.rect(display, (155, 166, 165), (x, y, 10, 10))
                pygame.draw.rect(display, (163, 121, 41), (x_home + 75, y_home + 50, 100, 130))
            try:
                for tree in range(len(trees_list)):
                    if trees_list[tree].y > heretic.y + 45 and not My_classes.Farmetic_classes.at_home \
                            and My_classes.Farmetic_classes.current_location == 'home':
                        if isinstance(trees_list[tree], Stump):
                            pygame.draw.rect(display, (137, 99, 36), (trees_list[tree].x, trees_list[tree].y, 50, 50))
                            pygame.draw.ellipse(display, (155, 136, 70), (trees_list[tree].x, trees_list[tree].y - 10,
                                                                          50, 20))
                            trees_list[tree].health -= 1
                            if trees_list[tree].health <= 0:
                                trees_list.pop(tree)
                                for tree1 in range(len(trees_list)):
                                    for tree2 in range(tree, len(trees_list)):
                                        if trees_list[tree2].y < trees_list[tree1].y:
                                            trees_list[tree1], trees_list[tree2] = trees_list[tree2], trees_list[tree1]

                        elif not My_classes.Farmetic_classes.at_home and not isinstance(trees_list[tree], Sapling):
                            pygame.draw.rect(display, (137, 99, 36),
                                             (trees_list[tree].x, trees_list[tree].y - 150, 50, 200))
                            pygame.draw.circle(display, (40, 122, 36),
                                               (trees_list[tree].x + 25, trees_list[tree].y - 130), 75)

            except IndexError:
                print('IndexError has been caught!')
            for fog in decors_list:
                if isinstance(fog, Fog) and fog.y > heretic.y - 40:
                    if fog.x in heretic.light_zone[0] and fog.y in heretic.light_zone[1]:
                        fog_colour = (200, 200, 200)
                    else:
                        fog_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                    fog_surf = pygame.Surface((fog.width, fog.height))
                    fog_surf.fill(fog_colour)
                    fog_surf.set_alpha(140)
                    display.blit(fog_surf, (fog.x, fog.y))

            '''
Прорисовка объектов перед еретиком:конец
            '''

            '''
Tелепортация
                    '''
            if heretic.x <= 150 and 400 <= heretic.y <= 550:
                tp_to_left_side = True
            else:
                tp_to_left_side = False

            if home_active and not My_classes.Farmetic_classes.at_home:
                display.blit(enter, (heretic.x - 25, heretic.y - 75))

            elif tp_to_left_side and not My_classes.Farmetic_classes.at_home:
                display.blit(leftside_tp, (heretic.x - 50, heretic.y - 75))

            elif My_classes.Farmetic_classes.remark_time > 0:
                print_on_screen(My_classes.Farmetic_classes.current_string)
                print(My_classes.Farmetic_classes.current_string)

            elif m_owner:
                display.blit(active_font.render('Атаковать', True, (0, 0, 0)), (heretic.x - 50, heretic.y - 75))

            elif crate_owner:
                display.blit(active_font.render('Открыть', True, (0, 0, 0)), (heretic.x - 50, heretic.y - 75))

            elif My_classes.Farmetic_classes.at_home and heretic.x in juicemaker.active_zone[0] and heretic.y in \
                    juicemaker.active_zone[1]:
                display.blit(juicemaker_sign, (heretic.x - 100, heretic.y - 75))

            elif active and inactive_time < 0 and not My_classes.Farmetic_classes.at_home:
                display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))

            elif My_classes.Farmetic_classes.at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
                display.blit(exit_home, (heretic.x - 25, heretic.y - 75))

            elif chopping_active and not My_classes.Farmetic_classes.at_home and len(trees_list) > 0:
                display.blit(chopping, (heretic.x - 40, heretic.y - 75))

            elif picked_up_time > 0:
                display.blit(picked_up, (heretic.x - 100, heretic.y - 75))

            elif heretic.x in sign_to_leftside.active_zone[0] and heretic.y in sign_to_leftside.active_zone[1]:
                display.blit(active_font.render("Читать", True, (0, 0, 0)), (heretic.x - 10, heretic.y - 75))

            for bush in bushes_list:
                if pos[0] in bush.visible_zone[0] and pos[1] in bush.visible_zone[1]:
                    display.blit(active_font.render('Ягодный куст', True, (0, 0, 0)), (pos[0] - 100, pos[1]))

            if pos[0] in home.visible_zone[0] and pos[1] in home.visible_zone[1]:
                display.blit(active_font.render('Мой дом', True, (0, 0, 0)), (pos[0] - 100, pos[1]))

            if drop_active:
                display.blit(active_font.render('Подобрать', True, (0, 0, 0)), (pos[0] - 100, pos[1]))

            for mob in mobs_list:
                if mob.remark_time and mob.location == heretic.location:
                    print_for_mob(mob, mob.remark)

        '''
    Лефт-Сайд
'''
    elif My_classes.Farmetic_classes.current_location == 'leftside':

        display.fill((115 - day_tick // 10, 125 - day_tick // 10, 120 - day_tick // 10))
        torch.work()
        if day_tick > 200:  # ночной обзор
            pygame.draw.circle(display, (100, 110, 105), (heretic.x + 30, heretic.y + 50), 180 - (day_tick - 450) // 15)
        if heretic.y >= torch.y - 40:
            torch.draw_object()
        for i in leftside_decors_list:
            if isinstance(i, Stones):
                pygame.draw.rect(display, (0, 0, 0), (i.x - 1, i.y - 1, i.width + 2, i.height + 2))
                if i.x in heretic.light_zone[0] and i.y in heretic.light_zone[1]:
                    stone_color = (181, 184, 177)
                else:
                    stone_color = (181 - day_tick // 10, 184 - day_tick // 10, 177 - day_tick // 10)
                pygame.draw.rect(display, stone_color, (i.x, i.y, i.width, i.height))

        sign_to_home.draw_object()

        """
        Вход в зону предмета
        """
        for drop in range(len(leftside_drops_list)):
            if heretic.x in leftside_drops_list[drop].active_zone[0] and heretic.y in \
                    leftside_drops_list[drop].active_zone[1] \
                    and pos[0] in leftside_drops_list[drop].visible_zone[0] and pos[1] in \
                    leftside_drops_list[drop].visible_zone[1]:
                drop_active = True
                d_owner = drop
                break
        else:
            drop_active = False

        """
        Вход в зону глыб
        """
        for rock in leftside_stones_list:
            if heretic.x in rock.active_zone[0] and heretic.y in rock.active_zone[1]:
                rock_owner = rock
                break
        else:
            if rock_owner:
                rock_owner = None

        '''
        Вход в зону ящиков
        '''
        for crate in crates_list:
            if crate.location == heretic.location and heretic.x in crate.active_zone[0] and heretic.y in crate.active_zone[1]:
                crate_owner = crate
                break

        else:
            if rock_owner:
                rock_owner = None

        """
Лефт-Сайд:блок отрисовки предметов
"""
        if drop_active:
            pygame.draw.rect(display, (213, 208, 11),
                             (leftside_drops_list[d_owner].x - 3, leftside_drops_list[d_owner].y - 3,
                              len(leftside_drops_list[d_owner].visible_zone[0]),
                              len(leftside_drops_list[d_owner].visible_zone[1])))
        for drop in leftside_drops_list:
            drop.draw_object(drop.x, drop.y)
            drop.up_down()

        for rock in leftside_stones_list:
            if isinstance(rock, Rock) and heretic.y - 10 > rock.y:
                rock.draw_object()
        try:
            for fog in leftside_decors_list:
                if isinstance(fog, Fog) and fog.y < heretic.y - 40:
                    if fog.x in heretic.light_zone[0] and fog.y in heretic.light_zone[1]:
                        fog_colour = (200, 200, 200)
                    else:
                        fog_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                    fog_surf = pygame.Surface((fog.width, fog.height))
                    fog_surf.fill(fog_colour)
                    fog_surf.set_alpha(140)
                    display.blit(fog_surf, (fog.x, fog.y))

                elif isinstance(fog, Flashes):
                    fog.draw_object(fog.x, fog.y)
                    fog.fly()
                    fog.life_time -= 1
                    if fog.life_time == 15:
                        fog.direction.replace("up", "down")
                    if not fog.life_time:
                        leftside_decors_list.remove(fog)

                elif isinstance(fog, Particles) and fog in leftside_decors_list:
                    fog.draw_object(fog.x, fog.y)
                    fog.fly()
        except ValueError as e:
            print(e.args)

        for mob in mobs_list:
            if mob.location == 'leftside':
                remark_chance = random.randint(0, 2000)
                if not remark_chance:
                    mob.remark_time = 60
                    if isinstance(mob, PeacefulMobs):
                        mob.remark = random.choice(['Бе-е-е', "Бе"])
                    elif isinstance(mob, AggressiveMobs):
                        mob.remark = random.choice(['Умри', "Убивать!"])
                if heretic.x in mob.active_zone[0] and heretic.y in mob.active_zone[1]:
                    m_owner = mob
                    break
        else:
            m_owner = None

        if not My_classes.Farmetic_classes.inventory_mode:
            for mob in mobs_list:
                if mob.location == 'leftside':
                    if isinstance(mob, PeacefulMobs):
                        if mob.x in heretic.light_zone[0] and mob.y in heretic.light_zone[1]:
                            mob_head_colour = (255, 228, 196)
                        else:
                            mob_head_colour = (255 - day_tick // 10, 228 - day_tick // 10, 196 - day_tick // 10)
                        if mob.direction == 'up':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 15, mob.y - 10, 30, 30))
                        if mob.direction == 'left' or mob.direction == 'right':
                            if mob.x in heretic.light_zone[0] and mob.y in heretic.light_zone[1]:
                                mob_colour = (200, 200, 200)
                            else:
                                mob_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                            pygame.draw.rect(display, mob_colour, (mob.x, mob.y, 90, 60))
                            if heretic.x in mob.active_zone[0] and heretic.y in mob.active_zone[1]:
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + 5, mob.y - 30, 80, 20))
                                pygame.draw.rect(display, (200, 0, 0),
                                                 (mob.x + 7, mob.y - 28, int(76.0 * mob.health / 10.0), 16))
                        else:
                            if mob.x in heretic.light_zone[0] and mob.y in heretic.light_zone[1]:
                                mob_colour = (200, 200, 200)
                            else:
                                mob_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                            pygame.draw.rect(display, mob_colour, (mob.x, mob.y, 60, 90))
                            if heretic.x in mob.active_zone[0] and heretic.y in mob.active_zone[1]:
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + 5, mob.y - 30, 50, 20))
                                pygame.draw.rect(display, (200, 0, 0),
                                                 (mob.x + 7, mob.y - 28, int(46.0 * mob.health / 10.0), 16))

                        if mob.direction == 'down':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 15, mob.y + 50, 30, 30))
                            for i in range(22, 33, 10):
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + i, mob.y + 60, 5, 5))
                        elif mob.direction == 'left':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 10, mob.y + 15, 30, 30))
                            for i in range(17, 28, 10):
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + i, mob.y + 25, 5, 5))
                        elif mob.direction == 'right':
                            pygame.draw.rect(display, mob_head_colour, (mob.x + 50, mob.y + 15, 30, 30))
                            for i in range(57, 68, 10):
                                pygame.draw.rect(display, (0, 0, 0), (mob.x + i, mob.y + 25, 5, 5))

                    elif isinstance(mob, AggressiveMobs):
                        mob.draw_object()

                mob.bleed()

        heretic.draw_object()
        if heretic.y < torch.y - 40:
            torch.draw_object()

        for i in decors_list:
            if isinstance(i, Smoke):
                pygame.draw.rect(display, (210, 10, 10), (i.x, i.y, i.width, i.height))
                if not My_classes.Farmetic_classes.game_tick % 20:
                    i.fly()
                i.life_time -= 1
                if not i.life_time:
                    decors_list.remove(i)

        for rock in leftside_stones_list:
            if isinstance(rock, Rock) and heretic.y - 10 <= rock.y:
                rock.draw_object()

        for fog in leftside_decors_list:
            if isinstance(fog, Fog) and fog.y > heretic.y - 40:
                if fog.x in heretic.light_zone[0] and fog.y in heretic.light_zone[1]:
                    fog_colour = (200, 200, 200)
                else:
                    fog_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
                fog_surf = pygame.Surface((fog.width, fog.height))
                fog_surf.fill(fog_colour)
                fog_surf.set_alpha(140)
                display.blit(fog_surf, (fog.x, fog.y))

            elif isinstance(fog, Powder):
                fog.draw_object(fog.x, fog.y)

        pygame.draw.rect(display, (0, 0, 0), (heretic.x - 15, heretic.y - 30, 110, 25))
        pygame.draw.rect(display, (200, 0, 0), (heretic.x - 10, heretic.y - 28,
                                                int(100.0 * float(heretic.health) // 100.0), 21))

        if rock_owner:
            display.blit(active_font.render("Добывать", True, (0, 0, 0)), (heretic.x - 40, heretic.y - 75))
        elif chopping_active and not My_classes.Farmetic_classes.at_home and len(trees_list) > 0:
            display.blit(chopping, (heretic.x - 40, heretic.y - 75))
        elif drop_active and inactive_time < 0:
            display.blit(pick_up, (heretic.x - 60, heretic.y - 75))
        elif picked_up_time > 0:
            display.blit(picked_up, (heretic.x - 100, heretic.y - 75))

        '''
Телепортация
        '''
        if 1250 <= heretic.x <= 1400 and 450 <= heretic.y <= 550:
            display.blit(active_font.render("К дому", True, (0, 0, 0)), (heretic.x - 100, heretic.y - 75))
        if active and inactive_time < 0 and not My_classes.Farmetic_classes.at_home:
            display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))

        elif My_classes.Farmetic_classes.at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
            display.blit(exit_home, (heretic.x - 25, heretic.y - 75))

        elif chopping_active and not My_classes.Farmetic_classes.at_home and len(trees_list) > 0:
            display.blit(chopping, (heretic.x - 40, heretic.y - 75))


    pygame.display.update()
    clock.tick(60)

    if My_classes.Farmetic_classes.current_location in ['home', 'leftside'] or \
            My_classes.Farmetic_classes.inventory_mode or My_classes.Farmetic_classes.at_home:
        inactive_time -= 1
        My_classes.Farmetic_classes.game_tick += 1
        eat_time -= 1
        #  drop_appear_tick -= 1
        picked_up_time -= 1
        My_classes.Farmetic_classes.remark_time -= 1

    #  if drop_appear_tick < 0 and len(drops_list) < 5:
    # x = random.randint(100, 1300)
    #  y = random.randint(100, 800)
    #  drops_list.append(Drop(x, y, [[j for j in range(x - 100, x + 100)], [k for k in range(y - 80, y + 100)]],
    #                         random.choice(drop_type)))
    # drop_appear_tick = 500
    if not menu_tick % 30 and menu_tick <= 210:
        title += FARMETIC[menu_tick // 30]

    if My_classes.Farmetic_classes.current_location == 'menu':
        menu_tick += 1
        menu_fog_tick = random.randint(0, 400)
        if not menu_fog_tick:
            menu_decors_list.append(Fog(-100, random.randint(100, 600), random.randint(50, 100),
                                        random.randint(50, 100), 2000))

    if sleeping and not My_classes.Farmetic_classes.game_tick % 15:
        heretic.health += random.randint(2, 5)
        if z_z_Z == 'z z z ':
            z_z_Z = ''
        else:
            z_z_Z += 'z '
        if heretic.health >= 100:
            sleeping = False
            heretic.direction = 'down'
            heretic.health = 100
            My_classes.Farmetic_classes.current_string = 'Я отлично выспался'
            My_classes.Farmetic_classes.remark_time = 90
    if My_classes.Farmetic_classes.current_location != 'menu' and My_classes.Farmetic_classes.current_location != 'settings':
        if heretic.health < 0:
            heretic.health = 0
        if sleeping and not tick % 3:
            tick += 3
        else:
            tick += 1
        if 900 < tick <= 1800 and not day_return:
            if sleeping and not day_tick % 3:
                day_tick += 3
            else:
                day_tick += 1
        elif tick > 2700:
            day_tick -= 1
            day_return = True
            if tick <= 2700 or day_tick == 0:
                day_return = False
                tick = 0

    heretic.light_zone = [[i for i in range(heretic.x - 150 + day_tick // 30, heretic.x + 200 - day_tick // 30)],
                          [j for j in range(heretic.y - 150 + day_tick // 30, heretic.y + 200 - day_tick // 30)]]
    heretic.visible_zone = [list(range(heretic.x, heretic.x + 76)), list(range(heretic.y, heretic.y + 100))]
    heretic.active_zone = [list(range(heretic.x - 100, heretic.x + 100)), list(range(heretic.y - 90, heretic.y + 120))]
    if isinstance(heretic.weapon, Weapon) and heretic.weapon.blood_marks:
        heretic.weapon.blood_mark()

    if 900 < tick <= 2700 and not tick % 100:
        x = random.randint(100, 1400)
        y = random.randint(100, 800)
        fog_col = random.randint(3, 6)
        for i in range(fog_col):
            decors_list.append(Fog(random.randint(x - 50, x + 70), random.randint(y - 50, y + 50),
                                   random.randint(120, 180), random.randint(40, 100), random.randint(120, 180)))
            leftside_decors_list.append(Fog(-200, random.randint(y - 50, y + 50),
                                            random.randint(120, 180), random.randint(50, 100), 3500))
    try:
        for i in range(len(decors_list)):
            decors_list[i].life_time -= 1
            if isinstance(decors_list[i], Fog):
                if My_classes.Farmetic_classes.game_tick % 2:
                    decors_list[i].fly()
            elif isinstance(decors_list[i], Blood):
                if decors_list[i].life_time >= 540 and not decors_list[i].life_time % 10:
                    decors_list[i].x -= 1
                    decors_list[i].y -= 1
                    decors_list[i].width += 2
                    decors_list[i].height += 2
            elif isinstance(decors_list[i], FallingBlood):
                # noinspection PyUnresolvedReferences
                decors_list[i].fall()

            if not decors_list[i].life_time:
                decors_list.pop(i)

        for i in range(len(leftside_decors_list)):
            leftside_decors_list[i].life_time -= 1
            if isinstance(leftside_decors_list[i], Fog):
                if My_classes.Farmetic_classes.game_tick % 2:
                    leftside_decors_list[i].fly()
            elif isinstance(leftside_decors_list[i], Blood):
                if leftside_decors_list[i].life_time >= 540 and not leftside_decors_list[i].life_time % 10:
                    leftside_decors_list[i].x -= 1
                    leftside_decors_list[i].y -= 1
                    leftside_decors_list[i].width += 2
                    leftside_decors_list[i].height += 2

            elif isinstance(leftside_decors_list[i], Powder):

                leftside_decors_list[i].fly()
                if leftside_decors_list[i].life_time < 20:
                    leftside_decors_list[i].direction = leftside_decors_list[i].direction.replace('up', 'down')

            if leftside_decors_list[i].life_time == 0:
                leftside_decors_list.pop(i)

        for i in menu_decors_list:
            if isinstance(i, Fog):
                i.fly()
                i.life_time -= 1
                if not i.life_time:
                    menu_decors_list.remove(i)
    except (ValueError, IndexError) as e:
        print(e)

    try:
        if mobs_list:
            for mob in mobs_list:
                if isinstance(mob, AggressiveMobs):
                    if mob.x < 50 and mob.location == 'home':
                        mob.x = 1250
                        mob.location = 'leftside'
                    elif mob.x > 1300 and mob.location == 'leftside':
                        mob.x = 100
                        mob.location = 'home'
    except (ValueError, IndexError) as e:
        print(e.args)

    for rock in leftside_stones_list:
        rock.regenerate()

    if heretic.poison_time == 540:
        My_classes.Farmetic_classes.remark_time = 60
        My_classes.Farmetic_classes.current_string = random.choice(['Мне нехорошо', 'Живот болит', 'Я слабею'])

    if not heretic.health and not heretic.is_tired:
        My_classes.Farmetic_classes.current_string = random.choice(['Черт', 'Я изнурен', 'Нет сил'])
        My_classes.Farmetic_classes.remark_time = 60
        heretic.is_tired = True
        try:
            for i in heretic.inventory:
                drop_chance = random.randint(0, 2)
                if not drop_chance:
                    x = random.randint(heretic.x - 50, heretic.x + 100)
                    y = random.randint(heretic.y + 10, heretic.y + 120)
                    i.x = x
                    i.y = y
                    i.active_zone = [list(range(x - 150, x + 150)), list(range(y - 150, y + 150))]

                    if isinstance(i, DroppedBerry):
                        i.visible_zone = [list(range(x - 3, x + 50)), list(range(y - 3, y + 50))]
                    else:
                        i.visible_zone = [list(range(x - 3, x + len(i.visible_zone[0]))), list(range(y - 3, y +
                                                                                                     len(i.visible_zone[
                                                                                                             1])))]
                    if My_classes.Farmetic_classes.current_location == 'home':
                        drops_list.append(i)
                    elif My_classes.Farmetic_classes.current_location == 'leftside':
                        leftside_drops_list.append(i)
                    heretic.inventory.remove(i)
        except (ValueError, IndexError) as e:
            print(e)

    if heretic.health:
        heretic.is_tired = False
    juicemaker.work()
    furnace.work()
    juicemaker.produce_juice()

    for i in mobs_list:
        if isinstance(i, PeacefulMobs):
            i.peaceful_exist()
        elif isinstance(i, AggressiveMobs):
            if len([j for j in mobs_list if
                    isinstance(j, PeacefulMobs) and j.location == i.location]) or heretic.health > 0:
                i.agressive_exist()
            else:
                i.peaceful_exist()
    if not random.randint(0, 800):
        produce_new_peaceful_mob()
    if My_classes.Farmetic_classes.goblins_spawn and random.randint(1, 1800) == 2 \
            and 1800 <= tick <= 3000 and len([k for k in mobs_list if isinstance(k, PeacefulMobs)]):
        produce_new_aggressive_mob()

    for grass in regrowing_list:
        if isinstance(grass, HighGrass):
        #    grass.flutter()
            pass
    heretic.be_poisoned()
    if heretic.attack_time:
        heretic.attack_time -= 1
    if My_classes.Farmetic_classes.current_location != heretic.location:
        heretic.location = My_classes.Farmetic_classes.current_location
    if not volume:
        if My_classes.Farmetic_classes.current_location == 'leftside':
            pygame.mixer.music.load(r"C:\Users\User\Desktop\Farmetic-master\Leftside Track.mp3")
            pygame.mixer.music.play(-1)
        elif My_classes.Farmetic_classes.current_location == 'home':
            pygame.mixer.music.load(r'C:\Users\User\Desktop\Farmetic-master\Home track.mp3')
            pygame.mixer.music.play(-1)
        volume = 80
    if not My_classes.Farmetic_classes.game_tick:
        My_classes.Farmetic_classes.current_string = ["Давай исследовать", "Привет, я Еретик"]
        My_classes.Farmetic_classes.remark_time = 119
