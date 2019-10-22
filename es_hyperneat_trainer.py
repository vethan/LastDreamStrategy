import neat
import neat.nn
import numpy

# 2-input XOR inputs and expected outputs.
import Actions.BasicAttackAction
import AuthoredAI.WarriorAI
import Game
import Unit.Warrior
import Vector2Int

try:
    import cPickle as pickle
except:
    import pickle
from pureples.shared.substrate import Substrate
from pureples.shared.visualize import draw_net
from pureples.es_hyperneat.es_hyperneat import ESNetwork

# Network inputs and expected outputs.
xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

grid = []
for x in range(0, 6):
    for y in range(0, 6):
        grid.append((x, y))

input_coordinates = grid + grid

output_coordinates = [(0, 0)] + grid + grid

sub = Substrate(input_coordinates, output_coordinates)

# ES-HyperNEAT specific parameters.
params = {"initial_depth": 2,
          "max_depth": 3,
          "variance_threshold": 0.03,
          "band_threshold": 0.3,
          "iteration_level": 1,
          "division_threshold": 0.5,
          "max_weight": 10.0,
          "activation": "sigmoid"}

# Config for CPPN.
config = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
                            neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
                            'config_cppn_xor')

move_adjustments = [Vector2Int.Vector2Int(0, 3),
                    Vector2Int.Vector2Int(-1, 2),
                    Vector2Int.Vector2Int(0, 2),
                    Vector2Int.Vector2Int(1, 2),
                    Vector2Int.Vector2Int(-2, 1),
                    Vector2Int.Vector2Int(-1, 1),
                    Vector2Int.Vector2Int(0, 1),
                    Vector2Int.Vector2Int(1, 1),
                    Vector2Int.Vector2Int(2, 1),
                    Vector2Int.Vector2Int(-3, 0),
                    Vector2Int.Vector2Int(-2, 0),
                    Vector2Int.Vector2Int(-1, 0),
                    Vector2Int.Vector2Int(0, 0),
                    Vector2Int.Vector2Int(1, 0),
                    Vector2Int.Vector2Int(2, 0),
                    Vector2Int.Vector2Int(3, 0),
                    Vector2Int.Vector2Int(-2, -1),
                    Vector2Int.Vector2Int(-1, -1),
                    Vector2Int.Vector2Int(0, -1),
                    Vector2Int.Vector2Int(1, -1),
                    Vector2Int.Vector2Int(2, -1),
                    Vector2Int.Vector2Int(-1, -2),
                    Vector2Int.Vector2Int(0, -2),
                    Vector2Int.Vector2Int(1, -2),
                    Vector2Int.Vector2Int(0, -3)]


def setup_game(net):
    game = Game.Game(6, 6, lambda team, unit, game: handle_turn(team, unit, game, net))
    unit = Unit.Warrior.Warrior(name="Warrior 1", team=0,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("b1"),
                                game=game, char='w')
    unit.ai = None
    game.add_unit(unit)

    unit = Unit.Warrior.Warrior(name="Warrior 1", team=0,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("a2"),
                                game=game,
                                char='w')
    unit.ai = None
    game.add_unit(unit)

    unit = Unit.Warrior.Warrior(name="Warrior 2", team=1,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("f5"),
                                game=game,
                                char='W')
    unit.ai = AuthoredAI.WarriorAI.WarriorAI(unit, game)
    game.add_unit(unit)

    unit = Unit.Warrior.Warrior(name="Warrior 2", team=1,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("e6"),
                                game=game,
                                char='W')
    unit.ai = AuthoredAI.WarriorAI.WarriorAI(unit, game)
    game.add_unit(unit)
    return game


def eval_genome(genome, config, display_game=False):
    cppn = neat.nn.FeedForwardNetwork.create(genome, config)
    network = ESNetwork(sub, cppn, params)
    net = network.create_phenotype_network()
    game = setup_game(net)
    while game.running:
        game.advance()
        if display_game:
            game.draw_grid()
            input(game.turn_order_string())

    fitness = 0
    for unit in game.units:
        if unit.team == 0:
            fitness += unit.hp
        else:
            fitness -= unit.hp

    return fitness


