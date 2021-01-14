import copy

from Group import Group


class Solver:

    def solve(self, table: [[]], steps: []):
        num_of_solves = 0
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j] == 0:
                    allowed_nums = self.find_allowed_nums(i, j, table)
                    if not allowed_nums:
                        return 0, steps
                    for k in allowed_nums:
                        table[i][j] = k
                        new_solves, new_steps = self.solve(copy.deepcopy(table), (steps + [(i, j, k)]).copy())
                        if new_solves == 1:
                            steps = new_steps
                        num_of_solves += new_solves
                    return num_of_solves, steps
        return 1, steps

    @staticmethod
    def find_allowed_nums(y: int, x: int, table: [[]]):
        set_begin = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in range(len(table)):
            set_begin = set_begin.difference({table[i][x], table[y][i]})

        group_x = x // Group.rows_in_group
        group_y = y // Group.rows_in_group
        for i in range(group_y * Group.rows_in_group, group_y * Group.rows_in_group + Group.rows_in_group):
            for j in range(group_x * Group.rows_in_group, group_x * Group.rows_in_group + Group.rows_in_group):
                set_begin = set_begin.difference({table[i][j]})
        return list(set_begin)

    def check_filled(self, table: [[]]):
        allowed_nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        t_table = list(map(list, zip(*table)))
        for i in range(len(table)):
            if allowed_nums.difference(set(table[i])):
                return False
            if allowed_nums.difference(set(t_table[i])):
                return False
            x_group, y_group = i % Group.rows_in_group, i // Group.rows_in_group
            if allowed_nums.difference(set(
                    [
                     j for k in table[y_group * Group.rows_in_group: y_group * Group.rows_in_group + Group.rows_in_group]
                     for j in k[x_group * Group.rows_in_group: x_group * Group.rows_in_group + Group.rows_in_group]
                    ])):
                return False
        return True
