import pygame, random
from My_classes.Farmetic_classes import AggressiveMobs, Mob, PeacefulMobs, Heretic, heretic, current_location, current_interface, current_string, remark_time, \
    mobs_directions, mobs_list, bushes_list, trails_list, drops_list, trees_list, leftside_drops_list, home_drops_list, \
    decors_list, leftside_decors_list, \
    leftside_stones_list, leftside_mobs_list, menu_decors_list, \
    produce_new_peaceful_mob, produce_new_aggressive_mob, print_on_screen, print_for_mob,\
    Trail, Bush, Tree, Stump, Sapling, Rock, Drop, Eatable, Log, Stone, Pine, Berry, DroppedBerry, Juice, RawMeat, Meat, \
    House, Decor, Stones, Fog, Blood, Smoke, Steps, Torch, Particles, Flashes, FallingBlood, Powder, Bed, WorkBenches, \
    JuiceMaker, GridStone, Furnace, Weapon, Sword, Stick, PickAxe, SharpenedStone, Storage, Chest, Sign, \
    blood_setting, tick, day_tick, game_tick, sleeping, home, x_home, y_home, h_length, h_width, at_home

'''
TODO:
Доработать режим Бога
Добавить все классы из Farmetic_classes !!!!!!


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

god_mode = False

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


remark_time = 0
current_string = ''

volume = 80
pygame.mixer.music.load(r'C:\Users\User\PycharmProjects\ClearSheet\Home track.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)
chopping_sound_1 = pygame.mixer.Sound(r'C:\Users\User\PycharmProjects\ClearSheet\chopping sound 1.wav')
sword_image = pygame.image.load("sword.png")

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
torch = Torch(1200, 350, 0, 0, -1)
chest = Chest(850, 160, 120, 100, [], 20, [list(range(840, 980)), list(range(150, 260))],
              [list(range(850, 970)), list(range(160, 260))])
gridstone = GridStone(980, 330, [list(range(940, 1050)), list(range(300, 420))], -1, 'off')

gridstone_recipes = ['Заточ. камень', "Копье", "Топор", "Кирка"]

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
inventory_mode = False
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
menu_tick = 0
day_return = False
drop_appear_tick = 500
z_z_Z = ''
main_mob = Mob(0, 0, 'left', [0, 2], [3, 3], 0, 0, True, 5, 0, 0, 0, '', 0, 0, 0, 'none', 'none')
heretic.x = x_home + 105
heretic.y = y_home + 50

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
for i in range(random.randint(5, 8)):
    x = random.randint(100, 1300)
    y = random.randint(100, 800)
    leftside_stones_list.append(Rock(x, y, 10, [list(range(x - 50, x + 150)), list(range(y - 50, y + 150))],
                                     [list(range(x - 30, x + 100)), list(range(y, y + 100))], 900,
                                     random.choice(['general', 'general', 'general', 'coal', 'coal', 'iron'])))

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
                if not inventory_mode:
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

                if current_location == 'menu':
                    if 450 <= event.pos[0] <= 950 and menu_tick > 600:
                        if 290 <= event.pos[1] <= 400:
                            current_location = 'home'
                        elif 570 <= event.pos[1] <= 680:
                            pygame.quit()
                        elif 430 <= event.pos[1] <= 540:
                            current_location = 'settings'

                elif current_location == 'settings':
                    if 600 <= event.pos[0] <= 750:
                        if 250 <= event.pos[1] <= 300:
                            blood_setting = not blood_setting
                        elif 380 <= event.pos[1] <= 430:
                            god_mode = not god_mode

                elif current_interface == 'gridstone':
                    if 10 <= event.pos[0] <= 310:
                        recipy = (event.pos[1] - 10) // 110
                        if recipy == 0:
                            gridstone.status = 'sharpened stone'
                            gridstone.product = SharpenedStone(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                        elif recipy == 3:
                            gridstone.status = 'pickaxe'
                            gridstone.product = PickAxe(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

                    elif 720 <= event.pos[0] <= 970 and 700 <= event.pos[1] <= 800:
                        gridstone.produce_tools(gridstone.status)

                if isinstance(m_owner, Mob) and event.pos[0] in m_owner.visible_zone[0] and event.pos[1] in \
                        m_owner.visible_zone[1] and not heretic.is_tired and not inventory_mode and not heretic.attack_time:
                    heretic.attack_mob(m_owner)

                elif drop_active and len(heretic.inventory) < 20 and not at_home:
                    picked_up_time = 60
                    if current_location == 'home':
                        picked_up = active_font.render('Я подобрал ' + drops_list[d_owner].type, True, (0, 0, 0))
                        heretic.inventory.append(drops_list[d_owner])
                        drops_list.pop(d_owner)
                    elif current_location == 'leftside':
                        picked_up = active_font.render('Я подобрал ' + leftside_drops_list[d_owner].type, True,
                                                       (0, 0, 0))
                        heretic.inventory.append(leftside_drops_list[d_owner])
                        leftside_drops_list.pop(d_owner)

                elif current_interface != 'none':
                    if current_interface == 'Chest':
                        if event.pos[0] < 600:
                            index = (event.pos[0] - 50) // 150 + (event.pos[1] - 100) // 150 * 4
                            put_item_in_the_storage(chest, index)
                        elif event.pos[0] > 820:
                            index = (event.pos[0] - 820) // 150 + (event.pos[1] - 100) // 150 * 4
                            chest.take_from_storage(index)

                elif inventory_mode and len(heretic.inventory) > 0:
                    x = random.randint(heretic.x - 50, heretic.x + 100)
                    y = random.randint(heretic.y + 10, heretic.y + 120)
                    index = (event.pos[0] - 50) // 150 + ((event.pos[1] - 100) // 150 * 4)
                    try:
                        heretic.inventory[index].x = x
                        heretic.inventory[index].y = y
                        heretic.inventory[index].active_zone = [list(range(x - 150, x + 150)),
                                                                list(range(y - 150, y + 150))]

                        if isinstance(heretic.inventory[index], DroppedBerry):
                            heretic.inventory[index].visible_zone = [list(range(x - 3, x + 50)),
                                                                     list(range(y - 3, y + 50))]
                        else:
                            heretic.inventory[index].visible_zone = [list(range(x - 3, x +
                                                                                len(heretic.inventory[
                                                                                        index].visible_zone[0]))),
                                                                     list(range(y - 3, y +
                                                                                len(heretic.inventory[
                                                                                        index].visible_zone[1])))]
                        if at_home:
                            home_drops_list.append(heretic.inventory[index])
                        elif current_location == 'leftside':
                            leftside_drops_list.append(heretic.inventory[index])
                        else:
                            drops_list.append(heretic.inventory[index])
                        heretic.inventory.pop(index)
                    except IndexError:
                        print('IndexError has been caught!')

            elif event.button == 3:
                if 825 <= event.pos[0] <= 925 and 245 <= event.pos[1] <= 345 and heretic.weapon != 'none':
                    heretic.weapon.unequip()
                else:
                    x = random.randint(heretic.x - 50, heretic.x + 120)
                    y = random.randint(heretic.y + 50, heretic.y + 120)
                    index = (event.pos[0] - 50) // 150 + (event.pos[1] - 100) // 150 * 4
                    try:
                        if isinstance(heretic.inventory[index], Eatable) or isinstance(heretic.inventory[index], Berry):
                            heretic.inventory[index].eat()
                            remark_time = 90
                            current_string = random.choice(['Вкусно', heretic.inventory[index].type + '! М-м-м',
                                                            "Объедение"])
                            eat_time = 90
                            if not isinstance(heretic.inventory[index], Berry):
                                energy_boost = '+ ' + str(heretic.inventory[index].energy)
                            else:
                                energy_boost = '+ 7'
                            heretic.inventory.pop(index)

                        elif isinstance(heretic.inventory[index], Pine):
                            if current_location == 'home':
                                trees_list.append(Sapling(x, y, 0, [[0], [0]]))
                                heretic.inventory.pop(index)
                            else:
                                current_string = "Почва не подходит"
                                remark_time = 100

                        elif isinstance(heretic.inventory[index], Weapon):
                            if heretic.weapon == 'none':
                                heretic.inventory[index].equip()

                    except IndexError:
                        print('IndexError has been caught!')

            '''
