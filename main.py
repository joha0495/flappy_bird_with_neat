import flappy_bird_neat 
import neat 
import os
import pickle

def run(config_file, function):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(function, 50)

    print('\nBest genome:\n{!s}'.format(winner))

    print("Saving the winner...")

    with open ('best_bird.pkl', 'wb') as output:
        pickle.dump(winner, output)


    with open('best_bird.pkl', 'rb') as input:
        winner = pickle.load(input)

    game = flappy_bird_neat.Game()
    game.game_loop([(1,winner)], config)
    
def helper(genomes, config):
    game = flappy_bird_neat.Game()  
    game.game_loop(genomes, config)

if __name__ == "__main__":
    cwd = os.getcwd()
    config_file = os.path.join(cwd, "config-neat.txt")
    run(config_file, helper)

