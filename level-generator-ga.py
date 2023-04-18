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

import random


def generate_population():
    valid_x = list(range(0, 60))
    valid_y = list(range(0, 17))
    valid_entity_types = ["CoinBox", "coinBrick", "coin", "Goomba", "Koopa", "RandomBox"]

    population = []
    for i in range(50):
        level = {
            "id": i,
            "length": random.randint(40, 80),
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

        # Generate random objects
        for obj_type in level["level"]["objects"]:
            obj_count = random.randint(0, 5)
            for j in range(obj_count):
                x = random.choice(valid_x)
                y = random.choice(valid_y)
                level["level"]["objects"][obj_type].append([x, y])

        # Generate random layers
        for layer_name in level["level"]["layers"]:
            x_start = random.randint(0, level["length"] - 1)
            x_end = random.randint(x_start + 1, level["length"])
            y = random.randint(0, 16)
            level["level"]["layers"][layer_name]["x"] = [x_start, x_end]
            level["level"]["layers"][layer_name]["y"] = [y, y]

        # Generate random entities
        for entity_type in valid_entity_types:
            entity_count = random.randint(0, 5)
            for j in range(entity_count):
                x = random.choice(valid_x)
                y = random.choice(valid_y)
                if entity_type == "RandomBox":
                    entity_data = [x, y, random.choice(["RedMushroom", "GreenMushroom", "Star"])]
                else:
                    entity_data = [x, y]
                level["level"]["entities"][entity_type].append(entity_data)

        population.append(level)

    return population