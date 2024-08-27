# Imports.
# Local imports.
from etacad.drawing_utils import delimit_axe, dim_linear, rect, text
from etacad.bar import Bar
from etacad.globals import Direction, ElementTypes, Orientation
from etacad.stirrup import Stirrup
from etacad.utils import gen_symmetric_list

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs


@define
class Beam:
    """
    Beam element, computes geometrics and physics props and manages dxf drawing methods (longitudinal, transversal,
    reinforcement detailing, etc.)

    :param width: Width of the beam.
    :type width: float
    :param height: Height of the beam.
    :type height: float
    :type length: Length of the beam.
    :param x: X-coordinate of the bottom left corner of the beam concrete shape.
    :type x: float
    :param y: Y-coordinate of the bottom left corner of the beam concrete shape.
    :type y: float
    :param direction: Direction of the beam (HORIZONTAL or VERTICAL).
    :type direction: str
    :param orientation: Orientation of the beam (TOP, RIGHT, DOWN, LEFT).
    :type orientation: str
    :param as_sup: Dictionary containing reinforcement information for the top side.
    :type as_sup: dict
    :param anchor_sup: Anchor length for the top reinforcement or list of lengths.
    :type anchor_sup: float | list
    :param as_right: Dictionary containing reinforcement information for the right side.
    :type as_right: dict
    :param anchor_right: Anchor length for the right reinforcement or list of lengths.
    :type anchor_right: float | list
    :param as_inf: Dictionary containing reinforcement information for the bottom side.
    :type as_inf: dict
    :param anchor_inf: Anchor length for the bottom reinforcement or list of lengths.
    :type anchor_inf: float | list
    :param as_left: Dictionary containing reinforcement information for the left side.
    :type as_left: dict
    :param anchor_left: Anchor length for the left reinforcement or list of lengths.
    :type anchor_left: float | list
    :param cover: Concrete cover for the reinforcement.
    :type cover: float
    :param stirrups_db: Diameter of stirrups or list of diameters.
    :type stirrups_db: float | list
    :param stirrups_sep: Separation between stirrups or list of separations.
    :type stirrups_sep: float | list
    :param stirrups_length: List of lengths for stirrups.
    :type stirrups_length: list
    :param stirrups_anchor: Anchor length of stirrups or list of anchor lengths.
    :type stirrups_anchor: float | list
    :param stirrups_x: List of x-coordinates for stirrups.
    :type stirrups_x: list
    :param columns: List of lists containing column width and height.
    :type columns: list[list[float, float]]
    :param columns_pos: List of positions (X-coordinate of start) for columns.
    :type columns_pos: list[float]
    :param columns_symbol: List of symbols representing columns.
    :type columns_symbol: list[str]
    :param nomenclature: Nomenclature prefix used for labeling elements.
    :type nomenclature: str
    :param number_init: Initial number for labeling elements.
    :type number_init: int
    :param element_type: Type of the structural element (e.g., BEAM).
    :type element_type: ElementTypes

    :ivar width: Width of the beam.
    :ivar height: Height of the beam.
    :ivar length: Length of the beam.
    :ivar x: X-coordinate of the bottom left corner of the beam concrete shape.
    :ivar y: Y-coordinate of the bottom left corner of the beam concrete shape.
    :ivar direction: Direction of the element (HORIZONTAL or VERTICAL).
    :ivar orientation: Orientation of the element (e.g., TOP, RIGHT, DOWN, LEFT).
    :ivar as_sup: Dictionary containing reinforcement information for the top side.
    :ivar max_db_sup: Maximum diameter of the top reinforcement bars.
    :ivar anchor_sup: Anchor length for the top reinforcement or list of lengths.
    :ivar number_init_sup: Initial numbering for the top reinforcement bars.
    :ivar as_right: Dictionary containing reinforcement information for the right side.
    :ivar max_db_right: Maximum diameter of the right reinforcement bars.
    :ivar anchor_right: Anchor length for the right reinforcement or list of lengths.
    :ivar number_init_right: Initial numbering for the right reinforcement bars.
    :ivar as_inf: Dictionary containing reinforcement information for the bottom side.
    :ivar max_db_inf: Maximum diameter of the bottom reinforcement bars.
    :ivar anchor_inf: Anchor length for the bottom reinforcement or list of lengths.
    :ivar number_init_inf: Initial numbering for the bottom reinforcement bars.
    :ivar as_left: Dictionary containing reinforcement information for the left side.
    :ivar max_db_left: Maximum diameter of the left reinforcement bars.
    :ivar anchor_left: Anchor length for the left reinforcement or list of lengths.
    :ivar number_init_left: Initial numbering for the left reinforcement bars.
    :ivar cover: Concrete cover for the reinforcement.
    :ivar stirrups_db: Diameter of stirrups or list of diameters.
    :ivar stirrups_sep: Separation between stirrups or list of separations.
    :ivar stirrups_length: List of lengths for stirrups.
    :ivar stirrups_anchor: Anchor length of stirrups or list of anchor lengths.
    :ivar stirrups_x: List of x-coordinates for stirrups.
    :ivar columns: List of lists containing column width and height.
    :ivar columns_pos: List of positions (X-coordinate of start) for columns.
    :ivar columns_symbol: List of symbols representing columns.
    :ivar bars_as_sup: List of top reinforcement bars as entities.
    :ivar bars_as_right: List of right reinforcement bars as entities.
    :ivar bars_as_inf: List of bottom reinforcement bars as entities.
    :ivar bars_as_left: List of left reinforcement bars as entities.
    :ivar all_bars: List of all reinforcement bars as entities.
    :ivar stirrups: List of stirrups as entities.
    :ivar all_elements: List of all elements/entities in the structure.
    :ivar nomenclature: Nomenclature prefix used for labeling elements.
    :ivar number_init: Initial number for labeling elements.
    :ivar element_type: Type of the structural element (e.g., BEAM).
    """
    # Geometric attributes.
    width: float
    height: float
    length: float
    x: float = field(default=0)
    y: float = field(default=0)
    direction: Direction = field(default=Direction.HORIZONTAL)
    orientation: Orientation = field(default=Orientation.RIGHT)

    # Steel attributes.
    as_sup: dict = field(default=None)
    max_db_sup: float = field(init=False)
    anchor_sup: float | list = field(default=0)
    number_init_sup: int = field(init=False)

    as_right: dict = field(default=None)
    max_db_right: float = field(init=False)
    anchor_right: float | list = 0
    number_init_right: int = field(init=False)

    as_inf: dict = field(default=None)
    max_db_inf: float = field(init=False)
    anchor_inf: float | list = 0
    number_init_inf: int = field(init=False)

    as_left: dict = field(default=None)
    max_db_left: float = field(init=False)
    anchor_left: float | list = 0
    number_init_left: int = field(init=False)

    cover: float = 0.025

    # Stirrups attribute.
    stirrups_db: float | list = field(default=None)
    stirrups_sep: float | list = field(default=None)
    stirrups_length: list = field(default=None)
    stirrups_anchor: float | list = field(default=None)
    stirrups_x: list = field(default=None)

    # Columns attributes.
    columns: list[list[float, float]] = field(default=None)
    columns_pos: list[float] = field(default=None)
    columns_symbol: list[str] = field(default=None)

    # Elements/Entities.
    bars_as_sup: list = field(init=False)
    bars_as_right: list = field(init=False)
    bars_as_inf: list = field(init=False)
    bars_as_left: list = field(init=False)
    all_bars: list = field(init=False)
    stirrups: list = field(init=False)
    all_elements: list = field(init=False)

    # Others.
    nomenclature: str = field(default="#")
    number_init: int = field(default=None)
    element_type: ElementTypes = field(default=ElementTypes.BEAM)

    def __attrs_post_init__(self):
        # Steel attributes.
        # Top bars.
        if self.as_sup:
            self.max_db_sup = max(self.as_sup.keys())

            if not type(self.anchor_sup) == list:
                self.anchor_sup = [self.anchor_sup] * sum(self.as_sup.values())

            self.number_init_sup = self.number_init if self.number_init is not None else 0
            self.number_init = self.number_init + sum(self.as_sup.values()) if self.number_init else len(self.as_sup)
        else:
            self.as_sup, self.max_db_sup, self.anchor_sup = {}, 0, 0

        # Right bars.
        if self.as_right:
            self.max_db_right = max(self.as_right.keys())

            if not type(self.anchor_right) == list:
                self.anchor_right = [self.anchor_right] * sum(self.as_right.values())

            self.number_init_right = self.number_init
            self.number_init += sum(self.as_right.values())
        else:
            self.as_right, self.max_db_right, self.anchor_right = {}, 0, 0

        # Inferior bars.
        if self.as_inf:
            self.max_db_inf = max(self.as_inf.keys())

            if not type(self.anchor_inf) == list:
                self.anchor_inf = [self.anchor_inf] * sum(self.as_inf.values())

            self.number_init_inf = self.number_init
            self.number_init += sum(self.as_inf.values())
        else:
            self.as_inf, self.max_db_inf, self.anchor_inf = {}, 0, 0

        # Left bars.
        if self.as_left:
            self.max_db_left = max(self.as_left.keys())

            if not type(self.anchor_left) == list:
                self.anchor_left = [self.anchor_left] * sum(self.as_left.values())

            self.number_init_left = self.number_init
            self.number_init += sum(self.as_left.values())
        else:
            self.as_left, self.max_db_left, self.anchor_left = {}, 0, 0

        # Stirrups attributes.
        if type(self.stirrups_db) == float:
            self.stirrups_db = [self.stirrups_db]

        if self.stirrups_anchor is None:
            self.stirrups_anchor = [0.1] * len(self.stirrups_db)
        elif type(self.stirrups_anchor) == float:
            self.stirrups_anchor = [self.stirrups_anchor] * len(self.stirrups_db)

        if type(self.stirrups_sep) == float:
            self.stirrups_sep = [self.stirrups_sep] * len(self.stirrups_db)

        if self.stirrups_length is None:
            self.stirrups_length = [self.length - (self.height + self.cover) * 2]

        if self.stirrups_x is None:
            self.stirrups_x = [self.height + self.cover]

        # Column attributes.
        if self.columns_symbol is None:
            self.columns_symbol = [*range(1, len(self.columns) + 1)]

        # Elements/Entities.
        self.bars_as_sup = self.__dict_to_bars(self.as_sup, width=self.width, x=self.x, y=self.y, side=0,
                                               anchor=self.anchor_sup, nomenclature=self.nomenclature,
                                               number_init=self.number_init_sup) if self.as_sup else []
        self.bars_as_right = self.__dict_to_bars(self.as_right, width=self.height, x=self.x, y=self.y, side=1,
                                                 anchor=self.anchor_right, nomenclature=self.nomenclature,
                                                 number_init=self.number_init_right) if self.as_right else []
        self.bars_as_inf = self.__dict_to_bars(self.as_inf, width=self.width, x=self.x, y=self.y, side=2,
                                               anchor=self.anchor_inf, nomenclature=self.nomenclature,
                                               number_init=self.number_init_inf) if self.as_inf else []
        self.bars_as_left = self.__dict_to_bars(self.as_left, width=self.height, x=self.x, y=self.y, side=3,
                                                anchor=self.anchor_left, nomenclature=self.nomenclature,
                                                number_init=self.number_init_left) if self.as_left else []
        self.all_bars = self.bars_as_sup + self.bars_as_right + self.bars_as_inf + self.bars_as_left

        self.stirrups = self.__list_to_stirrups()

        self.all_elements = self.all_bars + self.stirrups

    # Function that draws beam along longitudinal axe.
    def draw_longitudinal(self,
                          document: Drawing,
                          x: float = None,
                          y: float = None,
                          concrete_shape: bool = True,
                          bars: bool = True,
                          columns: bool = True,
                          columns_axes: bool = True,
                          stirrups: bool = True,
                          middle_axe: bool = True,
                          middle_axe_symbol: str = "A",
                          dim: bool = True,
                          dim_style: str = "EZ_M_25_H25_CM",
                          unifilar_bars: bool = False,
                          unifilar_stirrups: bool = True) -> list:
        """
        Draws the longitudinal section of the beam.

        :param document: The DXF document where the beam will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the left bottom corner of beam concrete shape.
        :type x: float, optional
        :param y: Y-coordinate of the left bottom corner of beam concrete shape.
        :type y: float, optional
        :param concrete_shape: If True, the concrete shape of the beam is drawn.
        :type concrete_shape: bool
        :param bars: If True, the reinforcement bars are drawn.
        :type bars: bool
        :param columns: If True, the columns are drawn.
        :type columns: bool
        :param columns_axes: If True, the axes of the columns are drawn.
        :type columns_axes: bool
        :param stirrups: If True, the stirrups are drawn.
        :type stirrups: bool
        :param middle_axe: If True, the middle axis of the beam is drawn.
        :type middle_axe: bool
        :param middle_axe_symbol: Symbol to represent the middle axis.
        :type middle_axe_symbol: str
        :param dim: If True, dimensions are drawn.
        :type dim: bool
        :param dim_style: The dimension style to be used.
        :type dim_style: str
        :param unifilar_bars: If True, the reinforcement bars are drawn as unifilar.
        :type unifilar_bars: bool
        :param unifilar_stirrups: If True, the stirrups are drawn as unifilar.
        :type unifilar_stirrups: bool
        :return: A list of graphical entities representing the longitudinal section of the beam.
        :rtype: list
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        group = []
        delimit_axe_height = self.height * 4
        delimit_axe_y = y - self.height

        # Drawing concrete shape.
        if concrete_shape:
            group += rect(doc=document,
                          width=self.length,
                          height=self.height,
                          x=x,
                          y=y,
                          sides=[1, 1, 1, 1],
                          polyline=True)  # Body.

        # Drawing columns.
        for i, x_column in enumerate(self.columns_pos):
            x_column_relative = x + x_column
            x_delimit_axe_relative = x_column_relative + self.columns[i][0] / 2
            if columns:
                group += rect(doc=document,
                              width=self.columns[i][0],
                              height=self.columns[i][1],
                              x=x_column_relative,
                              y=y,
                              fill=True,
                              polyline=True)
            if columns_axes:
                group += delimit_axe(document=document,
                                     x=x_delimit_axe_relative,
                                     y=delimit_axe_y,
                                     height=delimit_axe_height,
                                     radius=0.1,
                                     text_height=0.1,
                                     symbol=self.columns_symbol[i],
                                     attr=GfxAttribs(linetype="CENTER"))

        # Drawing axe.
        if middle_axe:
            group += delimit_axe(document=document,
                                 x=x - self.height,
                                 y=y + self.height / 2,
                                 height=self.length + self.height * 2,
                                 symbol=middle_axe_symbol,
                                 direction=Direction.HORIZONTAL,
                                 attr=GfxAttribs(linetype="CENTER"))

        # Drawing of stirrups.
        if stirrups:
            for stirrup in self.stirrups:
                group += stirrup.draw_longitudinal(document=document,
                                                   x=x + (stirrup.x - self.x),
                                                   y=y + (stirrup.y - self.y),
                                                   unifilar=unifilar_stirrups)

        # Drawing of bars.
        if bars:
            self.bars_as_sup[0].draw_longitudinal(document=document,
                                                  x=x + (self.bars_as_sup[0].x - self.x),
                                                  y=y + (self.bars_as_sup[0].y - self.y),
                                                  unifilar=unifilar_bars,
                                                  dimensions=False,
                                                  denomination=False)  # Only mayor bar.
            self.bars_as_inf[0].draw_longitudinal(document=document,
                                                  x=x + (self.bars_as_inf[0].x - self.x),
                                                  y=y + (self.bars_as_inf[0].y - self.y),
                                                  unifilar=unifilar_bars,
                                                  dimensions=False,
                                                  denomination=False)  # Only inferior mayor bar.
            for bar in self.bars_as_left:
                bar.draw_longitudinal(document=document,
                                      x=x + (bar.x - self.x),
                                      y=y + (bar.y - self.y),
                                      unifilar=unifilar_bars,
                                      dimensions=False,
                                      denomination=False)  # Only left bars.

        # Drawing dimensions.
        if dim:
            dim_y = y + self.height * 2
            dim_p_base = (x + self.length / 2, y + delimit_axe_height * 0.65)

            for stirrup in self.stirrups:
                group += dim_linear(document=document,
                                    p_base=(x + (stirrup.x - self.x) + stirrup.reinforcement_length / 2, dim_y),
                                    p1=(x + (stirrup.x - self.x), dim_y),
                                    p2=(x + (stirrup.x - self.x) + stirrup.reinforcement_length, dim_y),
                                    dimstyle=dim_style)

            group += dim_linear(document=document,
                                p_base=dim_p_base,
                                p1=(x, y + self.height),
                                p2=(x + self.length, y + self.height),
                                dimstyle=dim_style)

        return group

    def draw_transverse(self,
                        document: Drawing,
                        x: float, y: float,
                        x_section: float = None,
                        unifilar: bool = False,
                        dimensions: bool = True) -> list:
        """
        Draws the transverse section of the beam at a given x-section.

        :param document: The DXF document where the beam will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the starting point for drawing.
        :type x: float
        :param y: Y-coordinate of the starting point for drawing.
        :type y: float
        :param x_section: The x-coordinate of the section to be drawn.
        :type x_section: float, optional
        :param unifilar: If True, the bars are drawn as unifilar.
        :type unifilar: bool
        :param dimensions: If True, dimensions are drawn.
        :type dimensions: bool
        :return: A list of graphical entities representing the transverse section of the beam.
        :rtype: list
        """

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
        bars = filter(lambda e: e.type == ElementTypes.BAR, entities)
        stirrups = filter(lambda e: e.type == ElementTypes.STIRRUP, entities)

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
    def draw_longitudinal_rebar_detailing(self,
                                          document: Drawing,
                                          x: float = None,
                                          y: float = None,
                                          unifilar: bool = True,
                                          columns_axes: bool = True) -> list:
        """
        Draws the longitudinal rebar detailing for the beam.

        :param document: The DXF document where the detailing will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the starting point for drawing.
        :type x: float, optional
        :param y: Y-coordinate of the starting point for drawing.
        :type y: float, optional
        :param unifilar: If True, the rebar is drawn as unifilar.
        :type unifilar: bool
        :param columns_axes: If True, the axes of the columns are drawn.
        :type columns_axes: bool
        :return: A list of graphical entities representing the longitudinal rebar detailing.
        :rtype: list
        """
        def __draw_section_bars(bars: list = None,
                                spacing: float = 0.2,
                                rebar_x: float = None,
                                rebar_y: float = None,
                                barline=True,
                                text_reference: str = None) -> tuple:
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
                                                             rebar_y=rebar_y, barline=barline,
                                                             text_reference="As sup.")
            group += entities

        if self.as_left:
            barline = True if self.bars_as_left or self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_right, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=barline,
                                                             text_reference="As right.")
            group += entities

        if self.as_left:
            barline = True if self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_left, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=barline,
                                                             text_reference="As left.")
            group += entities

        if self.as_inf:
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_inf, spacing=0.2, rebar_x=rebar_x,
                                                             rebar_y=rebar_y, barline=False,
                                                             text_reference="As inf.")
            group += entities

        if columns_axes:
            for i, x_column in enumerate(self.columns_pos):
                delimit_axe_height = y - rebar_y
                delimit_axe_y = rebar_y
                x_column_relative = x + x_column
                x_delimit_axe_relative = x_column_relative + self.columns[i][0] / 2

                group += delimit_axe(document=document,
                                     x=x_delimit_axe_relative,
                                     y=delimit_axe_y,
                                     height=delimit_axe_height,
                                     radius=0.1,
                                     text_height=0.1,
                                     attr=GfxAttribs(linetype="CENTER"))

        return group

    # Function that draws transverse section.
    def draw_transverse_rebar_detailing(self, document: Drawing,
                                        x: float = None,
                                        y: float = None,
                                        x_section: float = None,
                                        unifilar: bool = False,
                                        dimensions: bool = True) -> list:
        """
        Draws the transverse rebar detailing for the beam at a given x-section.

        :param document: The DXF document where the detailing will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the starting point for drawing.
        :type x: float, optional
        :param y: Y-coordinate of the starting point for drawing.
        :type y: float, optional
        :param x_section: The x-coordinate of the section to be drawn.
        :type x_section: float, optional
        :param unifilar: If True, the rebar is drawn as unifilar.
        :type unifilar: bool
        :param dimensions: If True, dimensions are drawn.
        :type dimensions: bool
        :return: A list of graphical entities representing the transverse rebar detailing.
        :rtype: list
        """
        stirrups = self.__elements_section(elements=self.stirrups,
                                           x=x_section)

        group = []
        for stirrup in stirrups:
            group += stirrup.draw_transverse(document=document,
                                             x=x,
                                             y=y,
                                             unifilar=unifilar,
                                             dimensions=dimensions)

        return group

    def draw_table_rebar_detailing(self, x: float = None,
                                   y: float = None,
                                   unifilar: bool = False):
        pass

    def __dict_to_bars(self, bars: dict,
                       width: float,
                       x: float,
                       y: float,
                       side: int,
                       anchor: list,
                       nomenclature: str = None,
                       number_init: int = None) -> list:
        """
        Converts a dictionary of bars into a list of Bar objects, placing them according to the specified side of
        the beam.

        :param bars: Dictionary containing bar information.
        :type bars: dict
        :param width: Width of the beam section.
        :type width: float
        :param x: X-coordinate of the starting point for placing the bars.
        :type x: float
        :param y: Y-coordinate of the starting point for placing the bars.
        :type y: float
        :param side: Indicates the side of the beam where the bars are placed (0: top, 1: right, 2: bottom, 3: left).
        :type side: int
        :param anchor: List of anchor lengths for each bar.
        :type anchor: list
        :param nomenclature: Nomenclature for the bars.
        :type nomenclature: str, optional
        :param number_init: Initial number for bar numbering.
        :type number_init: int, optional
        :return: A list of Bar objects representing the bars placed in the specified section of the beam.
        :rtype: list
        :raises ValueError: If the side is not within the range [0, 3].
        """
        if side < 0 or side > 3:
            raise ValueError

        list_bars, list_denom = gen_symmetric_list(dictionary=bars, nomenclature=nomenclature, number_init=number_init,
                                                   factor=1)  # Creating symetric list of bars.

        # Calculating separtion and definition of initial x_sep and y_sep.
        if side == 0 or side == 2:  # Sides top (0) or bottom (2).
            db_max = max(self.max_db_sup, self.max_db_inf) / 1
            width_util = width - self.cover * 2 + (db_max - max(list_bars))
            separation = width_util / (len(list_bars) - 1)
            x_sep, y_sep = -separation, 0

        else:  # Sides right (1) or left (3).
            db_max = max([self.max_db_right, self.max_db_left]) / 1
            width_util = width - self.cover * 2
            separation = width_util / (len(list_bars) + 1)
            x_sep, y_sep = 0, 0

        # Generating bars.
        entities, delta_x, delta_y, orientation = [], 0, 0, Orientation.BOTTOM
        for i, db in enumerate(list_bars):
            # Calculation of x_delta and y_delta.
            if side == 0 or side == 2:
                x_sep += separation
                delta_x = -self.cover + db_max / 2
                if side == 0:
                    delta_y = self.height - self.cover - 3 * db / 2 - anchor[i]
                    delta_y_transverse = self.height - self.cover + self.max_db_sup / 2 - db
                    orientation = Orientation.RIGHT
                if side == 2:
                    delta_y = self.cover - self.max_db_inf / 2
                    delta_y_transverse = self.cover - self.max_db_inf / 2
                    orientation = Orientation.TOP
            else:
                y_sep += separation
                delta_y = self.cover - db / 2

                if side == 1:
                    delta_x = self.cover + db - max([self.max_db_sup, self.max_db_inf, self.max_db_right]) / 2 - self.width
                    delta_y_transverse = delta_y
                    orientation = Orientation.RIGHT
                if side == 3:
                    delta_x = - self.cover + max([self.max_db_sup, self.max_db_inf, self.max_db_left]) / 2
                    delta_y_transverse = delta_y
                    orientation = Orientation.RIGHT

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
    def __elements_section(self,
                           elements: list = None,
                           x: float = None) -> list:
        """
        Filters and returns the elements that are located within the specified X-coordinate section of the beam.

        :param elements: List of elements (bars and stirrups) to filter.
        :type elements: list, optional
        :param x: X-coordinate of the beam section. If None, defaults to the middle of the beam.
        :type x: float, optional
        :return: List of elements located within the specified X-coordinate section.
        :rtype: list
        """
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
        """
        Generates and returns a list of Stirrup objects based on data given at initialization.

        :return: A list of Stirrup objects representing the stirrups in the beam.
        :rtype: list
        """
        stirrup_width = self.width - (self.cover - max(self.max_db_sup, self.max_db_inf) / 2) * 2
        stirrup_height = self.height - (self.cover * 2 - self.max_db_sup / 2 - self.max_db_inf / 2)
        stirrups = zip(self.stirrups_db, self.stirrups_length, self.stirrups_sep, self.stirrups_anchor, self.stirrups_x)
        mandrel_radius_sup = self.max_db_sup / 2
        mandrel_radius_inf = self.max_db_inf / 2

        # Generating stirrups.
        entities = []  # Empty list that will contain stirrups elements.
        for stirrup in stirrups:
            stirrup_x = self.x + stirrup[4]  # Difining x coordinate.
            stirrup_y = self.y + self.cover - self.max_db_inf / 2 - stirrup[0]  # Subract of thick of stirrup.

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
                                    anchor=stirrup[3]))

        return entities
