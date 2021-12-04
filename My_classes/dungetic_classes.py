import pygame
import random

pygame.init()
pygame.mixer.init()

display = pygame.display.set_mode((0, 0))
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
goblins_spawn = True

mobs_directions = ['left', 'right', 'up', 'down']
mobs_list = []
bushes_list = []
trails_list = []
drops_list = []
trees_list = []
leftside_drops_list = []
crate_image = pygame.image.load(r"C:\Users\User\PycharmProjects\ClearSheet\crate.png").convert_alpha()
crate_image = pygame.transform.scale(crate_image, (crate_image.get_width() * 2, crate_image.get_height() * 2))
seeds_image = pygame.image.load("seeds.png").convert_alpha()
crates_list = []
regrowing_list = []
bullets_list = []

home_drops_list = []
decors_list = []
leftside_decors_list = []
leftside_stones_list = []
leftside_mobs_list = []
farmlands_list = []
menu_decors_list = []

game = True
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


def print_on_screen(s):
    if remark_time:
        if isinstance(s, list):
            display.blit(active_font.render(s[remark_time // 60], True, (0, 0, 0)),
                         (heretic.x - 8 * len(s[remark_time // 60]), heretic.y - 75))
        else:
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

    def __init__(self, h_x, h_y, health, direction, inventory, light_zone, strength, speed, weapon, poison_time,
                 is_tired,
                 visible_zone, active_zone, location, attack_time=0, half_attack_time=0, backpack=None):
        self.x = h_x
        self.y = h_y
        self.health = health
        self.direction = direction
        self.inventory = inventory
        self.light_zone = light_zone
        self.strength = strength
        self.speed = speed
        self.weapon = weapon
        self.poison_time = poison_time
        self.is_tired = is_tired
        self.visible_zone = visible_zone
        self.active_zone = active_zone
        self.location = location
        self.attack_time = attack_time
        self.half_attack_time = half_attack_time
        self.backpack = backpack

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
            for i in range(heretic.strength + 1):
                blood_y = random.choice(attacked_mob.visible_zone[1])
                (decors_list if current_location == 'home' else leftside_decors_list).append(
                    FallingBlood(random.choice(attacked_mob.visible_zone[0]),
                                 blood_y, "down", (100 - (blood_y - attacked_mob.y)) // 2,
                                 heretic.location))

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
        attacked_mob.bleeding = heretic.strength * 250
        if isinstance(attacked_mob, AggressiveMobs):
            attacked_mob.target = heretic
        if heretic.weapon != 'none':
            heretic.weapon.durability -= 1
            if not heretic.weapon.durability:
                heretic.weapon = 'none'
                heretic.strength = 1

    def shoot(self, target):
        if isinstance(self.weapon, LongRange):
            self.weapon.shoot(target, heretic)
            heretic.health -= self.weapon.strength
            self.weapon.durability -= 1
            if not self.weapon.durability:
                heretic.weapon = 'none'

    def draw_object(self):
        if heretic.backpack and heretic.direction == 'right':
            heretic.backpack.draw_on_heretic(heretic.x + 25, heretic.y + 45)
        elif heretic.backpack and heretic.direction == 'up':
            heretic.backpack.draw_on_heretic(heretic.x - 5, heretic.y + 45)

        if heretic.weapon != 'none' and heretic.direction == 'right':
            heretic.weapon.draw_object(heretic.x + 65 - ((heretic.half_attack_time -
                                                          heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0),
                                       heretic.y + 30)
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
            if self.backpack:
                self.backpack.draw_on_heretic(heretic.x + 40, heretic.y + 45)
            if heretic.weapon != 'none':
                heretic.weapon.draw_object(heretic.x + 65, heretic.y + 30 - ((heretic.half_attack_time -
                                                                              heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0))

        elif heretic.direction == 'left':
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 8, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (heretic.x + 38, heretic.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (heretic.x + 13, heretic.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (heretic.x + 43, heretic.y + 17, 4, 4))
            if heretic.backpack:
                heretic.backpack.draw_on_heretic(heretic.x + 20, heretic.y + 45)
            if heretic.weapon != 'none':
                heretic.weapon.draw_object(heretic.x + 45 + ((heretic.half_attack_time -
                                                              heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0),
                                           heretic.y + 30)

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
            m_type = random.choice(['melee', 'archer', 'melee'])
            loot = []
            if m_type == 'melee':
                weapon = random.choice(['none', 'none', SharpenedStone(0, 0, [[0, 0], [0, 0]], [[0, 0], [0, 0]],
                                                                   "Заточенный камень",
                                                                   ['Заточенный булыжник',
                                                                    "Острый, но хрупкий",
                                                                    "Основной материал для",
                                                                    "продвинутого оружия"],
                                                                   random.randint(2, 3), 10, 10, 1),
                                    Stick(0, 0, [[0, 0], [0, 0]], [[0, 0], [0, 0]],
                                          "Палка", ['Заточенный булыжник',
                                                    "Острый, но хрупкий",
                                                    "Основной материал для",
                                                    "продвинутого оружия"], random.randint(2, 3), 10, 10, 2)])
                strength = 3

                if isinstance(weapon, Weapon):
                    strength += weapon.strength
                    loot.append(weapon)
            elif m_type == 'archer':
                weapon = Bow(0, 0, [[0, 0], [0, 0]], [[0, 0], [0, 0]], 'Лук',
                             ['Короткий лук', "Не очень мощный,", "но позволяет поражать", "цель на расстоянии"],
                                       random.randint(4, 5), 15, 15, 2, max_reload=120)
                loot.append(weapon)


            mobs_list.append(AggressiveMobs(mob_x, mob_y, random.choice(mobs_directions),
                                            [[j for j in range(mob_x - 100, mob_x + 175)],
                                             [k for k in range(mob_y - 100, mob_y + 120)]],
                                            [[j for j in range(mob_x, mob_x + 75)],
                                             [k for k in range(mob_y, mob_y + 100)]],
                                            12, 20, True, loot, 2, 0, 0, '', target, strength, 150, 'home',
                                            weapon, type=m_type))


class Mob(object):

    def __init__(self, m_x, m_y, direction, active_zone, visible_zone, health, delay, stop, loot, speed, bleeding,
                 mob_remark_time, mob_remark, target, strength, attack_time, location, weapon, type=None):

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
        self.type = type

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
            (decors_list if self.location == 'home' else leftside_decors_list).append(FallingBlood(random.choice(self.visible_zone[0]), random.choice(self.visible_zone[1]),
                                            "down", 60, self.location))
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

    def draw_object(self, obj_x, obj_y, day_tick):
        if obj_x in heretic.light_zone[0] and obj_y in heretic.light_zone[1]:
            mob_head_colour = (255, 228, 196)
        else:
            mob_head_colour = (255 - day_tick // 10, 228 - day_tick // 10, 196 - day_tick // 10)
        if self.direction == 'up':
            pygame.draw.rect(display, mob_head_colour, (obj_x + 15, obj_y - 10, 30, 30))
        if self.direction == 'left' or self.direction == 'right':
            if obj_x in heretic.light_zone[0] and obj_y in heretic.light_zone[1]:
                mob_colour = (200, 200, 200)
            else:
                mob_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
            pygame.draw.rect(display, mob_colour, (obj_x, obj_y, 90, 60))
            if heretic.x in self.active_zone[0] and heretic.y in self.active_zone[1]:
                pygame.draw.rect(display, (0, 0, 0), (obj_x + 5, obj_y - 30, 80, 20))
                pygame.draw.rect(display, (200, 0, 0),
                                 (obj_x + 7, obj_y - 28, int(76.0 * self.health / 8.0), 16))
        else:
            if obj_x in heretic.light_zone[0] and obj_y in heretic.light_zone[1]:
                mob_colour = (200, 200, 200)
            else:
                mob_colour = (200 - day_tick // 10, 200 - day_tick // 10, 200 - day_tick // 10)
            pygame.draw.rect(display, mob_colour, (obj_x, obj_y, 60, 90))
            if heretic.x in self.active_zone[0] and heretic.y in self.active_zone[1]:
                pygame.draw.rect(display, (0, 0, 0), (obj_x + 5, obj_y - 30, 50, 20))
                pygame.draw.rect(display, (200, 0, 0),
                                 (obj_x + 7, obj_y - 28, int(46.0 * self.health / 8.0), 16))

        if self.direction == 'down':
            pygame.draw.rect(display, mob_head_colour, (obj_x + 15, obj_y + 50, 30, 30))
            for i in range(22, 33, 10):
                pygame.draw.rect(display, (0, 0, 0), (obj_x + i, obj_y + 60, 5, 5))
        elif self.direction == 'left':
            pygame.draw.rect(display, mob_head_colour, (obj_x + 10, obj_y + 15, 30, 30))
            for i in range(17, 28, 10):
                pygame.draw.rect(display, (0, 0, 0), (obj_x + i, obj_y + 25, 5, 5))
        elif self.direction == 'right':
            pygame.draw.rect(display, mob_head_colour, (obj_x + 50, obj_y + 15, 30, 30))
            for i in range(57, 68, 10):
                pygame.draw.rect(display, (0, 0, 0), (obj_x + i, obj_y + 25, 5, 5))

    @staticmethod
    def print_type(self):
        print(type(self))


class AggressiveMobs(Mob):

    def hit(self):
        self.attack_time = 100
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
                self.loot.remove(self.weapon)
                self.weapon = 'none'
                self.strength = 3

        for i in range(self.strength // 2):
            blood_y = random.choice(self.target.visible_zone[1])
            if self.location == 'home':
                decors_list.append(FallingBlood(random.choice(self.target.visible_zone[0]),
                                                blood_y, "down", (100 - (blood_y - self.target.y)) // 2))
            elif self.location == 'leftside':
                leftside_decors_list.append(FallingBlood(random.choice(self.target.visible_zone[0]),
                                                         blood_y, "down", (100 - (blood_y - self.target.y)) // 2, 'leftside'))

    def melee_aggressive_exist(self):

        if self.location == 'leftside' and self.target.location == 'home':
            self.walk_right()

        elif self.location == 'home' and self.target.location == 'leftside':
            self.walk_left()
        else:

            if self.x > self.target.x + len(self.target.visible_zone[0]) // 2:
                self.walk_left()

            elif self.x < self.target.x + len(self.target.visible_zone[0]) // 2:
                self.walk_right()

        if self.y < self.target.y - len(self.visible_zone[1]) // 2:
            self.walk_down()

        elif self.y > self.target.y + len(self.target.visible_zone[1]) // 2:
            self.walk_up()
        if self.x in self.target.active_zone[0] and self.y in self.target.active_zone[1] and not self.attack_time:
            if (self.target == heretic and heretic.location == self.location and not at_home) or self.target != heretic:
                self.hit()
        if self.attack_time:
            self.attack_time -= 1

        if ((self.target != heretic and self.target not in mobs_list) or
                (self.target == heretic and not heretic.health)):
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

        if tick >= 1800:
            if not game_tick % 10:
                self.health -= 1

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
            mobs_list.remove(self)

        self.collect_food()

    def archer_aggressive_exist(self):
        if self.location == 'leftside' and self.target.location == 'home':
            self.walk_right()

        elif self.location == 'home' and self.target.location == 'leftside':
            self.walk_left()
        else:

            if self.x - self.target.x + len(self.target.visible_zone[0]) // 2 > 200 or 0 < self.x - self.target.x + len(self.target.visible_zone[0]) // 2 <= 100:
                self.walk_left()

            elif self.x - self.target.x + len(self.target.visible_zone[0]) // 2 < -200 or -100 < self.x - self.target.x + len(self.target.visible_zone[0]) // 2 < 0:
                self.walk_right()

        if self.y - self.target.y - len(self.visible_zone[1]) // 2 < -150:
            self.walk_down()

        elif self.y - self.target.y + len(self.target.visible_zone[1]) // 2 > 150:
            self.walk_up()
        if isinstance(self.weapon, LongRange) and self.weapon.reload < self.weapon.max_reload:
            self.weapon.reload += 1

        if ((self.target != heretic and self.target not in mobs_list) or
                (self.target == heretic and not heretic.health)):
            heretic_chance = random.randint(0, 5)
            if not heretic_chance:
                self.target = heretic
            elif heretic_chance and len([i for i in mobs_list if isinstance(i, PeacefulMobs)]):
                self.target = random.choice([j for j in mobs_list if isinstance(j, PeacefulMobs)])

        if self.weapon.reload:
            self.speed = 3
        else:
            self.speed = 5
        if self.weapon.reload == self.weapon.max_reload:
            self.weapon.shoot(self.target, self)
            if not self.weapon.durability:
                self.loot.remove(self.weapon)
                self.weapon = 'none'
                self.type = 'melee'
        self.collect_food()


    def draw_object(self, obj_x, obj_y, day_tick):
        if self.weapon != 'none' and self.direction == 'right':
            self.weapon.draw_object(obj_x + 65, obj_y + 30)
        elif self.weapon != 'none' and self.direction == 'up':
            self.weapon.draw_object(obj_x - 15, obj_y + 30)
        pygame.draw.rect(display, (0, 120, 0), (obj_x, obj_y, 75, 100))
        if (obj_x in heretic.light_zone[0] or obj_x + 75 in heretic.light_zone[0]) and \
                (obj_y in heretic.light_zone[1] or obj_y + 75 in heretic.light_zone[1]):
            belt_color = (207, 140, 79)
        else:
            belt_color = (207 - day_tick // 15, 140 - day_tick // 15, 79 - day_tick // 15)
        pygame.draw.rect(display, belt_color, (obj_x - 1, obj_y + 60, 77, 15))
        if self.direction == 'down':
            for j in range(obj_x + 10, obj_x + 41, 30):
                pygame.draw.rect(display, (0, 0, 0), (j, obj_y + 10, 20, 20))
                pygame.draw.rect(display, (150, 0, 0), (j + 7, obj_y + 16, 5, 5))
            pygame.draw.rect(display, (182, 45, 7), (obj_x + 15, obj_y + 40, 40, 10))
            if self.weapon != 'none':
                self.weapon.draw_object(obj_x + 65, obj_y + 30)

        elif self.direction == 'left':
            for j in range(obj_x + 8, obj_x + 39, 30):
                pygame.draw.rect(display, (0, 0, 0), (j, obj_y + 10, 20, 20))
                pygame.draw.rect(display, (150, 0, 0), (j + 3, obj_y + 16, 5, 5))
            pygame.draw.rect(display, (182, 45, 7), (obj_x + 10, obj_y + 40, 40, 10))
            if self.weapon != 'none':
                self.weapon.draw_object(obj_x + 45, obj_y + 30)
        elif self.direction == 'right':
            for j in range(obj_x + 20, obj_x + 51, 30):
                pygame.draw.rect(display, (0, 0, 0), (j, obj_y + 10, 20, 20))
                pygame.draw.rect(display, (150, 0, 0), (j + 12, obj_y + 16, 5, 5))
            pygame.draw.rect(display, (182, 45, 7), (obj_x + 25, obj_y + 40, 40, 10))

        if heretic.x in self.active_zone[0] and heretic.y in self.active_zone[1]:
            pygame.draw.rect(display, (0, 0, 0), (obj_x + 5, obj_y - 30, 50, 20))
            pygame.draw.rect(display, (200, 0, 0),
                             (obj_x + 7, obj_y - 28, int(46.0 * self.health / 12.0), 16))

    def collect_food(self):
        for food in [drop for drop in drops_list if isinstance(drop, Eatable)]:
            if (self.x in food.active_zone[0] or self.x + 75 in food.active_zone[0]) \
                    and (self.y in food.active_zone[1] or self.y + 100 in food.active_zone[1]):
                self.loot.append(food)
                drops_list.remove(food)


heretic = Heretic(random.randint(100, 1300), random.randint(100, 800), 100, 'down', [], [[1], [2]], 1, 4, 'none', 0,
                  False,
                  [[0], [0]], [[0], [0]], 'home')


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


class FarmLands:

    def __init__(self, f_x, f_y, active_zone, visible_zone, crop=None):
        self.x = f_x
        self.y = f_y
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.crop = crop

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (88, 70, 36), (obj_x, obj_y, 60, 60))
        for i in range(obj_y + 15, obj_y + 50, 10):
            pygame.draw.line(display, (68, 50, 20), (obj_x + 5, i), (obj_x + 55, i), 6)
            if isinstance(self.crop, Seeds):
                if self.crop.max_growing_time - self.crop.growing_time <= 150:
                    for j in range(obj_x + 5, obj_x + 55, 11):
                        pygame.draw.rect(display, (181, 168, 135), (j, i - 5, 5, 5))
                else:
                    for j in range(obj_x + 5, obj_x + 55, 11):
                        pygame.draw.rect(display, (60, 159, 45),
                                         (j, i - 5 - (self.crop.max_growing_time - self.crop.growing_time) // 150,
                                          2 + (self.crop.max_growing_time - self.crop.growing_time) // 350,
                                          5 + (self.crop.max_growing_time - self.crop.growing_time) // 110))
            elif self.crop == 'Морковь':
                for j in range(obj_x + 5, obj_x + 55, 20):
                    pygame.draw.ellipse(display, (236, 127, 34), (j, i - 20, 12, 20))
                    pygame.draw.polygon(display, (0, 80, 0), ((j + 3, i - 25), (j + 6, i - 20), (j + 9, i - 25)))


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

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (137, 99, 36), (obj_x, obj_y - 150, 50, 200))
        pygame.draw.circle(display, (40, 122, 36), (obj_x + 25, obj_y - 130), 75)


class Stump(Tree):

    def regrowth(self):
        trees_list.append(Tree(self.x, self.y, random.randint(3, 5), [[j for j in range(self.x - 120, self.x + 70)],
                                                                      [k for k in range(self.y - 70, self.y + 100)]]))

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (137, 99, 36), (obj_x, obj_y, 50, 50))
        pygame.draw.ellipse(display, (155, 136, 70), (obj_x, obj_y - 10, 50, 20))


class Sapling(Tree):

    def regrowth(self):
        trees_list.append(
            Tree(self.x, self.y + 200, random.randint(8, 13), [[j for j in range(self.x - 120, self.x + 270)],
                                                               [k for k in range(self.y - 70, self.y + 300)]]))

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (137, 88, 36), (obj_x - self.health // 120, obj_y - self.health // 9, 20 +
                                                  self.health // 60, 60 + self.health // 130))


class Regrowing:

    def revive(self):
        pass


class HighGrass:

    def __init__(self, g_x, g_y, active_zone, visible_zone, status, life_time, wind, wind_return=False,
                 location='home'):
        self.x = g_x
        self.y = g_y
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.status = status
        self.regrowing_time = life_time
        self.wind = wind
        self.wind_return = wind_return
        self.location = location

    def draw_object(self, obj_x, obj_y):
        if self.status == 'uncut':
            for i in range(obj_x, obj_x + 60, 10):
                pygame.draw.polygon(display, (0, 0, 0), ((i - 1 + self.wind, obj_y + self.wind // 3),
                                                         (i + 5 + self.wind, obj_y),
                                                         (i + 5 + (3 - (i - obj_x) // 10 + 1) * 3, obj_y + 60),
                                                         (i + (3 - (i - obj_x) // 10 + 1) * 3, obj_y + 60)), 1)
                pygame.draw.polygon(display, (96, 185, 66), ((i + self.wind, obj_y + 1 + self.wind // 3),
                                                             (i + 4 + self.wind, obj_y + 1),
                                                             (i + 3 + (3 - (i - obj_x) // 10 + 1) * 3, obj_y + 60),
                                                             (i + 1 + (3 - (i - obj_x) // 10 + 1) * 3, obj_y + 60)))
                pygame.draw.polygon(display, (0, 0, 0), ((i + self.wind, obj_y), (i + 3 + self.wind, obj_y - 4),
                                                         (i + 6 + self.wind, obj_y)))
                pygame.draw.polygon(display, (96, 185, 66), (
                    (i + self.wind, obj_y + 1), (i + 3 + self.wind, obj_y - 3), (i + 4 + self.wind, obj_y)))

        elif self.status == 'cut':
            for i in range(obj_x, obj_x + 60, 10):
                pygame.draw.rect(display, (0, 0, 0), (
                    i - 1, obj_y + 40 - (900 - self.regrowing_time) // 22, 6, 20 + (900 - self.regrowing_time) // 22),
                                 1)
                pygame.draw.rect(display, (96, 185, 66), (
                    i, obj_y + 41 - (900 - self.regrowing_time) // 22, 4, 19 + (900 - self.regrowing_time) // 22))

        self.flutter()

    def flutter(self):

        if not random.randint(0, 800):
            self.wind = 1
        if self.wind and not game_tick % 5:
            if not self.wind_return:
                self.wind += 1
                if self.wind == 15:
                    self.wind_return = True
            else:
                self.wind -= 1
                if not self.wind:
                    self.wind_return = False

    def be_cut(self):

        self.status = 'cut'
        self.regrowing_time = 900
        drop_x, drop_y = random.choice(self.active_zone[0]), random.choice(self.active_zone[1])
        drops_list.append(GrassBundle(drop_x, drop_y,
                                      [list(range(drop_x - 50, drop_x + 150)), list(range(drop_y - 50, drop_y + 150))],
                                      [list(range(drop_x, drop_x + 50)), list(range(drop_y, drop_y + 50))],
                                      'Пучок травы', ['Небольшая связка',
                                                      "травы. Можно использовать",
                                                      "для создания чего-либо"]))
        for i in range(random.randint(1, 3)):
            drop_x, drop_y = random.choice(self.active_zone[0]), random.choice(self.active_zone[1])
            grow_time = random.randint(900, 1350)
            drops_list.append(Seeds(drop_x, drop_y,
                                    [list(range(drop_x - 50, drop_x + 150)),
                                     list(range(drop_y - 50, drop_y + 150))],
                                    [list(range(drop_x, drop_x + 50)), list(range(drop_y, drop_y + 50))],
                                    'Семена', ['В них теплится',
                                               "будущая жизнь."], random.choice(['Морковь', "Капуста", "Свекла"]),
                                    grow_time, grow_time, energy=5))


class Rock:

    def __init__(self, r_x, r_y, health, active_zone, visible_zone, regeneration_time, type):
        self.x = r_x
        self.y = r_y
        self.health = health
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.regeneration_time = regeneration_time
        self.type = type

    def be_broken(self):
        if heretic.x < self.x - 10:
            heretic.direction = "right"
        elif heretic.x > self.x + 80:
            heretic.direction = 'left'
        self.health -= 1
        heretic.attack_time = 60
        if self.type == 'general':
            stone_chance = random.randint(1, 4)
            if stone_chance == 1 and self.health:
                stone_x = random.choice(self.active_zone[0])
                stone_y = random.choice(self.active_zone[1])
                leftside_drops_list.append(Stone(stone_x, stone_y, [list(range(stone_x - 50, stone_x + 100)),
                                                                    list(range(stone_y - 50, stone_y))],
                                                 [list(range(stone_x, stone_x + 51)),
                                                  list(range(stone_y, stone_y + 51))],
                                                 "Камешек", ["Небольшой камень.", "Можно обработать"], 0))
        elif self.type == 'coal':
            stone_chance = random.randint(1, 6)
            if stone_chance == 1 and self.health:
                stone_x = random.choice(self.active_zone[0])
                stone_y = random.choice(self.active_zone[1])
                leftside_drops_list.append(Stone(stone_x, stone_y, [list(range(stone_x - 50, stone_x + 100)),
                                                                    list(range(stone_y - 50, stone_y))],
                                                 [list(range(stone_x, stone_x + 51)),
                                                  list(range(stone_y, stone_y + 51))],
                                                 "Камешек", ["Небольшой камень.", "Можно обработать"], 0))
            elif stone_chance == 2 and self.health:
                stone_x = random.choice(self.active_zone[0])
                stone_y = random.choice(self.active_zone[1])
                leftside_drops_list.append(Coal(stone_x, stone_y, [list(range(stone_x - 50, stone_x + 100)),
                                                                   list(range(stone_y - 50, stone_y))],
                                                [list(range(stone_x, stone_x + 51)),
                                                 list(range(stone_y, stone_y + 51))],
                                                "Уголь", ["Небольшой уголек", "Ценное топливо, но", "оставляет следы"],
                                                random.randint(8, 10)))
        elif self.type == 'iron':
            stone_chance = random.randint(1, 7)
            if stone_chance <= 2 and self.health:
                stone_x = random.choice(self.active_zone[0])
                stone_y = random.choice(self.active_zone[1])
                leftside_drops_list.append(Stone(stone_x, stone_y, [list(range(stone_x - 50, stone_x + 100)),
                                                                    list(range(stone_y - 50, stone_y))],
                                                 [list(range(stone_x, stone_x + 51)),
                                                  list(range(stone_y, stone_y + 51))],
                                                 "Камешек", ["Небольшой камень.", "Можно обработать"], 0))
            elif stone_chance == 6 and self.health:
                stone_x = random.choice(self.active_zone[0])
                stone_y = random.choice(self.active_zone[1])
                leftside_drops_list.append(IronOre(stone_x, stone_y, [list(range(stone_x - 50, stone_x + 100)),
                                                                      list(range(stone_y - 50, stone_y))],
                                                   [list(range(stone_x, stone_x + 51)),
                                                    list(range(stone_y, stone_y + 51))],
                                                   "Железная руда",
                                                   ["Рудное железо", "В нем видны", "вкрапления железа",
                                                    "Можно переплавить", "в слитки"],
                                                   0))

    def draw_object(self):
        pygame.draw.polygon(display, (181, 184, 177),
                            ((self.x, self.y + 100 - self.health * 10), (self.x + 70, self.y + 100 - self.health * 10),
                             (self.x + 100, self.y + 100),
                             (self.x - 30, self.y + 100)))
        if self.type == 'coal':
            pygame.draw.line(display, (20, 17, 11), (self.x + 40, self.y + 100 - self.health * 10),
                             (self.x + 30, self.y + 100), self.health * 2)
            pygame.draw.line(display, (20, 17, 11), (self.x + 50, self.y + 100 - self.health * 10),
                             (self.x + 60, self.y + 100), self.health + 2)

        elif self.type == 'iron':
            pygame.draw.line(display, (112, 75, 46), (self.x + 40, self.y + 100 - self.health * 10),
                             (self.x + 30, self.y + 100), self.health * 2)
            pygame.draw.line(display, (112, 75, 46), (self.x + 50, self.y + 100 - self.health * 10),
                             (self.x + 60, self.y + 100), self.health + 2)

    def regenerate(self):
        if self.regeneration_time > 0:
            self.regeneration_time -= 1
        if not self.regeneration_time and self.health < 10:
            self.health += 1
            self.regeneration_time = 900


class Berry:

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

    def __init__(self, d_x, d_y, active_zone, visible_zone, d_type, description, energy=0, attatched_to_cursor=0):
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.x = d_x
        self.y = d_y
        self.type = d_type
        self.description = description
        self.energy = energy
        self.attached_to_cursor = attatched_to_cursor

    def up_down(self):
        if game_tick % 60 == 1:
            self.y += 17
        elif game_tick % 60 == 29:
            self.y -= 17

    def pick_up(self):
        heretic.inventory.append(self)

    def draw_object(self, drop_x, drop_y):
        display.blit(active_font.render(self.type, True, (0, 0, 0)), (drop_x, drop_y))


class Eatable(Drop):

    def eat(self):
        global eat_time, energy_boost

        heretic.health += self.energy
        eat_time = 100
        energy_boost = '+ ' + str(self.energy)
        if heretic.health > 100:
            heretic.health = 100


class Fuel(Drop):

    def burn(self):
        pass


class Meltable(Drop):

    def melt(self):
        pass


class Log(Fuel):

    def print_type(self):
        print(type(self))

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (137, 99, 36), (drop_x, drop_y, 80, 50))
        pygame.draw.ellipse(display, (155, 136, 70), (drop_x - 15, drop_y, 30, 50))


class Leather(Drop):

    def draw_object(self, x, y):
        pygame.draw.polygon(display, (150, 92, 62), ((x, y), (x + 10, y + 10), (x + 15, y + 14),
                                                     (x + 20, y + 15), (x + 25, y + 14), (x + 30, y + 10),
                                                     (x + 40, y), (x + 60, y + 10), (x + 55, y + 15), (x + 50, y + 20),
                                                     (x + 48, y + 25), (x + 47, y + 30), (x + 48, y + 35),
                                                     (x + 50, y + 41), (x + 60, y + 50),
                                                     (x + 40, y + 60), (x + 30, y + 50), (x + 25, y + 46),
                                                     (x + 20, y + 45), (x + 15, y + 46), (x + 10, y + 50), (x, y + 60),
                                                     (x - 20, y + 50), (x - 10, y + 41), (x - 8, y + 35),
                                                     (x - 7, y + 30),
                                                     (x - 8, y + 25), (x - 10, y + 20), (x - 15, y + 15),
                                                     (x - 20, y + 10)))


class Wool(Drop):

    def draw_object(self, x, y):
        pygame.draw.polygon(display, (200, 200, 200), ((x, y), (x + 30, y - 5), (x + 60, y),
                                                       (x + 52, y + 30), (x + 35, y + 20), (x + 25, y + 20),
                                                       (x + 8, y + 30)))
        for i in range(y + 3, y + 20, 6):
            pygame.draw.lines(display, (160, 160, 160), False, ((x + 5, i + 5), (x + 30, i), (x + 55, i + 5)), 2)


class Stone(Drop):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (0, 0, 0), (drop_x - 1, drop_y - 1, 42, 42))
        pygame.draw.rect(display, (181, 184, 177), (drop_x, drop_y, 40, 40))
        pygame.draw.rect(display, (158, 158, 158), (drop_x, drop_y + 25, 40, 15))


class Coal(Fuel):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (20, 17, 11), (drop_x, drop_y, 15, 10))
        pygame.draw.rect(display, (20, 17, 11), (drop_x + 5, drop_y + 10, 40, 25))


class IronOre(Meltable):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (0, 0, 0), (drop_x - 1, drop_y - 1, 42, 42))
        pygame.draw.rect(display, (181, 184, 177), (drop_x, drop_y, 40, 40))
        pygame.draw.rect(display, (158, 158, 158), (drop_x, drop_y + 25, 40, 15))
        for i in range(drop_x + 5, drop_x + 35, 10):
            pygame.draw.line(display, (112, 75, 46), (i, drop_y + 2), (i + 5, drop_y + 20), 5)


class IronIngot(Drop):

    def draw_object(self, drop_x, drop_y):
        pygame.draw.rect(display, (89, 93, 110), (drop_x, drop_y, 50, 20))


class Pine(Fuel):

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


class Seeds(Eatable):

    def __init__(self, d_x, d_y, active_zone, visible_zone, d_type, description, plant, growing_time, max_growing_time,
                 energy=0, attatched_to_cursor=0):
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.x = d_x
        self.y = d_y
        self.type = d_type
        self.description = description
        self.energy = energy
        self.attached_to_cursor = attatched_to_cursor
        self.plant = plant
        self.growing_time = growing_time
        self.max_growing_time = max_growing_time

    def draw_object(self, obj_x, obj_y):
        display.blit(seeds_image, seeds_image.get_rect(center=(obj_x + 20, obj_y + 25)))


class Carrot(Eatable):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.ellipse(display, (236, 127, 34), (obj_x, obj_y, 55, 18))
        pygame.draw.polygon(display, (0, 80, 0), ((obj_x + 55, obj_y + 9), (obj_x + 70, obj_y + 2), (obj_x + 70, obj_y + 18)))


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


class RawMeat(Eatable, Meltable):

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


class Crops:

    def __init__(self, type, growing_time):
        self.type = type
        self.growing_time = growing_time


class GrassBundle(Drop, Crops):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.polygon(display, (0, 0, 0), (
            (obj_x - 1, obj_y + 61), (obj_x + 19, obj_y + 21), (obj_x + 33, obj_y + 16), (obj_x + 8, obj_y + 62)))
        pygame.draw.polygon(display, (96, 185, 66), (
            (obj_x, obj_y + 60), (obj_x + 20, obj_y + 20), (obj_x + 32, obj_y + 17), (obj_x + 7, obj_y + 61)))

        pygame.draw.polygon(display, (0, 0, 0), (
            (obj_x - 1, obj_y + 56), (obj_x + 39, obj_y + 23), (obj_x + 50, obj_y + 26), (obj_x + 8, obj_y + 62)))
        pygame.draw.polygon(display, (96, 185, 66), (
            (obj_x, obj_y + 55), (obj_x + 40, obj_y + 24), (obj_x + 49, obj_y + 27), (obj_x + 7, obj_y + 61)))

        pygame.draw.polygon(display, (0, 0, 0), (
            (obj_x - 1, obj_y + 56), (obj_x + 60, obj_y + 38), (obj_x + 70, obj_y + 42), (obj_x + 8, obj_y + 62)))
        pygame.draw.polygon(display, (96, 185, 66), (
            (obj_x, obj_y + 55), (obj_x + 61, obj_y + 39), (obj_x + 69, obj_y + 43), (obj_x + 7, obj_y + 61)))


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
        self.x += random.randint(1, 2)


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

    def __init__(self, p_x, p_y, p_direction, p_life_time, location='home'):
        self.x = p_x
        self.y = p_y
        self.direction = p_direction
        self.life_time = p_life_time
        self.location = location

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
            (decors_list if self.location == 'home' else leftside_decors_list).append(Blood(self.x, self.y, random.randint(15, 30), random.randint(15, 30), 600))
            (decors_list if self.location == 'home' else leftside_decors_list).remove(self)
           #print(len(list(filter(lambda i: isinstance(i, Blood), decors_list))))


class FallingLeaves(Particles):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (52, 152, 56), (obj_x, obj_y, random.randint(7, 9), random.randint(6, 7)))


class Mark(Particles):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (200, 0, 0), (obj_x - 5, obj_y - 5, 10, 10))
        self.life_time -= 1


class Torch(Drop, Decor):

    def __init__(self, p_x, p_y, active_zone, visible_zone, type, description, light_zone, life_time=1000):
        self.x = p_x
        self.y = p_y
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.type = type
        self.description = description
        self.life_time = life_time
        self.light_zone = light_zone

    def work(self, day_tick):
        """
        light_surf = pygame.Surface((150 - (day_tick - 450) // 15, 150 - (day_tick - 450) // 15))
        light_surf.fill((150, 150, 150))
        light_surf.set_alpha(140)
        display.blit(light_surf, (self.x - (150 - (day_tick - 450) // 15) // 2, self.y - (150 - (day_tick - 450) // 15) // 2))"""
        pygame.draw.circle(display, (90, 100, 95) if current_location == 'leftside' else (0, 170, 0), (self.x + 12, self.y + 60), 150 - (day_tick - 450) // 15)
        pygame.draw.circle(display, (100, 110, 105) if current_location == 'leftside' else (0, 185, 0), (self.x + 12, self.y + 60), 110 - (day_tick - 450) // 15)
        smoke_chance = random.randint(0, 150)
        if not smoke_chance:
            decors_list.append(Smoke(random.randint(self.x - 5, self.x + 30),
                                     random.randint(self.y - 30, self.y - 25), random.randint(5, 15),
                                     random.randint(5, 15), random.randint(120, 180)))

    def work2(self, tick):
        pygame.draw.ellipse(display, (219, 144, 31),
                            (self.x - 5 + tick % 30 // 9, self.y - 52 + tick % 25 // 8, 35, 45))
        pygame.draw.circle(display, (200, 0, 0), (self.x + 12, self.y - 25), 13)
        pygame.draw.polygon(display, (200, 0, 0), ((self.x + 1, self.y - 25), (self.x + 24, self.y - 25),
                                                   (self.x + 12, self.y - 50)))

    def draw_object(self, obj_x, obj_y):
        pygame.draw.polygon(display, (137, 99, 36), ((obj_x + 3, obj_y - 25), (obj_x + 8, obj_y + 45),
                                                     (obj_x + 19, obj_y + 45), (obj_x + 22, obj_y - 25)))
        pygame.draw.circle(display, (0, 0, 0), (obj_x + 12, obj_y - 25), 13)

        # self.life_time -= 1
    '''
    def light(self):
        if len([i for i in heretic.inventory if isinstance(i, Coal)]):
            for i in heretic.inventory:
                if isinstance(i, Coal):
                    heretic.inventory.remove(i)
            return True
        global current_string, remark_time
        return False'''


'''
Классы декора:конец
'''


class Bed(object):

    def __init__(self, b_x, b_y, active_zone):
        self.x = b_x
        self.y = b_y
        self.active_zone = active_zone


class WorkBenches(object):

    def __init__(self, w_x, w_y, active_zone, work_time, status, current_product=None, fuel=0):

        self.x = w_x
        self.y = w_y
        self.active_zone = active_zone
        self.work_time = work_time
        self.status = status
        self.product = current_product
        self.fuel = fuel

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

    def produce(self):
        m_x = self.x + 15
        m_y = self.y + 10
        act_zone = [list(range(m_x - 50, m_x + 150)), list(range(m_y - 50, m_y + 150))]
        vis_zone = [list(range(m_x, m_x + 50)), list(range(m_y, m_y + 50))]
        if self.status == 'Сырое мясо':
            self.product = Meat(m_x, m_y, act_zone, vis_zone, "Жареное мясо",
                                ['Вкусный еще теплый', 'кусок жареного мяса'], random.randint(20, 25))
        elif self.status == "Железная руда":
            self.product = IronIngot(m_x, m_y, act_zone, vis_zone, "Слиток железа",
                                     ['Неровный слиток', 'Основной материал', "для железных орудий"], 0)

        self.status = 'off'
        self.work_time = 0

    def melt_something(self, stat):
        global remark_time, current_string
        self.work_time = 600
        self.status = stat
        self.work()

    def work(self):
        if self.work_time >= 0 and self.fuel:
            if sleeping and not self.work_time % 3:
                self.work_time -= 3
            else:
                self.work_time -= 1
            if not self.work_time % 60 and self.fuel and self.work_time:
                self.fuel -= 1
            if not self.work_time:
                self.produce()

    def start_work(self):
        self.status = 'off'
        global current_interface
        current_interface = 'furnace'

    def draw_object(self, x, y):
        pygame.draw.rect(display, (89, 94, 100), (x, y, 100, 100))
        pygame.draw.polygon(display, (20, 20, 20),
                            ((x + 20, y + 35), (x + 35, y + 15), (x + 65, y + 15), (x + 80, y + 35)))
        pygame.draw.rect(display, (181, 184, 177), (x + 2, y + 40, 96, 58))
        pygame.draw.polygon(display, (20, 20, 20),
                            ((x + 10, y + 90), (x + 20, y + 65), (x + 30, y + 55), (x + 70, y + 55), (x + 80, y + 65),
                             (x + 90, y + 90)))
        if self.status != 'off' and self.fuel:
            pygame.draw.circle(display, (190, 0, 10), (x + 50, y + 65), 20 + self.work_time % 60 // 12)
            pygame.draw.circle(display, (200, 143, 25), (x + 50, y + 65), 10 + self.work_time % 60 // 15)

            pygame.draw.rect(display, (181, 184, 177), (x + 2, y + 40, 96, 15))

    def alternate_draw_object(self, x, y):
        pygame.draw.line(display, (170, 161, 161), (x + 30, y + 65),
                         (x + 10, y + 90), 15)
        pygame.draw.line(display, (170, 161, 161), (x + 70, y + 65),
                         (x + 90, y + 90), 15)
        pygame.draw.ellipse(display, (142, 47, 41), (x, y, 100, 75))
        pygame.draw.ellipse(display, (0, 0, 0), (x + 5, y + 5, 90, 50))
        if self.status == 'on':
            pygame.draw.ellipse(display, (216, 118, 49), (x + 10, y + 8, 80, 44))
        for i in range(y + 10, y + 46, 7):
            if i == y + 10 or i == y + 45:
                pygame.draw.line(display, (170, 161, 161), (x + 30, i), (x + 70, i), 4)
            elif i == y + 17 or i == y + 38:
                pygame.draw.line(display, (170, 161, 161), (x + 10, i), (x + 90, i), 4)
            else:
                pygame.draw.line(display, (170, 161, 161), (x + 5, i), (x + 95, i), 4)
        if self.status == 'meat':
            pygame.draw.ellipse(display, (168, 33, 0), (x + 15, y + 10, 70, 40))
        elif self.status == 'on':
            pygame.draw.ellipse(display, (168 - (600 - self.work_time) // 7, 33 - (600 - self.work_time)
                                          // 20, 0), (self.x + 15, self.y + 10, 70, 40))


class GridStone(WorkBenches):

    def produce_tools(self, tool):
        tool_x = random.choice(self.active_zone[0])
        tool_y = random.choice(self.active_zone[1])
        active_zone, visible_zone = [list(range(tool_x - 50, tool_x + 150)), list(range(tool_y - 50, tool_y + 150))], \
                                    [list(range(tool_x, tool_x + 50)), list(range(tool_y, tool_y + 50))]
        if tool == 'sharpened stone':
            if len([i for i in heretic.inventory if isinstance(i, Stone)]) >= 2:
                home_drops_list.append(SharpenedStone(tool_x, tool_y, active_zone, visible_zone, "Заточенный камень",
                                                      ['Заточенный булыжник', "Острый, но хрупкий",
                                                       "Основной материал для", "продвинутого оружия"],
                                                      random.randint(2, 3), 10, 10, 1))
                count = 0
                for i in heretic.inventory:
                    if isinstance(i, Stone):
                        heretic.inventory.remove(i)
                        count += 1
                        if count == 2:
                            break
            else:
                self.status = 'not enough resources'

        elif tool == 'pickaxe':
            if len([i for i in heretic.inventory if isinstance(i, Stone)]) >= 2 and \
                    len([i for i in heretic.inventory if isinstance(i, Log)]):
                home_drops_list.append(PickAxe(tool_x, tool_y, active_zone, visible_zone, "Примитивная кирка",
                                               ['Не очень прочная', "Облегчает добычу камня",
                                                "Низкий урон"],
                                               random.randint(1, 2), 25, 25, 2.5))
                count = 0
                for i in heretic.inventory:
                    if isinstance(i, Stone):
                        heretic.inventory.remove(i)
                        count += 1
                        if count == 2:
                            break
                for i in heretic.inventory:
                    if isinstance(i, Log):
                        heretic.inventory.remove(i)
                        break
            else:
                self.status = 'not enough resources'

        elif tool == 'shovel':
            home_drops_list.append(Shovel(tool_x, tool_y, active_zone, visible_zone, "Лопата",
                                          ['Позволяет делать', "тропинки или что-нибудь",
                                           "закопать"],
                                          random.randint(2, 3), 15, 15, 2.5))

        elif tool == 'crate':
            heretic.inventory.append(Crate(0, 0, 0, 0, [], 8, 0, 0, 'Ящик'))

        elif tool == 'bag':
            home_drops_list.append(Bag(tool_x, tool_y, 70, 60, [], 4,
                                       active_zone, visible_zone, 'Сумка',
                                       description=['Небольщая кожаная', "сумка. Содержимое:", "Пусто"]))

        elif tool == 'hoe':
            home_drops_list.append(Hoe(tool_x, tool_y, active_zone, visible_zone, "Мотыга",
                                       ['Не очень прочная', "Позволяет создавать грядки,",
                                        "на которых выращивают", "различные растения"], random.randint(1, 2), 10, 10,
                                       2))

        elif tool == 'bow':
            home_drops_list.append(Bow(tool_x, tool_y, active_zone, visible_zone, "Лук",
                                       ['Короткий лук', "Не очень мощный,", "но позволяет поражать",
                                        "цель на расстоянии"],
                                       random.randint(4, 5), 15, 15, 2, max_reload=120))

        elif tool == 'torch':
            home_drops_list.append(Torch(tool_x, tool_y, active_zone, visible_zone, [[], []], 'Факел', ['Источник света.', "Горит каждую ночь"]))

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

    def __init__(self, w_x, w_y, active_zone, visible_zone, w_type, description, strength, durability, max_durability,
                 speed, blood_marks=0, reload=0, max_reload=0):
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
        self.reload = reload
        self.max_reload = max_reload

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

        pygame.draw.polygon(display, (181, 186, 177),
                            ((obj_x, obj_y + 5), (obj_x - 15, obj_y + 21), (obj_x, obj_y + 14)))
        pygame.draw.polygon(display, (181, 186, 177),
                            ((obj_x + 12, obj_y + 5), (obj_x + 27, obj_y + 21), (obj_x + 12, obj_y + 14)))
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


class Shovel(Weapon):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (137, 99, 36), (obj_x + 5, obj_y + 30, 10, 40))
        pygame.draw.rect(display, (181, 186, 177), (obj_x, obj_y + 7, 20, 23))
        pygame.draw.rect(display, (127, 89, 26), (obj_x, obj_y + 70, 20, 5))
        pygame.draw.circle(display, (181, 186, 177), (obj_x + 10, obj_y + 10), 10)
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

    def dig(self):
        trails_list.append(Trail(heretic.x + 5, heretic.y + 80, "left", 60, 60, [list(range(heretic.x, heretic.y + 61)),
                                                                                 list(range(heretic.y + 75,
                                                                                            heretic.y + 136))],
                                 [list(range(heretic.x, heretic.y + 61)),
                                  list(range(heretic.y + 75, heretic.y + 136))],
                                 [[str(j) + " " + str(k) for j in range(heretic.x, heretic.x + 61, 10)] for k in
                                  range(heretic.y + 75, heretic.y + 136,
                                        10)], []))
        heretic.health -= 5
        self.durability -= 1
        if not self.durability:
            heretic.weapon = 'none'


class Hoe(Weapon):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (137, 99, 36),
                         (obj_x, obj_y, 12 if heretic.direction in ['left', 'right'] else 8, 45))
        if inventory_mode or heretic.direction == 'right':
            pygame.draw.polygon(display, (181, 186, 177),
                                ((obj_x - 3, obj_y + 12), (obj_x - 5, obj_y + 3), (obj_x + 30, obj_y + 12)))
        elif heretic.direction == 'left':
            pygame.draw.polygon(display, (181, 186, 177),
                                ((obj_x + 15, obj_y + 12), (obj_x + 17, obj_y + 3), (obj_x - 18, obj_y + 12)))
        elif heretic.direction == 'down':
            pygame.draw.polygon(display, (181, 186, 177),
                                ((obj_x - 2, obj_y + 12), (obj_x + 10, obj_y + 12), (obj_x + 4, obj_y + 18)))
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

    def make_farmlands(self):
        heretic.health -= random.randint(3, 5)
        self.durability -= 1
        if not self.durability:
            heretic.weapon = 'none'
        x, y = heretic.x + 30, heretic.y + 110
        farmlands_list.append(FarmLands(x, y, [list(range(x - 30, x + 90)), list(range(y - 30, y + 90))],
                                        [list(range(x, x + 60)), list(range(y, y + 60))]))


class LongRange(Weapon):

    def shoot(self, target, owner):
        pass


class Bow(LongRange):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.lines(display, (168, 167, 159), False,
                          ((obj_x, obj_y + self.reload // 20), (obj_x - 15 - self.reload // 10, obj_y + 20),
                           (obj_x, obj_y + 40 - self.reload // 20)), 3)
        pygame.draw.lines(display, (150, 89, 35), False,
                          ((obj_x, obj_y + self.reload // 20), (obj_x + 15, obj_y + 10), (obj_x + 20, obj_y + 20),
                           (obj_x + 15, obj_y + 30), (obj_x, obj_y + 40 - self.reload // 20)), 5)
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

    def shoot(self, target, owner):
        if isinstance(target, Mob):
            bullets_list.append(
                Bullet(owner.x + 37, owner.y + 50, (target.x + len(target.visible_zone[0]) // 2 - 37 - owner.x) // 38,
                       (target.y + len(target.visible_zone[1]) // 2 - 50 - owner.y) // 38, owner, current_location,
                       random.randint(2, 3)))
        self.reload = 0
        self.durability -= 1


def close():
    global current_interface

    current_interface = 'none'


class Storage(object):

    def __init__(self, s_x, s_y, s_length, s_width, storage, max_capability, active_zone, visible_zone, type,
                 location='home', description=None):
        if not description:
            description = ['Хранилище']
        self.x = s_x
        self.y = s_y
        self.length = s_length
        self.width = s_width
        self.storage = storage
        self.max_capability = max_capability
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.type = type
        self.location = location
        self.description = description

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


class Crate(Storage):
    @staticmethod
    def draw_object(obj_x, obj_y):
        display.blit(crate_image, crate_image.get_rect(center=(obj_x + 34, obj_y + 34)))

    def set(self):
        crates_list.append(Crate(heretic.x + 15, heretic.y + 30, 68, 68, [], 8,
                                 [list(range(heretic.x - 85, heretic.x + 115)),
                                  list(range(heretic.y - 50, heretic.y + 50))],
                                 [list(range(heretic.x + 15, heretic.x + 83)),
                                  list(range(heretic.y + 30, heretic.y + 98))], "Ящик", current_location))
        heretic.inventory.remove(self)


class BackPack(Storage):

    def equip(self):
        if heretic.backpack:
            x = random.randint(heretic.x - 50, heretic.x + 100)
            y = random.randint(heretic.y + 10, heretic.y + 120)
            heretic.backpack.x = x
            heretic.backpack.y = y
            heretic.backpack.active_zone = [list(range(x - 150, x + 150)),
                                            list(range(y - 150, y + 150))]
            (drops_list if heretic.location == 'home' else leftside_drops_list).append(heretic.backpack)
        heretic.backpack = self

    def draw_on_heretic(self, obj_x, obj_y):
        pass


class Bag(BackPack, Drop):

    def draw_object(self, x, y):
        pygame.draw.rect(display, (161, 112, 51), (x, y, 50, 70))
        pygame.draw.lines(display, (161, 112, 51), True, ((x, y), (x + 40, y - 15), (x + 60, y + 10)), 8)
        pygame.draw.polygon(display, (169, 82, 44),
                            ((x - 2, y), (x - 2, y + 25), (x + 25, y + 35), (x + 52, y + 25), (x + 52, y)))

        pygame.draw.circle(display, (0, 0, 0), (x + 25, y + 29), 3)

    def draw_on_heretic(self, obj_x, obj_y):
        pygame.draw.rect(display, (161, 112, 51), (obj_x, obj_y, 25, 40))
        pygame.draw.lines(display, (161, 112, 51), True,
                          ((obj_x, obj_y), (obj_x + 22, obj_y - 10), (obj_x + 35, obj_y + 6)), 5)
        pygame.draw.polygon(display, (169, 82, 44),
                            ((obj_x - 2, obj_y), (obj_x - 2, obj_y + 15), (obj_x + 12, obj_y + 20),
                             (obj_x + 27, obj_y + 15), (obj_x + 27, obj_y)))

        pygame.draw.circle(display, (0, 0, 0), (obj_x + 12, obj_y + 17), 2)


class Sign:

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


class Bullet:

    def __init__(self, b_x, b_y, g_speed, v_speed, owner, location, damage, mark_list=[]):
        self.x = b_x
        self.y = b_y
        self.g_speed = g_speed
        self.v_speed = v_speed
        self.mark_list = mark_list
        self.owner = owner
        self.location = location
        self.damage = damage

    def draw_object(self, obj_x, obj_y):
        pygame.draw.circle(display, (200, 10, 10), (obj_x, obj_y), 5)
        pygame.draw.circle(display, (10, 10, 10), (obj_x, obj_y), 6, 1)

    def move(self):
        self.x += self.g_speed
        self.y += self.v_speed

    def collide(self, target):
        target.health -= self.damage
        target.x += self.g_speed * 10
        target.y += self.v_speed * 10
        if blood_setting:
            for i in range(heretic.strength + 1):
                blood_y = random.choice(target.visible_zone[1])
                (decors_list if current_location == 'home' else leftside_decors_list).append(
                    FallingBlood(random.choice(target.visible_zone[0]),
                                 blood_y, "down", (100 - (blood_y - target.y)) // 2, heretic.location))
        target.bleeding = self.damage * 250
        target.active_zone = [[j for j in range(target.x - 100, target.x + 150)],
                              [k for k in range(target.y - 100, target.y + 100)]]

        '''
        if self.v_speed < 3:
            self.v_speed = 3 if self.v_speed > 0 else - 3
        if self.g_speed < 3:
            self.g_speed = 3 if self.g_speed > 0 else - 3
        '''


remark_time = 0
current_string = ''
current_interface = 'none'
current_location = 'menu'

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

clock = pygame.time.Clock()
active_font = pygame.font.Font(None, 60)
inventory_font = pygame.font.SysFont('Cambria', 75)
title_font = pygame.font.SysFont('Cambria', 125)
title = ''
FARMETIC = 'FARMETIC'
going_to_menu = 0

active = False

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
