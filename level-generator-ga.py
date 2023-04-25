import random
import json


#
# Initial population. Done
# Fitness function. Need Improvements
# Selection. Done
# Crossover. Done
# Mutation. Done

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
    fitness += 2 * ((10 * len(level["level"]["entities"]["CoinBox"])) + (
            5 * len(level["level"]["entities"]["coinBrick"])) + (5 * len(level["level"]["entities"]["coin"])) + (
                       4 * len(level["level"]["entities"]["Goomba"])) + (
                       4 * len(level["level"]["entities"]["Koopa"])) + (
                       3 * len(level["level"]["entities"]["RandomBox"])))
    # If enemy is close to mario's initial position at start of game, it might kill mario before he could
    # make a move so there should be negative fitness points for it.
    for enemy in level["level"]["entities"]["Goomba"] + level["level"]["entities"]["Koopa"]:
        if enemy[0] < 7:
            fitness -= 100

    # Check that no type of bricks should be on the same x-axis
    entities = level["level"]["entities"]
    coin_boxes = entities["CoinBox"]
    coin_bricks = entities["coinBrick"]
    random_boxes = entities["RandomBox"]

    brick_positions = []
    for brick_type in [coin_boxes, coin_bricks, random_boxes]:
        for brick in brick_type:
            brick_positions.append(brick[0])

    if len(set(brick_positions)) != len(brick_positions):
        # If x-axis of bricks are the same, give a penalty to the fitness
        fitness -= 50

    # Check that bricks are not close together in the same y-axis
    for brick_type in [coin_boxes, coin_bricks, random_boxes]:
        sorted_bricks = sorted(brick_type, key=lambda brick: brick[1])

        for i in range(len(sorted_bricks) - 1):
            curr_brick_y = sorted_bricks[i][1]
            next_brick_y = sorted_bricks[i + 1][1]

            if next_brick_y - curr_brick_y <= 2:
                # If bricks are close together in the same y-axis, give a penalty to the fitness
                fitness -= 10


    # Check that pipes are not too close together
    pipe_positions = [pos[0] for pos in level["level"]["objects"]["pipe"]]
    sorted_pipes = sorted(pipe_positions)
    for i in range(len(sorted_pipes) - 1):
        if sorted_pipes[i + 1] - sorted_pipes[i] < 10:
            fitness -= 50

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

    # Check if mushrooms are on top of a brick, or on the ground
    for mushroom in level["level"]["entities"]["Goomba"]:
        on_brick = False
        for brick in level["level"]["entities"]["coinBrick"]:
            if brick[0] == mushroom[0] and brick[1] + 1 == mushroom[1]:
                on_brick = True
                break
        if not on_brick and mushroom[1] != 12:
            fitness -= 10

    # Check that bricks don't overlap with pipes/obstacles
    for brick in level["level"]["entities"]["coinBrick"]:
        for obstacle in level["level"]["objects"]["pipe"] + level["level"]["entities"]["coinBrick"]:
            if obstacle[0] <= brick[0] < obstacle[0] + 2 and obstacle[1] <= brick[1] <= obstacle[1] + 1:
                fitness -= 20

    # Check that pipe height doesn't exceed
    for pipe in level["level"]["objects"]["pipe"]:
        if pipe[1] < 5 or pipe[1] > 9:
            fitness -= 10
    for pipe in level["level"]["objects"]["pipe"]:
        pipe_x, pipe_y = pipe[0], pipe[1]
        bricks_on_top = []
        for brick in level["level"]["entities"]["coinBrick"]:
            brick_x, brick_y = brick[0], brick[1]
            if brick_x == pipe_x and brick_y < pipe_y:
                bricks_on_top.append(brick)

        if len(bricks_on_top) > 0:
            for x in range(pipe_x - 1, pipe_x + 3):
                if [x, pipe_y] in level["level"]["entities"]["coinBrick"]:
                    fitness += 1
                else:
                    fitness -= 1

    # Check that there is enough space for the mushroom to move
    for mushroom in level["level"]["entities"]["Goomba"]:
        mushroom_x, mushroom_y = mushroom[0], mushroom[1]
        if [mushroom_x + 1, mushroom_y] in level["level"]["objects"]["pipe"] or \
                [mushroom_x + 2, mushroom_y] in level["level"]["objects"]["pipe"]:
            fitness -= 1
        if [mushroom_x + 1, mushroom_y] in level["level"]["entities"]["coinBrick"] or \
                [mushroom_x + 2, mushroom_y] in level["level"]["entities"]["coinBrick"]:
            fitness -= 1

    # Check that there is enough space for Mario to move where the mushroom is
    for mushroom in level["level"]["entities"]["Goomba"]:
        mushroom_x, mushroom_y = mushroom[0], mushroom[1]
        for x in range(mushroom_x, mushroom_x + 3):
            if [x, mushroom_y + 1] in level["level"]["objects"]["pipe"]:
                fitness -= 1
            if [x, mushroom_y + 1] in level["level"]["entities"]["coinBrick"]:
                fitness -= 1

    # Check that Mario can reach a coin
    for coin in level["level"]["entities"]["coin"]:
        coin_x, coin_y = coin[0], coin[1]
        for x in range(coin_x, coin_x + 3):
            if [x, coin_y + 1] in level["level"]["objects"]["pipe"]:
                fitness -= 1
            if [x, coin_y + 1] in level["level"]["entities"]["coinBrick"]:
                fitness -= 1


    return fitness

