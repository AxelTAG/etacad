# -*- coding: utf-8 -*-

# Imports.
# Local imports.
from etacad.drawing_utils import mtext, rect
from etacad.globals import CADTABLE_SET_DEFAULT, Aligment, ElementTypes
from etacad.utils import max_per_position, text_width_estimation

# External imports.
from attrs import define, field
from ezdxf.document import Drawing


@define
class CADTable:
    data: list[list] = field(default=None)
    rows: int = field(default=None)
    columns: int = field(default=None)
    labels: list = field(default=None)
    index: list = field(default=None)
    x: float = field(default=0)
    y: float = field(default=0)
    settings: dict = field(default=CADTABLE_SET_DEFAULT)
    element_type: ElementTypes = ElementTypes.CADTABLE

    # Table dimensions.
    row_heights: list = field(init=False)
    column_widths: list = field(init=False)
    rows_length: float = field(init=False)
    columns_height: float = field(init=False)
    column_width_labels: list = field(init=False)

    def __attrs_post_init__(self):
        # Table dimensions content.
        if self.settings["content_fit"] and self.data:
            self.rows = len(self.data)
            self.columns = len(self.data[0])
            self.row_heights = [self.settings["content_row_height"]] * self.rows

            column_widths = [0] * self.columns
            for row in self.data:
                for i, content in enumerate(row):
                    width = text_width_estimation(content, self.settings["content_text_height"])
                    if width > column_widths[i]:
                        column_widths[i] = width

            self.column_widths = column_widths

        elif self.data:
            self.rows = len(self.data)
            self.columns = len(self.data[0])
            self.row_heights = [self.settings["content_row_height"]] * self.rows
            self.column_widths = [self.settings["content_row_height"]] * self.columns

        else:
            self.row_heights = [self.settings["content_row_height"]] * self.rows
            self.column_widths = [self.settings["content_row_height"]] * self.columns

        self.rows_length = sum(self.column_widths)
        self.columns_height = sum(self.row_heights)

        # Table dimensions labels.
        if self.settings["labels_fit"]:
            self.column_width_labels = [text_width_estimation(label, self.settings["labels_text_height"]) for label in self.labels]
        else:
            self.column_width_labels = self.settings["labels_column_width"]

    def cell_content_edit(self, row: int, column: int, text=str):
        self.data[row][column] = text

    def draw_grid(self, document: Drawing,
                  rows: int = None,
                  columns: int = None,
                  x: float = None,
                  y: float = None,
                  row_heights: list = None,
                  column_widths: list = None) -> dict:
        if rows is None:
            rows = self.rows

        if columns is None:
            columns = self.columns

        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if row_heights is None:
            row_heights = self.row_heights

        if column_widths is None:
            column_widths = self.column_widths

        rows_length, columns_height = sum(column_widths), sum(row_heights)

        grid_hz_lines = []
        y_hz_line = y
        for i in range(rows):
            sides = [0, 0, 1, 0] if i < rows - 1 else [1, 0, 1, 0]
            grid_hz_lines += rect(doc=document,
                                  width=rows_length,
                                  height=row_heights[i],
                                  x=x,
                                  y=y_hz_line,
                                  sides=sides)
            y_hz_line += row_heights[i]

        grid_vt_lines = []
        x_vt_lines = x
        for i in range(columns):
            sides = [0, 0, 0, 1] if i < columns - 1 else [0, 1, 0, 1]
            grid_vt_lines += rect(doc=document,
                                  width=column_widths[i],
                                  height=columns_height,
                                  x=x_vt_lines,
                                  y=y,
                                  sides=sides)
            x_vt_lines += column_widths[i]

        # Setting groups of elements in dictionary.
        elements = {"grid_hz_lines": grid_hz_lines,
                    "grid_vt_lines": grid_vt_lines,
                    "all_elements": grid_hz_lines + grid_vt_lines}

        return elements

    def draw_labels(self, document: Drawing,
                    x: float = None,
                    y: float = None,
                    row_height: float = None,
                    column_widths: list = None) -> dict:
        if x is None:
            x = self.x

        if y is None:
            y = self.y + self.columns_height

        if row_height is None:
            row_height = [self.settings["labels_row_height"]]

        if column_widths is None:
            column_widths = self.column_widths

        elements = self.draw_grid(document=document,
                                  x=x,
                                  y=y,
                                  rows=1,
                                  columns=len(column_widths),
                                  row_heights=row_height,
                                  column_widths=column_widths)

        texts, x_mtext = [], x
        for i, label in enumerate(self.labels):
            x_mtext += column_widths[i] / 2
            texts += mtext(document=document,
                           textstr=label,
                           height=self.settings["labels_text_height"],
                           x=x_mtext,
                           y=y + self.settings["labels_row_height"] / 2,
                           width=column_widths[i],
                           rotation=0,
                           aligment=Aligment.MTEXT_MIDDLE_CENTER.value)
            x_mtext += column_widths[i] / 2
        elements["texts"] = texts

        # Setting groups of elements in dictionary.
        elements["all_elements"] = elements["all_elements"] + elements["texts"]

        return elements

    def draw_content(self, document: Drawing,
                     x: float = None,
                     y: float = None,
                     row_height: float = None,
                     column_widths: list = None) -> dict:
        if x is None:
            x = self.x

        if y is None:
            y = self.y + self.columns_height

        if row_height is None:
            row_height = self.row_heights

        if column_widths is None:
            column_widths = self.column_widths

        elements = self.draw_grid(document=document,
                                  x=x,
                                  y=y,
                                  rows=self.rows,
                                  columns=self.columns,
                                  row_heights=row_height,
                                  column_widths=column_widths)

        y_mtext = y
        reversed_data = self.data.copy()
        reversed_data.reverse()
        for j, row in enumerate(reversed_data):
            y_mtext += row_height[j] / 2
            texts, x_mtext = [], x
            for i, text in enumerate(row):
                x_mtext += column_widths[i] / 2
                texts += mtext(document=document,
                               textstr=text,
                               height=self.settings["content_text_height"],
                               x=x_mtext,
                               y=y_mtext,
                               width=column_widths[i],
                               rotation=0,
                               aligment=Aligment.MTEXT_MIDDLE_CENTER.value)
                x_mtext += column_widths[i] / 2
            y_mtext += row_height[j] / 2
            elements["texts_row" + str(j)] = texts
            elements["all_elements"] += texts

        return elements

    def draw_table(self, document: Drawing,
                   x: float = None,
                   y: float = None,
                   row_height: float = None,
                   column_widths: list = None) -> dict:
        if x is None:
            x = self.x

        if y is None:
            y = self.y + self.columns_height

        if row_height is None:
            row_height = self.row_heights

        if column_widths is None:
            column_widths = max_per_position(self.column_widths, self.column_width_labels)

        elements = {"labels": self.draw_labels(document=document,
                                               x=x,
                                               y=y + self.columns_height,
                                               column_widths=column_widths),
                    "content": self.draw_content(document=document,
                                                 x=x,
                                                 y=y,
                                                 row_height=row_height,
                                                 column_widths=column_widths)}
        # Setting groups of elements in dictionary.
        elements["all_elements"] = elements["labels"]["all_elements"] + elements["content"]["all_elements"]

        return elements