Взаимодействие
            '''
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                try:
                    if home_active and not at_home:
                        at_home = True
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

                    elif at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
                        at_home = False
                        heretic.direction = 'down'
                        heretic.x = home.x + 75
                        heretic.y = home.y + 60

                    elif current_location == 'home' and heretic.x in sign_to_leftside.active_zone[0] \
                            and heretic.y in sign_to_leftside.active_zone[1]:
                        sign_to_leftside.read()

                    elif current_location == 'leftside' and heretic.x in sign_to_home.active_zone[0] \
                            and heretic.y in sign_to_home.active_zone[1]:
                        sign_to_home.read()

                    elif active and len(bushes_list[b_owner].berries) > 0 and (not heretic.is_tired or god_mode) \
                            and len(heretic.inventory) < 20 and not at_home:
                        bushes_list[b_owner].berries.pop(random.randint(0, len(bushes_list[b_owner].berries)))
                        heretic.inventory.append(DroppedBerry(0, 0, [[], []], [[], []], 'Ягода',
                                                              ['Вкусная спелая ягода'], random.randint(6, 8)))
                        heretic.health -= random.randint(1, 3)

                    elif at_home and drop_active and len(heretic.inventory) < 20 and not inventory_mode and \
                            current_interface == 'none':
                        remark_time = 60
                        current_string = 'Я подобрал ' + home_drops_list[d_owner].type
                        heretic.inventory.append(home_drops_list[d_owner])
                        home_drops_list.pop(d_owner)

                    elif (active or chopping_active) and heretic.health <= 0 and remark_time <= 0:
                        remark_time = 60
                        current_string = random.choice(['Я очень устал', "Нет сил", "Нужно отдохнуть"])

                    elif at_home and heretic.x in juicemaker.active_zone[0] and heretic.y in juicemaker.active_zone[1] \
                            and juicemaker.work_time <= -1:
                        if len([i for i in heretic.inventory if
                                isinstance(i, Berry) or isinstance(i, DroppedBerry)]) >= 4:
                            current_string = 'Сок скоро будет готов'
                            remark_time = 60
                            juicemaker.make_juice()

                        else:
                            current_string = 'Нужно больше ягод'
                            remark_time = 60

                    elif at_home and heretic.x in furnace.active_zone[0] and heretic.y in furnace.active_zone[1] \
                            and furnace.work_time <= -1:
                        furnace.make_meat()

                    elif at_home and heretic.x in chest.active_zone[0] and heretic.y in chest.active_zone[1] and \
                            current_interface == 'none':
                        open("Chest")
                    elif at_home and heretic.x in gridstone.active_zone[0] and heretic.y in gridstone.active_zone[1] and \
                            current_interface == 'none':
                        open("gridstone")
                        gridstone.work()

                    elif chopping_active and inactive_time < 0 and (0 < heretic.health or god_mode):
                        trees_list[t_owner].chop()
                        inactive_time = 5
                        if not god_mode:
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
                                                      "Бревно", ['Необработанное бревно'], 0))
                            for i in range(random.randint(1, 2)):
                                x = random.choice(trees_list[t_owner].active_zone[0])
                                y = random.choice(trees_list[t_owner].active_zone[1])
                                drops_list.append(Pine(x, y, [[j for j in range(x - 150, x + 150)],
                                                              [k for k in range(y - 120, y + 180)]],
                                                       [[k for k in range(x - 8, x + 55)], [j for j in range(y - 5,
                                                                                                             y + 50)]],
                                                       "Желудь", ['Когда-то из него', "вырастет дерево"], 0))
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

                    elif rock_owner and rock_owner.health and heretic.health:
                        if not isinstance(heretic.weapon, PickAxe):
                            if not god_mode:
                                heretic.health -= random.randint(4, 6)
                        else:
                            heretic.weapon.mine(rock_owner)
                        if not heretic.attack_time:
                            rock_owner.be_broken()

                except IndexError:
                    print('IndexError is caught!')

                    '''
