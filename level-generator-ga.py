import random
import json


#
# Initial population.
# Fitness function.
# Selection.
# Crossover.
# Mutation.

class Chromosome:
    def __init__(self, level):
        self.obj_bush = level["level"]["objects"]["bush"]
        self.obj_sky = level["level"]["objects"]["sky"]
        self.obj_cloud = level["level"]["objects"]["cloud"]
        self.obj_pipe = level["level"]["objects"]["pipe"]
        self.obj_ground = level["level"]["objects"]["ground"]
        self.layers_sky = level["level"]["layers"]["sky"]["x"]
        self.layers_sky = level["level"]["layers"]["sky"]["y"]
        self.layers_ground = level["level"]["layers"]["ground"]["x"]
        self.layers_ground = level["level"]["layers"]["ground"]["y"]
        self.ent_coinBox = level["level"]["entities"]["CoinBox"]
        self.ent_coinBrick = level["level"]["entities"]["coinBrick"]
        self.ent_coin = level["level"]["entities"]["coin"]
        self.ent_goomba = level["level"]["entities"]["Goomba"]
        self.ent_koopa = level["level"]["entities"]["Koopa"]
        self.ent_random_box = level["level"]["entities"]["RandomBox"]

        def fitness(self):
            fitness = 0

            # more entities, fitter the chromosome is
            fitness += (10 * len(self.ent_coinBox)) + (5 * len(self.ent_coinBrick)) + (5 * len(self.ent_coin)) + (
                    4 * len(self.ent_goomba)) + (4 * len(self.ent_koopa)) + (3 * len(self.ent_random_box))
            # If enemy is close to mario's initial position at start of game, it might kill mario before he could
            # make a move so there should be negative fitness points for it.
            for enemy in self.ent_goomba + self.ent_koopa:
                if enemy[0] < 7:
                    fitness -= 100

            # Check if tiles are in line for Mario to jump from one to another
            return fitness


def calculate_fitness(level):
    fitness = 0

    # more entities, fitter the chromosome is
    fitness += (10 * len(level["level"]["entities"]["CoinBox"])) + (
            5 * len(level["level"]["entities"]["coinBrick"])) + (5 * len(level["level"]["entities"]["coin"])) + (
                       4 * len(level["level"]["entities"]["Goomba"])) + (
                       4 * len(level["level"]["entities"]["Koopa"])) + (
                       3 * len(level["level"]["entities"]["RandomBox"]))
    # If enemy is close to mario's initial position at start of game, it might kill mario before he could
    # make a move so there should be negative fitness points for it.
    for enemy in level["level"]["entities"]["Goomba"] + level["level"]["entities"]["Koopa"]:
        if enemy[0] < 7:
            fitness -= 100

    # Check if tiles are in line for Mario to jump from one to another
    for row in range(8, 9):
        tile_count = 0
        empty_tile = False
        for col in range(60):
            if [col, row] in level["level"]["objects"]["pipe"] or [col, row] in level["level"]["objects"]["bush"] or [col, row] in level["level"]["entities"]["coinBrick"]:
                empty_tile = False
                tile_count = 0
            elif [col, row] in level["level"]["entities"]["CoinBox"] or [col, row] in level["level"]["entities"][
                "coin"] or [col,
                            row] in level["level"]["entities"]["RandomBox"]:
                empty_tile = True
                tile_count = 0
            else:
                if empty_tile:
                    tile_count += 1
                    if tile_count >= 4:
                        fitness += 1
                else:
                    empty_tile = True
                    tile_count = 1

    return fitness


def crossover_mutation(level1, level2, crossover_percentage, mutation_percentage):
    # swapping object
    objects = ["bush", "sky", "cloud", "pipe", "ground"]

    for object in objects:
        len1 = len(level1["level"]["objects"][object])
        len2 = len(level2["level"]["objects"][object])

        # calculate crossover point
        crossover_point = int(crossover_percentage / 100 * len1)

        # perform crossover
        level1["level"]["objects"][object][:crossover_point] = level2["level"]["objects"][object][:crossover_point]

        # perform mutation
        for i in range(len1):
            if random.random() < mutation_percentage / 100:
                level1["level"]["objects"][object][i] = random.choice(level2["level"]["objects"][object])

    print("crossover, Mutation")
    return level1


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

    valid_x_random_box = list(range(0, length_of_level_x))
    valid_y_random_box = list(range(0, length_of_level_y - 2))

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
    # Generate RandomBox
    obj_count = random.randint(3, noOfKoopa)
    for j in range(obj_count):
        x = random.choice(valid_x_random_box)
        y = random.choice(valid_y_random_box)
        level["level"]["entities"]["RandomBox"].append([x, y, "RedMushroom"])

    return level


def generate_population(total_population):
    population = []
    for i in range(0, total_population):
        population.append(generate_chromosome())
    return population


def save_level_to_file(level):
    with open("levels/Level1-3.json", "w") as f:
        json.dump(level, f, indent=1)


c1 = generate_chromosome(60)
c2 = generate_chromosome(60)
print("\nc1\n", c1)
print("\nc2\n", c2)

c1 = crossover_mutation(c1, c2, 30, 5)
save_level_to_file(c1)
init_population = 50

#
# def crossover_mutation(level1, level2, crossover_percentage):
#     # swapping object
#     objects = ["bush", "sky", "cloud", "pipe", "ground"]
#     # length of number of objects in each level
#     bush_len1 = len(level1["objects"]["bush"])
#     bush_len2 = len(level2["objects"]["bush"])
#
#     sky_len1 = len(level1["objects"]["sky"])
#     sky_len2 = len(level2["objects"]["sky"])
#
#     cloud_len1 = len(level1["objects"]["cloud"])
#     cloud_len2 = len(level2["objects"]["cloud"])
#
#     pipe_len1 = len(level1["objects"]["pipe"])
#     pipe_len2 = len(level2["objects"]["pipe"])
#
#     ground_len1 = len(level1["objects"]["ground"])
#     ground_len2 = len(level2["objects"]["ground"])
#
#
#     crossover_point_bush1 = random.randint(1, bush_len1 - 1)
#     crossover_point_bush2 = random.randint(1, bush_len2 - 1)
#
#     crossover_point_sky1 = random.randint(1, sky_len1 - 1)
#     crossover_point_sky2 = random.randint(1, sky_len2 - 1)
#
#     crossover_point_cloud1 = random.randint(1, cloud_len1 - 1)
#     crossover_point_cloud2 = random.randint(1, cloud_len2 - 1)
#
#     crossover_point_pipe1 = random.randint(1, pipe_len1 - 1)
#     crossover_point_pipe2 = random.randint(1, pipe_len2 - 1)
#
#     crossover_point_ground1 = random.randint(1, ground_len1 - 1)
#     crossover_point_ground2 = random.randint(1, ground_len2 - 1)
#
#     # crossover_point_cloud = random.randint(1, length_of_level - 1)
#     # crossover_point_pipe = random.randint(1, length_of_level - 1)
#
#     for i in range(0, crossover_percentage/100):
#         object = random.choice(object)
#         len1 = len(level1["objects"][object])
#         len2 = len(level2["objects"][object])
#         level1["objects"][object] = level2["objects"][object]
#     print("crossover,Mutation")
