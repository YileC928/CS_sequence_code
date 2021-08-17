'''
Polling places

Yile Chen
Boya Fu

Main file for polling place simulation
'''

import sys
import random
import queue
import click
import util


class Voter(object):
    """
    Represents a voter in the precinct

    See constructor for description of attributes.
    """
    def __init__(self, arrival_time, voting_duration):
        '''
        Constructor for the Voter class

        Input:
            name: (float) time the voter arrives
            voting_duration: (float) the voter's voting duration
            start_time: (float) time the voter start voting
            departure_time: (float) time the voter stop voting
        '''
        self.arrival_time = arrival_time
        self.voting_duration = voting_duration
        self.start_time = None
        self.departure_time = None


class Precinct(object):
    """
    Represents a precienct

    A Precinct object has the following composition relationships:

    - Has a Voter object associated with it (the voter in the precinct)
    - Has a VotingBooths ovject associated with it
        (the voting booths in the precinct)
    """

    def __init__(self, name, hours_open, max_num_voters,
                 num_booths, arrival_rate, voting_duration_rate):
        '''
        Constructor for the Precinct class

        Input:
            name: (str) Name of the precinct
            hours_open: (int) Hours the precinct will remain open
            max_num_voters: (int) Number of voters in the precinct
            num_booths: (int) Number of voting booths in the precinct
            arrival_rate: (float) Rate at which voters arrive
            voting_duration_rate: (float) Lambda for voting duration
        '''

        self.name = name
        self.hours_open = hours_open
        self.max_num_voters = max_num_voters
        self.num_booths = num_booths
        self.arrival_rate = arrival_rate
        self.voting_duration_rate = voting_duration_rate


    def simulate(self, percent_straight_ticket, straight_ticket_duration, seed):
        '''
        Simulate a day of voting

        Input:
            percent_straight_ticket: (float) Percentage of straight-ticket
                                voters as a decimal between 0 and 1 (inclusive)
            straight_ticket_duration: (float) Voting duration for
                                straight-ticket voters
            seed: (int) Random seed to use in the simulation

        Output:
            List of voters who voted in the precinct
        '''

        arrival_time = 0
        lst_voter = []
        random.seed(seed)
        v_booth = VotingBooths(self.num_booths)
        i = 0
        while i < self.max_num_voters:
            gap, voting_duration = util.gen_voter_parameters(
                self.arrival_rate, self.voting_duration_rate,
                percent_straight_ticket,straight_ticket_duration)
            arrival_time += gap
            if arrival_time < self.hours_open*60:
                voter = Voter(arrival_time, voting_duration)
                v_booth.gen_start_dept_time(voter, voting_duration)
                lst_voter.append(voter)
            i += 1

        return lst_voter

class VotingBooths(object):
    """
    Represents the voting booths of the precinct

    A VotingBooths object has the following composition relationships:

    - Has a Voter object associated with it (the voter voting in the booths)
    """

    def __init__(self, num_booths):
        '''
        Constructor for the Precinct class

        Input:
            num_booths: (int) Number of voting booths in the precinct
            __queue: (queue) Queue of voters in the booth
        '''

        self.num_booths = num_booths
        self.__queue = queue.PriorityQueue(maxsize = self.num_booths)

    def gen_start_dept_time(self, voter, voting_duration):
        '''
        Generate the start and departure time of voters in the booth

        Input:
            voter: (Voter) Voter voting in voting booths
            voting_duration: (float) the voter's voting duration

        Output:
            No output.
            Update the start time and departure time of list of voters
        '''

        if not self.__queue.full():
            voter.start_time = voter.arrival_time
        else:
            voter_finish = self.__queue.get(block = False)[1]
            if voter.arrival_time >= voter_finish.departure_time:
                voter.start_time = voter.arrival_time
            else:
                voter.start_time = voter_finish.departure_time
        voter.departure_time = voter.start_time + voting_duration
        self.__queue.put((voter.departure_time, voter), block = False)


