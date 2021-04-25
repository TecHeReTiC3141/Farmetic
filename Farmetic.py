import pygame, random

'''
TODO:
Доработать режим Бога

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
blood_setting = True
god_mode = False

mobs_directions = ['left', 'right', 'up', 'down']
mobs_list = []
bushes_list = []
trails_list = []
drops_list = []
trees_list = []
leftside_drops_list = []

home_drops_list = []
decors_list = []
leftside_decors_list = []
leftside_stones_list = []
leftside_mobs_list = []

menu_decors_list = []

game = True
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


def print_on_screen(s):
    if remark_time > 0:
        display.blit(active_font.render(s, True, (0, 0, 0)), (heretic.x - 8 * len(s), (heretic.y - 75)))


def print_for_mob(talking_mob, mob_remark):
    display.blit(active_font.render(mob_remark, True, (0, 0, 0)), (talking_mob.x - 4 * len(mob_remark),
                                                                   (talking_mob.y - 75)))


def put_item_in_the_storage(storage, i):
    if len(storage.storage) < storage.max_capability and len(heretic.inventory) > i:
        storage.storage.append(heretic.inventory[i])
        heretic.inventory.pop(i)


class Heretic(object):

    def __init__(self, h_x, h_y, health, direction, inventory, light_zone, strength, weapon, poison_time, is_tired,
                 visible_zone, active_zone, attack_time=0, half_attack_time=0):
        self.x = h_x
        self.y = h_y
        self.health = health
        self.direction = direction
        self.inventory = inventory
        self.light_zone = light_zone
        self.strength = strength
        self.weapon = weapon
        self.poison_time = poison_time
        self.is_tired = is_tired
        self.visible_zone = visible_zone
        self.active_zone = active_zone
        self.attack_time = attack_time
        self.half_attack_time = half_attack_time

    def attack_mob(self, attacked_mob):
        attacked_mob.health -= self.strength
        attacked_mob.speed = random.randint(3, 4)
        if not god_mode:
            self.health -= self.strength * 2
            if isinstance(self.weapon, Weapon):
                 self.attack_time = self.weapon.speed * 50
                 self.half_attack_time = self.weapon.speed * 25
                 self.weapon.blood_marks += random.randint(150, 300)
            else:
                self.attack_time = 60
                self.half_attack_time = 30
        if not random.randint(0, 8) and heretic.strength > 2:
            attacked_mob.stop = True
            attacked_mob.delay = 20
        else:
            attacked_mob.stop = False
            attacked_mob.delay = random.randint(210, 240)
        if blood_setting:
            for i in range(heretic.strength):
                blood_y = random.choice(attacked_mob.visible_zone[1])
                decors_list.append(FallingBlood(random.choice(attacked_mob.visible_zone[0]),
                                                blood_y, "down", (100 - (blood_y - attacked_mob.y)) // 2))

        if heretic.x > attacked_mob.x:
            attacked_mob.x -= abs(self.x - attacked_mob.x) // 2
        else:
            attacked_mob.x += abs(self.x - attacked_mob.x) // 2
        if heretic.y > attacked_mob.y:
            attacked_mob.y -= abs(self.y - attacked_mob.y) // 2
        else:
            attacked_mob.y += abs(self.y - attacked_mob.y) // 2
        attacked_mob.active_zone = [[j for j in range(attacked_mob.x - 100, attacked_mob.x + 150)],
                                    [k for k in range(attacked_mob.y - 100, attacked_mob.y + 100)]]
        attacked_mob.bleeding = heretic.strength * 200
        if isinstance(attacked_mob, AggressiveMobs):
            attacked_mob.target = heretic
        if heretic.weapon != 'none':
            heretic.weapon.durability -= 1
            if not heretic.weapon.durability:
                heretic.weapon = 'none'
                heretic.strength = 1

    def draw_object(self):
        if heretic.weapon != 'none' and heretic.direction == 'right':
            heretic.weapon.draw_object(heretic.x + 65 - ((heretic.half_attack_time -
                                                                         heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0), heretic.y + 30)
        elif heretic.weapon != 'none' and heretic.direction == 'up':
            heretic.weapon.draw_object(heretic.x - 15, heretic.y + 30 + ((heretic.half_attack_time -
                                                                         heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0))
        pygame.draw.rect(display, (0, 0, 0), (heretic.x, heretic.y, 75, 100))
        if god_mode:
            eye_colour = (237, 202, 59)
        else:
            eye_colour = (0, 0, 0)
        if heretic.direction == 'down':
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 10, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 40, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (heretic.x + 18, heretic.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (heretic.x + 48, heretic.y + 17, 4, 4))
            if heretic.weapon != 'none':
                heretic.weapon.draw_object(heretic.x + 65, heretic.y + 30 - ((heretic.half_attack_time -
                                                                         heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0))

        elif heretic.direction == 'left':
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 8, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 38, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (heretic.x + 13, heretic.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (heretic.x + 43, heretic.y + 17, 4, 4))
            if heretic.weapon != 'none':
                heretic.weapon.draw_object(heretic.x + 45 + ((heretic.half_attack_time -
                                                                         heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0), heretic.y + 30)

        elif heretic.direction == 'right':
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 20, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 50, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (heretic.x + 31, heretic.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (heretic.x + 61, heretic.y + 17, 4, 4))
        pygame.draw.rect(display, (0, 0, 0), (heretic.x - 15, heretic.y - 30, 110, 25))
        if not heretic.poison_time:
            pygame.draw.rect(display, RED, (heretic.x - 10, heretic.y - 28,
                                            int(100.0 * float(heretic.health) / 100.0), 21))
        else:
            pygame.draw.rect(display, GREEN, (heretic.x - 10, heretic.y - 28,
                                              int(100.0 * float(heretic.health) / 100.0), 21))

    def be_poisoned(self):
        if self.poison_time > 0:
            if not self.poison_time % 20:
                self.health -= 1
            self.poison_time -= 1


def produce_new_peaceful_mob():
    if len([i for i in mobs_list if isinstance(i, PeacefulMobs)]) < 6:
        spawn_chance = random.randint(1, 800)
        if spawn_chance == 2:
            x = random.randint(0, 1440)
            y = random.randint(0, 800)
            mobs_list.append(PeacefulMobs(x, y, random.choice(mobs_directions),
                                          [[j for j in range(x - 100, x + 150)],
                                           [k for k in range(y - 100, y + 100)]],
                                          [[j for j in range(x, x + 90)], [k for k in range(y, y + 60)]],
                                          8, 20, True, [RawMeat(0, 0, [[0], [0]], [[0], [0]],
                                                                "Сырое мясо",
                                                                ['Большой кусок сырого', "мяса. Следует пожарить."],
                                                                random.randint(20, 25))], 2, 0, 0, '', 0, 0, 0, 'home',
                                          'none'))


def produce_new_aggressive_mob():
    """
    Создает нового агрессивного моба

    :return: новый объект класс AggressiveMod
    """
    if len([i for i in mobs_list if isinstance(i, AggressiveMobs)]) < 4:
        spawn_chance = random.randint(1, 1400)
        if spawn_chance == 2 and 1800 <= tick <= 3000 and len([k for k in mobs_list if isinstance(k, PeacefulMobs)]):
            for i in range(random.randint(4, 5)):
                spawn_point = random.randint(1, 2)
                if spawn_point == 1:
                    mob_x = random.choice([-100, 1500])
                    mob_y = random.randint(0, 800)
                else:
                    mob_x = random.randint(100, 1300)
                    mob_y = random.choice([-100, 900])
                heretic_chance = random.randint(0, 5)
                if not heretic_chance:
                    target = heretic
                else:
                    target = random.choice([j for j in mobs_list if isinstance(j, PeacefulMobs)])
                weapon = random.choice(['none', 'none', SharpenedStone(0, 0, [[0, 0], [0, 0]], [[0, 0], [0, 0]],
                                                                       "Заточенный камень",
                                                                       ['Заточенный булыжник',
                                                                        "Острый, но хрупкий",
                                                                        "Основной материал для",
                                                                        "продвинутого оружия"],
                                                                       random.randint(2, 3), 10, 10, 1),
                                        Stick(0, 0, [[0, 0], [0, 0]], [[0, 0], [0, 0]],
                                              "Палка",
                                              ['Заточенный булыжник',
                                               "Острый, но хрупкий",
                                               "Основной материал для",
                                               "продвинутого оружия"],
                                              random.randint(2, 3), 10, 10, 2)])
                strength = 3
                if isinstance(weapon, Weapon):
                    strength += weapon.strength


                mobs_list.append(AggressiveMobs(mob_x, mob_y, random.choice(mobs_directions),
                                                [[j for j in range(mob_x - 100, mob_x + 175)],
                                                 [k for k in range(mob_y - 100, mob_y + 120)]],
                                                [[j for j in range(mob_x, mob_x + 75)],
                                                 [k for k in range(mob_y, mob_y + 100)]],
                                                12, 20, True, [weapon if isinstance(weapon, Weapon) else None], 2, 0, 0, '', target, strength, 150, 'home',
                                                weapon))


class Mob(object):

    def __init__(self, m_x, m_y, direction, active_zone, visible_zone, health, delay, stop, loot, speed, bleeding,
                 mob_remark_time, mob_remark, target, strength, attack_time, location, weapon):

        self.x = m_x
        self.y = m_y
        self.direction = direction
        self.visible_zone = visible_zone
        self.active_zone = active_zone
        self.health = health
        self.delay = delay
        self.stop = stop
        self.loot = loot
        self.speed = speed
        self.bleeding = bleeding
        self.remark_time = mob_remark_time
        self.remark = mob_remark
        self.target = target
        self.strength = strength
        self.attack_time = attack_time
        self.location = location
        self.weapon = weapon

    def walk_left(self):
        self.direction = 'left'
        self.x -= self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 90)], [k for k in range(self.y, self.y + 60)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.x <= 0:
            self.x = 0

    def walk_right(self):
        self.direction = 'right'
        self.x += self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 90)], [k for k in range(self.y, self.y + 60)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.x >= 1360:
            self.x = 1360

    def walk_up(self):
        self.direction = 'up'
        self.y -= self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 60)], [k for k in range(self.y, self.y + 90)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.y <= 0:
            self.y = 0

    def walk_down(self):
        self.direction = 'down'
        self.y += self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 60)], [k for k in range(self.y, self.y + 90)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.y >= 800:
            self.y = 800

    def eat_grass(self):

        pass

    def bleed(self):
        if self.bleeding and not self.bleeding % 100:
            decors_list.append(Blood(random.choice(mob.visible_zone[0]), random.choice(mob.visible_zone[1]),
                                     random.randint(15, 30), random.randint(15, 30), 600))
        if self.bleeding:
            self.bleeding -= 1

    def peaceful_exist(self):
        self.delay -= 1
        if self.delay <= 0:
            action = random.randint(-3, 4)
            if action < 0:
                self.stop = True
                self.direction = random.choice(mobs_directions)
                self.delay = random.randint(150, 240)
            else:
                self.speed = 2
                self.stop = False
                self.direction = random.choice(mobs_directions)
                self.delay = random.randint(150, 180)

        else:
            if not self.stop:
                if self.direction == 'left':
                    self.walk_left()
                elif self.direction == 'right':
                    self.walk_right()
                elif self.direction == 'up':
                    self.walk_up()
                elif self.direction == 'down':
                    self.walk_down()
                if (self.x <= 0 and self.direction == 'left') or (1350 <= self.x and self.direction == 'right') or \
                        (self.y <= 0 and self.direction == 'up') or (780 <= self.y and self.direction == 'down'):
                    up_side_down_direction = mobs_directions.index(self.direction)
                    if up_side_down_direction % 2:
                        self.direction = mobs_directions[up_side_down_direction - 1]
                    else:
                        self.direction = mobs_directions[up_side_down_direction + 1]

        if self.x < 0:
            self.walk_right()

        elif self.x > 1440:
            self.walk_left()

        if self.y < 0:
            self.walk_down()

        elif self.y > 900:
            self.walk_up()

        if self.stop:
            eating_chance = random.randint(0, 60)
            if eating_chance < 2:
                self.eat_grass()

        if self.health <= 0:

            for loot_item in self.loot:
                loot_item.x = random.randint(self.x - 50, self.x + 50)
                loot_item.y = random.randint(self.y - 50, self.y + 50)
                loot_item.active_zone = [[k for k in range(loot_item.x - 50, loot_item.x + 150)],
                                         [j for j in range(loot_item.y - 50, loot_item.y + 150)]]
                loot_item.visible_zone = [[k for k in range(loot_item.x, loot_item.x + 70)],
                                          [j for j in range(loot_item.y, loot_item.y + 70)]]
                drops_list.append(loot_item)

            dead_mob_x = random.randint(self.x - 10, self.x + 20)
            dead_mob_y = random.randint(self.y - 10, self.y + 20)
            fog_col1 = random.randint(2, 5)
            for i in range(fog_col1):
                decors_list.append(Fog(random.randint(dead_mob_x - 50, dead_mob_x + 70),
                                       random.randint(dead_mob_y - 50, dead_mob_y + 50),
                                       random.randint(40, 100), random.randint(40, 100), random.randint(120, 180)))
            mobs_list.pop(mobs_list.index(self))

        if self.remark_time > 0:
            self.remark_time -= 1


class PeacefulMobs(Mob):

    @staticmethod
    def print_type(self):
        print(type(self))


class AggressiveMobs(Mob):

    def hit(self):
        self.attack_time = 150
        if not (self.target == heretic and god_mode):
            self.target.health -= self.strength
        if self.target.health < 0:
            self.target.health = 0
        if isinstance(self.target, PeacefulMobs):
            self.target.speed = random.randint(3, 4)
            self.target.stop = False
        if self.x > self.target.x:
            self.target.x -= 100
        else:
            self.target.x += 100
        if self.y > self.target.y:
            self.target.y -= 100
        else:
            self.target.y += 100
        self.target.active_zone = [[j for j in range(self.target.x - 100, self.target.x + 150)],
                                   [k for k in range(self.target.y - 100, self.target.y + 100)]]
        if isinstance(self.weapon, Weapon):
            self.weapon.durability -= 1
            if not self.weapon.durability:
                self.weapon = 'none'
                self.strength = 3

    def agressive_exist(self):

        if (self.x > self.target.x + len(self.target.visible_zone[0]) // 2) or (
                self.location == 'home' and current_location == 'leftside'):
            self.walk_left()

        elif self.x < self.target.x - len(self.visible_zone[0]) // 2:
            self.walk_right()

        if self.y < self.target.y - len(self.visible_zone[1]) // 2:
            self.walk_down()

        elif self.y > self.target.y + len(self.target.visible_zone[1]) // 2:
            self.walk_up()
        if self.x in self.target.active_zone[0] and self.y in self.target.active_zone[1] and not self.attack_time:
            if (self.target == heretic and current_location == 'home' and not at_home) or self.target != heretic:
                self.hit()
        if self.attack_time:
            self.attack_time -= 1

        if ((self.target != heretic and self.target not in mobs_list) or (
                self.target == heretic and not heretic.health)):
            heretic_chance = random.randint(0, 5)
            if not heretic_chance and current_location == 'home':
                self.target = heretic
            elif heretic_chance and len([i for i in mobs_list if isinstance(i, PeacefulMobs)]):
                self.target = random.choice([j for j in mobs_list if isinstance(j, PeacefulMobs)])

        if self.x < 0:
            self.walk_right()

        elif self.x > 1440:
            self.walk_left()

        if self.y < 0:
            self.walk_down()

        elif self.y > 900:
            self.walk_up()

        if tick <= 1000:
            if not tick % 200:
                self.health -= 1

        if self.health <= 0:
            mobs_list.remove(self)

        self.collect_food()

    def draw_object(self):
        if self.weapon != 'none' and self.direction == 'right':
            self.weapon.draw_object(self.x + 65, self.y + 30)
        elif self.weapon != 'none' and self.direction == 'up':
            self.weapon.draw_object(self.x - 15, self.y + 30)
        pygame.draw.rect(display, (0, 120, 0), (self.x, self.y, 75, 100))
        if (self.x in heretic.light_zone[0] or self.x + 75 in heretic.light_zone[0]) and \
                (self.y in heretic.light_zone[1] or self.y + 75 in heretic.light_zone[1]):
            belt_color = (207, 140, 79)
        else:
            belt_color = (207 - day_tick // 15, 140 - day_tick // 15, 79 - day_tick // 15)
        pygame.draw.rect(display, belt_color, (self.x - 1, self.y + 60, 77, 15))
        if self.direction == 'down':
            for j in range(self.x + 10, self.x + 41, 30):
                pygame.draw.rect(display, (0, 0, 0), (j, self.y + 10, 20, 20))
                pygame.draw.rect(display, (150, 0, 0), (j + 7, self.y + 16, 5, 5))
            pygame.draw.rect(display, (182, 45, 7), (self.x + 15, self.y + 40, 40, 10))
            if self.weapon != 'none':
                self.weapon.draw_object(self.x + 65, self.y + 30)

        elif self.direction == 'left':
            for j in range(self.x + 8, self.x + 39, 30):
                pygame.draw.rect(display, (0, 0, 0), (j, self.y + 10, 20, 20))
                pygame.draw.rect(display, (150, 0, 0), (j + 3, self.y + 16, 5, 5))
            pygame.draw.rect(display, (182, 45, 7), (self.x + 10, self.y + 40, 40, 10))
            if self.weapon != 'none':
                self.weapon.draw_object(self.x + 45, self.y + 30)
        elif self.direction == 'right':
            for j in range(self.x + 20, self.x + 51, 30):
                pygame.draw.rect(display, (0, 0, 0), (j, self.y + 10, 20, 20))
                pygame.draw.rect(display, (150, 0, 0), (j + 12, self.y + 16, 5, 5))
            pygame.draw.rect(display, (182, 45, 7), (self.x + 25, self.y + 40, 40, 10))

        if heretic.x in self.active_zone[0] and heretic.y in self.active_zone[1]:
            pygame.draw.rect(display, (0, 0, 0), (self.x + 5, self.y - 30, 50, 20))
            pygame.draw.rect(display, (200, 0, 0),
                             (self.x + 7, self.y - 28, int(46.0 * self.health / 10.0), 16))

    def collect_food(self):
        for food in [drop for drop in drops_list if isinstance(drop, Eatable)]:
            if (self.x in food.active_zone[0] or self.x + 75 in food.active_zone[0]) \
                    and (self.y in food.active_zone[1] or self.y + 100 in food.active_zone[1]):
                self.loot.append(food)
                drops_list.remove(food)


heretic = Heretic(random.randint(100, 1300), random.randint(100, 800), 100, 'down', [], [[1], [2]], 1, 'none', 0, False,
                  [[0], [0]], [[0], [0]])


class Trail(object):

    def __init__(self, t_x, t_y, direction, t_length, t_width, active_zone, visible_zone, light_zones, steps):
        self.x = t_x
        self.y = t_y
        self.direction = direction
        self.length = t_length
        self.width = t_width
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.light_zones = light_zones
        self.steps = steps


class Bush(object):

    def __init__(self, b_x, b_y, regrowth_time, berries, active_zone, visible_zone):
        self.x = b_x
        self.y = b_y
        self.berries = berries
        self.regrowth_time = regrowth_time
        self.berries = berries
        self.active_zone = active_zone
        self.visible_zone = visible_zone


class Tree(object):

    def __init__(self, t_x, t_y, health, active_zone):
        self.x = t_x
        self.y = t_y
        self.health = health
        self.active_zone = active_zone

    def chop(self):
        self.health -= 1


class Stump(Tree):

    def regrowth(self):
        trees_list.append(Tree(self.x, self.y, random.randint(3, 5), [[j for j in range(self.x - 120, self.x + 70)],
                                                                      [k for k in range(self.y - 70, self.y + 100)]]))


class Sapling(Tree):

    def regrowth(self):
        trees_list.append(Tree(self.x, self.y, random.randint(8, 13), [[j for j in range(self.x - 120, self.x + 70)],
                                                                       [k for k in range(self.y - 70, self.y + 100)]]))


class Rock(object):

    def __init__(self, r_x, r_y, health, active_zone, visible_zone, regeneration_time):
        self.x = r_x
        self.y = r_y
        self.health = health
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.regeneration_time = regeneration_time

    def be_broken(self):
        self.health -= 1
        heretic.attack_time = 60
        stone_chance = random.randint(1, 5)
        if stone_chance == 1 and self.health:
            stone_x = random.choice(self.active_zone[0])
            stone_y = random.choice(self.active_zone[1])
            leftside_drops_list.append(Stone(stone_x, stone_y, [list(range(stone_x - 50, stone_x + 100)),
                                                                list(range(stone_y - 50, stone_y))],
                                             [list(range(stone_x, stone_x + 51)), list(range(stone_y, stone_y + 51))],
                                             "Камешек", ["Небольшой камень.", "Можно обработать"], 0))

    def draw_object(self):
        pygame.draw.polygon(display, (181, 184, 177),
                            ((self.x, self.y + 100 - self.health * 10), (self.x + 70, self.y + 100 - self.health * 10),
                             (self.x + 100, self.y + 100),
                             (self.x - 30, self.y + 100)))

    def regenerate(self):
        if self.regeneration_time > 0:
            self.regeneration_time -= 1
        if not self.regeneration_time and self.health < 10:
            self.health += 1
            self.regeneration_time = 900


class Berry(object):

    def __init__(self, b_x, b_y, b_type, description):
        self.x = b_x
        self.y = b_y
        self.type = b_type
        self.description = description

    def eat(self):
        global eat_time, energy_boost
        heretic.health += random.randint(6, 8)
        eat_time = 100
        energy_boost = '+ 7'
        if heretic.health > 100:
            heretic.health = 100


'''
Классы предметов на земле:начало
'''


class Drop(object):

    def __init__(self, d_x, d_y, active_zone, visible_zone, d_type, description, energy):
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.x = d_x
        self.y = d_y
        self.type = d_type
        self.description = description
        self.energy = energy

    def up_down(self):
        if game_tick % 60 == 1:
            self.y += 17
        elif game_tick % 60 == 29:
            self.y -= 17

    def pick_up(self):
        heretic.inventory.append(self)

    def draw_object(self, drop_x, drop_y):
        pass


class Eatable(Drop):

    def eat(self):
        global eat_time, energy_boost

        heretic.health += self.energy
        eat_time = 100
        energy_boost = '+ ' + str(self.energy)
        if heretic.health > 100:
            heretic.health = 100


class Log(Drop):

    def print_type(self):
        print(type(self))

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (137, 99, 36), (drop_x, drop_y, 80, 50))
        pygame.draw.ellipse(display, (155, 136, 70), (drop_x - 15, drop_y, 30, 50))


class Stone(Drop):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (0, 0, 0), (drop_x - 1, drop_y - 1, 42, 42))
        pygame.draw.rect(display, (181, 184, 177), (drop_x, drop_y, 40, 40))
        pygame.draw.rect(display, (158, 158, 158), (drop_x, drop_y + 25, 40, 15))


class Pine(Drop):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (112, 68, 36), (drop_x, drop_y, 50, 30))
        pygame.draw.rect(display, (157, 104, 57), (drop_x + 10, drop_y + 30, 30, 20))
        pygame.draw.rect(display, (112, 68, 36), (drop_x + 20, drop_y - 10, 10, 10))

    @staticmethod
    def print_type(self):
        print(type(self))


class DroppedBerry(Eatable):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (200, 0, 0), (drop_x, drop_y, 50, 50))
        pygame.draw.rect(display, (0, 170, 0), (drop_x + 20, drop_y - 15, 10, 15))

    @staticmethod
    def print_type(self):
        print(type(self))


class Juice(Eatable):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.polygon(display, (171, 242, 242), ((drop_x - 5, drop_y), (drop_x, drop_y + 35),
                                                       (drop_x + 20, drop_y + 35), (drop_x + 25, drop_y)))
        pygame.draw.rect(display, (200, 0, 0), (drop_x, drop_y + 1, 20, 30))

    @staticmethod
    def print_type(self):
        print(type(self))


def poison():
    heretic.poison_time = 600


class RawMeat(Eatable):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.ellipse(display, (168, 33, 0), (drop_x, drop_y, 70, 40))

    def eat(self):
        global eat_time, energy_boost
        heretic.health += self.energy
        eat_time = 100
        energy_boost = '+ ' + str(self.energy)
        if heretic.health > 100:
            heretic.health = 100
        poison_chance = random.randint(0, 1)
        if poison_chance:
            poison()


class Meat(Eatable):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.ellipse(display, (98, 5, 0), (drop_x, drop_y, 70, 40))

    @staticmethod
    def print_type(self):
        print(type(self))


'''
Классы предметов на земле:конец
'''


class House(Trail):

    @staticmethod
    def tp_to_home():
        display.fill((0, 0, 0))
        pygame.time.wait(1500)
        at_home = True


'''
Классы декора:начало
'''


class Decor(object):

    def __init__(self, decor_x, decor_y, d_width, d_height, life_time):
        self.x = decor_x
        self.y = decor_y
        self.width = d_width
        self.height = d_height
        self.life_time = life_time


class Stones(Decor):

    @staticmethod
    def print_type(self):
        print(type(self))


class Fog(Decor):

    @staticmethod
    def print_type(self):
        print(type(self))

    def fly(self):
        self.x += 1


class Blood(Decor):

    @staticmethod
    def print_type(self):
        print(type(self))


class Smoke(Decor):

    def fly(self):
        self.y -= 1


class Steps(Decor):

    def draw_object(self, obj_x, obj_y):
        try:
            step_surf = pygame.Surface((self.width, self.height))
            step_surf.fill((0, 0, 0))
            step_surf.set_alpha(120)
            display.blit(step_surf, (obj_x, obj_y))
            self.get_smaller()
        except pygame.error:
            decors_list.remove(self)

    def get_smaller(self):
        if not self.life_time % 10:
            self.x += 1
            self.y += 1
            self.width -= 2
            self.height -= 2


class Particles:

    def __init__(self, p_x, p_y, p_direction, p_life_time):
        self.x = p_x
        self.y = p_y
        self.direction = p_direction
        self.life_time = p_life_time

    def fly(self):

        if 'up' in self.direction:
            self.y -= 1

        elif 'down' in self.direction:
            self.y += 2

        if 'left' in self.direction:
            self.x -= 1

        elif 'right' in self.direction:
            self.x += 1

    def draw_object(self, obj_x, obj_y):
        pass


class Flashes(Particles):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.polygon(display, (208, 206, 195), ((obj_x, obj_y), (obj_x + 5, obj_y + 7), (obj_x - 5, obj_y + 7)))


class Powder(Particles):

    def draw_object(self, obj_x, obj_y):
        powder_surf = pygame.Surface((25, 25))
        powder_surf.fill((165, 162, 151))
        powder_surf.set_alpha(200)
        display.blit(powder_surf, (obj_x, obj_y))


class FallingBlood(Particles):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (200, 0, 0), (obj_x, obj_y, 10, 15))

    def fall(self):
        if not self.life_time:
            decors_list.append(Blood(self.x, self.y, random.randint(15, 30), random.randint(15, 30), 600))
            decors_list.remove(self)


class Torch(Decor):

    def work(self):
        if day_tick > 200:
            pygame.draw.circle(display, (90, 100, 95), (self.x + 12, self.y + 60), 150 - (day_tick - 450) // 15)
            pygame.draw.circle(display, (100, 110, 105), (self.x + 12, self.y + 60), 110 - (day_tick - 450) // 15)
            smoke_chance = random.randint(0, 150)
            if not smoke_chance:
                decors_list.append(Smoke(random.randint(self.x - 5, self.x + 30),
                                         random.randint(self.y - 30, self.y - 25), random.randint(5, 15),
                                         random.randint(5, 15), random.randint(120, 180)))

    def draw_object(self):
        pygame.draw.polygon(display, (137, 99, 36), ((self.x + 3, self.y - 25), (self.x + 8, self.y + 45),
                                                     (self.x + 19, self.y + 45), (self.x + 22, self.y - 25)))
        pygame.draw.circle(display, (0, 0, 0), (self.x + 12, self.y - 25), 13)
        if day_tick > 200:
            pygame.draw.ellipse(display, (219, 144, 31),
                                (self.x - 5 + tick % 30 // 9, self.y - 52 + tick % 25 // 8, 35, 45))
            pygame.draw.circle(display, (200, 0, 0), (self.x + 12, self.y - 25), 13)
            pygame.draw.polygon(display, (200, 0, 0), ((self.x + 1, self.y - 25), (self.x + 24, self.y - 25),
                                                       (self.x + 12, self.y - 50)))


'''
Классы декора:конец
'''


class Bed(object):

    def __init__(self, b_x, b_y, active_zone):
        self.x = b_x
        self.y = b_y
        self.active_zone = active_zone


class WorkBenches(object):

    def __init__(self, w_x, w_y, active_zone, work_time, status):

        self.x = w_x
        self.y = w_y
        self.active_zone = active_zone
        self.work_time = work_time
        self.status = status

    def work(self):
        if self.work_time >= 0:
            if sleeping and not self.work_time % 3:
                self.work_time -= 3
            else:
                self.work_time -= 1


class JuiceMaker(WorkBenches):

    def make_juice(self):
        if len([i for i in heretic.inventory if isinstance(i, Berry) or isinstance(i, DroppedBerry)]) >= 4:
            self.work_time = 600
            ber_count = 0
            for j in range(len(heretic.inventory)):
                try:
                    if isinstance(heretic.inventory[j], Berry) or isinstance(heretic.inventory[j], DroppedBerry) \
                            and ber_count <= 4:
                        ber_count += 1
                        heretic.inventory.pop(j)
                except IndexError:
                    if isinstance(heretic.inventory[j], Berry) or isinstance(heretic.inventory[j], DroppedBerry) \
                            and ber_count <= 4:
                        ber_count += 1
                        heretic.inventory.pop(j)
                    print('IndexError has been caught!')

    def produce_juice(self):
        if not self.work_time:
            j_x = 660
            j_y = 220
            home_drops_list.append(Juice(j_x, j_y, [[k for k in range(j_x - 50, j_x + 150)],
                                                    [j for j in range(j_y - 50, j_y + 150)]],
                                         [[k for k in range(j_x, j_x + 50)], [j for j in range(j_y, j_y + 50)]], "Сок",
                                         ['Вкусный освежающий', 'напиток. Делается из 4', "ягод"],
                                         random.randint(20, 25)))


class Furnace(WorkBenches):

    def produce_meat(self):
        self.status = 'off'
        m_x = self.x + 15
        m_y = self.y + 10
        home_drops_list.append(Meat(m_x, m_y, [list(range(m_x - 50, m_x + 150)), list(range(m_y - 50, m_y + 150))],
                                    [list(range(m_x, m_x + 50)), list(range(m_y, m_y + 50))], "Жареное мясо",
                                    ['Вкусный еще теплый', 'кусок жареного мяса'], random.randint(20, 25)))

    def make_meat(self):
        global remark_time, current_string
        if len([i for i in heretic.inventory if isinstance(i, RawMeat)]) and len([i for i in heretic.inventory
                                                                                  if isinstance(i, Log)]):
            self.work_time = 600
            remark_time = 60
            current_string = 'Вскоре все приготовится'
            if self.status == 'off':
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], RawMeat):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], Log):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')

            elif self.status == 'meat':

                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], Log):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')

            elif self.status == 'fuel':
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], RawMeat):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')

            self.status = 'on'

        elif len([i for i in heretic.inventory if isinstance(i, RawMeat)]):

            if self.status == 'off':
                self.status = 'meat'
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], RawMeat):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')

            elif self.status == 'fuel':
                self.status = 'on'
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], RawMeat):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')
                self.work_time = 600
                remark_time = 60
                current_string = 'Вскоре все приготовится'

            else:
                remark_time = 60
                current_string = 'Здесь уже есть мясо'

        elif len([i for i in heretic.inventory if isinstance(i, Log)]):

            if self.status == 'off':
                self.status = 'fuel'
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], Log):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')
                remark_time = 60
                current_string = "Нужно мясо"

            elif self.status == 'meat':
                self.status = 'on'
                for j in range(len(heretic.inventory)):
                    try:
                        if isinstance(heretic.inventory[j], Log):
                            heretic.inventory.pop(j)
                            break
                    except IndexError:
                        print('error with furnace')
                self.work_time = 600
                remark_time = 60
                current_string = 'Скоро все будет готово'

            else:
                remark_time = 60
                current_string = 'Здесь уже есть топливо'

        else:
            if self.status == 'meat':
                remark_time = 60
                current_string = 'Нужно дерево'
            elif self.status == 'fuel':
                remark_time = 60
                current_string = 'Нужно мясо'
            elif self.status == 'off':
                remark_time = 60
                current_string = 'Нужно дерево и мясо'


class GridStone(WorkBenches):

    def produce_tools(self, tool):
        tool_x = random.choice(self.active_zone[0])
        tool_y = random.choice(self.active_zone[1])
        if tool == 'sharpened stone':
            home_drops_list.append(SharpenedStone(tool_x, tool_y, [list(range(tool_x - 50, tool_x + 150)),
                                                                   list(range(tool_y - 50, tool_y + 150))],
                                                  [list(range(tool_x, tool_x + 50)),
                                                   list(range(tool_y, tool_y + 50))], "Заточенный камень",
                                                  ['Заточенный булыжник', "Острый, но хрупкий",
                                                   "Основной материал для", "продвинутого оружия"],
                                                  random.randint(2, 3), 10, 10, 1))
        elif tool == 'pickaxe':
            home_drops_list.append(PickAxe(tool_x, tool_y, [list(range(tool_x - 50, tool_x + 150)),
                                                            list(range(tool_y - 50, tool_y + 150))],
                                           [list(range(tool_x, tool_x + 50)),
                                            list(range(tool_y, tool_y + 50))], "Примитивная кирка",
                                           ['Не очень прочная', "Облегчает добычу камня",
                                            "Низкий урон"],
                                           random.randint(1, 2), 25, 25, 2.5))

    def work(self):
        global current_interface

        current_interface = 'gridstone'
        self.status = 'off'

    def draw_object(self):
        pygame.draw.circle(display, (150, 143, 136), (self.x + 50, self.y + 50), 50)
        pygame.draw.circle(display, (0, 0, 0), (self.x + 50, self.y + 50), 8)
        pygame.draw.rect(display, (130, 82, 43), (self.x - 5, self.y + 60, 110, 15))
        pygame.draw.line(display, (130, 82, 43), (self.x + 35, self.y + 70), (self.x + 5, self.y + 100), 12)
        pygame.draw.line(display, (130, 82, 43), (self.x + 65, self.y + 70), (self.x + 95, self.y + 100), 12)


class Button(object):

    def __init__(self, button_x, button_y, button_length, button_width, descrpition, active_zone):
        self.x = button_x
        self.y = button_y
        self.length = button_length
        self.width = button_width
        self.description = descrpition
        self.active_zone = active_zone


class Weapon(Drop):

    def __init__(self, w_x, w_y, active_zone, visible_zone, w_type, description, strength, durability, max_durability, speed, blood_marks=0):
        self.x = w_x
        self.y = w_y
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.type = w_type
        self.description = description
        self.strength = strength
        self.durability = durability
        self.max_durability = max_durability
        self.speed = speed
        self.blood_marks = blood_marks

    def draw_object(self, obj_x, obj_y):
        pass

    def equip(self):
        heretic.weapon = self
        heretic.strength = self.strength
        heretic.inventory.remove(self)

    def unequip(self):
        heretic.inventory.append(self)
        heretic.strength = 1
        heretic.weapon = 'none'

    def up_down(self):
        if game_tick % 60 == 1:
            self.y += 17
        elif game_tick % 60 == 29:
            self.y -= 17

    def blood_mark(self):
        self.blood_marks -= 1


class Stick(Weapon):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (137, 99, 36), (obj_x, obj_y, 25, 60))
        pygame.draw.ellipse(display, (155, 136, 70), (obj_x, obj_y - 5, 25, 10))
        if inventory_mode:
            pygame.draw.rect(display, (0, 0, 0), (obj_x - 40, obj_y + 45, 90, 25))
            if self.durability >= self.max_durability // 2:
                pygame.draw.rect(display, (0, 200, 0), (obj_x - 39, obj_y + 46,
                                                        int(88 * float(self.durability) / self.max_durability), 23))
            elif self.max_durability // 5 <= self.durability <= self.max_durability // 2:
                pygame.draw.rect(display, (150, 150, 0), (obj_x - 39, obj_y + 46,
                                                          int(88 * float(self.durability) / self.max_durability), 23))
            else:
                pygame.draw.rect(display, (200, 0, 0), (obj_x - 39, obj_y + 46,
                                                        int(88 * float(self.durability) / self.max_durability), 23))


class Sword(Weapon):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (184, 173, 118), (obj_x, obj_y, 20, 45))
        pygame.draw.polygon(display, (184, 173, 118), ((obj_x, obj_y), (obj_x + 10, obj_y - 10), (obj_x + 20, obj_y)))
        pygame.draw.rect(display, (184, 173, 118), (obj_x - 10, obj_y + 40, 40, 6))
        pygame.draw.rect(display, (184, 173, 118), (obj_x + 4, obj_y + 46, 12, 20))


class SharpenedStone(Weapon):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.polygon(display, (0, 0, 0), ((obj_x + 15, obj_y - 1), (obj_x + 30, obj_y + 10),
                                                 (obj_x + 30, obj_y + 30), (obj_x + 15, obj_y + 40),
                                                 (obj_x - 1, obj_y + 30), (obj_x - 1, obj_y + 15)))

        pygame.draw.polygon(display, (181, 184, 177), ((obj_x + 15, obj_y), (obj_x + 29, obj_y + 11),
                                                       (obj_x + 29, obj_y + 29), (obj_x + 15, obj_y + 39),
                                                       (obj_x, obj_y + 31), (obj_x, obj_y + 15)))
        if 0 < self.blood_marks < 300:
            pygame.draw.polygon(display, (200, 0, 0), ((obj_x + 15, obj_y - 1), (obj_x + 30, obj_y + 10),
                                                 (obj_x + 15, obj_y + 8), (obj_x, obj_y + 10)))
        if not self.blood_marks % 150 and self.blood_marks:
            decors_list.append(FallingBlood(obj_x, obj_y, "down", 60))
        if inventory_mode:
            pygame.draw.rect(display, (0, 0, 0), (obj_x - 40, obj_y + 45, 90, 25))
            if self.durability >= self.max_durability // 2:
                pygame.draw.rect(display, (0, 200, 0), (obj_x - 39, obj_y + 46,
                                                        int(88 * float(self.durability) / self.max_durability), 23))
            elif self.max_durability // 5 <= self.durability <= self.max_durability // 2:
                pygame.draw.rect(display, (150, 150, 0), (obj_x - 39, obj_y + 46,
                                                          int(88 * float(self.durability) / self.max_durability), 23))
            else:
                pygame.draw.rect(display, (200, 0, 0), (obj_x - 39, obj_y + 46,
                                                        int(88 * float(self.durability) / self.max_durability), 23))


class PickAxe(Weapon):

    def draw_object(self, obj_x, obj_y):

        pygame.draw.polygon(display, (181, 186, 177), ((obj_x, obj_y + 5), (obj_x - 15, obj_y + 21), (obj_x, obj_y + 14)))
        pygame.draw.polygon(display, (181, 186, 177), ((obj_x + 12, obj_y + 5), (obj_x + 27, obj_y + 21), (obj_x + 12, obj_y + 14)))
        pygame.draw.rect(display, (137, 99, 36), (obj_x, obj_y, 12, 50))
        if inventory_mode:
            pygame.draw.rect(display, (0, 0, 0), (obj_x - 40, obj_y + 45, 90, 25))
            if self.durability >= self.max_durability // 2:
                pygame.draw.rect(display, (0, 200, 0), (obj_x - 39, obj_y + 46,
                                                        int(88 * float(self.durability) / self.max_durability), 23))
            elif self.max_durability // 5 <= self.durability <= self.max_durability // 2:
                pygame.draw.rect(display, (150, 150, 0), (obj_x - 39, obj_y + 46,
                                                          int(88 * float(self.durability) / self.max_durability), 23))
            else:
                pygame.draw.rect(display, (200, 0, 0), (obj_x - 39, obj_y + 46,
                                                        int(88 * float(self.durability) / self.max_durability), 23))

    def mine(self, rock):

        heretic.health -= 2
        self.durability -= 1
        if not self.durability:
            heretic.weapon = 'none'
        for i in range(random.randint(3, 5)):
            leftside_decors_list.append(
                Flashes(random.choice(rock.visible_zone[0]), random.choice(rock.visible_zone[1]),
                        random.choice(["right", "left"]) + " " + "up", random.randint(35, 40)))


def close():
    global current_interface

    current_interface = 'none'


class Storage(object):

    def __init__(self, s_x, s_y, s_length, s_width, storage, max_capability, active_zone, visible_zone):
        self.x = s_x
        self.y = s_y
        self.length = s_length
        self.width = s_width
        self.storage = storage
        self.max_capability = max_capability
        self.active_zone = active_zone
        self.visible_zone = visible_zone

    def open(self):
        global current_interface

        current_interface = type(self)
        print(current_interface)

    def take_from_storage(self, index):
        if len(heretic.inventory) < 20 and len(self.storage) > index:
            heretic.inventory.append(self.storage[index])
            self.storage.pop(index)


class Chest(Storage):

    def open(self):
        global current_interface

        current_interface = 'Chest'
        print(current_interface)

    def draw_object(self):
        pygame.draw.rect(display, (142, 94, 57), (self.x + 5, self.y + 5, self.length - 10, self.width - 10))
        if self.length > self.width:
            pygame.draw.rect(display, (181, 112, 48), (self.x + self.length // 2 - 15, self.y + self.width // 2,
                                                       30, 30))
            pygame.draw.circle(display, (0, 0, 0), (self.x + self.length // 2, self.y + self.width // 2 + 10), 7)
            pygame.draw.line(display, (181, 112, 48),
                             (self.x, self.y + self.width // 2 - 10),
                             (self.x + self.length, self.y + self.width // 2 - 10), 10)
            pygame.draw.line(display, (181, 112, 48),
                             (self.x + self.length // 3, self.y + self.width // 2 - 5),
                             (self.x + self.length // 3, self.y), 15)
            pygame.draw.line(display, (181, 112, 48),
                             (self.x + self.length // 3 * 2, self.y + self.width // 2 - 5),
                             (self.x + self.length // 3 * 2, self.y), 15)
            pygame.draw.polygon(display, (0, 0, 0), ((self.x + self.length // 2, self.y + self.width // 2 + 10),
                                                     (self.x + self.length // 2 - 7, self.y + self.width // 2 + 25),
                                                     (self.x + self.length // 2 + 7, self.y + self.width // 2 + 25)))
        else:
            pygame.draw.rect(display, (181, 112, 48), (self.x + self.length // 2, self.y + self.width // 2 - 15,
                                                       30, 30))


class Sign(object):

    def __init__(self, sign_x, sign_y, sign_direction, sign_description, active_zone):
        self.x = sign_x
        self.y = sign_y
        self.direction = sign_direction
        self.description = sign_description
        self.active_zone = active_zone

    def read(self):
        global current_interface
        current_interface = self
        sign_surf.fill((128, 128, 128))

    def draw_object(self):
        if self.direction == 'left':
            pygame.draw.rect(display, (137, 99, 36), (self.x, self.y, 30, 80))
            pygame.draw.rect(display, (137, 99, 36), (self.x - 40, self.y - 20, 90, 60))
            pygame.draw.rect(display, (0, 0, 0), (self.x - 10, self.y - 5, 50, 30))
            pygame.draw.polygon(display, (0, 0, 0),
                                ((self.x - 30, self.y + 10), (self.x - 10, self.y - 10), (self.x - 10, self.y + 30)))
        elif self.direction == 'right':
            pygame.draw.rect(display, (137, 99, 36), (self.x, self.y, 30, 80))
            pygame.draw.rect(display, (137, 99, 36), (self.x - 20, self.y - 20, 90, 60))
            pygame.draw.rect(display, (0, 0, 0), (self.x - 10, self.y - 5, 50, 30))
            pygame.draw.polygon(display, (0, 0, 0),
                                ((self.x + 60, self.y + 10), (self.x + 40, self.y - 10), (self.x + 40, self.y + 30)))


remark_time = 0
current_string = ''
current_interface = 'none'

volume = 80
pygame.mixer.music.load(r'C:\Users\User\PycharmProjects\ClearSheet\Home track.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)
chopping_sound_1 = pygame.mixer.Sound(r'C:\Users\User\PycharmProjects\ClearSheet\chopping sound 1.wav')

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

x_home = random.randint(100, 1000)
y_home = random.randint(100, 600)
h_length = random.choice([i for i in range(200, 300) if not i % 10])
h_width = random.choice([i for i in range(180, 200) if not i % 10])
home = House(x_home, y_home, '', h_length, h_width, [[j for j in range(x_home + 75, x_home + 125)],
                                                     [k for k in range(y_home + 50, y_home + h_width + 10)]],
             [[j for j in range(x_home, x_home + h_length)], [k for k in range(y_home, y_home + h_width + 10)]],
             [[str(j) + ' ' + str(k) for j in range(x_home, x_home + h_length, 10) for k in range(y_home,
                                                                                                  y_home + h_width,
                                                                                                  10)]], [])

bed = Bed(310, 160, [[i for i in range(300, 400)], [j for j in range(160, 270)]])
juicemaker = JuiceMaker(550, 160, [[i for i in range(500, 650)], [j for j in range(160, 240)]], -1, 'none')
furnace = Furnace(700, 160, [[i for i in range(700, 800)], [j for j in range(160, 260)]], -1, 'off')
torch = Torch(1200, 350, 0, 0, -1)
chest = Chest(850, 160, 120, 100, [], 20, [list(range(840, 980)), list(range(150, 260))],
              [list(range(850, 970)), list(range(160, 260))])
gridstone = GridStone(980, 330, [list(range(940, 1080)), list(range(300, 420))], -1, 'off')

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
sleeping = False
tp_to_left_side = False
tp_to_home = False
go_to_bed = False
b_owner = None
d_owner = None
t_owner = None
m_owner = None
rock_owner = None
game_tick = 0
day_tick = 0
menu_tick = 0
tick = 0
day_return = False
drop_appear_tick = 500
at_home = False
z_z_Z = ''
main_mob = Mob(0, 0, 'left', [0, 2], [3, 3], 0, 0, True, 5, 0, 0, 0, '', 0, 0, 0, 'none', 'none')
 
heretic.x = x_home + 75
heretic.y = y_home + 50
current_location = 'menu'
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
mobs_list = []
for i in range(random.randint(5, 7)):
    x = random.randint(-100, 1500)
    y = random.randint(-100, 900)
    mobs_list.append(PeacefulMobs(x, y, random.choice(mobs_directions), [[j for j in range(x - 100, x + 150)],
                                                                         [k for k in range(y - 100, y + 100)]],
                                  [[j for j in range(x, x + 90)], [k for k in range(y, y + 60)]],
                                  10, 20, True, [RawMeat(0, 0, [[0], [0]], [[0], [0]],
                                                         "Сырое мясо",
                                                         ['Большой кусок сырого', "мяса. Следует пожарить."],
                                                         random.randint(20, 25))], 2, 0, 0, '', 'none', 0, 0, 'home',
                                  'none'))

"""
Создание булыжников
"""
for i in range(random.randint(5, 8)):
    x = random.randint(100, 1300)
    y = random.randint(100, 800)
    leftside_stones_list.append(Rock(x, y, 10, [list(range(x - 50, x + 150)), list(range(y - 50, y + 150))],
                                     [list(range(x - 30, x + 100)), list(range(y, y + 100))], 900))

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
                        elif recipy == 3:
                            gridstone.status = 'pickaxe'

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
                        chest.open()
                    elif at_home and heretic.x in gridstone.active_zone[0] and heretic.y in gridstone.active_zone[1] and \
                            current_interface == 'none':
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

        if any([keys[pygame.K_a], keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_d]]):
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
                    pygame.draw.rect(display, (0, 0, 0), (i, j, 130, 130))
                    pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))

            for i in range(10, 781, 110):
                pygame.draw.rect(display, (0, 0, 0), (10, i, 300, 100))
                pygame.draw.rect(display, (184, 173, 118), (15, i + 5, 290, 90))
                if i // 110 < len(gridstone_recipes):
                    display.blit(active_font.render(gridstone_recipes[i // 110], True, (0, 0, 0)), (20, i + 30))
            if gridstone.status != 'off':
                pygame.draw.rect(display, (0, 0, 0), (720, 700, 250, 100))
                pygame.draw.rect(display, (200, 0, 0), (725, 705, 240, 90))
                display.blit(active_font.render("Крафт", True, (0, 0, 0)), (730, 720))

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
        elif at_home and heretic.x in furnace.active_zone[0] and heretic.y in furnace.active_zone[1]:
            display.blit(active_font.render('Гриль', True, (200, 0, 0)), (heretic.x - 20, heretic.y - 75))
        elif at_home and heretic.x in chest.active_zone[0] and heretic.y in chest.active_zone[1]:
            display.blit(active_font.render('Сундук', True, (200, 0, 0)), (heretic.x - 35, heretic.y - 75))
        elif at_home and heretic.x in gridstone.active_zone[0] and heretic.y in gridstone.active_zone[1]:
            display.blit(active_font.render('Точило', True, (200, 0, 0)), (heretic.x - 35, heretic.y - 75))
        elif chopping_active and not at_home and len(trees_list) > 0:
            display.blit(chopping, (heretic.x - 40, heretic.y - 75))
        elif drop_active and inactive_time < 0:
            display.blit(pick_up, (heretic.x - 60, heretic.y - 75))
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
            if isinstance(blood, Blood) and blood_setting:
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

                    mob.peaceful_exist()
                elif isinstance(mob, AggressiveMobs):
                    mob.draw_object()
                    if len([j for j in mobs_list if isinstance(j, PeacefulMobs)]) or heretic.health > 0:
                        mob.agressive_exist()
                    else:
                        mob.peaceful_exist()
                mob.bleed()

            for fog in decors_list:
                if isinstance(fog, FallingBlood):
                    fog.fly()
                    fog.draw_object(fog.x, fog.y)
                    fog.life_time -= 1
                    fog.fall()
                if isinstance(fog, Fog) and fog.y < heretic.y - 40:
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

        if not inventory_mode:
            for mob in leftside_mobs_list:
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

                    mob.peaceful_exist()
                elif isinstance(mob, AggressiveMobs):
                    mob.draw_object()
                    if len([j for j in mobs_list if isinstance(j, PeacefulMobs)]) or heretic.health > 0:
                        mob.agressive_exist()
                    else:
                        mob.peaceful_exist()
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
        for mob in range(len(mobs_list)):
            if isinstance(mobs_list[mob], AggressiveMobs) and mobs_list[mob].x < 50:
                mobs_list[mob].x = 1300
                mobs_list[mob].location = 'leftside'
                leftside_mobs_list.append(mobs_list.pop(mob))
    except (ValueError, IndexError) as e:
        print(e)

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
                    drops_list.append(i)
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
    if current_location != 'home':
        for i in mobs_list:
            if isinstance(i, PeacefulMobs):
                i.peaceful_exist()
            elif isinstance(i, AggressiveMobs):
                if len([j for j in mobs_list if isinstance(j, PeacefulMobs)]) or heretic.health > 0:
                    i.agressive_exist()
                else:
                    i.peaceful_exist()
    produce_new_peaceful_mob()
    produce_new_aggressive_mob()
    heretic.be_poisoned()
    if heretic.attack_time:
        heretic.attack_time -= 1
    if not volume:
        if current_location == 'leftside':
            pygame.mixer.music.load(r"C:\Users\User\PycharmProjects\ClearSheet\Leftside Track.mp3")
            pygame.mixer.music.play(-1)
        elif current_location == 'home':
            pygame.mixer.music.load(r'C:\Users\User\PycharmProjects\ClearSheet\Home track.mp3')
            pygame.mixer.music.play(-1)
        volume = 100
