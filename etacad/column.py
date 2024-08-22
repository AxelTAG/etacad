# Local imports.
from etacad.bar import Bar
from etacad.drawing_utils import delimit_axe, dim_linear, rect
from etacad.globals import ColumnTypes, Direction, ElementTypes, Orientation
from etacad.stirrup import Stirrup
from etacad.utils import gen_symmetric_list

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs


@define
class Column:
    # Geometric attributes.
    width: float
    depth: float
    height: float
    diameter: float = field(default=None)
    column_type: int = field(default=ColumnTypes.RECTANGULAR)
    x: float = field(default=0)
    y: float = field(default=0)
    direction: int = Direction.VERTICAL
    orientation: int = Orientation.RIGHT

    # Longitudinal steel attributes.
    as_sup: dict = field(default=None)
    as_right: dict = field(default=None)
    as_inf: dict = field(default=None)
    as_left: dict = field(default=None)
    max_db_sup: float = field(init=False)
    max_db_right: float = field(init=False)
    max_db_inf: float = field(init=False)
    max_db_left: float = field(init=False)
    anchor_sup: list = field(default=0)
    anchor_right: list = field(default=0)
    anchor_inf: list = field(default=0)
    anchor_left: list = field(default=0)
    bars_as_sup: list = field(init=False)
    bars_as_right: list = field(init=False)
    bars_as_inf: list = field(init=False)
    bars_as_left: list = field(init=False)
    number_init_sup: int = field(default=0)
    number_init_right: int = field(default=0)
    number_init_inf: int = field(default=0)
    number_init_left: int = field(default=0)
    cover: float = field(default=None)

    # Stirrup attributes.
    stirrups_db: list = field(default=None)
    stirrups_anchor: list = field(default=None)
    stirrups_sep: list = field(default=None)
    stirrups_length: list = field(default=None)
    stirrups_x: list = field(default=None)
    stirrups: list = field(init=False)

    # Crossing beams attributes.
    beams: list = field(default=None)
    beams_pos: list = field(default=None)
    beam_symbol: list = field(default=None)

    # Physics attributes.
    concrete_volume: float = field(init=False)

    # Box attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)

    # Others.
    nomenclature: str = field(default=0)
    num_init: int = field(default="#")
    element_type = ElementTypes.COLUMN

    def __attrs_post_init__(self):
        # Longitudinal steel attributes.
        self.anchor_sup = self.anchor_sup if type(self.anchor_sup) == list else [self.anchor_sup] * sum(
            self.as_sup.values())
        self.anchor_right = self.anchor_right if type(self.anchor_right) == list else [self.anchor_right] * sum(
            self.as_right.values())
        self.anchor_inf = self.anchor_inf if type(self.anchor_inf) == list else [self.anchor_inf] * sum(
            self.as_inf.values())
        self.anchor_left = self.anchor_left if type(self.anchor_left) == list else [self.anchor_left] * sum(
            self.as_left.values())

        self.max_db_sup = max(self.as_sup.keys()) if self.as_sup is not None else 0
        self.max_db_right = max(self.as_right.keys()) if self.as_right is not None else 0
        self.max_db_inf = max(self.as_inf.keys()) if self.as_inf is not None else 0
        self.max_db_left = max(self.as_left.keys()) if self.as_left is not None else 0

        self.bars_as_sup = self.__dict_to_bars(bars=self.as_sup,
                                               width=self.width,
                                               x=self.x,
                                               y=self.y,
                                               side=Orientation.TOP,
                                               anchor=self.anchor_sup,
                                               nomenclature=self.nomenclature,
                                               number_init=self.number_init_sup) if self.as_sup else []
        self.bars_as_right = self.__dict_to_bars(bars=self.as_right,
                                                 width=self.depth,
                                                 x=self.x,
                                                 y=self.y,
                                                 side=Orientation.RIGHT,
                                                 anchor=self.anchor_right,
                                                 nomenclature=self.nomenclature,
                                                 number_init=self.number_init_right) if self.as_sup else []
        self.bars_as_inf = self.__dict_to_bars(bars=self.as_inf,
                                               width=self.width,
                                               x=self.x,
                                               y=self.y,
                                               side=Orientation.BOTTOM,
                                               anchor=self.anchor_inf,
                                               nomenclature=self.nomenclature,
                                               number_init=self.number_init_inf) if self.as_sup else []
        self.bars_as_left = self.__dict_to_bars(bars=self.as_left,
                                                width=self.depth,
                                                x=self.x,
                                                y=self.y,
                                                side=Orientation.LEFT,
                                                anchor=self.anchor_left,
                                                nomenclature=self.nomenclature,
                                                number_init=self.number_init_left) if self.as_sup else []

        # Stirrups attributes.
        self.stirrups = self.__list_to_stirrups()

        # Concrete attributes.
        self.concrete_volume = self.width * self.depth * self.height

        # Box attributes.
        self.box_width = self.width
        self.box_height = self.height

    def draw_longitudinal(self, document: Drawing,
                          x: float = None,
                          y: float = None,
                          concrete_shape: bool = True,
                          bars: bool = True,
                          beams: bool = True,
                          beams_axes: bool = True,
                          stirrups: bool = True,
                          middle_axe: bool = True,
                          middle_axe_symbol: str = "A",
                          dim: bool = True,
                          dim_style: str = "EZ_M_25_H25_CM",
                          unifilar_bars: bool = False,
                          unifilar_stirrups: bool = True) -> list:
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        entities = []
        delimit_axe_width = self.width * 4
        delimit_axe_x = x - self.width * 2

        # Drawing concrete shape.
        if concrete_shape:
            entities += rect(doc=document,
                             width=self.width,
                             height=self.height,
                             x=x,
                             y=y,
                             polyline=True)

        # Drawing beams.
        if beams:
            for i, y_beam in enumerate(self.beams_pos):
                y_column_relative = y + y_beam
                y_delimit_axe_relative = y_column_relative + self.beams[i][1] / 2
                if beams:
                    entities += rect(doc=document,
                                     width=self.beams[i][0],
                                     height=self.beams[i][1],
                                     x=x,
                                     y=y_column_relative,
                                     fill=True,
                                     polyline=True)
                if beams_axes:
                    entities += delimit_axe(document=document,
                                            x=delimit_axe_x,
                                            y=y_delimit_axe_relative,
                                            height=delimit_axe_width,
                                            radius=0.1,
                                            text_height=0.1,
                                            symbol=self.beam_symbol[i],
                                            direction=Direction.HORIZONTAL,
                                            attr=GfxAttribs(linetype="CENTER"))

        # Drawing axe.
        if middle_axe:
            entities += delimit_axe(document=document,
                                    x=x + self.width / 2,
                                    y=y - self.width * 2,
                                    height=self.height + self.width * 4,
                                    symbol=middle_axe_symbol,
                                    direction=Direction.VERTICAL,
                                    attr=GfxAttribs(linetype="CENTER"))

        # Drawing dimensions.
        if dim:
            for stirrup in self.stirrups:
                entities += dim_linear(document=document,
                                       p_base=(x - self.width * 3, y + stirrup.y + stirrup.reinforcement_length / 2),
                                       p1=(x, y + stirrup.y),
                                       p2=(x, y + stirrup.y + stirrup.reinforcement_length),
                                       rotation=90,
                                       dimstyle=dim_style)

            entities += dim_linear(document=document,
                                   p_base=(x - self.width * 5, y + self.height / 2),
                                   p1=(x, y),
                                   p2=(x, y + self.height),
                                   rotation=90,
                                   dimstyle=dim_style)

        # Drawing of stirrups.
        if stirrups:
            for stirrup in self.stirrups:
                entities += stirrup.draw_longitudinal(document=document,
                                                      x=x + stirrup.x,
                                                      y=y + stirrup.y,
                                                      unifilar=unifilar_stirrups)

        # Drawing of bars.
        if bars:
            for bar in self.bars_as_inf:
                entities += bar.draw_longitudinal(document=document,
                                                  x=x + bar.x,
                                                  y=y + bar.y,
                                                  unifilar=unifilar_bars,
                                                  dimensions=False,
                                                  denomination=False)  # Only left bars.

        return entities

    def draw_transverse(self) -> list:
        pass

    def draw_longitudinal_rebar_detailing(self) -> list:
        pass

    def draw_transverse_rebar_detailing(self) -> list:
        pass

    def __dict_to_bars(self, bars: dict, width: float, x: float, y: float, side: Orientation, anchor: list,
                       nomenclature: str = None, number_init: int = None) -> list:

        # Creating symetric list of bars.
        list_bars, list_denom = gen_symmetric_list(dictionary=bars, nomenclature=nomenclature, number_init=number_init)

        # Calculating separation and definition of initial x_sep and y_sep.
        if side == Orientation.TOP or side == Orientation.BOTTOM:  # Sides top (0) or bottom (2).
            db_max = max(self.max_db_sup, self.max_db_inf)
            width_util = width - self.cover * 2 + (db_max - max(list_bars))
            separation = width_util / (len(list_bars) - 1)
            x_sep, y_sep = -separation, 0

        elif side == Orientation.RIGHT or side == Orientation.LEFT:  # Sides right (1) or left (3).
            db_max = max([self.max_db_right, self.max_db_left])
            width_util = width - self.cover * 2
            separation = width_util / (len(list_bars) + 1)
            x_sep, y_sep = 0, 0
        else:
            raise ValueError

        # Generating bars.
        entities, delta_x, delta_y, orientation = [], 0, 0, "bottom"
        for i, db in enumerate(list_bars):
            # Calculation of x_delta and y_delta.
            if side == Orientation.TOP or side == Orientation.BOTTOM:
                x_sep += separation
                delta_x = self.cover + db_max / 2
                if side == Orientation.TOP:
                    delta_y_transverse = self.height - self.cover + self.max_db_sup / 2 - db
                if side == Orientation.BOTTOM:
                    delta_y_transverse = self.cover - self.max_db_inf / 2
            elif side == Orientation.RIGHT or side == Orientation.LEFT:
                y_sep += separation
                delta_y = self.cover - db / 2
                if side == Orientation.RIGHT:
                    delta_x = self.cover + db - max(
                        [self.max_db_sup, self.max_db_inf, self.max_db_right]) / 2 - self.width
                    delta_y_transverse = delta_y
                if side == Orientation.LEFT:
                    delta_x = - self.cover + max([self.max_db_sup, self.max_db_inf, self.max_db_left]) / 2
                    delta_y_transverse = delta_y
            else:
                raise ValueError

            x_bar_long = x + x_sep + delta_x
            x_bar_transverse = x_sep - delta_x
            y_bar_long = y + self.cover
            y_bar_transverse = y_sep + delta_y_transverse

            entities.append(Bar(reinforcement_length=self.height - self.cover * 2,
                                diameter=db,
                                x=x_bar_long,
                                y=y_bar_long,
                                left_anchor=anchor[i],
                                right_anchor=anchor[i],
                                mandrel_radius=db,
                                direction=Direction.VERTICAL,
                                orientation=Orientation.BOTTOM,
                                transverse_center=(x_bar_transverse, y_bar_transverse),
                                denomination=list_denom[i]))

        return entities

    def __elements_section(self, elements: list = None, y: float = None) -> list:
        """
        Filter elements that are in the Y coordinate given.

        :param elements: Group of entities (bars and stirrups).
        :type elements: list
        :param y: Y coordinate of the section.
        :type y: float
        :return: Group of entities that are in the Y coordinate given.
        :rtype: list
        """
        if elements is None:
            elements = self.all_elements

        if y is None:
            y = self.height / 2  # Default value if is nothing entered.

        # Filtering elements by X coordinate.
        entities = []
        for element in elements:
            if element.y <= y <= element.y + element.reinforcement_length:
                entities.append(element)

        return entities

    def __list_to_stirrups(self) -> list:
        """
        Generates Stirrup instances of data given at initialization.

        :return: List of Stirrup instances.
        :rtype: list
        """
        if self.stirrups_db is None:
            return []

        stirrup_width = self.width - self.cover * 2 + max(self.max_db_sup, self.max_db_inf)
        stirrup_height = self.depth - (self.cover * 2 - self.max_db_sup / 2 - self.max_db_inf / 2)
        stirrups = zip(self.stirrups_db, self.stirrups_length, self.stirrups_sep, self.stirrups_anchor, self.stirrups_x)
        mandrel_radius_sup = self.max_db_sup / 2
        mandrel_radius_inf = self.max_db_inf / 2

        # Generating stirrups.
        entities = []  # Empty list that will contain stirrups elements.
        for stirrup in stirrups:
            stirrup_x = self.cover - self.max_db_inf / 2 - stirrup[0]  # Subract of thick of stirrup.
            stirrup_y = self.y + stirrup[4]  # Difining y coordinate.

            # Creating of stirrup.
            entities.append(Stirrup(width=stirrup_width + stirrup[0] * 2,
                                    height=stirrup_height + stirrup[0] * 2,
                                    diameter=stirrup[0],
                                    reinforcement_length=stirrup[1],
                                    spacing=stirrup[2],
                                    x=stirrup_x,
                                    y=stirrup_y,
                                    mandrel_radius_top=mandrel_radius_sup,
                                    mandrel_radius_bottom=mandrel_radius_inf,
                                    anchor=stirrup[3],
                                    direction="vertical"))

        return entities
