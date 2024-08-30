# Local imports.
from etacad.bar import Bar
from etacad.drawing_utils import delimit_axe, dim_linear, rect, text
from etacad.globals import (COLUMN_SET_TRANSVERSE, COLUMN_SET_LONG_REBAR, ColumnTypes, Direction, ElementTypes,
                            Orientation)
from etacad.stirrup import Stirrup
from etacad.utils import gen_symmetric_list

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs


@define
class Column:
    """
    Column element, computes geometrics and physics props and manages dxf drawing methods (longitudinal, transversal,
    reinforcement detailing, etc.)

    :param width: Width of the column in meters.
    :type width: float
    :param depth: Depth of the column in meters.
    :type depth: float
    :param height: Height of the column in meters.
    :type height: float
    :param diameter: Diameter of the column in meters. Default is None.
    :type diameter: float, optional
    :param column_type: Type of column (e.g., rectangular, circular).
    :type column_type: int
    :param x: X-coordinate of the column's position.
    :type x: float
    :param y: Y-coordinate of the column's position.
    :type y: float
    :param direction: Direction of the column (e.g., vertical, horizontal).
    :type direction: Direction
    :param orientation: Orientation of the column (e.g., left, right).
    :type orientation: Orientation

    :ivar as_sup: Dictionary containing the top longitudinal reinforcement details.
    :vartype as_sup: dict
    :ivar as_right: Dictionary containing the right longitudinal reinforcement details.
    :vartype as_right: dict
    :ivar as_inf: Dictionary containing the bottom longitudinal reinforcement details.
    :vartype as_inf: dict
    :ivar as_left: Dictionary containing the left longitudinal reinforcement details.
    :vartype as_left: dict

    :ivar max_db_sup: Maximum diameter of the top longitudinal bars.
    :vartype max_db_sup: float
    :ivar max_db_right: Maximum diameter of the right longitudinal bars.
    :vartype max_db_right: float
    :ivar max_db_inf: Maximum diameter of the bottom longitudinal bars.
    :vartype max_db_inf: float
    :ivar max_db_left: Maximum diameter of the left longitudinal bars.
    :vartype max_db_left: float
    :ivar max_db_hz: Maximum horizontal diameter among the longitudinal bars.
    :vartype max_db_hz: float
    :ivar max_db_vt: Maximum vertical diameter among the longitudinal bars.
    :vartype max_db_vt: float

    :ivar anchor_sup: List of top bar anchorage lengths.
    :vartype anchor_sup: list
    :ivar anchor_right: List of right bar anchorage lengths.
    :vartype anchor_right: list
    :ivar anchor_inf: List of bottom bar anchorage lengths.
    :vartype anchor_inf: list
    :ivar anchor_left: List of left bar anchorage lengths.
    :vartype anchor_left: list

    :ivar bars_as_sup: List of bars in the top longitudinal reinforcement.
    :vartype bars_as_sup: list
    :ivar bars_as_right: List of bars in the right longitudinal reinforcement.
    :vartype bars_as_right: list
    :ivar bars_as_inf: List of bars in the bottom longitudinal reinforcement.
    :vartype bars_as_inf: list
    :ivar bars_as_left: List of bars in the left longitudinal reinforcement.
    :vartype bars_as_left: list

    :ivar number_init_sup: Initial number for top longitudinal bars.
    :vartype number_init_sup: int
    :ivar number_init_right: Initial number for right longitudinal bars.
    :vartype number_init_right: int
    :ivar number_init_inf: Initial number for bottom longitudinal bars.
    :vartype number_init_inf: int
    :ivar number_init_left: Initial number for left longitudinal bars.
    :vartype number_init_left: int

    :ivar cover: Concrete cover thickness.
    :vartype cover: float

    :ivar stirrups_db: List of stirrup diameters.
    :vartype stirrups_db: list
    :ivar stirrups_anchor: List of stirrup anchorage lengths.
    :vartype stirrups_anchor: list
    :ivar stirrups_sep: List of stirrup separations.
    :vartype stirrups_sep: list
    :ivar stirrups_length: List of stirrup lengths.
    :vartype stirrups_length: list
    :ivar stirrups_x: List of stirrup X-coordinates.
    :vartype stirrups_x: list
    :ivar stirrups: List of stirrup elements.
    :vartype stirrups: list

    :ivar beams: List of crossing beams.
    :vartype beams: list
    :ivar beams_pos: List of crossing beams' positions.
    :vartype beams_pos: list
    :ivar beam_symbol: List of crossing beams' symbols.
    :vartype beam_symbol: list

    :ivar all_bars: List of all bars in the column.
    :vartype all_bars: list
    :ivar all_elements: List of all elements in the column.
    :vartype all_elements: list

    :ivar concrete_volume: Concrete volume required for the column.
    :vartype concrete_volume: float

    :ivar box_width: Width of the bounding box for the column.
    :vartype box_width: float
    :ivar box_height: Height of the bounding box for the column.
    :vartype box_height: float

    :ivar nomenclature: Nomenclature for the column reinforcement.
    :vartype nomenclature: str
    :ivar num_init: Initial number for bar enumeration.
    :vartype num_init: int
    :ivar element_type: Type of element, set to COLUMN by default.
    :vartype element_type: int
    """
    # Geometric attributes.
    width: float
    depth: float
    height: float
    diameter: float = field(default=None)
    column_type: int = field(default=ColumnTypes.RECTANGULAR)
    x: float = field(default=0)
    y: float = field(default=0)
    direction: Direction = Direction.VERTICAL
    orientation: Orientation = Orientation.RIGHT

    # Longitudinal steel attributes.
    as_sup: dict = field(default=None)
    as_right: dict = field(default=None)
    as_inf: dict = field(default=None)
    as_left: dict = field(default=None)

    max_db_sup: float = field(init=False)
    max_db_right: float = field(init=False)
    max_db_inf: float = field(init=False)
    max_db_left: float = field(init=False)
    max_db_hz: float = field(init=False)
    max_db_vt: float = field(init=False)

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

    # Entities groups.
    all_bars: list = field(init=False)
    all_elements: list = field(init=False)

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

        self.max_db_hz = max(self.max_db_sup, self.max_db_inf)
        self.max_db_vt = max(self.max_db_right, self.max_db_left)

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

        # Entities groups.
        self.all_bars = self.bars_as_sup + self.bars_as_right + self.bars_as_inf + self.bars_as_left
        self.all_elements = self.all_bars + self.stirrups

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
        """
        Draws the longitudinal view of the column, including concrete shape, beams,
        stirrups, and bars. Also includes dimensioning and optional middle axes.

        :param document: The drawing document to which the elements will be added.
        :type document: Drawing
        :param x: X-coordinate for the drawing position. Defaults to column's x position.
        :type x: float, optional
        :param y: Y-coordinate for the drawing position. Defaults to column's y position.
        :type y: float, optional
        :param concrete_shape: Whether to draw the concrete shape. Defaults to True.
        :type concrete_shape: bool
        :param bars: Whether to draw the longitudinal bars. Defaults to True.
        :type bars: bool
        :param beams: Whether to draw crossing beams. Defaults to True.
        :type beams: bool
        :param beams_axes: Whether to draw the axes for beams. Defaults to True.
        :type beams_axes: bool
        :param stirrups: Whether to draw the stirrups. Defaults to True.
        :type stirrups: bool
        :param middle_axe: Whether to draw the middle axis. Defaults to True.
        :type middle_axe: bool
        :param middle_axe_symbol: Symbol to use for the middle axis. Defaults to "A".
        :type middle_axe_symbol: str
        :param dim: Whether to add dimensions to the drawing. Defaults to True.
        :type dim: bool
        :param dim_style: Style of the dimensions. Defaults to "EZ_M_25_H25_CM".
        :type dim_style: str
        :param unifilar_bars: Whether to draw bars in unifilar view. Defaults to False.
        :type unifilar_bars: bool
        :param unifilar_stirrups: Whether to draw stirrups in unifilar view. Defaults to True.
        :type unifilar_stirrups: bool
        :return: A list of entities drawn on the document.
        :rtype: list
        """
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
                                       p_base=(x - self.width * 3,
                                               y + (stirrup.y - self.y) + stirrup.reinforcement_length / 2),
                                       p1=(x, y + (stirrup.y - self.y)),
                                       p2=(x, y + (stirrup.y - self.y) + stirrup.reinforcement_length),
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
                                                      x=x + (stirrup.x - self.x),
                                                      y=y + (stirrup.y - self.y),
                                                      unifilar=unifilar_stirrups)

        # Drawing of bars.
        if bars:
            for bar in self.bars_as_inf:
                delta_unfilar = 0 if not unifilar_bars else -bar.radius
                entities += bar.draw_longitudinal(document=document,
                                                  x=x + (bar.x - self.x) + delta_unfilar,
                                                  y=y + (bar.y - self.y),
                                                  unifilar=unifilar_bars,
                                                  dimensions=False,
                                                  denomination=False)  # Only left bars.

        return entities

    def draw_transverse(self,
                        document: Drawing,
                        x: float,
                        y: float,
                        y_section: float = None,
                        unifilar: bool = False,
                        dimensions: bool = True,
                        settings: dict = COLUMN_SET_TRANSVERSE) -> list:
        """
        Draws the transverse view of the column at a given y-section.
        generate a drawing from the transverse perspective.

        :param document: The DXF document where the column will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the starting point for drawing.
        :type x: float
        :param y: Y-coordinate of the starting point for drawing.
        :type y: float
        :param y_section: The y-coordinate of the section to be drawn.
        :type y_section: float, optional
        :param unifilar: If True, the bars are drawn as unifilar.
        :type unifilar: bool
        :param dimensions: If True, dimensions are drawn.
        :type dimensions: bool
        :param settings: Dict with column transverse drawing settings.
        :type settings: dict
        :return: A list of entities representing the transverse view of the column.
        :rtype: list
        """
        if y_section is None:
            y_section = self.height / 2

        # Checking if y given is in column height.
        if not 0 <= y_section <= self.height:
            return []

        # Obtaining elements for given y_section.
        entities = self.__elements_section(y=y_section)

        # Filtering elements.
        bars = filter(lambda e: e.element_type == ElementTypes.BAR, entities)
        stirrups = filter(lambda e: e.element_type == ElementTypes.STIRRUP, entities)

        # Concrete shape drawing.
        group = rect(doc=document, width=self.width, height=self.depth, x=x, y=y, polyline=True)

        # Drawing of bars.
        for bar in bars:
            group += bar.draw_transverse(document=document, x=x, y=y)

        # Drawing of stirrups.
        for stirrup in stirrups:
            delta_x = self.cover - max(self.max_db_sup, self.max_db_inf) / 2 - stirrup.diameter
            delta_y = self.cover - self.max_db_inf / 2 - stirrup.diameter

            group += stirrup.draw_transverse(document=document,
                                             x=x + delta_x,
                                             y=y + delta_y,
                                             unifilar=unifilar)

        # Drawing of dimensions.
        if dimensions:
            group += dim_linear(document=document,
                                p_base=(x - settings["text_dim_distance"], y + self.depth / 2),
                                p1=(x, y),
                                p2=(x, y + self.depth),
                                rotation=90,
                                dimstyle="EZ_M_10_H25_CM")
            group += dim_linear(document=document,
                                p_base=(x + self.width / 2, y + self.depth + settings["text_dim_distance"]),
                                p1=(x, y + self.depth),
                                p2=(x + self.width, y + self.depth),
                                dimstyle="EZ_M_10_H25_CM")

        return group

    def draw_longitudinal_rebar_detailing(self,
                                          document: Drawing,
                                          x: float = None,
                                          y: float = None,
                                          unifilar: bool = True,
                                          beam_axes: bool = True,
                                          settings: dict = COLUMN_SET_LONG_REBAR) -> list:
        """
        Draws the longitudinal rebar detailing for the column.

        :param document: The DXF document where the detailing will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the starting point for drawing.
        :type x: float, optional
        :param y: Y-coordinate of the starting point for drawing.
        :type y: float, optional
        :param unifilar: If True, the rebar is drawn as unifilar.
        :type unifilar: bool
        :param beam_axes: If True, the axes of the beam are drawn.
        :type beam_axes: bool
        :param settings: Dict with column longitudinal rebar drawing settings.
        :type settings: dict
        :return: A list of graphical entities representing the longitudinal rebar detailing.
        :rtype: list
        """
        def __draw_section_bars(bars: list = None,
                                spacing: float = 0.2,
                                rebar_x: float = None,
                                rebar_y: float = None,
                                barline=True,
                                text_reference: str = None) -> tuple:
            entities = []
            graph_list = []

            if text_reference:
                entities += text(document=document,
                                 text=text_reference,
                                 height=settings["text_height"],
                                 point=(rebar_x + 0.02, rebar_y + self.height + spacing * 2))

            for bar in bars:
                if bar.denomination not in graph_list:
                    rebar_x += spacing + bar.box_height
                    entities += bar.draw_longitudinal(document=document,
                                                      x=rebar_x,
                                                      y=rebar_y,
                                                      unifilar=unifilar,
                                                      dimensions=True)
                    graph_list.append(bar.denomination)

            if barline:
                entities += rect(doc=document,
                                 width=0,
                                 height=self.height + self.depth * 4,
                                 x=rebar_x + spacing,
                                 y=rebar_y - spacing,
                                 sides=(0, 1, 0, 0))

            rebar_x += spacing

            return entities, rebar_x, rebar_y

        group, rebar_x, rebar_y = [], x, y
        if self.as_sup:
            barline = True if self.as_right or self.bars_as_left or self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_sup,
                                                             spacing=0.2,
                                                             rebar_x=rebar_x,
                                                             rebar_y=rebar_y,
                                                             barline=barline,
                                                             text_reference="As sup.")
            group += entities

        if self.as_left:
            barline = True if self.bars_as_left or self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_right,
                                                             spacing=0.2,
                                                             rebar_x=rebar_x,
                                                             rebar_y=rebar_y,
                                                             barline=barline,
                                                             text_reference="As right.")
            group += entities

        if self.as_left:
            barline = True if self.bars_as_inf else False
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_left,
                                                             spacing=0.2,
                                                             rebar_x=rebar_x,
                                                             rebar_y=rebar_y,
                                                             barline=barline,
                                                             text_reference="As left.")
            group += entities

        if self.as_inf:
            entities, rebar_x, rebar_y = __draw_section_bars(bars=self.bars_as_inf,
                                                             spacing=0.2,
                                                             rebar_x=rebar_x,
                                                             rebar_y=rebar_y,
                                                             barline=False,
                                                             text_reference="As inf.")
            group += entities

        # if beam_axes:
        #     for i, x_column in enumerate(self.beams_pos):
        #         delimit_axe_height = y - rebar_y
        #         delimit_axe_y = rebar_y
        #         x_column_relative = x + x_column
        #         x_delimit_axe_relative = x_column_relative + self.columns[i][0] / 2
        #
        #         group += delimit_axe(document=document,
        #                              x=x_delimit_axe_relative,
        #                              y=delimit_axe_y,
        #                              height=delimit_axe_height,
        #                              radius=0.1,
        #                              text_height=0.1,
        #                              attr=GfxAttribs(linetype="CENTER"))

        return group

    def draw_transverse_rebar_detailing(self, document: Drawing,
                                        x: float = None,
                                        y: float = None,
                                        y_section: float = None,
                                        unifilar: bool = False,
                                        dimensions: bool = True) -> list:
        """
        Draws the transverse rebar detailing for the column at a given y-section.

        :param document: The DXF document where the detailing will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the starting point for drawing.
        :type x: float, optional
        :param y: Y-coordinate of the starting point for drawing.
        :type y: float, optional
        :param y_section: The y-coordinate of the section to be drawn.
        :type y_section: float, optional
        :param unifilar: If True, the rebar is drawn as unifilar.
        :type unifilar: bool
        :param dimensions: If True, dimensions are drawn.
        :type dimensions: bool
        :return: A list of graphical entities representing the transverse rebar detailing.
        :rtype: list
        """
        if y_section is None:
            y_section = self.height / 2

        # Checking if x given is in beam length.
        if not 0 <= y_section <= self.height:
            return []

        stirrups = self.__elements_section(elements=self.stirrups,
                                           y=y_section)

        group = []
        for stirrup in stirrups:
            group += stirrup.draw_transverse(document=document,
                                             x=x,
                                             y=y,
                                             unifilar=unifilar,
                                             dimensions=dimensions)

        return group

    def __dict_to_bars(self, bars: dict,
                       width: float,
                       x: float,
                       y: float,
                       side: Orientation,
                       anchor: list,
                       nomenclature: str = None,
                       number_init: int = None) -> list:
        """
        Converts a dictionary of bars into a list of Bar objects, placing them according to the specified side of
        the column.

        :param bars: Dictionary containing bar information.
        :type bars: dict
        :param width: Width of the column section.
        :type width: float
        :param x: X-coordinate of the starting point for placing the bars.
        :type x: float
        :param y: Y-coordinate of the starting point for placing the bars.
        :type y: float
        :param side: Indicates the side of the column where the bars are placed (0: top, 1: right, 2: bottom, 3: left).
        :type side: int
        :param anchor: List of anchor lengths for each bar.
        :type anchor: list
        :param nomenclature: Nomenclature for the bars.
        :type nomenclature: str, optional
        :param number_init: Initial number for bar numbering.
        :type number_init: int, optional
        :return: A list of Bar objects representing the bars placed in the specified section of the column.
        :rtype: list
        :raises ValueError: If the side is not within the range [0, 3].
        """
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
        entities, delta_x, delta_y, orientation = [], 0, 0, Orientation.BOTTOM
        for i, db in enumerate(list_bars):
            # Calculation of x_delta and y_delta.
            if side == Orientation.TOP or side == Orientation.BOTTOM:
                x_sep += separation
                delta_x = (self.cover - db_max / 2 + (db_max / 2 - db / 2)) * -1
                if side == Orientation.TOP:
                    delta_y_transverse = self.depth - self.cover + self.max_db_sup / 2 - db
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

    def __elements_section(self,
                           elements: list = None,
                           y: float = None) -> list:
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
            y = self.y + self.height / 2  # Default value if is nothing entered.

        # Filtering elements by X coordinate.
        entities = []
        for element in elements:
            if element.y <= self.y + y <= element.y + element.reinforcement_length:
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
            stirrup_x = self.x + self.cover - self.max_db_inf / 2 - stirrup[0]  # Subract of thick of stirrup.
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
                                    anchor=stirrup[3]))

        return entities
