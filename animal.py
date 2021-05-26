# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 14:16:25 2020

@author: med-n-code
"""

import random

class Animal():
    
    # Initializer method
    def __init__(self, species, cell, max_age, reproduction_time, is_new_born):
        """
        Initializes a new animal

        Parameters
        ----------
        species : str
            DESCRIPTION.
        cell : Grid_cell
            DESCRIPTION.
        max_age : int
            DESCRIPTION.
        reproduction_time : int
            DESCRIPTION.
        is_new_born : boolean
            DESCRIPTION.

        Returns
        -------
        None.
        """
                     
        self.species = species
        self.cell = cell
        self.MAX_AGE = max_age
        self.REPRODUCTION_TIME = reproduction_time
        
        if(is_new_born):
            self.age = 0
        
        else:
            self.age = random.randint(0, self.MAX_AGE // 2)
            
        self.time_since_last_meal = 0
        self.time_since_reproduction = 0
        
        # stores if an animal is alive or dead, used for movement in simulation
        self.alive = True

    def __str__(self):
        """ Creates a string from an object
        Args:
           self (Animal): the object on which the method is called
        Returns:
           str: String summarizing the object
        """
        
        s = self.species + " at position "+ str(self.position) +":, age="+str(self.age)+", time_since_last_meal="+\
           str(self.time_since_last_meal)
        return s
    
    
    def get_position(self): return self.cell.get_position()
    
    def get_row(self): return self.cell.get_row()
    
    def get_column(self): return self.cell.get_column()
    
    def get_all_neighbours(self, up_to_distance = 1):
        return self.cell.get_neighbours(up_to_distance)
    
    def get_can_reproduce(self): return self.can_reproduce
    
    
    def set_position(self, cell):
        """
        Sets the location of the animal.

        Parameters
        ----------
        cell : Grid_cell
            DESCRIPTION.

        Returns
        -------
        None.
        """
        
        self.cell = cell
        
        
    def set_dead(self):
        """
        Sets animal's state to dead and moves it
        off the map until it is removed entirely

        Returns
        -------
        None.

        """
        
        # dead to prevent movement and off the map to free up
        # cell for movement of other animal until permanently removed
        self.alive = False
        self.cell = None
    
    
    def can_eat(self, other):
        """
        Checks if self can eat other.

        Parameters
        ----------
        other : Animal
            another animal (zebra or lion).

        Returns
        -------
        boolean
            True if self can eat other, and False otherwise.

        """       
        
        # the only possible case of eating is if the attacker is a Lion
        # and the victim is a Zebra
        return (self.species == "Lion" and other.species == "Zebra")


    def time_passes(self):
        """
        Increases time-based attributes

        Returns
        -------
        None.
        """
        
        # one time step is added to age and time since last meal
        self.age += 1
        self.time_since_last_meal += 1
        self.time_since_reproduction += 1
        
        
    def can_reproduce(self):
        """
        Determines if an animal will reproduce.

        Returns
        -------
        None.
        """
        
        # possible conditions of reproduction for each species
        return (self.time_since_reproduction >= self.REPRODUCTION_TIME)


    def dies_of_old_age(self):
        """
        Determines if an animal dies of old age.

        Returns
        -------
        boolean
            True if animal dies of old age, False otherwise.

        """
        
        # age reached max age
        return (self.age == self.MAX_AGE)


    def dies_of_hunger(self):
        """
        Determines if an animal dies of hunger.

        Returns
        -------
        boolean
            True if animal dies of hunger, False otherwise.
            
        """
        
        # possible conditions of hunger death by species
        return (self.species == "Lion" and self.time_since_last_meal == 6)
        
    
    def get_offspring_position(self, all_animals, animal_positions):
        """
        ...

        Parameters
        ----------
        animal_positions : list of tuples of ints
            The positions of the animals in the simulation.

        Returns
        -------
        Grid_cell
            DESCRIPTION.

        """
        
        # immediate neighbours of animal
        # list of lists of Grid_cells [[GC, GC, ...],...]
        list_neighbours = self.get_all_neighbours(up_to_distance = 1)
        
        # positions of immediate neighbour animals
        neighbour_positions = [n.get_position for n in list_neighbours[0]
                                   if(n.get_position in animal_positions)]
        
        # list of animals around self, of the same species, and capable of reproducing
        possible_parent = [a for a in all_animals
                           if(a.get_position() in neighbour_positions and 
                              a.species == self.species and a.can_reproduce())]
        
        # existential check for parent
        if(len(possible_parent) > 0):
            # choose a random parent
            parent = possible_parent[random.randint(0, len(possible_parent) - 1)]
            
            # find all neighbours immediate to either parents (self and parent)
            neighbours_parent_1 = set(list_neighbours)
            neighbours_parent_2 = set(parent.get_all_neighbours(up_to_distance = 1))
            potential_offspring_position = neighbours_parent_1.union(neighbours_parent_2)
            
            # exclude position of parents themselves
            parent_positions = set([self.get_position(), parent.get_position()])
            potential_offspring_position.difference_update(parent_positions)
            
            # existential check for position
            if(len(potential_offspring_position) > 0):
                # update reproduction time
                self.time_since_reproduction = 0
                parent.time_since_reproduction = 0
                
                # choose random position and return it
                selected_index = random.randint(0, len(potential_offspring_position) - 1)
                return potential_offspring_position[selected_index]
            
            else:
                print("location fail")
                
        else:
            print("parent fail")
        
        return None # no parent found, or no position found
    
        """
        available_neighbours = self.cell.get_available_neighbours(animal_positions)
        
        if(len(available_neighbours[0]) == 0):
            return None
        
        else:
            return available_neighbours[0][random.randint(0, len(available_neighbours[0]) - 1)]
        """
        
    # end of Animal class
    
    
class Zebra(Animal):
    
    def __init__(self, cell, is_new_born):
        
        species = "Zebra"
        max_age = random.randint(8, 10)
        reproduction_time = random.randint(3, 4)
        
        Animal.__init__(self, species, cell, max_age, reproduction_time, is_new_born)
        
        
    def get_child(self, cell):
        """
        Creates an instance of Zebra, child of the instance that was called

        Parameters
        ----------
        cell : Grid_cell
            DESCRIPTION.

        Returns
        -------
        Zebra(Animal)
            An instance of Zebra, child of the instance that was called

        """
        
        return Zebra(cell, True)
    
    
    def pick_neighbour(self, all_animals, animal_positions):
        """
        ...

        Parameters
        ----------
        all_animals : list of Animals
            The animals (zebras and lions) in the simulation.
        animal_positions : list of tuples of ints
            The positions of the animals in the simulation.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        #avoid_positions = [animal_positions[i] for i in range(len(animal_positions))]
        
        available_neighbours = self.cell.get_available_neighbours(animal_positions)
        
        if(len(available_neighbours[0]) == 0):
            return self.cell
        
        else:
            return available_neighbours[0][random.randint(0, len(available_neighbours[0]) - 1)]
    
    
    
    # End of Zebra class
    
    
