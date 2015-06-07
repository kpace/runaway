from map import Map
from game_manager import GameManager

def main():
    m = Map('../maps/m1.txt')
    g = GameManager(m)
    g.movement()

if __name__ == "__main__":
    main()