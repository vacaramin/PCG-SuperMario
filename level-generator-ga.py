import random
import json
import numpy as np

# Improved
# Initial population.
# Fitness function.
# Selection.
# Crossover.
# Mutation.


def calculate_fitness(level):
    fitness = 0

    # more entities, fitter the chromosome is
    fitness += 1 * ((1 * len(level["level"]["entities"]["CoinBox"])) + (
            1 * len(level["level"]["entities"]["coinBrick"])) + (1 * len(level["level"]["entities"]["coin"])) + (
                             1 * len(level["level"]["entities"]["Goomba"])) + (
                             1 * len(level["level"]["entities"]["Koopa"])) + (
                             1 * len(level["level"]["entities"]["RandomBox"])))

    # If enemy is close to mario's initial position at start of game, it might kill mario before he could
    # make a move so there should be negative fitness points for it.
    #mushroom initial position
    for enemy in level["level"]["entities"]["Goomba"]:
        if enemy[0] < 13:
            fitness -= 16
    #Turtle initial position
    for enemy in level["level"]["entities"]["Koopa"]:
        if enemy[0] < 13:
            fitness -= 16
    #the brick and coin must not overlap
    for coin in level['level']['entities']['coin']:
        for brick in level['level']['objects']['ground']: 
            if coin[0]==brick[0] and coin[1]==brick[1]:
                fitness-=7
    for coin in level['level']['entities']['coin']:
        for pipe in level['level']['objects']['pipe']: 
            if coin[0]==pipe[0] and coin[1]==pipe[1]:
                fitness-=10
    #considerate amount of pipes and holes
    if len(level['level']['objects']['sky'])>2:
        fitness+=10
    if len(level['level']['objects']['pipe'])>2:
        fitness+=10
    # if hole is at mario's initial position at start of game, it might kill mario before he could make a move
    # so there should be less negative fitness points for it.
    for hole in level['level']['objects']['sky']:
        if hole[0] < 7:
            fitness -= 15

    # there should not be any brick/hole/ground on the pipe
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['entities']['RandomBox']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 3  >= randombox[1]):
                fitness -= 12
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['entities']['CoinBox']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 3 >= randombox[1]):
                fitness -= 12
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['entities']['coinBrick']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 3 >= randombox[1]):
                fitness -= 12
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['objects']['ground']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 3 >= randombox[1]):
                fitness -= 12
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['objects']['sky']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 3 >= randombox[1]):
                fitness -= 12

    # There shouldn't be a brick close to top of the pipe is
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['entities']['RandomBox']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 5  >= randombox[1]):
                fitness -= 10
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['entities']['CoinBox']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 5 >= randombox[1]):
                fitness -= 10
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['entities']['coinBrick']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 5 >= randombox[1]):
                fitness -= 10
    for pipe in level['level']['objects']['pipe']:
        for randombox in level['level']['objects']['ground']:
            if (pipe[0] <= randombox[0] and pipe[0] +2 >= randombox[0]) and (pipe[1] <= randombox[1] and pipe[1] - 5 >= randombox[1]):
                fitness -= 10

    # Pipes should not be that close that they should stack on each other
    for pipe1 in level['level']['objects']['pipe']:
        for pipe2 in level['level']['objects']['pipe']:
            if not (pipe1[0] == pipe2[0] and pipe1[1] == pipe2[1]):
                if abs(pipe1[0] - pipe2[0]) <= 4:
                    fitness -= 15

    # the coin should not be high enough to be reached
    for coin in level['level']['entities']['coin']:
        if coin[1] < 11 and coin[1] > 3:
            fitness += 3
        else:
            fitness -= 3
    #considerate amount of enemies
    if len(level['level']['entities']['Goomba'])<5 and len(level['level']['entities']['Koopa'])<5:
        fitness+=5
    else:
        fitness-=5
    # complete hole more fitness

    for hole in level['level']['objects']['sky']:
        if hole[1] == 14:
            fitness += 5
    #random box and coin box must not be too much greater in height
    for randombox in level['level']['entities']['RandomBox']:
        if randombox[1]>5:
            fitness+=5
    for coinbox in level['level']['entities']['CoinBox']:
        if coinbox[1]>5:
            fitness+=5

    # Pipes should not be that close that they should stack on each other
    for brick1 in level['level']['entities']['RandomBox']:
        for brick2 in level['level']['entities']['CoinBox']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[0] - brick2[0]) <= 4:
                    fitness -= 2
    for brick1 in level['level']['entities']['RandomBox']:
        for brick2 in level['level']['entities']['coinBrick']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[0] - brick2[0]) <= 4:
                    fitness -= 2
    for brick1 in level['level']['entities']['RandomBox']:
        for brick2 in level['level']['objects']['ground']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[0] - brick2[0]) <= 4:
                    fitness -= 2
    for brick1 in level['level']['entities']['coinBrick']:
        for brick2 in level['level']['objects']['ground']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[0] - brick2[0]) <= 4:
                    fitness -= 2
    for brick1 in level['level']['entities']['coinBrick']:
        for brick2 in level['level']['entities']['CoinBox']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[0] - brick2[0]) <= 4:
                    fitness -= 2
    for brick1 in level['level']['entities']['CoinBox']:
        for brick2 in level['level']['objects']['ground']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[0] - brick2[0]) <= 4:
                    fitness -= 2