Открытие/закрытие инвентаря
            '''
            elif event.key == pygame.K_i:
                if inventory_mode:
                    inventory_mode = False
                    chosen_item = None
                else:
                    inventory_mode = True

            elif event.key == pygame.K_d and inventory_mode:
                try:
                    if pos[0] < 650:
                        pos_index_d = (pos[0] - 50) // 150 + (pos[1] - 100) // 150 * 4
                        if pos_index_d < len(heretic.inventory):
                            chosen_item = heretic.inventory[pos_index_d]
                except IndexError:
                    print('IndexError has been caught!')

            elif event.key == pygame.K_ESCAPE and current_location != 'menu':
                going_to_menu += 1
                current_location = 'menu'

    '''
Движение
    '''
    keys = pygame.key.get_pressed()
    if not inventory_mode and not sleeping and current_location != 'menu' and current_location != 'settings':
        if keys[pygame.K_a] and (heretic.x > -3 and not at_home or at_home and 300 <= heretic.x):
            if on_path:
                heretic.x -= 8
            elif heretic.is_tired:
                heretic.x -= 3
            else:
                heretic.x -= 5

            heretic.direction = 'left'
        elif keys[pygame.K_d] and (heretic.x < 1367 and not at_home or at_home and 1020 >= heretic.x):
            heretic.direction = 'right'
            if on_path:
                heretic.x += 7
            elif heretic.is_tired:
                heretic.x += 3
            else:
                heretic.x += 5

        if keys[pygame.K_w] and (heretic.y > 0 and not at_home or at_home and heretic.y > 150):
            if on_path:
                heretic.y -= 7
            elif heretic.is_tired:
                heretic.y -= 3
            else:
                heretic.y -= 4
            heretic.direction = 'up'

        elif keys[pygame.K_s] and (heretic.y < 800 and not at_home or at_home and heretic.y < 501):
            heretic.direction = 'down'
            if on_path:
                heretic.y += 5
            elif heretic.is_tired:
                heretic.y += 3
            else:
                heretic.y += 4

        if any([keys[pygame.K_a], keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_d]]) and not at_home:
            if not tick % 30:
                if heretic.direction in ['left', 'right']:
                    decors_list.append(Steps(random.randint(heretic.x + 10, heretic.x + 50), heretic.y + 80,
                                             random.randint(24, 30), random.randint(12, 16), random.randint(100, 120)))
                else:
                    decors_list.append(Steps(random.randint(heretic.x + 10, heretic.x + 50), heretic.y + 80,
                                             random.randint(12, 16), random.randint(24, 30), random.randint(100, 120)))
            if current_location == 'leftside':
                if not random.randint(0, 250):
                    for i in range(random.randint(2, 5)):
                        leftside_decors_list.append(Powder(random.randint(heretic.x, heretic.x + 50),
                                                           random.randint(heretic.y + 50, heretic.y + 120), random.choice(['left', 'right']) + ' up', 70))

    """
    Перемещение
    """
    if current_location == 'home' and heretic.x < 10:
        current_location = 'leftside'
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
    elif current_location == 'leftside' and heretic.x > 1350:
        current_location = 'home'
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

    if current_location == 'menu':
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

    elif current_location == 'settings':
        display.fill((188, 252, 240))
        display.blit(title_font.render('Настройки', True, (0, 0, 0)), (350, 10))
        display.blit(inventory_font.render('Кровь', True, (0, 0, 0)), (100, 200))
        display.blit(inventory_font.render('Режим Бога', True, (0, 0, 0)), (100, 330))
        pygame.draw.rect(display, (0, 0, 0), (600, 250, 150, 50))
        if blood_setting:
            pygame.draw.rect(display, (0, 200, 0), (610, 255, 40, 40))
        else:
            pygame.draw.rect(display, (200, 0, 0), (700, 255, 40, 40))

        pygame.draw.rect(display, (0, 0, 0), (600, 380, 150, 50))
        if god_mode:
            pygame.draw.rect(display, (0, 200, 0), (610, 385, 40, 40))
        else:
            pygame.draw.rect(display, (200, 0, 0), (700, 385, 40, 40))

    elif current_interface != 'none':
        if current_interface == 'Chest':
            display.fill((184, 173, 118))
            display.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
            display.blit(inventory_font.render('Сундук', True, (0, 0, 0)), (1000, 10))
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
                for j in range(100, 701, 150):
                    pygame.draw.rect(display, (0, 0, 200), (i, j, 130, 130))
                    pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))

            for i in range(len(chest.storage)):
                if isinstance(chest.storage[i], Berry) or isinstance(chest.storage[i], DroppedBerry):
                    chest.storage[i].draw_object(870 + 150 * (i % 4), 140 + 150 * (i // 4))

                elif isinstance(chest.storage[i], Log):
                    chest.storage[i].draw_object(845 + 150 * (i % 4), 130 + 150 * (i // 4))

                elif isinstance(chest.storage[i], Pine):
                    chest.storage[i].draw_object(850 + 150 * (i % 4), 130 + 150 * (i // 4))

                elif isinstance(chest.storage[i], Juice):
                    chest.storage[i].draw_object(860 + 150 * (i % 4), 140 + 150 * (i // 4))

                elif isinstance(chest.storage[i], RawMeat):
                    chest.storage[i].draw_object(850 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(chest.storage[i], Meat):
                    chest.storage[i].draw_object(850 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Stick):
                    chest.storage[i].draw_object(880 + 150 * (i % 4), 130 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], Stone):
                    heretic.inventory[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], SharpenedStone):
                    heretic.inventory[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], PickAxe):
                    heretic.inventory[i].draw_object(860 + 150 * (i % 4), 150 + 150 * (i // 4))

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
                if i // 110 < len(gridstone_recipes):
                    display.blit(active_font.render(gridstone_recipes[i // 110], True, (0, 0, 0)), (20, i + 30))
            if gridstone.status != 'off':
                pygame.draw.rect(display, (0, 0, 0), (720, 700, 250, 100))
                pygame.draw.rect(display, (200, 0, 0), (725, 705, 240, 90))
                display.blit(active_font.render("Крафт", True, (0, 0, 0)), (760, 720))

    elif inventory_mode:

        display.fill((184, 173, 118))
        display.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
        display.blit(inventory_font.render('Часы: день/ночь', True, (0, 0, 0)), (800, 10))
        pygame.draw.rect(display, (0, 0, 0), (800, 150, 600, 60))
        pygame.draw.rect(display, (184, 173, 118), (1260, 155, 130, 50))
        pygame.draw.rect(display, (200, 0, 0), (810, 155, int(445 * heretic.health // 100), 50))
        pygame.draw.rect(display, (0, 0, 200), (810, 230, 130, 130))
        pygame.draw.rect(display, (190, 190, 190), (825, 245, 100, 100))
        if heretic.weapon != 'none':
            heretic.weapon.draw_object(865, 260)
            display.blit(active_font.render(heretic.weapon.type, True, (0, 0, 0)), (825, 365))

        else:
            pygame.draw.rect(display, (184, 173, 118), (860, 260, 20, 45))
            pygame.draw.polygon(display, (184, 173, 118), ((860, 260), (870, 252), (880, 260)))
            pygame.draw.rect(display, (184, 173, 118), (850, 300, 40, 6))
            pygame.draw.rect(display, (184, 173, 118), (864, 306, 12, 20))

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

                elif isinstance(heretic.inventory[i], Stone):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], SharpenedStone):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

                elif isinstance(heretic.inventory[i], PickAxe):
                    heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))

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

    elif at_home:
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
            pygame.draw.line(display, (170, 161, 161), (furnace.x + 30, furnace.y + 65),
                             (furnace.x + 10, furnace.y + 90), 15)
            pygame.draw.line(display, (170, 161, 161), (furnace.x + 70, furnace.y + 65),
                             (furnace.x + 90, furnace.y + 90), 15)
            pygame.draw.ellipse(display, (142, 47, 41), (furnace.x, furnace.y, 100, 75))
            pygame.draw.ellipse(display, (0, 0, 0), (furnace.x + 5, furnace.y + 5, 90, 50))
            if furnace.status == 'on':
                pygame.draw.ellipse(display, (216, 118, 49), (furnace.x + 10, furnace.y + 8, 80, 44))
            for i in range(furnace.y + 10, furnace.y + 46, 7):
                if i == furnace.y + 10 or i == furnace.y + 45:
                    pygame.draw.line(display, (170, 161, 161), (furnace.x + 30, i), (furnace.x + 70, i), 4)
                elif i == furnace.y + 17 or i == furnace.y + 38:
                    pygame.draw.line(display, (170, 161, 161), (furnace.x + 10, i), (furnace.x + 90, i), 4)
                else:
                    pygame.draw.line(display, (170, 161, 161), (furnace.x + 5, i), (furnace.x + 95, i), 4)
            if furnace.status == 'meat':
                pygame.draw.ellipse(display, (168, 33, 0), (furnace.x + 15, furnace.y + 10, 70, 40))
            elif furnace.status == 'on':
                pygame.draw.ellipse(display, (168 - (600 - furnace.work_time) // 7, 33 - (600 - furnace.work_time)
                                              // 20, 0), (furnace.x + 15, furnace.y + 10, 70, 40))

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

        if active and inactive_time < 0 and not at_home:
            display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))
        elif remark_time > 0:
            print_on_screen(current_string)
        elif at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
            display.blit(exit_home, (heretic.x - 25, heretic.y - 75))
        elif at_home and heretic.x in juicemaker.active_zone[0] and heretic.y in juicemaker.active_zone[1]:
            display.blit(juicemaker_sign, (heretic.x - 100, heretic.y - 75))
        elif drop_active and inactive_time < 0:
            display.blit(pick_up, (heretic.x - 60, heretic.y - 75))
        elif at_home and heretic.x in furnace.active_zone[0] and heretic.y in furnace.active_zone[1]:
            display.blit(active_font.render('Гриль', True, (200, 0, 0)), (heretic.x - 20, heretic.y - 75))
        elif at_home and heretic.x in chest.active_zone[0] and heretic.y in chest.active_zone[1]:
            display.blit(active_font.render('Сундук', True, (200, 0, 0)), (heretic.x - 35, heretic.y - 75))
        elif at_home and heretic.x in gridstone.active_zone[0] and heretic.y in gridstone.active_zone[1]:
            display.blit(active_font.render('Точило', True, (200, 0, 0)), (heretic.x - 35, heretic.y - 75))
        elif chopping_active and not at_home and len(trees_list) > 0:
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

    elif current_location == 'home':
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
            if bush.y > heretic.y + 40 and not at_home and current_location == 'home' \
                    and heretic.x in bush.active_zone[0]:
                continue
            if bush.x not in heretic.light_zone[0] or bush.y not in heretic.light_zone[1]:
                colour = (0, 100 - day_tick // 20, 0)
            else:
                colour = (0, 100, 0)
            pygame.draw.rect(display, colour, (bush.x, bush.y, 100, 100))
            for ber in bush.berries:
                pygame.draw.rect(display, (200, 0, 0), (ber.x, ber.y, 10, 10))

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
                    if trees_list[tree].health < 500:
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x, trees_list[tree].y, 20, 60))
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - 30, trees_list[tree].y + 20, 30,
                                                                  10))
                    elif 1000 >= trees_list[tree].health >= 500:
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x, trees_list[tree].y - 60, 25, 120))
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - 40, trees_list[tree].y + 30, 40,
                                                                  15))
                        pygame.draw.rect(display, (137, 88, 36), (trees_list[tree].x - 40, trees_list[tree].y, 15, 30))
                        pygame.draw.ellipse(display, (40, 122, 36), (trees_list[tree].x - 60, trees_list[tree].y - 10,
                                                                     40, 40))
                    trees_list[tree].health += 1
                    if trees_list[tree].health >= 1800:
                        trees_list[tree].regrowth()
                        trees_list.pop(tree)

                else:
                    if trees_list[tree].y > heretic.y + 45 and not at_home and current_location == 'home':
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
        if not inventory_mode:

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

            for fog in decors_list:
                if isinstance(fog, FallingBlood):
                    fog.fly()
                    fog.draw_object(fog.x, fog.y)
                    fog.life_time -= 1
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
                if bush.y > heretic.y + 40 and not at_home and current_location == 'home' and heretic.x in \
                        bush.active_zone[0]:
                    if bush.x not in heretic.light_zone[0] or bush.y not in heretic.light_zone[1]:
                        colour = (0, 100 - day_tick // 20, 0)
                    else:
                        colour = (0, 100, 0)
                    pygame.draw.rect(display, colour, (bush.x, bush.y, 100, 100))
                    for ber in bush.berries:
                        pygame.draw.rect(display, (200, 0, 0), (ber.x, ber.y, 10, 10))

            if home.y > heretic.y and not at_home and current_location == 'home':
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
                    if trees_list[tree].y > heretic.y + 45 and not at_home and current_location == 'home':
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

                        elif not at_home and not isinstance(trees_list[tree], Sapling):
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

            if home_active and not at_home:
                display.blit(enter, (heretic.x - 25, heretic.y - 75))

            elif tp_to_left_side and not at_home:
                display.blit(leftside_tp, (heretic.x - 50, heretic.y - 75))

            elif remark_time > 0:
                print_on_screen(current_string)

            elif m_owner is not None:
                display.blit(active_font.render('Атаковать', True, (0, 0, 0)), (heretic.x - 50, heretic.y - 75))

            elif at_home and heretic.x in juicemaker.active_zone[0] and heretic.y in juicemaker.active_zone[1]:
                display.blit(juicemaker_sign, (heretic.x - 100, heretic.y - 75))

            elif active and inactive_time < 0 and not at_home:
                display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))

            elif at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
                display.blit(exit_home, (heretic.x - 25, heretic.y - 75))

            elif chopping_active and not at_home and len(trees_list) > 0:
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
                if mob.remark_time > 0:
                    print_for_mob(mob, mob.remark)

        '''
    Лефт-Сайд
