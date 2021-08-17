'''
Epidemic modelling

Yile Chen

Functions for running a simple epidemiological simulation
'''



import random
import click
TEST_SEED = 20170217

##1##
def count_infected(city):
    '''
    Count the number of infected people

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
    Returns (int): count of the number of people who are
      currently infected
    '''

    infected = []
    for person in city:
        if person [0] == "I":
            infected.append(person)
    
    num_infected = len(infected)

    return num_infected


##2##
def has_an_infected_neighbor(city, position):
    '''
    Determine whether a person has an infected neighbor

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check

    Returns:
      True, if the person has an infected neighbor, False otherwise.
    '''

    # This function should only be called when the person at position
    # is susceptible to infection.
    assert city[position] == "S"

    position_L = position - 1
    position_R = position + 1
    position_last = len(city) - 1
    
    if len(city) == 1:
        neighbor_infected = False
    else:
        if position == position_last:
            if city[position_L][0] == "I":
                neighbor_infected = True
            else:
                neighbor_infected = False
        elif position == 0:
            if city[position_R][0] == "I":
                neighbor_infected = True
            else:
                neighbor_infected = False
        else:
            if city[position_R][0] == "I" or city[position_L][0] == "I":
                neighbor_infected = True
            else:
                neighbor_infected = False
        
    return neighbor_infected


##3##
def advance_person_at_position(city, position, days_contagious):
    '''
    Compute the next state for the person at the specified position.

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check
      days_contagious (int): the number of a days a person is infected

    Returns: (string) disease state of the person after one day
    '''

    if city[position] == "S":
        if has_an_infected_neighbor(city, position) == True:
            state_after1d = "I0"
        else:
            state_after1d = "S"
    elif city[position] == "V":
        state_after1d = "V"
    elif city[position][0] == "I":
        days_infected =  int(city[position][1:])
        days_total = days_contagious - 1
        if days_infected < days_total:
            days_after1d = days_infected + 1
            state_after1d = "I" + str(days_after1d)
        else:
            state_after1d = "R"
    else:
        state_after1d = "R"
    
    return state_after1d


##4##
def simulate_one_day(starting_city, days_contagious):
    '''
    Move the simulation forward a single day.

    Inputs:
      starting_city (list): the state of all people in the simulation at the
        start of the day
      days_contagious (int): the number of a days a person is infected

    Returns:
      new_city (list): disease state of the city after one day
    '''

    new_city = []
    for position in range(0, len(starting_city)):
        new_state = advance_person_at_position(starting_city, position, days_contagious)
        new_city.append(new_state)

    return new_city


##5##
def run_simulation(starting_city, days_contagious,
                   random_seed=None, vaccine_effectiveness=0.0):
    '''
    Run the entire simulation

    Inputs:
      starting_city (list): the state of all people in the city at the
        start of the simulation
      days_contagious (int): the number of a days a person is infected
      random_seed (int): the random seed to use for the simulation
      vaccine_effectiveness (float): the chance that a vaccination will be
        effective

      Returns tuple (list of strings, int): the final state of the city
        and the number of days actually simulated.
    '''

    random.seed(random_seed)
    
    if random_seed != None:
        starting_city = vaccinate_city(starting_city, vaccine_effectiveness)
        print(starting_city)
        
    if count_infected(starting_city) == 0:
        final_city = starting_city
        num_simday = 0
    else:
        num_simday = 0
        while count_infected(starting_city) != 0:
            starting_city = simulate_one_day(starting_city, days_contagious)
            num_simday += 1
            if count_infected(starting_city) == 0:
                break
        final_city = starting_city

    return (final_city, num_simday)
        

##6##
def vaccinate_city(starting_city, vaccine_effectiveness):
    '''
    Vaccinate everyone in a city

    Inputs:
      starting_city (list): the state of all people in the simulation at the
        start of the simulation
      vaccine_effectiveness (float): the chance that a vaccination will be
        effective

    Returns:
      new_city (list): state of the city after vaccinating everyone in the city
    '''

    new_city = []
    for person in starting_city:
        if person == "S":
          if random.random() < vaccine_effectiveness:
              person = "V"
        
        new_city.append(person)
        
    return new_city


###7###
def calc_avg_days_to_zero_infections(
        starting_city, days_contagious,
        random_seed, vaccine_effectiveness,
        num_trials):
    '''
    Conduct N trials with the specified vaccine effectiveness and
    calculate the average number of days for a city to reach zero
    infections

    Inputs:
      starting_city (list): the state of alpl people in the city at the
        start of the simulation
      days_contagious (int): the number of a days a person is infected
      random_seed (int): the starting random seed. Use this value for
        the FIRST simulation, and then increment it once for each
        subsequent run.
      vaccine_effectiveness (float): the chance that a vaccination will be
        effective
      num_trials (int): the number of trials to run

    Returns (float): the average number of days for a city to reach zero
      infections
    '''
    assert num_trials > 0

    num_done = 0
    sim_results = []
    
    while num_done < num_trials:
        sim = run_simulation(starting_city, days_contagious,
                   random_seed, vaccine_effectiveness)
        num_done += 1
        days = sim[1]
        random_seed += 1
        sim_results.append(days)

    average_days = sum(sim_results)/len(sim_results)
    
    return average_days


################ Do not change the code below this line #######################


@click.command()
@click.argument("city", type=str)
@click.option("--days-contagious", default=2, type=int)
@click.option("--random_seed", default=None, type=int)
@click.option("--vaccine-effectiveness", default=0.0, type=float)
@click.option("--num-trials", default=1, type=int)
@click.option("--task-type", default="single",
              type=click.Choice(['single', 'average']))
@click.option("--debug", is_flag=True)

def cmd(city, days_contagious, random_seed, vaccine_effectiveness,
        num_trials, task_type, debug):
    '''
    Process the command-line arguments and do the work.
    '''

    global DEBUG
    DEBUG = debug

    # Convert the city string into a city list.
    city = [p.strip() for p in city.split(",")]
    emsg = ("Error: people in the city must be susceptible ('S'),"
            " recovered ('R'), or infected ('Ix', where *x* is an integer")
    for p in city:
        if p[0] == "I":
            try:
                _ = int(p[1])
            except ValueError:
                print(emsg)
                return -1
        elif p not in {"S", "R"}:
            print(emsg)
            return -1

    if task_type == "single":
        print("Running one simulation...")
        final_city, num_days_simulated = run_simulation(
            city, days_contagious, random_seed, vaccine_effectiveness)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials...")
        avg_days = calc_avg_days_to_zero_infections(
            city, days_contagious, random_seed, vaccine_effectiveness,
            num_trials)
        msg = ("Over {} trial(s), on average, it took {:3.1f} days for the "
               "number of infections to reach zero")
        print(msg.format(num_trials, avg_days))

    return 0


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter