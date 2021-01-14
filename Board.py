import copy
import random

from Group import Group
from Solver import Solver


class Board:
    rows = 9

    def __init__(self):
        self.__table = [[(j + i * 3 + (i // 3 + 1)) % Board.rows + 1 for j in range(Board.rows)] for i in range(Board.rows)]
        self.__begin_table = [[0 for j in range(Board.rows)] for i in range(Board.rows)]
        self.__solver = Solver()

    @staticmethod
    def generate_board(difficult: int):
        board = Board()
        board.shuffle()
        board.delete_elements(difficult)
        return board

    def transpose(self):
        self.__table = list(map(list, zip(*self.__table)))

    def swap_two_rows(self, row_number: int, row_number_2: int):
        self.__table[row_number], self.__table[row_number_2] = \
            self.__table[row_number_2], self.__table[row_number]

    def swap_two_cols(self, col_number: int, col_number_2: int):
        self.transpose()
        self.swap_two_rows(col_number, col_number_2)
        self.transpose()

    def swap_two_groups(self, group1: int, group2: int):
        self.__table[group1 * Group.rows_in_group: group1 * Group.rows_in_group + Group.rows_in_group], \
        self.__table[group2 * Group.rows_in_group: group2 * Group.rows_in_group + Group.rows_in_group] = \
            self.__table[group2 * Group.rows_in_group: group2 * Group.rows_in_group + Group.rows_in_group], \
            self.__table[group1 * Group.rows_in_group: group1 * Group.rows_in_group + Group.rows_in_group]

    def swap_two_groups_transpose(self, group1: int, group2: int):
        self.transpose()
        self.swap_two_groups(group1, group2)
        self.transpose()

    def shuffle(self):
        seed = random.choice(range(10000, 89999))
        if seed % 10 % 2 == 0:
            self.transpose()
        seed = seed // 10
        for i in range(seed % 10):
            rand_row = random.choice(range(Board.rows))
            big_group = rand_row // Group.rows_in_group
            bias = random.choice(range(Group.rows_in_group))
            self.swap_two_rows(rand_row, big_group * Group.rows_in_group + bias)
        seed = seed // 10
        for i in range(seed % 10):
            rand_col = random.choice(range(Board.rows))
            big_group = rand_col // Group.rows_in_group
            bias = random.choice(range(Group.rows_in_group))
            self.swap_two_cols(rand_col, big_group * Group.rows_in_group + bias)
        seed = seed // 10
        for i in range(seed % 10):
            group = random.choice(range(Group.rows_in_group))
            group2 = random.choice(range(Group.rows_in_group))
            self.swap_two_groups(group, group2)
        seed = seed // 10
        for i in range(seed % 10):
            group = random.choice(range(Group.rows_in_group))
            group2 = random.choice(range(Group.rows_in_group))
            self.swap_two_groups_transpose(group, group2)

    def delete_elements(self, num_to_delete: int):
        correct_steps = []
        see_table = [[1 for j in range(Board.rows)] for i in range(Board.rows)]
        for i in range(num_to_delete):
            while True:
                x = random.choice(range(Board.rows))
                y = random.choice(range(Board.rows))

                if see_table[y][x] == 1:
                    num_in_cell = self.__table[y][x]
                    self.delete(y, x)

                    num_of_solves, steps = self.__solver.solve(copy.deepcopy(self.__table), [])
                    if num_of_solves > 1 or num_of_solves == 0:
                        self.put(y, x, num_in_cell)
                    else:
                        see_table[y][x] = 0
                        correct_steps = steps
                        break
        self.__begin_table = copy.deepcopy(self.__table)

    def step_by_step_visualisation(self, steps: []):
        for y, x, num in steps:
            self.put(y, x, num)
            input("Нажмите enter для продолжения"
                  "\n")
            self.print_board()

    def print_board(self):
        for i in range(Board.rows):
            for j in range(Board.rows):
                print(self.__table[i][j], end=" ")
                if (j + 1) % 3 == 0 and j != 8:
                    print("|", end=" ")
            print()
            if (i + 1) % 3 == 0 and i != 8:
                print("-" * ((Board.rows + 1) * 2 + 1))

    def put(self, y: int, x: int, num: int):
        if self.__table[y][x] == 0:
            self.__table[y][x] = num
            return True
        else:
            return False

    def delete(self, y: int, x: int):
        if self.__begin_table[y][x] == 0:
            self.__table[y][x] = 0
            return True
        else:
            return False

    def get_table(self):
        return self.__table

    def get_begin_table(self):
        return self.__begin_table

    def set_table(self, table: [[]]):
        self.__table = table

    def set_begin_table(self, table: [[]]):
        self.__begin_table = table

    def is_filled(self):
        return self.__solver.check_filled(copy.deepcopy(self.__table))

    def check_board(self):
        if len(self.__table) != Board.rows and len(self.__begin_table) != Board.rows:
            return False

        for i in self.__table:
            if len(i) != Board.rows:
                return False
            for j in i:
                if j > 9 or j < 0:
                    return False
        for i in self.__begin_table:
            if len(i) != Board.rows:
                return False
            for j in i:
                if j > 9 or j < 0:
                    return False
        return True

    @staticmethod
    def save(board: "Board"):
        with open("save.pkl", "w+") as save_file:
            for i in board.get_table():
                for j in i:
                    save_file.write(str(j)+" ")
                save_file.write("\n")
            for i in board.get_begin_table():
                for j in i:
                    save_file.write(str(j)+" ")
                save_file.write("\n")

    @staticmethod
    def load():
        board = Board()
        with open("save.pkl") as save_file:
            try:
                board.set_table([list(map(int, save_file.readline().split())) for _ in range(Board.rows)])
                board.set_begin_table([list(map(int, save_file.readline().split())) for _ in range(Board.rows)])
            except Exception as e:
                return None
        if board.check_board():
            return board
        else:
            return None
