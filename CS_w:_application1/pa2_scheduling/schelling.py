"""
CS121: Schelling Model of Housing Segregation

  Program for simulating a variant of Schelling's model of
  housing segregation.  This program takes six parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: home at Location (i, j) is in
        the neighborhood of the home at Location (k,l)
        if k-R <= i <= k+R and l-R <= j <= l+R

    similarity_satisfaction_range (lower bound and upper bound) -
         acceptable range for ratio of the number of
         homes of a similar color to the number
         of occupied homes in a neighborhood.

    patience - number of satisfactory homes that must be visited before choosing
        the last one visited.

    max_steps - the maximum number of passes to make over the city
        during a simulation.

    Sample: python3 schelling.py --grid_file=tests/a20-sample-writeup.txt --r=1
         --sim_lb=0.40 --sim_ub=0.7 --patience=3 --max_steps=1
    The sample command is shown on two lines, but should be entered on
    a single line in the linux command-line
"""

import click
import utility

def neighborhood_list(grid, R, k, l):
    '''
    Find the R-neighborhood centered around a homeowner at a 
    specific location (k,l). Home at Location (i, j) is in the 
    neighborhood of the home at Location (k,l)

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        k (int): the row number of the location of the homeowner
        l (int): the column number of the location of the homeowner
        
    Return (list): list of the neighborhood
    '''

    lst_neighborhood=[]

    # To improve efficiency of the codes and avoid going through every element
    # of grid, we only check the elements within a certain radius around the 
    # centered homeowner.

    for i in range(max(k-R, 0),min(k+R+1, len(grid))):
        for j in range(max(l-R, 0),min(l+R+1, len(grid))):

    # The definition of the neighborhood:

            if (abs(k-i)+abs(l-j) >= 0) and (abs(k-i)+abs(l-j) <= R):
                lst_neighborhood.append((i,j))
    return lst_neighborhood


def similarity_score(grid, R, k, l):
    '''
    Find the the similarity score of a homeowner at a given location (k,l).

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        k (int): the row number of the given location of the homeowner
        l (int): the column number of the given location of the homeowner
        
    Return (float): similarity score
    '''

    occupied_homes_num = 0
    same_color_num = 0
    score_num = 0

    for p in neighborhood_list(grid, R, k, l):

    # Homes that are for sale are not included in the neighborhood when 
    # calculating similarity scores.

        if grid[p[0]][p[1]] != 'F':
            occupied_homes_num += 1

    # Calculate the number of homes in the neighborhood centered on that 
    # location with occupants of the same color as the homeowner.

            if grid[p[0]][p[1]] == grid[k][l]: 
                same_color_num +=1

    # Definition of the similarity score:
    # similarity score = S / H

    similarity_score_num = same_color_num / occupied_homes_num
    return similarity_score_num


def is_satisfied(grid, R, location, sim_sat_range):
    '''
    Determine whether or not the homeowner at a specific location is
    satisfied using an R-neighborhood centered around the location.
    That is, is does their similarity score fall with the specified
    range (inclusive)

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
          
    Return (boolean): True if is satisfied; False otherwise 
    '''

    # Since it does not make sense to call this function on a home
    # that is for sale, add an assertion to verify that the home 
    # is not for sale.

    assert grid[location[0]][location[1]] != "F"   

    # Calculate the similarity score of the grid location.

    base_score = similarity_score(grid, R, location[0], location[1])
    if (base_score >= sim_sat_range[0]) and (base_score <= sim_sat_range[1]):
        return True
    else:
        return False


def swap(grid, location1, location2):
    '''
    Swap one location in the grid (location1) to a new location (location2), 
    for applying the satisfaction rule to the new location, and then swaping
    the homeowner back to their original location.

    Inputs:
        grid: the grid
        location1 (int, int): a grid location
        location2 (int, int): a grid location
        
    Returns: N/A (modify the grid argument)
    '''

    grid[location1[0]][location1[1]],grid[location2[0]][location2[1]] = grid[location2[0]][location2[1]],grid[location1[0]][location1[1]]

def relocate_one_home(grid, R, location, sim_sat_range, patience, homes_for_sale):
    '''
    Determine whether a home would be relocated
    
    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied with his similarity score.
        patience (int): number of satisfactory homes that must be visited before choosing
        the last one visited.
        for_sale (list of tuples): a list of locations with homes for sale

    Returns (int): 1 if the home is relocated, 0 if the home is not
    '''

    num = 0
    if is_satisfied(grid, R, location, sim_sat_range) == False:
        for location_sale in homes_for_sale:
            swap(grid, location, location_sale) 
            if is_satisfied(grid, R, location_sale, sim_sat_range) == False:
                swap(grid, location, location_sale)
            else:
                if patience == 1:
                    homes_for_sale.remove(location_sale)
                    homes_for_sale.insert(0, location)
                    num = 1
                    break
                else:
                    patience -= 1
                    swap(grid, location, location_sale)
                    
    return num


def sim_one_step (grid, R, sim_sat_range, patience, homes_for_sale):
    '''
    Simulate one step, which consists of a maroon wave and a blue wave.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied with his similarity score
        patience (int): number of satisfactory homes that must be visited before choosing
        the last one visited
        for_sale (list of tuples): a list of locations with homes for sale

    Returns (int): The number of relocations completed in one step
    '''
    grid_size = len(grid)
    lst_locations = []
    for i in range (grid_size):
        for j in range (grid_size):
            lst_locations.append((i,j))
    
    num_relocation = 0
    
    #A Maroon Wave
    for location in lst_locations: 
        if grid[location[0]][location[1]] == "M": 
            num_relocation += relocate_one_home(grid, R, location, sim_sat_range, patience, homes_for_sale)
    
    #A Blue Wave
    for location in lst_locations: 
        if grid[location[0]][location[1]] == "B": 
            num_relocation += relocate_one_home(grid, R, location, sim_sat_range, patience, homes_for_sale)

    return num_relocation


def do_simulation(grid, R, sim_sat_range, patience, max_steps, homes_for_sale):
    '''
    Do a full simulation.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied with his similarity score
        patience (int): number of satisfactory homes that must be visited before choosing
        the last one visited
        max_steps (int): maximum number of steps to do
        for_sale (list of tuples): a list of locations with homes for sale

    Returns (int): The number of relocations completed
    '''
    
    steps_done = 0
    num_relocation_done = 0
    while steps_done < max_steps:
        num_relocation_one_step = sim_one_step(grid, R, sim_sat_range, patience, homes_for_sale)
        num_relocation_done += num_relocation_one_step
        steps_done += 1
        if num_relocation_one_step == 0 or steps_done == max_steps:
            break

    return num_relocation_done


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1,
              help="neighborhood radius")
@click.option('--sim_lb', type=float, default=0.40,
              help="Lower bound of similarity range")
@click.option('--sim_ub', type=float, default=0.70,
              help="Upper bound of similarity range")
@click.option('--patience', type=int, default=1, help="patience level")
@click.option('--max_steps', type=int, default=1)
def cmd(grid_file, r, sim_lb, sim_ub, patience, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)
    for_sale = utility.find_homes_for_sale(grid)
    sim_sat_range = (sim_lb, sim_ub)


    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    num_relocations = do_simulation(grid, r, sim_sat_range, patience,
                                    max_steps, for_sale)

    if len(grid) < 20:
        print("Final state of the city:")
        for row in grid:
            print(row)
        print()

    print("Total number of relocations done: " + str(num_relocations))

if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
