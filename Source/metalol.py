import random as pif
import time


def clamp(n, start, end):
    if n > end:
        return end
    if n < start:
        return start
    return n


#*Main generator function
def create_meta():
    return "Alors tu " + basic_move() + into() + random_move() + random_end() * pif.randint(0, 1)


#*random move pickers
def random_move():
    move = moves[pif.randint(0, len(moves)-1)]
    return move()


def basic_move():
    move = basic_moves[pif.randint(0, len(basic_moves)-1)]
    return move()



#*random item pickers
def random_character():
    return characters[pif.randint(0, len(characters)-1)]


def random_modifier():
    i = clamp(pif.randint(-len(characters)*2, len(characters)-1), 0, 99999999)
    return modifiers[i] + " " * (i != 0)


def random_place():
    return places[pif.randint(0, len(places) - 1)]


def random_end():
    return endings[pif.randint(0, len(endings) - 1)]


#*basic moves
def ctrl_key():
    n = pif.randint(0, 3)
    return "%sctrl-%s " % (random_modifier(), action_keys[n])

def rush():
    return "%srush %s " % (random_modifier(), random_place())

def key():
    n = pif.randint(0,3)
    return random_modifier() + action_keys[n]

#*composed moves
def into():
    return "into %s " % (basic_move())


def combo():
    return "%scombo %s " % (random_modifier(), basic_move())


def dash():
    return "%sdash %s " % (random_modifier(), random_move())


def counter():
    return "%scounter %sde %s " % (random_modifier(), basic_move(), random_character())



places = ["tower", "toplane", "botlane", "midlane", "bush", "jungle"]
action_keys = ['Q', 'W', 'E', 'R']
characters = ["Garren", "Jinx", "Teemo", "Ash"]
modifiers = ["", "double", "turbo", "speed", "triple"]
endings = ["Alt-F4", "ggwp"]
basic_moves = [ctrl_key, dash, rush, key]
moves = [ctrl_key, into, combo, dash, counter, rush]


def main():
    pif.seed = time
    print(create_meta())


if __name__ == '__main__':
    main()