# Bricks in horizontal line will have better fitness
    # Pipes should not be that close that they should stack on each other
    for brick1 in level['level']['entities']['RandomBox']:
        for brick2 in level['level']['entities']['CoinBox']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[1] - brick2[1]) == 0:
                    fitness += 5
    for brick1 in level['level']['entities']['RandomBox']:
        for brick2 in level['level']['entities']['coinBrick']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[1] - brick2[1]) == 0:
                    fitness += 5
    for brick1 in level['level']['entities']['RandomBox']:
        for brick2 in level['level']['objects']['ground']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[1] - brick2[1]) == 0:
                    fitness += 5
    for brick1 in level['level']['entities']['coinBrick']:
        for brick2 in level['level']['objects']['ground']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[1] - brick2[1]) == 0:
                    fitness += 5
    for brick1 in level['level']['entities']['coinBrick']:
        for brick2 in level['level']['entities']['CoinBox']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[1] - brick2[1]) == 0:
                    fitness += 5
    for brick1 in level['level']['entities']['CoinBox']:
        for brick2 in level['level']['objects']['ground']:
            if not (brick1[0] == brick2[0] and brick1[1] == brick2[1]):
                if abs(brick1[1] - brick2[1]) == 0:
                    fitness += 5

    return fitness


def crossover_mutation(level1, level2, crossover_percentage, mutation_percentage):
    # swapping object
    objects = ["bush", "sky", "cloud", "pipe", "ground"]

    for object in objects:
        len1 = len(level1["level"]["objects"][object])
        len2 = len(level2["level"]["objects"][object])

        # calculate crossover point
        crossover_point = int(crossover_percentage / 100 * len1)
        #print(crossover_point)
        #print('over to you')
        # perform crossover
        level1["level"]["objects"][object][:crossover_point], level2["level"]["objects"][object][:crossover_point] = \
        level2["level"]["objects"][object][:crossover_point], level1["level"]["objects"][object][:crossover_point]

        # perform mutation
        for i in range(len1):
            if random.random() < mutation_percentage / 100:
                #print(i,len(level1['level']['objects'][object]))
               # print('yikes')
                if i<len(level1['level']['objects'][object]):
                    level1["level"]["objects"][object][i] = random.choice(level2["level"]["objects"][object])

    print("crossover, Mutation")
    return level1


