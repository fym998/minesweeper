"""
SPDX-License-Identifier: GPL-3.0-or-later
This file is part of minesweeper.
Copyright (C) 2024 符益铭

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from enum import Enum, auto
from random import randrange


class CellState(Enum):
    COVERED = auto()
    UNCOVERED = auto()
    FLAGGED = auto()
    SUSPECTED = auto()
    DETONATED = auto()


class Cell:
    def __init__(self, is_mine: bool = False, adjacent_mines:int = 0):
        self.is_mine = is_mine
        self.adjacent_mines = adjacent_mines
        self.state: CellState = CellState.COVERED

    def lclick(self):
        if self.flagged:
            return
        if self.is_mine:
            self.state = CellState.DETONATED
        else:
            self.state = CellState.UNCOVERED

    def rclick(self):
        if self.state == CellState.COVERED:
            self.state = CellState.FLAGGED
        elif self.state == CellState.FLAGGED:
            self.state = CellState.SUSPECTED
        elif self.state == CellState.SUSPECTED:
            self.state = CellState.COVERED


    @property
    def covered(self) -> bool:
        return self.state == CellState.COVERED

    @property
    def uncovered(self) -> bool:
        return self.state == CellState.UNCOVERED

    @property
    def flagged(self) -> bool:
        return self.state == CellState.FLAGGED

    @property
    def suspected(self) -> bool:
        return self.state == CellState.SUSPECTED

    @property
    def detonated(self) -> bool:
        return self.state == CellState.DETONATED


class GameState(Enum):
    NOT_STARTED = auto()
    ONGOING = auto()
    FAILED = auto()
    SUCCESSFUL = auto()


class Game:
    def __init__(
        self, rows, cols, num_mines,
        update_callback=None,
        end_callback=None
    ):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        # self.num_flags = 0
        self.num_uncovered = 0
        self.update_callback = update_callback
        self.end_callback = end_callback

        self.__grid = [
            [Cell() for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.state: GameState = GameState.NOT_STARTED


    @property
    def not_started(self) -> bool:
        return self.state == GameState.NOT_STARTED

    @property
    def ongoing(self) -> bool:
        return self.state == GameState.ONGOING

    @property
    def successful(self) -> bool:
        return self.state == GameState.SUCCESSFUL

    @property
    def failed(self) -> bool:
        return self.state == GameState.FAILED

    @property
    def ended(self) -> bool:
        return self.state == GameState.FAILED or self.state == GameState.SUCCESSFUL


    def validate_coord(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.rows and y >= 0 and y < self.cols

    def get_cell(self, x: int, y: int) -> Cell:
        if not self.validate_coord(x, y):
            raise ValueError("坐标超限")
        return self.__grid[x][y]

    def get_adjacent_coords(self, x: int, y: int) -> list[list[int]]:
        ret = []
        for x1 in range(x-1, x+2):
            for y1 in range(y-1, y+2):
                if self.validate_coord(x1, y1) and (x != x1 or y != y1):
                    ret.append((x1, y1))
        return ret

    def get_adjacent_cells(self, x: int, y: int) -> list[Cell]:
        return [self.__grid[x][y] for x, y in self.get_adjacent_coords(x, y)]

    def get_adjacent_mine_num(self, x: int, y: int) -> int:
        return self.get_cell(x, y).adjacent_mines


    def __plant_mines_and_start(self, excluded_coords: set[tuple[int, int]] = None):
        planted_mines = 0

        while planted_mines < self.num_mines:
            x = randrange(0, self.rows)
            y = randrange(0, self.cols)
            if not self.get_cell(x, y).is_mine and (
                    not excluded_coords or not (x, y) in excluded_coords):
                self.get_cell(x, y).is_mine = True
                planted_mines += 1
                for cell in self.get_adjacent_cells(x, y):
                    cell.adjacent_mines += 1

        self.state = GameState.ONGOING

    def __update(self):
        if self.update_callback:
            self.update_callback(self)

    def __end(self):
        if self.end_callback:
            self.end_callback(self)

    def __fail(self):
        self.state = GameState.FAILED
        self.__update()
        self.__end()

    def __success(self):
        self.state = GameState.SUCCESSFUL
        self.__update()
        self.__end()


    @property
    def num_flags(self) -> int:
        return sum([cell.flagged for row in self.__grid for cell in row])


    def lclick(self, x: int, y: int, update=True):
        if not self.validate_coord(x, y):
            raise ValueError("坐标超限")

        if self.not_started:
            self.__plant_mines_and_start({(x, y)})
        
        if self.ended:
            return

        cell = self.get_cell(x, y)

        if cell.covered:
            cell.lclick()

            if cell.detonated:
                self.__fail()
                return

            if cell.uncovered:
                self.num_uncovered += 1

                if self.num_uncovered == self.cols*self.rows - self.num_mines:
                    self.__success()
                    return

                if self.get_adjacent_mine_num(x, y) == 0:
                    for x1, y1 in self.get_adjacent_coords(x,y):
                        if self.validate_coord(x1, y1):
                            self.lclick(x1, y1, update=False)
  
                if update:
                    self.__update()

    def rclick(self, x: int, y: int):
        if not self.validate_coord(x, y):
            raise ValueError("坐标超限")
        
        if self.ended:
            return

        cell = self.get_cell(x, y)
        cell.rclick()

        # if cell.flagged:
        #     self.num_flags+=1
        # else:
        #     self.num_flags-=1

        self.__update()

    def lrclick(self, x: int, y: int):
        if not self.validate_coord(x, y):
            raise ValueError("坐标超限")
        
        if self.ended:
            return
        
        if not self.get_cell(x, y).uncovered:
            return

        adjacent_coords = self.get_adjacent_coords(x, y)
        adjacent_cells = self.get_adjacent_cells(x, y)
        if self.get_adjacent_mine_num(x, y) == sum([cell.flagged for cell in adjacent_cells]):
            for x1, y1 in adjacent_coords:
                if not self.get_cell(x1, y1).flagged:
                    self.lclick(x1, y1, update=False)

        self.__update()

