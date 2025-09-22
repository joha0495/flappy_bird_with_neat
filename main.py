import flappy_bird_neat 
import neat 
import os
import pickle

def run(config, function):
    """
    Runs the NEAT algorithm to train a neural network to play Flappy Bird.
    Saves the best genome to a pickle file.
    After training, runs the game using the best genome.

    Parameters:
    config_file: Path to the NEAT config file.
    function: Function to evaluate genomes.
    """

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(function, 50)

    print('\nBest genome:\n{!s}'.format(winner))

    print("Testing best genome...")

    with open ('best_bird.pkl', 'wb') as output:
        pickle.dump(winner, output)


def get_config(config_file):
    """
    Returns the NEAT config object."""
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    return config

def helper(genomes, config):
    """
    creates a game object and calls the game loop.

    Parameters:
    genomes: List of genomes to test.
    config: NEAT config object.
    """
    game = flappy_bird_neat.Game()  
    game.game_loop(genomes, config)

def test_best(config):
    """
    tests the best genome.

    Parameters:
    config: NEAT config object.
    """
    with open('best_bird.pkl', 'rb') as input:
        winner = pickle.load(input)

    game = flappy_bird_neat.Game()
    game.game_loop([(1,winner)], config)


if __name__ == "__main__":
    cwd = os.getcwd()
    config_file = os.path.join(cwd, "config-neat.txt")
    config = get_config(config_file)
    # train neat
    run(config, helper)
    # runs flappy bird with the best genome 
    test_best(config)

