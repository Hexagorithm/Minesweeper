from game import Game
from settings import *
def main():
    game = Game(bomb_amount,tile_amount,screen_size)
    game.run()

if __name__ == "__main__":
    main()