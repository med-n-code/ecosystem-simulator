import random
import matplotlib.pyplot as plt
import time as t
from animal import Zebra, Lion
from grid_cell import Grid_cell


def initialize_population(grid, grid_size, number_zebra, number_lion):
    """
    Initializes the grid by placing animals onto it.

    Parameters
    ----------
    number_lion
    number_zebra
    grid : list of lists of Grid_cells (2D array of Grid_cells)
        All the cells in the simulation's grid with their indices
        correlating to their position.
    grid_size : int
        The size of the grid.

    Returns
    -------
    animal_positions : list of tuples of ints
        All the positions on the grid where animals are.
    """

    # All possible position on the grid
    all_positions = [(a, b) for a in range(grid_size) for b in range(grid_size)]
    all_animals = []

    # Create zebras, each in a grid cell
    for i in range(number_zebra):
        # Random choice from all_positions, which is removed from selection afterwards
        position = all_positions.pop(random.randint(0, len(all_positions) - 1))

        all_animals.append(Zebra(grid[position[0]][position[1]], False))

    # Create lions, each in a grid cell
    for i in range(number_lion):
        # Random choice from all_positions, which is removed from selection afterwards
        position = all_positions.pop(random.randint(0, len(all_positions) - 1))

        all_animals.append(Lion(grid[position[0]][position[1]], False))

    return all_animals


def print_grid(all_animals, grid_size):
    """ Prints the grid
    Args:
       all_animals (list of animals): The animals in the ecosystem
       grid_size (int): The size of the grid
    Returns:
       Nothing
    Behavior:
       Prints the grid
    """

    # get the set of tuples where lions and zebras are located
    lions_tuples = {a.get_position() for a in all_animals if a.species == "Lion"}
    zebras_tuples = {a.get_position() for a in all_animals if a.species == "Zebra"}

    print("*" * (grid_size + 2))
    for row in range(grid_size):
        print("*", end="")
        for col in range(grid_size):
            if (row, col) in lions_tuples:
                print("L", end="")
            elif (row, col) in zebras_tuples:
                print("Z", end="")
            else:
                print(" ", end="")
        print("*")
    print("*" * (grid_size + 2))


def sort_lists(all_animals, animal_positions):
    """
    Sorts both animals and their positions LRTB. The lists
    will end up aligned such that the position of the animal
    at index i in all_animals is the tuple at index i in
    animal_positions.

    Parameters
    ----------
    all_animals : list of Animals
        The animals (zebras and lions) in the simulation.
    animal_positions : list of tuples of ints
        The positions of the animals in the simulation.

    Returns
    -------
    None.
    """

    sort_animals(all_animals)  # sort animals
    sort_positions(animal_positions)  # sort positions


def sort_animals(all_animals):
    """ Sorts the animals, left to right and top to bottom
    Args:
       all_animals (list of animals): The animals in the ecosystem
    Returns:
       Nothing
    Behavior:
       Sorts the list of animals
    """

    def get_key(a):
        return a.get_row() + 0.001 * a.get_column()

    all_animals.sort(key=get_key)


def sort_positions(animal_positions):

    def get_key(a):
        return a[0] + 0.001 * a[1]

    animal_positions.sort(key=get_key)


def remove_dead_animals(dead_index, all_animals, animal_positions):
    """
    Removes elements in all_animals and animal_positions at
    the indices specified in dead_index.

    Parameters
    ----------
    dead_index : list of ints
        The indices in all_animals and animal_positions which are dead
        animals to be removed from the simulation.
    all_animals : list of Animals
        The animals (zebras and lions) in the simulation.
    animal_positions : list of tuples of ints
        The positions of the animals in the simulation.

    Returns
    -------
    None.
    """

    # indices must be in reverse order so as not to 
    # change any other index in both lists
    dead_index.sort(reverse=True)

    # cycle through indices indicating dead animals
    # and remove them from both lists
    for i in dead_index:
        del (all_animals[i])
        del (animal_positions[i])


def age_hunger(all_animals, animal_positions):
    """
    Increases the age of animals and checks if they have died of
    hunger or of old age. Animals who die have their index placed
    in a list for removal after the whole increase and check is done

    Parameters
    ----------
    all_animals : list of Animals
        The animals (zebras and lions) in the simulation.
    animal_positions : list of tuples of ints
        The positions of the animals in the simulation.

    Returns
    -------
    None.
    """

    dead_index = []  # list of animals that have died, to be removed after
    animal_index = 0  # keep track of the current animal's index

    # loop through all_animals and animal_positions in parallel
    # since need to test animal's info and save position if dead
    for animal in all_animals:
        animal.time_passes()

        # die of old age -> save event descript., add animal to death list
        if (animal.dies_of_old_age() or animal.dies_of_hunger()):
            dead_index.append(animal_index)
            animal.set_dead()

        animal_index += 1

    # remove dead animals from animals in ecosystem list and reset death list for later
    remove_dead_animals(dead_index, all_animals, animal_positions)
    dead_index.clear()