class Lion(Animal):
    
    def __init__(self, cell, is_new_born):
        
        self.aggressivity = round(random.random(), 2)
        
        species = "Lion"
        max_age = random.randint(16, 22)
        reproduction_time = random.randint(6, 8)
        
        Animal.__init__(self, species, cell, max_age, reproduction_time, is_new_born)
        
        
    def get_child(self, cell):
        """
        Creates an instance of Lion, child of the instance that was called

        Parameters
        ----------
        cell : Grid_cell
            DESCRIPTION.

        Returns
        -------
        Lion(Animal)
            An instance of Lion, child of the instance that was called

        """
        
        return Lion(cell, True)
    
    def pick_neighbour(self, all_animals, animal_positions):
        """
        ...

        Parameters
        ----------
        all_animals : list of Animals
            The animals (zebras and lions) in the simulation.
        animal_positions : list of tuples of ints
            The positions of the animals in the simulation.

        Returns
        -------
        Grid_cell
            DESCRIPTION.

        """
        
        # list of animal position excluding positions held by Lions
        avoid_positions = [animal_positions[i] for i in range(len(animal_positions))
                           if(isinstance(all_animals[i], Lion))]
        
        # get neighbours containing zebras or empty (lions excluded by avoid list)
        available_neighbours = self.cell.get_available_neighbours(avoid_positions)
        other_neighbours = []
        zebra_neighbours = []
        
        # classify neighbours as being empty or containing zebras
        for neighbour in available_neighbours[0]:
            
            if(not(neighbour.position in animal_positions)):
                other_neighbours.append(neighbour)
            
            elif(all_animals[animal_positions.index(neighbour.position)].species == "Zebra"):
                zebra_neighbours.append(neighbour)
                
            else:
                print("Error in neighbour selection... have fun!")
        
        # move to zebra neighbours either on chance or if no empty neighbour
        # only if zebra neighbours exist
        if(len(zebra_neighbours) > 0):
            return zebra_neighbours[random.randint(0, len(zebra_neighbours) - 1)]
        
        # move to empty neighbours based on chance and empty neighbours existing
        elif(len(other_neighbours) > 0):
            return other_neighbours[random.randint(0, len(other_neighbours) - 1)]
        
        # if surrounded by lions, don't move (returning own positions will prevent moving)
        else:
            return self.cell