def crossover_mutation(level1, level2, crossover_percentage, mutation_percentage):
    """
        Perform crossover and mutation on two levels.

        Args:
            level1 (dict): The first level.
            level2 (dict): The second level.
            crossover_pct (float): The percentage of genetic material to exchange.
            mutation_pct (float): The percentage of genetic material to mutate.

        Returns:
            A new level that is a crossover of level_a and level_b with mutations applied.
        """
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
                if len1 < len2:
                    level1["level"]["objects"][object][i] = random.choice(level2["level"]["objects"][object][i])

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
        population.append(generate_chromosome(60))
    return population


def save_level_to_file(level):
    with open("levels/Level1-3.json", "w") as f:
        json.dump(level, f, indent=1)




def selection(population, size, top_candidate_selection_size):
    # Calculate fitness for each individual in the population
    pop_fitness = [calculate_fitness(individual) for individual in population]

    # Sort the population by fitness in descending order
    sorted_pop = [x for _, x in sorted(zip(pop_fitness, population), key=lambda x: x[0], reverse=True)]

    # Select the top candidates with highest fitness
    num_top_candidates = top_candidate_selection_size
    top_candidates = sorted_pop[:num_top_candidates]

    # Print the fitness values of the top candidates
    for candidate in top_candidates:
        print(calculate_fitness(candidate))

    return top_candidates

def genetic_algorithm(population_size, num_generations, crossover_pct, mutation_pct):
    # Generate an initial population of individuals.
    population = generate_population(population_size)

    # Evaluate the fitness of each individual in the population.
    fitness_scores = [calculate_fitness(individual) for individual in population]

    # Keep track of the best individual in each generation.
    best_individuals = [max(zip(fitness_scores, population))[1]]

    for i in range(num_generations):
        # Select parents based on their fitness.
        parents = selection(population, population_size//2, population_size//4)

        # Create offspring by applying genetic operators to the parents.
        offspring = []
        for j in range(population_size//2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover_mutation(parent1, parent2, crossover_pct, mutation_pct)
            offspring.append(child)

        # Evaluate the fitness of the offspring.
        offspring_fitness_scores = [calculate_fitness(individual) for individual in offspring]

        # Select the best individuals from the parent and offspring populations.
        combined_population = population + offspring
        combined_fitness_scores = fitness_scores + offspring_fitness_scores
        sorted_population = [x for _, x in sorted(zip(combined_fitness_scores, combined_population), key=lambda x: x[0], reverse=True)]
        population = sorted_population[:population_size]
        fitness_scores = [calculate_fitness(individual) for individual in population]

        # Record the best individual in this generation.
        best_individuals.append(max(zip(fitness_scores, population))[1])

    return best_individuals
c1 = genetic_algorithm(40,10,50,10)
save_level_to_file(c1)