def move_animals(all_animals, animal_positions, grid):
    """
    Manages the movement of all animals in the simulation every round.
    Each animal is checked in LRTB order for moving opportunity.
    The possible neighbours are generated from the animal's associated
    cell and one (if exists) is selected as its new location. If a lion
    moves onto a zebra, it eats it; if a zebra moves onto a lion, it is
    eaten. Animals of the same species can't move onto one another.
    The indices of animals eaten during this operation are recorded and
    later removed from the simulation's lists.

    Parameters
    ----------
    all_animals : list of Animals
        The animals (zebras and lions) in the simulation.
    animal_positions : list of tuples of ints
        The positions of the animals in the simulation.
    grid : list of lists of Grid_cells (2D array of Grid_cells)
        All the cells in the simulation's grid with their indices
        correlating to their position.

    Returns
    -------
    None.
    """

    index_animal = 0  # keep track of the current animal's index
    dead_index = []  # list of animals that have died, to be removed after

    for animal in all_animals:

        # only move if alive
        if (animal.alive):
            # potential new location (row, col)
            selected_neighbour = animal.pick_neighbour(all_animals, animal_positions)
            move_position = selected_neighbour.position

            # if new location is occupied -> save animal occupying it, check if eating happens
            if (move_position in animal_positions):
                index_other = animal_positions.index(move_position)  # index of other animal
                target_position_animal = all_animals[index_other]  # other animal

                # check if-elif each animal in the pair can eat the other
                if (animal.can_eat(target_position_animal)):
                    # add meal (the one move to) to dead list
                    dead_index.append(index_other)
                    target_position_animal.set_dead()

                    # move the animal out of the way in the position list
                    animal_positions[index_other] = (-1, -1)

                    animal.time_since_last_meal = 0  # refresh last meal of eater

                    # if current animal in loop can eat -> also moves
                    animal.set_position(grid[move_position[0]][move_position[1]])
                    animal_positions[index_animal] = move_position

                elif (target_position_animal.can_eat(animal)):
                    # add index of animal that was moving to dead list
                    dead_index.append(index_animal)
                    animal.set_dead()

                    # move the animal out of the way in the position list
                    animal_positions[index_animal] = (-1, -1)

                    # refresh last meal of eater
                    target_position_animal.time_since_last_meal = 0

            # location isn't occupied -> just move
            else:
                animal.set_position(grid[move_position[0]][move_position[1]])
                animal_positions[index_animal] = move_position

        index_animal += 1

    # remove dead animals from animals in ecosystem list and reset death list for later
    remove_dead_animals(dead_index, all_animals, animal_positions)
    dead_index.clear()


def reproduce_animals(all_animals, animal_positions):
    """
    Manages the reproduction of all animals in the simulation every round.
    Each animal is checked in LRTB order for reproduction opportunity.

    Parameters
    ----------
    all_animals : list of Animals
        The animals (zebras and lions) in the simulation.
    animal_positions : list of tuples of ints
        The positions of the animals in the simulation.

    Returns
    -------
    None.
    """

    children = []  # new animals to be added to the simulation

    for animal in all_animals:

        if (animal.can_reproduce()):
            offspring_cell = animal.get_offspring_position(all_animals, animal_positions)

            # cell for offspring found -> add offspring to list and its position
            if (offspring_cell != None):
                print("WOOHOO")
                children.append(animal.get_child(offspring_cell))
                animal_positions.append(offspring_cell.get_position())

    # add children to all_animals list
    all_animals.extend(children)


