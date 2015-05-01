from random import *

def slender_movement(player_x, player_y, slender_x, slender_y):

    map_size = 100  # assuming map is 100 units long?

    distance = round(((player_x - slender_x) ** 2 + (player_y - slender_y) ** 2) ** 0.5, 1)

    chance = randint(0, map_size)

    if chance < distance:  # the closer Slender gets to player, the less likely it is to move randomly
        x_movement = randint(-1, 1)
        y_movement = randint(-1, 1)

        slender_x += x_movement
        slender_y += y_movement

        return slender_x, slender_y

    else:
        if slender_x < player_x:
            slender_x += 1
        else:
            slender_x -= 1

        if slender_y < player_y:
            slender_y += 1
        else:
            slender_y -= 1

        return slender_x, slender_y