def handle_turn(team, unit, game, net):
    if unit.ai is not None:
        unit.ai.decide_turn_action()
        return

    health_percents = numpy.zeros([6, 6])
    my_position = numpy.zeros([6, 6])
    for selected in game.units:
        if selected is unit:
            my_position[unit.position.x][unit.position.y] = 1
        if selected.team == team:
            health_percents[selected.position.x][selected.position.y] = selected.hp / selected.max_hp
        else:
            health_percents[selected.position.x][selected.position.y] = -selected.hp / selected.max_hp

    inputs = numpy.concatenate((my_position.flatten(), health_percents.flatten()))
    output = net.activate(inputs)

    move_options = output[1:37]
    attack_options = output[37:]
    move_first = output[0]

    move_grid = numpy.asarray(move_options).reshape((6, 6))

    attack_grid = numpy.asarray(attack_options).reshape((6, 6))
    attack_point = None
    max_attack = -1000000
    move_point = None
    max_move = -1000000

    # for i in range(0, 25):
    #    if move_options[i] > max_move:
    #        max_move = move_options[i]
    #        move_point = Vector2Int.Vector2Int.add(unit.position, move_adjustments[i])

    for x in range(0, 6):
        for y in range(0, 6):
            if (move_grid[x][y] > max_move
                    and Vector2Int.Vector2Int.manhattan_distance(Vector2Int.Vector2Int(x, y),
                                                                 unit.position) <= unit.move):
                max_move = move_grid[x][y]
                move_point = Vector2Int.Vector2Int(x, y)
            if attack_grid[x, y] > max_attack:
                max_attack = attack_grid[x, y]
                target_unit = game.get_unit_from_point(Vector2Int.Vector2Int(x, y))
                if target_unit is not None and target_unit.team is not unit.team:
                    attack_point = target_unit

    if move_point is not None and (move_first < 0.5 or attack_point is None):
        unit.move_to(move_point)

    if attack_point is not None:
        dist = Vector2Int.Vector2Int.manhattan_distance(unit.position, attack_point.position)
        if unit.weapon.min_range <= dist <= unit.weapon.max_range:
            for action in unit.actions:
                if isinstance(action, Actions.BasicAttackAction.BasicAttackAction):
                    action.get_targeted_action(attack_point).select()
                    unit.action_taken = True

        if move_point is not None and not unit.move_used:
            unit.move_to(move_point)


# Create the population and run the XOR task by providing the above fitness function.
def run(gens):
    pop = neat.population.Population(config)
    pe = neat.ParallelEvaluator(4, eval_genome)

    stats = neat.statistics.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.reporting.StdOutReporter(True))

    winner = pop.run(pe.evaluate, gens)
    print("es_hyperneat_xor_large done")
    return winner


# If run as script.
if __name__ == '__main__':

    # cProfile.run('run(2)', 'restats')
    # import pstats

    # p = pstats.Stats('restats')
    # p.sort_stats('cumulative').print_stats(20)
    winner = run(300)
    print('\nBest genome:\n{!s}'.format(winner))

    # Verify network output against training data.
    print('\nOutput:')
    cppn = neat.nn.FeedForwardNetwork.create(winner, config)
    network = ESNetwork(sub, cppn, params)
    winner_net = network.create_phenotype_network(
        filename='es_hyperneat_xor_large_winner.png')  # This will also draw winner_net.
    for inputs, expected in zip(xor_inputs, xor_outputs):
        new_input = inputs + (1.0,)
        winner_net.reset()
        for i in range(network.activations):
            output = winner_net.activate(new_input)
        print("  input {!r}, expected output {!r}, got {!r}".format(inputs, expected, output))

    # Save CPPN if wished reused and draw it to file.
    draw_net(cppn, filename="es_hyperneat_xor_large_cppn")
    with open('es_hyperneat_xor_large_cppn.pkl', 'wb') as output:
        pickle.dump(cppn, output, pickle.HIGHEST_PROTOCOL)
