from Board import Board
from Solver import Solver


class Session:
    def __init__(self, difficult: int, is_load=False, is_comp=False):
        if is_load:
            self.__board = Board.load()
            if self.__board is None:
                print("Файл поврежден. Начните новую игру")
                return
        else:
            self.__board = Board.generate_board(difficult)
        self.__is_comp = is_comp
        self.__solver = Solver()
        self.start()

    def start(self):
        if self.__is_comp:
            self.__board.print_board()
            num_of_solves, steps = self.__solver.solve(self.__board.get_table(), [])
            if num_of_solves != 0:
                self.__board.step_by_step_visualisation(steps)
                print("Судоку решена!")
                return
            print("Судоку не имеет решений!")
        else:
            self.user_walkthrough()

    def user_walkthrough(self):
        while not self.__board.is_filled():
            self.__board.print_board()
            print("""Введите команду:\nput col row number - вставка числа на позицию\ndel col row - удаление числа\nexit - выйти (состояние игры будет сохранено)
            """)
            if self.make__user_step() == 2:
                return
        self.__board.print_board()
        print("Поздравляем! Судоку решена!")

    def make__user_step(self):
        user_input = input().split()
        if len(user_input) == 4:
            if user_input[0] == "put":
                if user_input[1].isdigit() and 0 < int(user_input[1]) < 10:
                    if user_input[2].isdigit() and 0 < int(user_input[2]) < 10:
                        if user_input[3].isdigit() and 0 < int(user_input[3]) < 10:
                            if self.__board.put(
                                    int(user_input[1]) - 1,
                                    int(user_input[2]) - 1,
                                    int(user_input[3])
                            ):
                                return 1
                            else:
                                print("Попытка вставить число туда, где оно уже есть!")

        elif len(user_input) == 3:
            if user_input[0] == "del":
                if user_input[1].isdigit() and 0 < int(user_input[1]) < 10:
                    if user_input[2].isdigit() and 0 < int(user_input[2]) < 10:
                        if self.__board.delete(
                                int(user_input[1]) - 1,
                                int(user_input[2]) - 1
                        ):
                            return 1
                        else:
                            print("Попытка удалить то число, которое было изначально!")
        elif len(user_input) == 1 and user_input[0] == "exit":
            Board.save(self.__board)
            return 2
        return 0
