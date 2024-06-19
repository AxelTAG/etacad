# Imports.
# Local imports.
from drawing_utils import delimit_axe, dim_linear, rect, text
from bar import Bar
from element import Element
from stirrup import Stirrup
from utils import gen_symmetric_list, str_to_dict_bar

# External imports.
import ezdxf
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs
from ezdxf import zoom


class Beam(Element):
    def __init__(self, width: float, height: float, length: float, as_sup: dict = None, as_right: dict = None,
                 as_inf: dict = None, as_left: dict = None, anchor_sup: float | list = 0, anchor_right: float | list = 0,
                 anchor_inf: float | list = 0, anchor_left: float | list = 0, stirrups_db: list = None,
                 stirrups_sep: list = None, stirrups_length: list = None, stirrups_anchor: list = None,
                 stirrups_x: list = None, columns: list = None, columns_pos: list = None, columns_symbol: list = None,
                 cover: float = 0.025, x: float = 0, y: float = 0, direction: str = "horizontal",
                 orientation: str = "right", nomenclature: str = None, number_init: int = None):

        super().__init__(width=width, height=height, type="beam", x=x, y=y)

        # Armor attributes.
        if as_sup:
            self.as_sup = as_sup
            self.max_db_sup = max(self.as_sup.keys())
            self.anchor_sup = anchor_sup if type(anchor_sup) == list else [anchor_sup] * sum(self.as_sup.values())
            self.number_init_sup = number_init if number_init is not None else 0
            number_init = number_init + len(as_sup) if number_init else len(as_sup)
        else:
            self.as_sup, self.max_db_sup, self.anchor_sup = {}, 0, 0

        if as_right:
            self.as_right = as_right
            self.max_db_right = max(self.as_right.keys())
            self.anchor_right = anchor_right if type(anchor_right) == list else [anchor_right] * sum(self.as_right.values())
            self.number_init_right = number_init
            number_init += len(as_right)
        else:
            self.as_right, self.max_db_right, self.anchor_right = {}, 0, 0

        if as_inf:
            self.as_inf = as_inf
            self.max_db_inf = max(self.as_inf.keys())
            self.anchor_inf = anchor_inf if type(anchor_inf) == list else [anchor_inf] * sum(self.as_inf.values())
            self.number_init_inf = number_init
            number_init += len(as_inf)
        else:
            self.as_inf, self.max_db_inf, self.anchor_inf = {}, 0, 0

        if as_left:
            self.as_left = as_left
            self.max_db_left = max(self.as_left.keys()) if self.as_right else 0
            self.anchor_left = anchor_left if type(anchor_left) == list else [anchor_left] * sum(self.as_left.values())
            self.number_init_left = number_init
        else:
            self.as_left, self.max_db_left, self.anchor_left = {}, 0, 0

        self.cover = cover

        # Stirrups attributes.
        self.stirrups_db = stirrups_db
        self.stirrups_sep = stirrups_sep
        self.stirrups_length = stirrups_length

        if stirrups_anchor is None:
            self.stirrups_anchor = [0.1] * len(stirrups_db)
        else:
            self.stirrups_anchor = stirrups_anchor

        self.stirrups_x = stirrups_x

        # Geometric attributes.
        self.length = length
        self.direction = direction
        self.orientation = orientation

        # Columns attributes.
        self.columns = columns
        self.columns_pos = columns_pos

        if columns_symbol is None:
            self.columns_symbol = range(1, len(self.columns) + 1)
        else:
            self.columns_symbol = columns_symbol

        # Elements/Entities.
        self.bars_as_sup = self.__dict_to_bars(self.as_sup, width=self.width, x=x, y=y, side=0,
                                               anchor=self.anchor_sup, nomenclature=nomenclature,
                                               number_init=self.number_init_sup) if as_sup else []
        self.bars_as_right = self.__dict_to_bars(self.as_right, width=height, x=x, y=y, side=1,
                                                 anchor=self.anchor_right, nomenclature=nomenclature,
                                                 number_init=self.number_init_right) if as_right else []
        self.bars_as_inf = self.__dict_to_bars(self.as_inf, width=self.width, x=x, y=y, side=2,
                                               anchor=self.anchor_inf, nomenclature=nomenclature,
                                               number_init=self.number_init_inf) if as_inf else []
        self.bars_as_left = self.__dict_to_bars(self.as_left, width=height, x=x, y=y, side=3,
                                                anchor=self.anchor_left, nomenclature=nomenclature,
                                                number_init=self.number_init_left) if as_left else []
        self.all_bars = self.bars_as_sup + self.bars_as_right + self.bars_as_inf + self.bars_as_left

        self.stirrups = self.__list_to_stirrups()

        self.all_elements = self.all_bars + self.stirrups

    # Function that draws beam along longitudinal axe.
    def draw_longitudinal(self, document: Drawing, x: float = None, y: float = None, concrete_shape: bool = True,
                          bars: bool = True, columns: bool = True, columns_axes: bool = True,
                          stirrups: bool = True, middle_axe: bool = True, middle_axe_symbol: str = "A",
                          dim: bool = True, dim_style: str = "EZ_M_25_H25_CM", unifilar_bars: bool = False,
                          unifilar_stirrups: bool = True) -> list:

        if x is None:
            x = self.x
        if y is None:
            y = self.y

        group = []
        delimit_axe_height = self.height * 4
        delimit_axe_y = y - self.height

        # Drawing concrete shape.
        if concrete_shape:
            group += rect(doc=document, width=self.length, height=self.height, x=x, y=y, sides=[1, 1, 1, 1],
                          polyline=True)  # Body.

        # Drawing columns.
        for i, x_column in enumerate(self.columns_pos):
            x_column_relative = x + x_column
            x_delimit_axe_relative = x_column_relative + self.columns[i][0] / 2
            if columns:
                group += rect(doc=document, width=self.columns[i][0], height=self.columns[i][1], x=x_column_relative,
                              y=y, fill=True, polyline=True)
            if columns_axes:
                group += delimit_axe(document=document, x=x_delimit_axe_relative, y=delimit_axe_y,
                                     height=delimit_axe_height, radius=0.1, text_height=0.1,
                                     symbol=self.columns_symbol[i], attr=GfxAttribs(linetype="CENTER"))

        # Drawing axe.
        if middle_axe:
            group += delimit_axe(document=document, x=x - self.height, y=y + self.height / 2,
                                 height=self.length + self.height * 2, symbol=middle_axe_symbol, direction=0,
                                 attr=GfxAttribs(linetype="CENTER"))

        # Drawing of stirrups.
        if stirrups:
            for stirrup in self.stirrups:
                group += stirrup.draw_longitudinal(document=document, x=x + stirrup.x, y=y + stirrup.y,
                                                   unifilar=unifilar_stirrups)

        # Drawing of bars.
        if bars:
            self.bars_as_sup[0].draw_longitudinal(document=document,
                                                  x=x + self.bars_as_sup[0].x,
                                                  y=y + self.bars_as_sup[0].y,
                                                  unifilar=unifilar_bars,
                                                  dimensions=False)  # Only mayor bar.
            self.bars_as_inf[0].draw_longitudinal(document=document,
                                                  x=x + self.bars_as_inf[0].x,
                                                  y=y + self.bars_as_inf[0].y,
                                                  unifilar=unifilar_bars,
                                                  dimensions=False)  # Only inferior mayor bar.
            for bar in self.bars_as_left:
                bar.draw_longitudinal(document=document,
                                      x=x + bar.x,
                                      y=y + bar.y,
                                      unifilar=unifilar_bars,
                                      dimensions=False)  # Only left bars.

        # Drawing dimensions.
        if dim:
            dim_y = y + self.height * 2
            dim_p_base = (x + self.length / 2, y + delimit_axe_height * 0.65)

            for stirrup in self.stirrups:
                group += dim_linear(document=document,
                                    p_base=(x + stirrup.x + stirrup.reinforcement_length / 2, dim_y),
                                    p1=(x + stirrup.x, dim_y),
                                    p2=(x + stirrup.x + stirrup.reinforcement_length, dim_y),
                                    dimstyle=dim_style)

            group += dim_linear(document=document,
                                p_base=dim_p_base,
                                p1=(x, y + self.height),
                                p2=(x + self.length, y + self.height),
                                dimstyle=dim_style)

        return group

    # Function that draws transverse section.
    def draw_transverse_rebar_detailing(self, document: Drawing, x: float = None, y: float = None,
                                        x_section: float = None, unifilar: bool = False,
                                        dimensions: bool = True) -> list:

        stirrups = self.__elements_section(elements=self.stirrups, x=x_section)

        group = []
        for stirrup in stirrups:
            group += stirrup.draw_transverse(document=document, x=x, y=y, unifilar=unifilar, dimensions=dimensions)

        return group

    def draw_transverse(self, document: Drawing, x: float, y: float, x_section: float = None,
                        unifilar: bool = False, dimensions: bool = True) -> list:

        if x_section is None:
            x_section = self.length / 2

        # Checking if x given is in beam length.
        if not self.x <= x_section <= self.x + self.length:
            return []

        # Configurations variables.
        text_dim_distance = 0.05
        text_dim_height = 0.05

        # Obtaining elements for given x_section.
        entities = self.__elements_section(x=x_section)

        # Filtering elements.
        bars = filter(lambda e: e.type == "bar", entities)
        stirrups = filter(lambda e: e.type == "stirrup", entities)

        # Concrete shape drawing.
        group = rect(doc=document, width=self.width, height=self.height, x=x, y=y, polyline=True)

        # Drawing of bars.
        for bar in bars:
            group += bar.draw_transverse(document=document, x=x, y=y)

        # Drawing of stirrups.
        for stirrup in stirrups:
            delta_x = self.cover - max(self.max_db_sup, self.max_db_inf) / 2000 - stirrup.diameter

            group += stirrup.draw_transverse(document=document, x=x + delta_x, y=y + stirrup.y,
                                             unifilar=unifilar)

        # Drawing of dimensions.
        if dimensions:
            group += dim_linear(document=document, p_base=(x - text_dim_distance, y + self.height / 2),
                                p1=(x, y), p2=(x, y + self.height), rotation=90, dimstyle="EZ_M_10_H25_CM")
            group += dim_linear(document=document, p_base=(x + self.width / 2, y + self.height + text_dim_distance),
                                p1=(x, y + self.height), p2=(x + self.width, y + self.height),
                                dimstyle="EZ_M_10_H25_CM")

        return group

    # Function that draws the rebar detailing.
    def draw_longitudinal_rebar_detailing(self, document: Drawing, x: float = None, y: float = None,
                                          unifilar: bool = True, columns_axes: bool = True) -> list:

        def __draw_section_bars(bars: list = None, spacing: float = 0.2, rebar_x: float = None,
                                rebar_y: float = None, barline=True, text_reference: str = None) -> tuple:
            text_height = 0.05
            entities = []
            graph_list = []

            if text_reference:
                entities += text(document=document, text=text_reference, height=text_height,
                                 point=(rebar_x - self.height * 2 * 0.8, rebar_y + self.height * 0.05 - spacing))

            for bar in bars:
                if bar.denomination not in graph_list:
                    rebar_y -= spacing + bar.box_height
                    entities += bar.draw_longitudinal(document=document, x=rebar_x, y=rebar_y, unifilar=unifilar,
                                                      dimensions=True)
                    graph_list.append(bar.denomination)
            rebar_y -= spacing
            if barline:
                entities += rect(doc=document, width=self.length + self.height * 4, height=0,
                                 x=rebar_x - self.height * 2, y=rebar_y, sides=(1, 0, 0, 0))

            return entities, rebar_x, rebar_y

        group, rebar_x, rebar_y = [], x, y
        if self.as_sup:
            barline = True if self.as_right or self.bars_as_left or self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_sup, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=barline, text_reference="As sup.")
            group += entities

        if self.as_left:
            barline = True if self.bars_as_left or self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_right, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=barline, text_reference="As right.")
            group += entities

        if self.as_left:
            barline = True if self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_left, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=barline, text_reference="As left.")
            group += entities

        if self.as_inf:
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_inf, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=False, text_reference="As inf.")
            group += entities

        if columns_axes:
            for i, x_column in enumerate(self.columns_pos):
                delimit_axe_height = y - rebar_y
                delimit_axe_y = rebar_y
                x_column_relative = x + x_column
                x_delimit_axe_relative = x_column_relative + self.columns[i][0] / 2

                group += delimit_axe(document=document, x=x_delimit_axe_relative, y=delimit_axe_y,
                                     height=delimit_axe_height, radius=0.1, text_height=0.1,
                                     attr=GfxAttribs(linetype="CENTER"))

        return group

    def draw_table_rebar_detailing(self, x: float = None, y: float = None, unifilar: bool = False):
        pass

    def __dict_to_bars(self, bars: dict, width: float, x: float, y: float, side: int, anchor: list,
                       nomenclature: str = None, number_init: int = None) -> list:

        if side < 0 or side > 3:
            raise ValueError

        list_bars, list_denom = gen_symmetric_list(dictionary=bars, nomenclature=nomenclature, number_init=number_init,
                                                   factor=1000)  # Creating symetric list of bars.

        # Calculating separtion and definition of initial x_sep and y_sep.
        if side == 0 or side == 2:  # Sides top (0) or bottom (2).
            db_max = max(self.max_db_sup, self.max_db_inf) / 1000
            width_util = width - self.cover * 2 + (db_max - max(list_bars))
            separation = width_util / (len(list_bars) - 1)
            x_sep, y_sep = -separation, 0

        else:  # Sides right (1) or left (3).
            db_max = max([self.max_db_right, self.max_db_left]) / 1000
            width_util = width - self.cover * 2
            separation = width_util / (len(list_bars) + 1)
            x_sep, y_sep = 0, 0

        # Generating bars.
        entities, delta_x, delta_y, orientation = [], 0, 0, "bottom"
        for i, db in enumerate(list_bars):
            # Calculation of x_delta and y_delta.
            if side == 0 or side == 2:
                x_sep += separation
                delta_x = -self.cover + db_max / 2
                if side == 0:
                    delta_y = self.height - self.cover - 3 * db / 2 - anchor[i]
                    delta_y_transverse = self.height - self.cover + self.max_db_sup / 2000 - db
                    orientation = "right"
                if side == 2:
                    delta_y = self.cover - self.max_db_inf / 2000
                    delta_y_transverse = self.cover - self.max_db_inf / 2000
                    orientation = "top"
            else:
                y_sep += separation
                delta_y = self.cover - db / 2

                if side == 1:
                    delta_x = self.cover + db - max([self.max_db_sup, self.max_db_inf, self.max_db_right]) / 2000 - self.width
                    delta_y_transverse = delta_y
                    orientation = "right"
                if side == 3:
                    delta_x = - self.cover + max([self.max_db_sup, self.max_db_inf, self.max_db_left]) / 2000
                    delta_y_transverse = delta_y
                    orientation = "right"

            x_bar_long = x + self.cover
            x_bar_transverse = x_sep - delta_x
            y_bar_long = y + y_sep + delta_y
            y_bar_transverse = y_sep + delta_y_transverse

            entities.append(Bar(reinforcement_length=self.length - self.cover * 2, diameter=db,
                                x=x_bar_long, y=y_bar_long,
                                left_anchor=anchor[i], right_anchor=anchor[i], mandrel_radius=db,
                                orientation=orientation,
                                transverse_center=(x_bar_transverse, y_bar_transverse), denomination=list_denom[i]))

        return entities

    # Function that returns elements in a given x_beam position.
    def __elements_section(self, elements: list = None, x: float = None) -> list:
        if elements is None:
            elements = self.all_elements

        if x is None:
            x = self.length / 2  # Default value if is nothing entered.

        # Filtering elements by X coordinate.
        entities = []
        for element in elements:
            if element.x <= x <= element.x + element.reinforcement_length:
                entities.append(element)

        return entities

    # Function that creates stirrups from list.
    def __list_to_stirrups(self) -> list:

        stirrup_width = self.width - (self.cover - max(self.max_db_sup, self.max_db_inf) / 2000) * 2
        stirrup_height = self.height - (self.cover * 2 - self.max_db_sup / 2000 - self.max_db_inf / 2000)
        stirrups = zip(self.stirrups_db, self.stirrups_length, self.stirrups_sep, self.stirrups_anchor, self.stirrups_x)
        mandrel_radius_sup = self.max_db_sup / 2000
        mandrel_radius_inf = self.max_db_inf / 2000

        # Generating stirrups.
        entities = []  # Empty list that will contain stirrups elements.
        for stirrup in stirrups:
            stirrup_x = self.x + stirrup[4]  # Difining x coordinate.
            stirrup_y = self.cover - self.max_db_inf / 2000 - stirrup[0]  # Subract of thick of stirrup.

            # Creating of stirrup.
            entities.append(Stirrup(width=stirrup_width + stirrup[0] * 2, height=stirrup_height + stirrup[0] * 2,
                                    diameter=stirrup[0], reinforcement_length=stirrup[1], spacing=stirrup[2],
                                    x=stirrup_x, y=stirrup_y, mandrel_radius_top=mandrel_radius_sup,
                                    mandrel_radius_bottom=mandrel_radius_inf, anchor=stirrup[3]))

        return entities
