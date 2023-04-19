import random
import json

level = {
    "id": 0,
    "length": 0,
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


def generate_chromosome():
    valid_x_bush = list(range(2, 60))
    valid_y_bush = 12

    valid_x_sky = list(range(0, 50))
    valid_y_sky = 0 #list(range(13, 14)) should be 13, 14 so both can be a hole

    valid_x_cloud = list(range(1, 60))
    valid_y_cloud = list(range(3, 6))

    valid_x_pipe = list(range(8, 30))
    valid_y_pipe = list(range(9, 12))
    valid_z_pipe = list(range(4, 6))
    # pre-requisite
    valid_x_ground = list(range(0, 59))
    valid_y_ground = list(range(3, 12))

    valid_layer_x_sky = [0, 60]
    valid_layer_y_sky = [0, 13]

    valid_layer_x_ground = [0, 60]
    valid_layer_y_ground = [14, 16]
    valid_entity_types = ["CoinBox", "coinBrick", "coin", "Goomba", "Koopa", "RandomBox"]

    level = {
        "id": 1,
        "length": 60,  # random.randint(40, 80),
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
    obj_count = random.randint(0, 10)
    for j in range(obj_count):
        x = random.choice(valid_x_bush)
        y = valid_y_bush
        level["level"]["objects"]["bush"].append([x, y])

    # Generate Sky
    obj_count = random.randint(0, 10)
    for j in range(obj_count):
        x = random.choice(valid_x_sky)
        #y = random.choice(valid_y_sky)
        level["level"]["objects"]["sky"].append([x, 14])
        level["level"]["objects"]["sky"].append([x, 13])

    # Generate Cloud
    obj_count = random.randint(0, 10)
    for j in range(obj_count):
        x = random.choice(valid_x_cloud)
        y = random.choice(valid_y_cloud)
        level["level"]["objects"]["cloud"].append([x, y])

    # Generate Pipe
    obj_count = random.randint(0, 10)
    for j in range(obj_count):
        x = random.choice(valid_x_pipe)
        y = random.choice(valid_y_pipe)
        z = random.choice(valid_z_pipe)
        level["level"]["objects"]["pipe"].append([x, y, z])

    # Generate ground
    obj_count = random.randint(15, 31)
    for j in range(obj_count):
        x = random.choice(valid_x_ground)
        y = random.choice(valid_y_ground)
        level["level"]["objects"]["ground"].append([x, y])

    level["level"]["layers"]["sky"]["x"] = valid_layer_x_sky
    level["level"]["layers"]["sky"]["y"] = valid_layer_y_sky

    level["level"]["layers"]["ground"]["x"] = valid_layer_x_ground
    level["level"]["layers"]["ground"]["y"] = valid_layer_y_ground
    with open("levels/Level1-3.json", "w") as f:
        json.dump(level, f, indent=1)
    return


generate_chromosome()
init_population = 50


def generate_population():
    population = []
    for i in range(0, 50):
        population.append(generate_chromosome())
    return population

#def fitness(chromosome_list):