'''
    elif current_location == 'leftside':

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

        if not inventory_mode:
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
                if not game_tick % 20:
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

        if active and inactive_time < 0 and not at_home:
            display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))
        elif at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
            display.blit(exit_home, (heretic.x - 25, heretic.y - 75))
        elif rock_owner:
            display.blit(active_font.render("Добывать", True, (0, 0, 0)), (heretic.x - 40, heretic.y - 75))
        elif chopping_active and not at_home and len(trees_list) > 0:
            display.blit(chopping, (heretic.x - 40, heretic.y - 75))
        elif drop_active and inactive_time < 0:
            display.blit(pick_up, (heretic.x - 60, heretic.y - 75))
        elif picked_up_time > 0:
            display.blit(picked_up, (heretic.x - 100, heretic.y - 75))

        '''
Телепортация
        '''
        if 1250 <= heretic.x <= 1400 and 400 <= heretic.y <= 550:
            tp_to_home = True
        else:
            tp_to_home = False

        if home_active and not at_home:
            display.blit(enter, (heretic.x - 25, heretic.y - 75))

        elif tp_to_left_side and not at_home:
            display.blit(leftside_tp, (heretic.x - 50, heretic.y - 75))

        elif tp_to_home:
            display.blit(home_tp, (heretic.x - 20, heretic.y - 75))

        elif active and inactive_time < 0 and not at_home:
            display.blit(collect_berry, (heretic.x - 100, heretic.y - 75))

        elif at_home and 450 <= heretic.y < 600 <= heretic.x <= 750:
            display.blit(exit_home, (heretic.x - 25, heretic.y - 75))

        elif chopping_active and not at_home and len(trees_list) > 0:
            display.blit(chopping, (heretic.x - 40, heretic.y - 75))

        elif drop_active and inactive_time < 0:
            display.blit(pick_up, (heretic.x - 60, heretic.y - 75))

        elif picked_up_time > 0:
            display.blit(picked_up, (heretic.x - 100, heretic.y - 75))

    pygame.display.update()
    clock.tick(60)

    if current_location in ['home', 'leftside'] or inventory_mode or at_home:
        inactive_time -= 1
        game_tick += 1
        eat_time -= 1
        #  drop_appear_tick -= 1
        picked_up_time -= 1
        remark_time -= 1

    #  if drop_appear_tick < 0 and len(drops_list) < 5:
    # x = random.randint(100, 1300)
    #  y = random.randint(100, 800)
    #  drops_list.append(Drop(x, y, [[j for j in range(x - 100, x + 100)], [k for k in range(y - 80, y + 100)]],
    #                         random.choice(drop_type)))
    # drop_appear_tick = 500
    if not menu_tick % 30 and menu_tick <= 210:
        title += FARMETIC[menu_tick // 30]

    if current_location == 'menu':
        menu_tick += 1
        menu_fog_tick = random.randint(0, 400)
        if not menu_fog_tick:
            menu_decors_list.append(Fog(-100, random.randint(100, 600), random.randint(50, 100),
                                        random.randint(50, 100), 2000))

    if sleeping and game_tick % 15 == 0:
        heretic.health += random.randint(2, 5)
        if z_z_Z == 'z z z ':
            z_z_Z = ''
        else:
            z_z_Z += 'z '
        if heretic.health >= 100:
            sleeping = False
            heretic.direction = 'down'
            heretic.health = 100
            current_string = 'Я отлично выспался'
            remark_time = 90
    if current_location != 'menu' and current_location != 'settings':
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

    if 900 < tick <= 2700 and not tick % 90:
        x = random.randint(100, 1400)
        y = random.randint(100, 800)
        fog_col = random.randint(3, 6)
        for i in range(fog_col):
            decors_list.append(Fog(random.randint(x - 50, x + 70), random.randint(y - 50, y + 50),
                                   random.randint(120, 180), random.randint(40, 100), random.randint(120, 180)))
            leftside_decors_list.append(Fog(random.randint(x - 50, x + 70), random.randint(y - 50, y + 50),
                                            random.randint(120, 180), random.randint(50, 100),
                                            random.randint(130, 200)))
    try:
        for i in range(len(decors_list)):
            decors_list[i].life_time -= 1
            if isinstance(decors_list[i], Fog):
                if game_tick % 2:
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

            if decors_list[i].life_time == 0:
                decors_list.pop(i)

        for i in range(len(leftside_decors_list)):
            leftside_decors_list[i].life_time -= 1
            if isinstance(leftside_decors_list[i], Fog):
                if game_tick % 2:
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
        remark_time = 60
        current_string = random.choice(['Мне нехорошо', 'Живот болит', 'Я слабею'])

    if not heretic.health and not heretic.is_tired:
        current_string = random.choice(['Черт', 'Я изнурен', 'Нет сил'])
        remark_time = 60
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
                    if current_location == 'home':
                        drops_list.append(i)
                    elif current_location == 'leftside':
                        leftside_drops_list.append(i)
                    heretic.inventory.remove(i)
        except (ValueError, IndexError) as e:
            print(e)

    if heretic.health:
        heretic.is_tired = False
    juicemaker.work()
    furnace.work()
    juicemaker.produce_juice()
    if not furnace.work_time:
        furnace.produce_meat()
    for i in mobs_list:
        if isinstance(i, PeacefulMobs):
            i.peaceful_exist()
        elif isinstance(i, AggressiveMobs):
            if len([j for j in mobs_list if isinstance(j, PeacefulMobs) and j.location == i.location]) or heretic.health > 0:
                i.agressive_exist()
            else:
                i.peaceful_exist()
    if not random.randint(0, 800):
        produce_new_peaceful_mob()
    if random.randint(1, 1200) == 2 and 1800 <= tick <= 3000 and len([k for k in mobs_list if isinstance(k, PeacefulMobs)]):
        produce_new_aggressive_mob()
    heretic.be_poisoned()
    if heretic.attack_time:
        heretic.attack_time -= 1
    if current_location != heretic.location:
        heretic.location = current_location
    if not volume:
        if current_location == 'leftside':
            pygame.mixer.music.load(r"C:\Users\User\PycharmProjects\ClearSheet\Leftside Track.mp3")
            pygame.mixer.music.play(-1)
        elif current_location == 'home':
            pygame.mixer.music.load(r'C:\Users\User\PycharmProjects\ClearSheet\Home track.mp3')
            pygame.mixer.music.play(-1)
        volume = 80
    if not game_tick:
        current_string = ["Давай исследовать", "Привет, я Еретик"]
        remark_time = 119