def generate_chromosome(length_of_level):
    # defining the length of levelp
    length_of_level_x = length_of_level
    length_of_level_y = 13

    # Defining a range for X and Y for each item in level, so the random values are not out of bound
    valid_x_bush = list(range(2, 60))
    valid_y_bush = 12

    valid_x_sky = list(range(0, 50))
    valid_y_sky = 0  # list(range(13, 14)) should be 13, 14 so both can be a hole

    valid_x_cloud = list(range(1, length_of_level_x))
    valid_y_cloud = list(range(3, 6))

    valid_x_pipe = list(range(8, length_of_level_x))
    valid_y_pipe = list(range(9, 12))

    valid_x_ground = list(range(0, length_of_level_x))
    valid_y_ground = list(range(3, 12))

    valid_layer_x_sky = [0, length_of_level_x]
    valid_layer_y_sky = [0, 13]

    valid_layer_x_ground = [0, length_of_level_x]
    valid_layer_y_ground = [14, 16]

    valid_x_coinbox = list(range(4, length_of_level_x - 2))
    valid_y_coinbox = list(range(4, 8))

    valid_x_coinbrick = list(range(0, length_of_level_x))
    valid_y_coinbrick = list(range(4, 9))

    valid_x_coin = list(range(0, length_of_level_x))
    valid_y_coin = list(range(3, 12))

    valid_x_goomba = list(range(0, length_of_level_x))  # mushroom
    valid_y_goomba = list(range(4, 12))

    valid_x_koopa = list(range(0, length_of_level_x))  # mushroom
    valid_y_koopa = list(range(4, 12))

    valid_x_random_box = list(range(0, length_of_level_x))
    valid_y_random_box = list(range(0, length_of_level_y - 6))

    noOfBush = 10
    noOfSky = 10
    noOfCloud = 10
    noOfPipe = 10
    noOfGround = 10
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
    obj_count = 2 + random.randint(1, noOfBush)
    for j in range(obj_count):
        x = random.choice(valid_x_bush)
        y = valid_y_bush
        level["level"]["objects"]["bush"].append([x, y])

    # Generate Sky
    obj_count = 2 + random.randint(1, noOfSky)
    for j in range(obj_count):
        x = random.choice(valid_x_sky)
        # y = random.choice(valid_y_sky)
        level["level"]["objects"]["sky"].append([x, 14])
        level["level"]["objects"]["sky"].append([x, 13])

    # Generate Cloud
    obj_count = 2 + random.randint(1, noOfCloud)
    for j in range(obj_count):
        x = random.choice(valid_x_cloud)
        y = random.choice(valid_y_cloud)
        level["level"]["objects"]["cloud"].append([x, y])

    # Generate Pipe
    obj_count = 2 + random.randint(1, noOfPipe)
    for j in range(obj_count):
        x = random.choice(valid_x_pipe)
        y = random.choice(valid_y_pipe)
        level["level"]["objects"]["pipe"].append([x, y, 0])

    # Generate ground
    obj_count = 2 + random.randint(1, noOfGround)
    for j in range(obj_count):
        x = random.choice(valid_x_ground)
        y = random.choice(valid_y_ground)
        level["level"]["objects"]["ground"].append([x, y])

    level["level"]["layers"]["sky"]["x"] = valid_layer_x_sky
    level["level"]["layers"]["sky"]["y"] = valid_layer_y_sky

    level["level"]["layers"]["ground"]["x"] = valid_layer_x_ground
    level["level"]["layers"]["ground"]["y"] = valid_layer_y_ground

    # Generate coinbox
    obj_count = 2 + random.randint(3, noOfCoinBox)
    for j in range(obj_count):
        x = random.choice(valid_x_coinbox)
        y = random.choice(valid_y_coinbox)
        level["level"]["entities"]["CoinBox"].append([x, y])
    level["level"]["entities"]["CoinBox"].append([4, 8])

    # Generate coinbrick
    obj_count = 2 + random.randint(3, noOfCoinBrick)
    for j in range(obj_count):
        x = random.choice(valid_x_coinbrick)
        y = random.choice(valid_y_coinbrick)
        level["level"]["entities"]["coinBrick"].append([x, y])

    # Generate coin
    obj_count = 2 + random.randint(0, noOfcoin)
    for j in range(obj_count):
        x = random.choice(valid_x_coin)
        y = random.choice(valid_y_coin)
        level["level"]["entities"]["coin"].append([x, y])

    # Generate goomba
    obj_count = 1 + random.randint(3, noOfGoomba)
    for j in range(obj_count):
        x = random.choice(valid_x_goomba)
        y = random.choice(valid_y_goomba)
        level["level"]["entities"]["Goomba"].append([y, x])

    # Generate koopa
    obj_count = 1 + random.randint(3, noOfKoopa)
    for j in range(obj_count):
        x = random.choice(valid_x_koopa)
        y = random.choice(valid_y_koopa)
        level["level"]["entities"]["Koopa"].append([y, x])
    # Generate RandomBox
    obj_count = 1 + random.randint(3, noOfKoopa)
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


def selection(population, size, top_candidate_selection_size,threshold):
    # Calculate fitness for each individual in the population
    pop_fitness = np.array([calculate_fitness(individual) for individual in population])
    """THE THRESHOLD PART
    pop_fitness1=[]
    pop_fitness=(pop_fitness/100)% 1.1
    population1=[]
    for i in range(len(pop_fitness)):
        if i>=threshold:
            pop_fitness1.append(pop_fitness[i])
            population1.append(population[i])
    population=population1
    pop_fitness=pop_fitness1
    ENDING OF THRESHOLD PART"""
    #Ordering the fitness list in descending manner
    ko=np.argsort(np.array(pop_fitness))
    pop_fitness=ko[::-1][:len(ko)]
    
    # Sort the population by fitness in descending order
    
    sorted_pop = [population[i] for i in pop_fitness]
    
    # Select the top candidates with highest fitness
    num_top_candidates = top_candidate_selection_size
    top_candidates = sorted_pop[:num_top_candidates]

    # Print the fitness values of the top candidates
    for candidate in top_candidates:
        print(calculate_fitness(candidate))

    return top_candidates


# population = generate_population(40)
# pop_fitness = []
# for i in range(0,40):
#     pop_fitness.append(calculate_fitness(population[i]))
#
# print(pop_fitness)

#c1 = generate_chromosome(60)
#c2 = generate_chromosome(60)

population = generate_population(400)
parents = selection(population,400,100)
for i in range(400):
    offspring=[]
    for j in range(400):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover_mutation(parent1, parent2, 50, 5)
            offspring.append(child)
    parents=selection(offspring,len(offspring),100,0.5)
    


save_level_to_file(parents[0])