def find_avg_wait_time(precinct, percent_straight_ticket,
                    ntrials, initial_seed=0):
    '''
    Simulates a precinct multiple times with a given percentage of
    straight-ticket voters. For each simulation, computes the average
    waiting time of the voters,and returns the median of those
    average waiting times.

    Input:
        precinct: (dictionary) A precinct dictionary
        percent_straight_ticket: (float) Percentage straight-ticket voters
        ntrials: (int) The number of trials to run
        initial_seed: (int) Initial seed for random number generator

    Output:
        The median of the average waiting times returned by simulating
        the precinct 'ntrials' times.
    '''

    p = Precinct(precinct["name"],
                 precinct["hours_open"],
                 precinct["num_voters"],
                 precinct["num_booths"],
                 precinct["arrival_rate"],
                 precinct["voting_duration_rate"])

    seed = initial_seed
    trials_done = 0
    lst_avg_wt = []
    while trials_done < ntrials:
        voters = p.simulate(percent_straight_ticket,
                             precinct["straight_ticket_duration"], seed)
        avg_wt = sum([v.start_time - v.arrival_time
                        for v in voters])/len(voters)
        lst_avg_wt.append(avg_wt)
        seed += 1
        trials_done += 1

    lst_avg_wt.sort()
    mean_wt = lst_avg_wt[ntrials//2]

    return mean_wt


def find_percent_split_ticket(precinct, target_wait_time, ntrials, seed=0):
    '''
    Finds the percentage of split-ticket voters needed to bound
    the (average) waiting time.

    Input:
        precinct: (dictionary) A precinct dictionary
        target_wait_time: (float) The minimum waiting time
        ntrials: (int) The number of trials to run when computing
                 the average waiting time
        seed: (int) A random seed

    Output:
        A tuple (percent_split_ticket, waiting_time) where:
        - percent_split_ticket: (float) The percentage of split-ticket
                                voters that ensures the average waiting time
                                is above target_waiting_time
        - waiting_time: (float) The actual average waiting time with that
                        percentage of split-ticket voters

        If the target waiting time is infeasible, returns (0, None)
    '''

    percent_split_ticket10 = 0
    actual_wait_time = 0
    while actual_wait_time <= target_wait_time:
        percent_straight_ticket = (100 - percent_split_ticket10)/100
        actual_wait_time = find_avg_wait_time(precinct, percent_straight_ticket,
                                              ntrials, seed)
        percent_split_ticket10 += 10
        percent_split_ticket = (percent_split_ticket10 - 10)/100
        if percent_split_ticket10 - 10 == 100:
            if actual_wait_time < target_wait_time:
                actual_wait_time = None
            percent_split_ticket = 1
            break

    return (percent_split_ticket, actual_wait_time)


# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, len-as-condition, too-many-locals
# pylint: disable-msg= missing-docstring, too-many-branches
# pylint: disable-msg= line-too-long
@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, target_wait_time, print_voters):
    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = {}
        for p in precincts:
            precinct = Precinct(p["name"],
                                p["hours_open"],
                                p["num_voters"],
                                p["num_booths"],
                                p["arrival_rate"],
                                p["voting_duration_rate"])
            voters[p["name"]] = precinct.simulate(p["percent_straight_ticket"], p["straight_ticket_duration"], seed)
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    sys.exit(-1)
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        percent, avg_wt = find_percent_split_ticket(precinct, target_wait_time, 20, seed)

        if percent == 0:
            msg = "Waiting times are always below {:.2f}"
            msg += " in precinct '{}'"
            print(msg.format(target_wait_time, precinct["name"]))
        else:
            msg = "Precinct '{}' exceeds average waiting time"
            msg += " of {:.2f} with {} percent split-ticket voters"
            print(msg.format(precinct["name"], avg_wt, percent*100))


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