def run_whole_simulation(grid_size, simulation_duration,
                         repeat_count, number_zebra, number_lion):
    """
    

    Parameters
    ----------
    grid_size : int
        The size of the grid for the simulation.
    simulation_duration : int
        Duration of an individual simulation (time periods).
    repeat_count : int
        Number of times to repeat a simulation to obtain an average.
    number_zebra : int
        Number of zebras at the beginning of each repetition of a simulation.
    number_lion : int
        Number of lions at the beginning of each repetition of a simulation..

    Returns
    -------
    None.
    """

    # how many time periods will be completed overall
    total_runs = repeat_count * simulation_duration

    # to store the number of zebras and lions every step (month)
    zebra_count = [[0 for j in range(simulation_duration)] for k in range(repeat_count)]
    lion_count = [[0 for j in range(simulation_duration)] for k in range(repeat_count)]

    print("")  # string management for console

    start_time = t.time()

    for repeat in range(repeat_count):
        # List of grid cells, with the indices (i,j) representing (row,col)
        grid = [[Grid_cell((a, b)) for b in range(grid_size)] for a in range(grid_size)]

        # Let each cell create a list of neighbouring cells
        for i in range(len(grid)):

            for j in range(len(grid[i])):
                grid[i][j].define_neighbours(grid)

        all_animals = initialize_population(grid, grid_size, number_zebra, number_lion)  # initialize all animals
        animal_positions = [a.get_position() for a in all_animals]  # get positions of animals

        # run through the whole simulation
        for time in range(simulation_duration):

            sort_lists(all_animals, animal_positions)
            age_hunger(all_animals, animal_positions)
            move_animals(all_animals, animal_positions, grid)
            sort_lists(all_animals, animal_positions)
            reproduce_animals(all_animals, animal_positions)

            """
            if(time >= 30 or time <= 5): 
                print(time)
                print_grid(all_animals, grid_size)
                print("")
            """

            if (time % (simulation_duration // 5) == 0):
                progress = repeat * simulation_duration + time
                print("\r%d%% complete" % ((100 * progress) / total_runs), end="")

            # stores the current number of zebras and lions for plotting
            zebra_count[repeat][time] = (sum([1 for a in all_animals if a.species == "Zebra"]))
            lion_count[repeat][time] = (sum([1 for a in all_animals if a.species == "Lion"]))

    print("\r100% complete", end="")
    print("")

    print(t.time() - start_time)

    i, j = 0, 0

    # calculate averages for each time period in a simulation over all repetitions
    zebra_average = [(sum([zebra_count[i][j] for i in range(repeat_count)]) / repeat_count)
                     for j in range(simulation_duration)]
    lion_average = [(sum([lion_count[i][j] for i in range(repeat_count)]) / repeat_count)
                    for j in range(simulation_duration)]

    # calculate medians for each time period in a simulation over all repetitions
    # zebra_median = [(stat.median([zebra_count[i][j] for i in range(repeat_count)]))
    #               for j in range(simulation_duration)]
    # lion_median = [(stat.median([lion_count[i][j] for i in range(repeat_count)]))
    #               for j in range(simulation_duration)]

    # calculate modes for each time period in a simulation over all repetitions
    # zebra_mode = [(stat.mode([zebra_count[i][j] for i in range(repeat_count)]))
    #                 for j in range(simulation_duration)]
    # lion_mode = [(stat.mode([lion_count[i][j] for i in range(repeat_count)]))
    #               for j in range(simulation_duration)]

    # plot all stats lists with appropriate colour and label
    plt.plot(zebra_average, "r", label="Average Zebra")
    plt.plot(lion_average, "b", label="Average Lion")
    # plt.plot(zebra_median, "tab:orange", label = "Med Z")
    # plt.plot(lion_median, "tab:purple", label = "Med L")
    # plt.plot(zebra_mode, "tab:pink", label = "Mod Z")
    # plt.plot(lion_mode, "tab:cyan", label = "Mod L")

    # add axis labels
    plt.xlabel("time")
    plt.ylabel("Number of individuals")

    plt.legend(loc="best")  # add legend

    title = """
            Simulation of %d time periods, repeated %d time%s and averaged.
            """ % (simulation_duration, repeat_count, "s" if (repeat_count > 1) else "")

    plt.title(title)

    description = "Initial random age = [0 : 1/2 max age].\n" \
                  "Max age random within fixed range.\n" \
                  "Reproduction at specific times.\n" \
                  "Lion will eat nearby zebra.\n" \
                  "Zebras avoid moving onto lions.\n" \
                  "Zebras NEVER die of hunger.\n"

    plt.gca().set_position((.1, .2, .8, .7))

    plt.figtext(0.5, 0.0, description, fontsize="large", horizontalalignment="center")

    # save plot to the specified file
    # plt.savefig(image_file_name)


run_whole_simulation(grid_size=20, simulation_duration=50,
                     repeat_count=1, number_zebra=26,
                     number_lion=10)

print("Simulation complete")
