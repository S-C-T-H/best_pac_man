import os
import time
from pac_man_classes import PacMan, Enemy, Board, BACK_COLOR, ENEMY_COLOR1, PACMAN_COLOR


def main():
    hero = PacMan(13, 13, PACMAN_COLOR + '0' + BACK_COLOR, 'up')
    enemy_1 = Enemy(0, 0, ENEMY_COLOR1 + '+' + BACK_COLOR, 'down')
    enemy_2 = Enemy(24, 0, ENEMY_COLOR1 + '=' + BACK_COLOR, 'down')
    enemy_3 = Enemy(24, 24, ENEMY_COLOR1 + '%' + BACK_COLOR, 'left')
    enemy_4 = Enemy(0, 24, ENEMY_COLOR1 + '@' + BACK_COLOR, 'up')
    board = Board()
    board.build_walls()
    while True:
        hero.update(board)
        update_enemies(enemy_1, enemy_2, enemy_3, enemy_4, hero=hero, board=board)
        board.draw()
        if game_over(enemy_1, enemy_2, enemy_3, enemy_4, hero=hero):
            print('Игра окончена')
            break
        time.sleep(0.5)
        os.system('cls')


# def move_everyone(*characters: Character, board: Board):
#     for character in characters:
#         character.move(board)
#
# def follow_hero(*enemies:Enemy, hero:PacMan):
#     for enemy in enemies:
#         enemy.follow(hero)
def update_enemies(*enemies: Enemy, board: Board, hero: PacMan):
    for enemy in enemies:
        enemy.update(board, hero)


def game_over(*enemies: Enemy, hero: PacMan):
    for enemy in enemies:
        if enemy.catch_hero(hero):
            return True
    return False


main()
