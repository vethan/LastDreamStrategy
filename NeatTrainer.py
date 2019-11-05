import os

import neat
import numpy

import Actions.BasicAttackAction
import AuthoredAI.WarriorAI
import AuthoredAI.RangerAI
import Game
import Unit.Warrior
import Unit.Ranger
import Vector2Int
from pureples.shared import visualize

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

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


def setup_game(net, debug=False):
    game = Game.Game(6, 6, lambda team, unit, game: handle_turn(team, unit, game, net))
    unit = Unit.Ranger.Ranger(name="Ranger 1", team=0,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("b1"),
                                game=game, char='r')
    unit.ai = None
    unit.debug_print = debug
    game.add_unit(unit)

    unit = Unit.Warrior.Warrior(name="Warrior 1", team=0,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("a2"),
                                game=game,
                                char='w')
    unit.ai = None
    unit.debug_print = debug

    game.add_unit(unit)

    unit = Unit.Ranger.Ranger(name="Ranger 2", team=1,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("f5"),
                                game=game,
                                char='R')
    unit.ai = AuthoredAI.RangerAI.RangerAI(unit, game)
    unit.debug_print = debug

    game.add_unit(unit)

    unit = Unit.Warrior.Warrior(name="Warrior 2", team=1,
                                start_position=Vector2Int.Vector2Int.from_battleship_coord("e6"),
                                game=game,
                                char='W')
    unit.ai = AuthoredAI.WarriorAI.WarriorAI(unit, game)
    unit.debug_print = debug

    game.add_unit(unit)
    return game


def eval_genome(genome, config, display_game=False):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = setup_game(net, display_game)
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


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    pe = neat.ParallelEvaluator(4, eval_genome)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-299')
    # winner = p.run(pe.evaluate, 1)
    # eval_genome(winner, config, True)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(pe.evaluate, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    eval_genome(winner, config, True)

    visualize.draw_net(winner_net, filename="neat_trainer_networks")
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genome, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.ini')
    run(config_path)
