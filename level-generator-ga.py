import random
import json


class Chromosome:
    def __init__(self, level):
        self.obj_bush = level["objects"]["bush"]
        self.obj_sky = level["objects"]["sky"]
        self.obj_cloud = level["objects"]["cloud"]
        self.obj_pipe = level["objects"]["pipe"]
        self.obj_ground = level["objects"]["ground"]
        self.layers_sky = level["layers"]["sky"]["x"]
        self.layers_sky = level["layers"]["sky"]["y"]
        self.layers_ground = level["layers"]["ground"]["x"]
        self.layers_ground = level["layers"]["ground"]["y"]
        self.ent_coinBox = level["entities"]["CoinBox"]
        self.ent_coinBrick = level["entities"]["coinBrick"]
        self.ent_coin = level["entities"]["coin"]
        self.ent_goomba = level["entities"]["Goomba"]
        self.ent_koopa = level["entities"]["Koopa"]
        self.ent_random_box = level["entities"]["RandomBox"]


def generate_chromosome(length_of_level):
    # defining the length of level
    length_of_level_x = length_of_level
    length_of_level_y = 13

    # Defining a range for X and Y for each item in level, so the random values are not out of bound
    valid_x_bush = list(range(2, 60))
    valid_y_bush = 12

    valid_x_sky = list(range(0, 50))
    valid_y_sky = 0  # list(range(13, 14)) should be 13, 14 so both can be a hole

    valid_x_cloud = list(range(1, length_of_level_x))
    valid_y_cloud = list(range(3, 6))

    valid_x_pipe = list(range(8, 30))
    valid_y_pipe = list(range(9, 12))
    valid_z_pipe = list(range(4, 6))

    valid_x_ground = list(range(0, length_of_level_x))
    valid_y_ground = list(range(3, 12))

    valid_layer_x_sky = [0, length_of_level_x]
    valid_layer_y_sky = [0, 13]

    valid_layer_x_ground = [0, length_of_level_x]
    valid_layer_y_ground = [14, 16]

    valid_x_coinbox = list(range(4, length_of_level_x - 2))
    valid_y_coinbox = list(range(2, 8))

    valid_x_coinbrick = list(range(0, length_of_level_x))
    valid_y_coinbrick = list(range(0, 9))

    valid_x_coin = list(range(0, length_of_level_x))
    valid_y_coin = list(range(0, 12))

    valid_x_goomba = list(range(0, length_of_level_x))  # mushroom
    valid_y_goomba = list(range(0, 12))

    valid_x_koopa = list(range(0, length_of_level_x))  # mushroom
    valid_y_koopa = list(range(0, 12))

    valid_x_RandomBox = list(range(0, length_of_level_x))
    valid_y_RandomBox = list(range(0, length_of_level_y - 2))

    noOfBush = 10
    noOfSky = 10
    noOfCloud = 10
    noOfPipe = 10
    noOfGround = 30
    noOfCoinBox = 10
    noOfCoinBrick = 10
    NoOfCoin = 10
    noOfGoomba = 10
    noOfKoopa = 10
    noOfRandomBox = 10
    noOfcoin = 30
    valid_entity_types = ["CoinBox", "coinBrick", "coin", "Goomba", "Koopa", "RandomBox"]

    level = {
        "id": 1,
        "length": length_of_level,  # random.randint(40, 80),
        "level": {
            "objects": {
                "bush": [],
                "sky": [],
                "cloud": [],
                "pipe": [],
                "ground": []
            },
            "layers": {
                "sky": {
                    "x": [0, 0],
                    "y": [0, 0]
                },
                "ground": {
                    "x": [0, 0],
                    "y": [0, 0]
                }
            },
            "entities": {
                "CoinBox": [],
                "coinBrick": [],
                "coin": [],
                "Goomba": [],
                "Koopa": [],
                "RandomBox": []
            }
        }
    }
    # Generate Bush
    obj_count = random.randint(1, noOfBush)
    for j in range(obj_count):
        x = random.choice(valid_x_bush)
        y = valid_y_bush
        level["level"]["objects"]["bush"].append([x, y])

    # Generate Sky
    obj_count = random.randint(1, noOfSky)
    for j in range(obj_count):
        x = random.choice(valid_x_sky)
        # y = random.choice(valid_y_sky)
        level["level"]["objects"]["sky"].append([x, 14])
        level["level"]["objects"]["sky"].append([x, 13])

    # Generate Cloud
    obj_count = random.randint(1, noOfCloud)
    for j in range(obj_count):
        x = random.choice(valid_x_cloud)
        y = random.choice(valid_y_cloud)
        level["level"]["objects"]["cloud"].append([x, y])

    # Generate Pipe
    obj_count = random.randint(1, noOfPipe)
    for j in range(obj_count):
        x = random.choice(valid_x_pipe)
        y = random.choice(valid_y_pipe)
        z = random.choice(valid_z_pipe)
        level["level"]["objects"]["pipe"].append([x, y, z])

    # Generate ground
    obj_count = random.randint(15, noOfGround)
    for j in range(obj_count):
        x = random.choice(valid_x_ground)
        y = random.choice(valid_y_ground)
        level["level"]["objects"]["ground"].append([x, y])

    level["level"]["layers"]["sky"]["x"] = valid_layer_x_sky
    level["level"]["layers"]["sky"]["y"] = valid_layer_y_sky

    level["level"]["layers"]["ground"]["x"] = valid_layer_x_ground
    level["level"]["layers"]["ground"]["y"] = valid_layer_y_ground

    # Generate coinbox
    obj_count = random.randint(3, noOfCoinBox)
    for j in range(obj_count):
        x = random.choice(valid_x_coinbox)
        y = random.choice(valid_y_coinbox)
        level["level"]["entities"]["CoinBox"].append([x, y])
    level["level"]["entities"]["CoinBox"].append([4, 8])

    # Generate coinbrick
    obj_count = random.randint(3, noOfCoinBrick)
    for j in range(obj_count):
        x = random.choice(valid_x_coinbrick)
        y = random.choice(valid_y_coinbrick)
        level["level"]["entities"]["coinBrick"].append([x, y])

    # Generate coin
    obj_count = random.randint(0, noOfcoin)
    for j in range(obj_count):
        x = random.choice(valid_x_coin)
        y = random.choice(valid_y_coin)
        level["level"]["entities"]["coin"].append([x, y])

    # Generate goomba
    obj_count = random.randint(3, noOfGoomba)
    for j in range(obj_count):
        x = random.choice(valid_x_goomba)
        y = random.choice(valid_y_goomba)
        level["level"]["entities"]["Goomba"].append([y, x])

    # Generate koopa
    obj_count = random.randint(3, noOfKoopa)
    for j in range(obj_count):
        x = random.choice(valid_x_koopa)
        y = random.choice(valid_y_koopa)
        level["level"]["entities"]["Koopa"].append([y, x])

    return level


def generate_population(total_population):
    population = []
    for i in range(0, total_population):
        population.append(generate_chromosome())
    return population


def save_level_to_file(level):
    with open("levels/Level1-3.json", "w") as f:
        json.dump(level, f, indent=1)


generate_chromosome(200)
init_population = 50
