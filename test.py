from random import randint
tile_amount = 10
bomb_amount = 10
def create_map(tile_amount, bomb_amount):
    map = []
    for _ in range(tile_amount):
        map.append([['_', False] for _ in range(tile_amount)])
    for _ in range(bomb_amount):
        x = randint(0, tile_amount - 1)
        y = randint(0, tile_amount - 1)
        if map[y][x][0] == '_':
            map[y][x][0] = 'B'
    for y, row in enumerate(map):
        for x, item in enumerate(row):
            if item[0] == '_':
                around = []
                y_limit = len(map) - 1
                x_limit = len(row) - 1
                if y > 0 and x > 0:  # topleft
                    around.append(map[y - 1][x - 1][0])
                if y > 0:  # top
                    around.append(map[y - 1][x][0])
                if y > 0 and x < x_limit:  # topright
                    around.append(map[y - 1][x + 1][0])
                if x > 0:  # left
                    around.append(map[y][x - 1][0])
                if x < x_limit:  # right
                    around.append(map[y][x + 1][0])
                if y < y_limit and x > 0:  # bottomleft
                    around.append(map[y + 1][x - 1][0])
                if y < y_limit:  # midbottom
                    around.append(map[y + 1][x][0])
                if y < y_limit and x < x_limit:  # bottomright
                    around.append(map[y + 1][x + 1][0])
                map[y][x][0] = str(around.count('B'))

    return map

def show_map(map):
    for row in map:
        print('{}\n'.format(' '.join( [item[0] for item in row] )))
    print('Exit')

map = create_map(10, 10)
show_map(map)