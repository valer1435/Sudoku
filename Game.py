import sys
import os.path

from Session import Session


class Game:
    LOW_DIFFICULT = 1
    HIGH_DIFFICULT = 50
    SAVE_FILE_PATH = "save.pkl"
    CHOOSE_DIFFICULT_TEXT = "Выберите сложность (кол-во выколотых клеток от 1 до 50)\n"
    CHOOSE_SAVE = "Загрузить последнюю сохраненную игру? y/n\n"

    def start(self):
        while True:
            print("Новая игра")
            is_comp = input("Выберите режим игры:\n1) 1 - вы решаете судоку сами\n2) 2 - за вас решает компьютер\n3) 3 - выход из игры\n")
            if is_comp == "3":
                sys.exit(0)
            if is_comp == "2":
                difficult = input(Game.CHOOSE_DIFFICULT_TEXT)
                while not difficult.isdigit() or int(difficult) > Game.HIGH_DIFFICULT or int(difficult) < Game.LOW_DIFFICULT:
                    difficult = input(Game.CHOOSE_DIFFICULT_TEXT)
                Session(int(difficult), is_comp=True)
            if is_comp == "1":
                if os.path.exists(Game.SAVE_FILE_PATH):
                    is_load = input(Game.CHOOSE_SAVE)
                    while is_load not in ["y", "n"]:
                        is_load = input(Game.CHOOSE_SAVE)
                    if is_load == "n":
                        difficult = input(Game.CHOOSE_DIFFICULT_TEXT)
                        while not difficult.isdigit() or int(difficult) > Game.HIGH_DIFFICULT or int(difficult) < Game.LOW_DIFFICULT:
                            difficult = input(Game.CHOOSE_DIFFICULT_TEXT)
                        Session(int(difficult))
                    else:
                        Session(Game.LOW_DIFFICULT, is_load=True)
                else:
                    difficult = input(Game.CHOOSE_DIFFICULT_TEXT)
                    while not difficult.isdigit() or int(difficult) > Game.HIGH_DIFFICULT or int(
                            difficult) < Game.LOW_DIFFICULT:
                        difficult = input(Game.CHOOSE_DIFFICULT_TEXT)
                    Session(int(difficult))


if __name__ == "__main__":
    Game().start()
