# Author:  Martin McBride
# Created: 2022-11-30
# Copyright (C) 2022, Martin McBride
# License: MIT

from dataclasses import dataclass
import numpy as np

import cairo
from generativepy.drawing import BUTT

from generativepy.color import Color

from generativepy.geometry import FillParameters, StrokeParameters

class TableLayout():
    """
    Table layout can be used to layout other elements in a grid, without draewing the table. Doesn't require a ctx
    """

    def __init__(self, position):
        self.position = position
        self.rows = [100]
        self.cols = [100]
        self.row_pos = [0, 100]
        self.col_pos = [0, 100]

    def of_rows_cols(self, rows, cols):
        """
        Set the size and number of rows and columns
        :param rows: A list of the height of each row in user space units. The length of the list controls the number of rows.
        :param cols: A list of the width of each loum in user space units. The length of the list controls the number of columns.
        :return:
        """
        self.rows = rows
        self.cols = cols
        self.row_pos = [0] + list(np.cumsum(self.rows))
        self.col_pos = [0] + list(np.cumsum(self.cols))
        return self

    def get(self, row, col):
        """
        Get the position of the centre of cell (row, col)
        :param row:
        :param col:
        :return: (x, y) position of the centre of the cell.
        """
        return self.position[0]+(self.col_pos[col]+self.col_pos[col+1])/2, self.position[1]+(self.row_pos[row]+self.row_pos[row+1])/2

@dataclass
class TableAppearance:
    '''
    Parameters that control the appearance of the table.
    '''
    background = FillParameters(Color(1))
    lines = StrokeParameters(Color(0), line_width=2, cap=BUTT)

class Table:
    '''
    Draw a table.

    A table has rows and columns with customisable width and height. The table can return the coordinates of the centre
    point of any cell, allowing text or other itesm to be positioned there.
    '''

    def __init__(self, ctx, position):
        self.ctx = ctx
        self.appearance = TableAppearance()
        self.table_layout = TableLayout(position)

    def of_rows_cols(self, rows, cols):
        """
        Set the size and number of rows and columns
        :param rows: A list of the height of each row in user space units. The length of the list controls the number of rows.
        :param cols: A list of the width of each loum in user space units. The length of the list controls the number of columns.
        :return:
        """
        self.table_layout.of_rows_cols(rows, cols)
        return self

    def background(self, pattern):
        '''
        Sets the entire table background
        :param pattern: color or fill pattern
        :return: self
        '''
        self.appearance.background = FillParameters(pattern)
        return self

    def linestyle(self, pattern=Color(0), line_width=None, dash=None, cap=None, join=None, miter_limit=None):
        '''
        Sets the line style of the whole table
        :param pattern:  the fill pattern or color to use for the outline, None for default
        :param line_width: width of stroke line, None for default
        :param dash: dash pattern of line, as for Pycairo, None for default
        :param cap: line end style, None for default
        :param join: line join style, None for default
        :param miter_limit: mitre limit, None for default
        :return: self
        '''
        self.appearance.lines = StrokeParameters(pattern, line_width, dash, cap, join, miter_limit)
        return self

    def draw(self):
        '''
        Draw the table
        :return:
        '''

        width = sum(self.table_layout.cols)
        height = sum(self.table_layout.rows)

        self.ctx.new_path()
        self.appearance.background.apply(self.ctx)
        self.ctx.rectangle(self.table_layout.position[0], self.table_layout.position[1], width, height)
        self.ctx.fill_preserve()
        self.appearance.lines.apply(self.ctx)
        self.ctx.stroke()
        for i in range(len(self.table_layout.row_pos) - 1):
            self.ctx.move_to(self.table_layout.position[0], self.table_layout.position[1]+self.table_layout.row_pos[i])
            self.ctx.line_to(self.table_layout.position[0]+width , self.table_layout.position[1]+self.table_layout.row_pos[i])
            self.ctx.stroke()
        for i in range(len(self.table_layout.col_pos) - 1):
            self.ctx.move_to(self.table_layout.position[0]+self.table_layout.col_pos[i], self.table_layout.position[1])
            self.ctx.line_to(self.table_layout.position[0]+self.table_layout.col_pos[i], self.table_layout.position[1]+height)
            self.ctx.stroke()

    def get(self, row, col):
        """
        Get the position of the centre of cell (row, col)
        :param row:
        :param col:
        :return: (x, y) position of the centre of the cell.
        """
        return self.table_layout.get(row, col)