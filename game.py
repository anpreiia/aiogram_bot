import time

SPROUT = "🌱"
GROUND = "🕳"
NONE = 'none'
PLANTS = dict([])

EMPTY_GARDEN = [[NONE, 1], [NONE, 1], [NONE, 1], [NONE, 1], [NONE, 1],
                [NONE, 1], [NONE, 1], [NONE, 1], [NONE, 1], [NONE, 1]]

PLAYER_START_MONEY = 15


class Crop:
    def __init__(self,
                 id: str = "crop",
                 name: str = "имя",
                 cost: int = 1,
                 sell_price: int = 2,
                 sprite: str = ".",
                 grow_time: int = 10, ):
        self.id = id
        self.name = name
        self.cost = cost
        self.sell_price = sell_price
        self.sprite = sprite
        self.grow_time = grow_time

        PLANTS[self.id] = self
        print(f"{self.id}:{self.sprite}:{self.name}>>{self.cost}:{self.sell_price}>>{grow_time}s")


TULP = Crop("TULP", "тюобпан", 15, 20, "🌷", 30)


def is_it_grow(planting_time: int, plant: str) -> bool:
    if (planting_time + PLANTS[plant].grow_time) < int(time.time()):
        return True
    else:
        return False


def get_place_emoji(plant: str, planting_time: int) -> str:
    if plant == NONE:
        return GROUND

    if is_it_grow(planting_time, plant):
        return PLANTS[plant].sprite
    else:
        return SPROUT


def draw_garden(garden: list) -> str:
    gl = ""
    for i in range(0, 5):
        gl += get_place_emoji(garden[i][0], garden[i][1])
    gl += "\n"
    for i in range(5, 10):
        gl += get_place_emoji(garden[i][0], garden[i][1])
    return gl


def sell_all(garden: list) -> [int, list]:
    income = 0
    for i in range(len(garden)):
        if garden[i][0] != NONE:
            if is_it_grow(garden[i][1], garden[i][0]):
                income += PLANTS[garden[i][0]].sell_price
                garden[i][0] = NONE
                garden[i][1] = 1
    return [income, garden]


def buy_in_renge(ids: list, money: int, garden: list, plant: str) -> [int, list] or False:
    for i in ids:
        if 0 > i or i > 9:
            return False

    plant_cost = PLANTS[plant].cost

    for i in ids:
        if garden[i][0] != NONE:
            continue

        if money >= plant_cost:
            money -= plant_cost
            garden[i][0] = plant
            garden[i][1] = int(time.time())
    return [money, garden]
