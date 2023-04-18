import argparse
import numpy as np
from game import potential_game, congestion_game

from utils.plotter import plot_many
from utils.algos import optimistic_solver,nash_ucb,exponential_weights_annealing,nash_ca
from utils.regret import regret
from utils.game_maker import make_game

import json
import os
import time

def generate_filename():
    """
    Generate a filename based on the current timestamp.

    Returns:
        str: Filename string.
    """
    timestamp = int(time.time())
    filename = "simulation_{}.json".format(timestamp)

    # Add the 'log_files' folder to the filename
    folder = "log_files"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)

    return filepath, timestamp

def update_log_file(timestamp, kwargs):
    """
    Update the log file with the parameters of the simulation and the associated timestamp.

    Args:
        timestamp (int): Timestamp for the simulation.
        kwargs (dict): Dictionary of parameters.

    Returns:
        None
    """
    log_entry = {
        "timestamp": timestamp,
        "parameters": kwargs
    }

    log_filename = "simulation_log.txt"

    with open(log_filename, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def save_simulation_results(filename, kwargs, regrets, av_regret_val):
    """
    Save the regrets and parameters of the simulation to a JSON file.

    Args:
        filename (str): Filename for the JSON file.
        kwargs (dict): Dictionary of parameters.
        regrets (list): List of regrets for each run.
        av_regret_val (float): Average regret value.

    Returns:
        None
    """
    # Create a dictionary to store the results and parameters
    data = {
        "parameters": kwargs,
        "regrets": regrets,
        "average_regret": av_regret_val
    }

    # Save the data to a JSON file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def parse_args():
    """
    Helper function to set up command line argument parsing
    """
    parser = argparse.ArgumentParser()
    # Set up arguments
    parser.add_argument("-n", "--dimension", default=5, type=int,
                        help='Number of Strategies for each player')
    parser.add_argument("-k", "--players", default=5, type=int,
                        help='Number of Players')
    parser.add_argument("-t", "--timesteps", default=100, type=int,
                        help='Number of timesteps')
    parser.add_argument("-r", "--runs", default=1, type=int,
                        help='Number of Runs')
    parser.add_argument("-e", "--regret", default="nash", type=str,
                        help='Type of Regret')
    parser.add_argument("-nl", "--noise", default=0, type=float,
                        help='Noise Level')
    parser.add_argument("-c", "--constant", default=0.1, type=float,
                        help='Constant')
    parser.add_argument("-a", "--alpha", default=0.1, type=float,
                        help='Alpha')
    parser.add_argument("-g", "--game", default="congestion", type=str,
                        help='Game Type')
    parser.add_argument("-s", "--solver", default="nash_ca", type=str,
                        help='Which solver to use')

    return parser.parse_args()

def main(**kwargs):
    """
    Main function to run the simulation for different types of games, solvers and regret types.

    Keyword Args:
        dimension (int): Number of strategies for each player.
        players (int): Number of players.
        timesteps (int): Number of timesteps.
        runs (int): Number of runs.
        noise (float): Noise level.
        constant (float): Constant.
        alpha (float): Alpha parameter.
        game (str): Game type (e.g. "congestion" or "random").
        solver (str): Solver to use (e.g. "nash_ca" or "nash_ucb").
        regret (str): Type of regret (e.g. "nash" or "potential").

    Returns:
        None
    """

    # Parse keyword arguments
    n = kwargs.get("dimension")
    k = kwargs.get("players")
    t_max = kwargs.get("timesteps")
    runs = kwargs.get("runs")
    nl = kwargs.get("noise")
    c = kwargs.get("constant")
    alpha = kwargs.get("alpha")
    g = kwargs.get("game")
    s = kwargs.get("solver")
    e = kwargs.get("regret")

    iterations = t_max

    regrets = []
    cumulative_regrets = []

    # Iterate through the specified number of runs
    for r in range(runs):
        print(r)
        regrets.append([])
        cumulative_regrets.append([])

        # Initialize the game and solver based on the provided game type and solver type
        if g == "random":
            Potential, unknown_utilitys = make_game(g, n, k)
            Game = potential_game(Potential, unknown_utilitys,nl)
        if g == "congestion":
            number_facilities, number_agents, facility_means = make_game(g, n, k)
            Game = congestion_game(facility_means,number_agents,nl)

        if s == "optimistic":
            algorithm = optimistic_solver(Game,c, alpha)
        if s == "nash_ucb":
            algorithm = nash_ucb(Game,c,iterations)
        if s == "exp_weight":
            algorithm = exponential_weights_annealing(Game,0.75)
        if s == "nash_ca":
            algorithm = nash_ca(Game, c,20)

        # Instantiate a regret object and initialize cumulative regret
        reg = regret(Game)
        cumulative_regret = 0

        # Run the simulation for the specified number of iterations
        for t in range(iterations):

            #Generate probability tensor over all choices
            prob = algorithm.next_sample_prob(Game)

            #Sample choice from probability tensor
            choice = np.random.choice(np.arange(prob.size), p=prob.flatten())
            sample_tuple = np.unravel_index(choice, prob.shape)

            #Sample this joint action from the game
            Game.sample(tuple(sample_tuple))

            #Calculate regret and append lists
            regrets[r].append(reg.regrets(e,prob))
            cumulative_regret += regrets[r][t]
            cumulative_regrets[r].append(cumulative_regret)

            #Output log
            print("______")
            print(t)
            print("Sample: ", sample_tuple)
            print("Regret: ", regrets[r][t])
            print("Cumulative Regret: ", cumulative_regret)

    av_regret_val = reg.av_regret(e)

    filename, timestamp = generate_filename()
    save_simulation_results(filename, kwargs, regrets, av_regret_val)
    update_log_file(timestamp, kwargs)

    # Plot cumulative regrets
    plot_many(kwargs, np.array(cumulative_regrets),av_regret_val)


if __name__ == "__main__":
    """
    Entry point for the script. Parses command line arguments and runs the main function.
    """
    # Parse command line arguments
    args = vars(parse_args())
    # Execute the main function with the parsed arguments
    main(**args)