import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action
from warehouse.cell import Cell

class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()
        # TODO

        self.rows = rows
        self.columns = columns
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)
        self.matrix_str = self.__str__()

        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == constants.FORKLIFT:
                    self.line_forklift = i
                    self.column_forklift = j
                if self.matrix[i][j] == constants.EXIT:
                    self.line_exit = i
                    self.column_exit = j

    def can_move_up(self, line, column) -> bool:
        if self.matrix[line][column-1] != constants.EMPTY:
            return False
        else:
            return True
        pass

    def can_move_right(self, line, column) -> bool:
        if self.matrix[line+1][column] != constants.EMPTY:
            return False
        else:
            return True
        pass

    def can_move_down(self, line, column) -> bool:
        if self.matrix[line][column+1] != constants.EMPTY:
            return False
        else:
            return True
        pass

    def can_move_left(self, line, column) -> bool:
        if self.matrix[line-1][column] != constants.EMPTY:
            return False
        else:
            return True
        pass
    
    def get_pair_value(self, cell1 : Cell, cell2 : Cell) -> int:
        counter = 0
        self.cell1 = cell1
        self.cell2 = cell2
        while cell1 != cell2:
            if self.can_move_up(self, self.cell1.line, self.cell1.column):
                self.move_up(self)
                counter += 1
            elif self.can_move_right(self, self.cell1.line, self.cell1.column):
                self.move_right(self)
                counter += 1
            elif self.can_move_down(self, self.cell1.line, self.cell1.column):
                self.move_down(self)
                counter += 1
            elif self.can_move_left(self, self.cell1.line, self.cell1.column):
                self.move_left(self)
                counter += 1
        return counter

    def move_up(self) -> None:
        if self.can_move_up(self.line_forklift, self.column_forklift):
            self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
            self.matrix[self.line_forklift][self.column_forklift-1] = constants.FORKLIFT
            self.line_forklift = self.line_forklift-1

    def move_right(self) -> None:
        if self.can_move_right(self.line_forklift, self.column_forklift):
            self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
            self.matrix[self.line_forklift+1][self.column_forklift] = constants.FORKLIFT
            self.line_forklift = self.line_forklift+1

    def move_down(self) -> None:
        if self.can_move_down(self.line_forklift, self.column_forklift):
            self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
            self.matrix[self.line_forklift][self.column_forklift+1] = constants.FORKLIFT
            self.column_forklift = self.column_forklift+1
            

    def move_left(self) -> None:
        if self.can_move_left(self.line_forklift, self.column_forklift):
            self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
            self.matrix[self.line_forklift-1][self.column_forklift] = constants.FORKLIFT
            self.line_forklift = self.line_forklift-1

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.line_forklift or column != self.column_forklift):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
