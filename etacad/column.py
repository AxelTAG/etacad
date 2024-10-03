# Local imports.
from etacad.bar import Bar
from etacad.cadtable import CADTable
from etacad.concrete import Concrete
from etacad.drawing_utils import delimit_axe, dim_linear, rect, text
from etacad.globals import (COLUMN_SET_TRANSVERSE, COLUMN_SET_LONG_REBAR, ColumnTypes, Direction, ElementTypes,
                            Orientation, CONCRETE_WEIGHT, COLUMN_SET_LONG, COLUMN_SET_TRANSVERSE_REBAR)
from etacad.stirrup import Stirrup
from etacad.utils import gen_symmetric_list, gen_position_bars

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs
from itertools import chain


@define
class Column:
    """
    Column element, computes geometrics and physics props and manages dxf drawing methods (longitudinal, transversal,
    reinforcement detailing, etc.)

    :param width: Width of the column (rectangular section) in units of length.
    :type width: float
    :param depth: Depth of the column (rectangular section) in units of length.
    :type depth: float
    :param height: Height of the column in units of length.
    :type height: float
    :param diameter: Diameter of the column if circular (optional), defaults to None.
    :type diameter: float, optional
    :param column_type: Type of column section (rectangular or circular), defaults to RECTANGULAR.
    :type column_type: int
    :param x: X-coordinate of the column's position, defaults to 0.
    :type x: float
    :param y: Y-coordinate of the column's position, defaults to 0.
    :type y: float
    :param direction: Orientation of the column (VERTICAL or HORIZONTAL), defaults to VERTICAL.
    :type direction: Direction
    :param orientation: Column's orientation (RIGHT, LEFT, etc.), defaults to RIGHT.
    :type orientation: Orientation
    :param as_sup: Dictionary representing the longitudinal steel in the upper part of the column.
    :type as_sup: dict, optional
    :param as_right: Dictionary representing the longitudinal steel in the right side of the column.
    :type as_right: dict, optional
    :param as_inf: Dictionary representing the longitudinal steel in the lower part of the column.
    :type as_inf: dict, optional
    :param as_left: Dictionary representing the longitudinal steel in the left side of the column.
    :type as_left: dict, optional
    :param anchor_sup: List of anchorage values for the upper part of the column.
    :type anchor_sup: list, optional
    :param anchor_right: List of anchorage values for the right side of the column.
    :type anchor_right: list, optional
    :param anchor_inf: List of anchorage values for the lower part of the column.
    :type anchor_inf: list, optional
    :param anchor_left: List of anchorage values for the left side of the column.
    :type anchor_left: list, optional
    :param cover: Concrete cover of the column in units of length.
    :type cover: float, optional
    :param concrete_specific_weight: Specific weight of the concrete used in the column.
    :type concrete_specific_weight: float
    :param stirrups_db: List of diameters of the stirrups used in the column.
    :type stirrups_db: list, optional
    :param stirrups_anchor: List of anchorage values for the stirrups.
    :type stirrups_anchor: list, optional
    :param stirrups_sep: List of spacing values between stirrups.
    :type stirrups_sep: list, optional
    :param stirrups_length: List of lengths of stirrups.
    :type stirrups_length: list, optional
    :param stirrups_x: List of x-coordinates for stirrups placement.
    :type stirrups_x: list, optional
    :param beams: List of crossing beams interacting with the column.
    :type beams: list, optional
    :param beams_pos: List of positions for the crossing beams.
    :type beams_pos: list, optional
    :param beam_symbol: List of symbols used to represent crossing beams.
    :type beam_symbol: list, optional
    :param nomenclature: Column identification string or nomenclature.
    :type nomenclature: str, optional

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

    :ivar box_width: Width of the bounding box for the column.
    :vartype box_width: float
    :ivar box_height: Height of the bounding box for the column.
    :vartype box_height: float

    :ivar nomenclature: Nomenclature for the column reinforcement.
    :vartype nomenclature: str
    :ivar element_type: Type of element, set to COLUMN by default.
    :vartype element_type: int
    """
    # Geometric attributes.
    width: float = field(converter=float)
    depth: float = field(converter=float)
    height: float = field(converter=float)
    diameter: float = field(default=None)
    column_type: int = field(default=ColumnTypes.RECTANGULAR)
    x: float = field(default=0, converter=float)
    y: float = field(default=0, converter=float)
    direction: Direction = field(default=Direction.VERTICAL)
    orientation: Orientation = field(default=Orientation.RIGHT)

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

    number_init_sup: int = field(init=False)
    number_init_right: int = field(init=False)
    number_init_inf: int = field(init=False)
    number_init_left: int = field(init=False)

    cover: float = field(default=0, converter=float)

    # Concrete attributes.
    concrete: Concrete = field(init=False)
    concrete_specific_weight: float = CONCRETE_WEIGHT

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

    # Box attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)

    # Position bar attributes.
    nomenclature: str = field(default="#")
    positions: dict = field(init=False)

    # Column attributes.
    denomination: str = field(default=None)
    number_init: int = field(default=None)
    element_type: ElementTypes = field(default=ElementTypes.COLUMN)

    def __attrs_post_init__(self):
        # Longitudinal steel attributes.
        if self.number_init is None:
            self.number_init = 0

        # Top bars.
        if self.as_sup:
            self.max_db_sup = max(self.as_sup.keys())
            self.number_init_sup = self.number_init if self.number_init else 0
            self.number_init = self.number_init + len(self.as_sup) if self.number_init else len(self.as_sup)

            self.anchor_sup = self.anchor_sup if type(self.anchor_sup) == list else [self.anchor_sup] * sum(
                self.as_sup.values())
        else:
            self.as_sup, self.max_db_sup, self.number_init_sup = {}, 0, 0

        # Right bars.
        if self.as_right:
            self.max_db_right = max(self.as_right.keys())
            self.number_init_right = self.number_init if self.number_init is not None else 0
            self.number_init = self.number_init + len(self.as_right) if self.number_init else len(self.as_right)

            self.anchor_right = self.anchor_right if type(self.anchor_right) == list else [self.anchor_right] * sum(
                self.as_right.values())
        else:
            self.as_right, self.max_db_right, self.number_init_right = {}, 0, 0

        # Inferior bars.
        if self.as_inf:
            self.max_db_inf = max(self.as_inf.keys())
            self.number_init_inf = self.number_init if self.number_init is not None else 0
            self.number_init = self.number_init + len(self.as_inf) if self.number_init else len(self.as_inf)

            self.anchor_inf = self.anchor_inf if type(self.anchor_inf) == list else [self.anchor_inf] * sum(
                self.as_inf.values())
        else:
            self.as_inf, self.max_db_inf, self.number_init_inf = {}, 0, 0

        # Left bars.
        if self.as_left:
            self.max_db_left = max(self.as_left.keys())
            self.number_init_left = self.number_init if self.number_init is not None else 0
            self.number_init = self.number_init + len(self.as_left) if self.number_init else len(self.as_left)

            self.anchor_left = self.anchor_left if type(self.anchor_left) == list else [self.anchor_left] * sum(
                self.as_left.values())
        else:
            self.as_left, self.max_db_left, self.number_init_left = {}, 0, 0

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

        # Concrete attributes.
        vertices = [(0, 0),
                    (0, self.depth),
                    (self.width, self.depth),
                    (self.width, 0)]

        self.concrete = Concrete(vertices=vertices,
                                 height=self.height,
                                 x=self.x,
                                 y=self.y,
                                 specific_weight=self.concrete_specific_weight)

        # Stirrups attributes.
        self.stirrups = self.__list_to_stirrups()

        # Position bar attributes.
        min_number_init = min(self.number_init_sup, self.number_init_right, self.number_init_inf, self.number_init_left)

        self.positions = gen_position_bars(dictionaries=[self.as_sup, self.as_right, self.as_inf, self.as_left],
                                           nomenclature=self.nomenclature,
                                           number_init=min_number_init)

        # Entities groups.
        self.all_bars = self.bars_as_sup + self.bars_as_right + self.bars_as_inf + self.bars_as_left
        self.all_elements = self.all_bars + self.stirrups

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
                          unifilar_stirrups: bool = True) -> dict:
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
        :return: A dict of entities drawn on the document.
        :rtype: dict
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {"concrete": [],
                    "beam_elements": [],
                    "beam_axe_elements": [],
                    "column_axe_elements": [],
                    "dimensions_elements": [],
                    "stirrups": [],
                    "bars": []}

        delimit_axe_width = self.width * 4
        delimit_axe_x = x - self.width * 2

        # Drawing concrete shape.
        if concrete_shape:
            elements["concrete"] = self.concrete.draw_longitudinal(document=document,
                                                                   x=x,
                                                                   y=y,
                                                                   dimensions=dim,
                                                                   dimensions_inner=False,
                                                                   settings=COLUMN_SET_LONG["concrete_settings"])

        # Drawing beams.
        if self.beams:
            if beams:
                for i, y_beam in enumerate(self.beams_pos):
                    y_column_relative = y + y_beam
                    y_delimit_axe_relative = y_column_relative + self.beams[i][1] / 2
                    if beams:
                        elements["beam_elements"] += rect(doc=document,
                                                          width=self.beams[i][0],
                                                          height=self.beams[i][1],
                                                          x=x,
                                                          y=y_column_relative,
                                                          fill=True,
                                                          polyline=True)
                    if beams_axes:
                        elements["beam_axe_elements"] += delimit_axe(document=document,
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
            elements["column_axe_elements"] += delimit_axe(document=document,
                                                           x=x + self.width / 2,
                                                           y=y - self.width * 2,
                                                           height=self.height + self.width * 4,
                                                           symbol=middle_axe_symbol,
                                                           direction=Direction.VERTICAL,
                                                           attr=GfxAttribs(linetype="CENTER"))

        # Drawing of stirrups.
        if stirrups:
            for stirrup in self.stirrups:
                elements["stirrups"].append(stirrup.draw_longitudinal(document=document,
                                                                      x=x + (stirrup.x - self.x),
                                                                      y=y + (stirrup.y - self.y),
                                                                      unifilar=unifilar_stirrups))
            # Drawing dimensions.
            if dim:
                for stirrup in self.stirrups:
                    elements["dimensions_elements"] += dim_linear(document=document,
                                                                  p_base=(x - self.width * 3,
                                                                          y + (stirrup.y - self.y) + stirrup.reinforcement_length / 2),
                                                                  p1=(x, y + (stirrup.y - self.y)),
                                                                  p2=(x, y + (stirrup.y - self.y) + stirrup.reinforcement_length),
                                                                  rotation=90,
                                                                  dimstyle=dim_style)

        # Drawing of bars.
        if self.as_sup or self.as_right or self.as_inf or self.as_left:
            if bars:
                for bar in self.bars_as_inf:
                    delta_unfilar = 0 if not unifilar_bars else - bar.radius
                    elements["bars"].append(bar.draw_longitudinal(document=document,
                                                                  x=x + (bar.x - self.x) + delta_unfilar,
                                                                  y=y + (bar.y - self.y),
                                                                  unifilar=unifilar_bars,
                                                                  dimensions=False,
                                                                  denomination=False))  # Only left bars.

        # Setting groups of elements in dictionary.
        elements["all_elements"] = (elements["concrete"]["all_elements"] +
                                    elements["beam_elements"] +
                                    elements["beam_axe_elements"] +
                                    elements["column_axe_elements"] +
                                    elements["dimensions_elements"] +
                                    list(chain(*[bar_dict["all_elements"] for bar_dict in elements["bars"]])) +
                                    list(chain(*[st_dict["all_elements"] for st_dict in elements["stirrups"]])))

        return elements

    def draw_transverse(self,
                        document: Drawing,
                        x: float = None,
                        y: float = None,
                        y_section: float = None,
                        unifilar: bool = False,
                        dimensions: bool = True,
                        settings: dict = COLUMN_SET_TRANSVERSE) -> dict:
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
        :return: A dict of entities representing the transverse view of the column.
        :rtype: dict
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        if y_section is None:
            y_section = self.height / 2

        # Checking if y given is in column height.
        if not 0 <= y_section <= self.height:
            return []

        elements = {"concrete": None,
                    "bars": [],
                    "stirrups": []}

        # Obtaining elements for given y_section.
        entities = self.__elements_section(y=y_section)

        # Filtering elements.
        bars = filter(lambda e: e.element_type == ElementTypes.BAR, entities)
        stirrups = filter(lambda e: e.element_type == ElementTypes.STIRRUP, entities)

        # Concrete shape drawing.
        elements["concrete"] = self.concrete.draw_transverse(document=document,
                                                             x=x,
                                                             y=y,
                                                             dimensions=True,
                                                             dimensions_boxing=True,
                                                             dimensions_inner=False,
                                                             settings=settings["concrete_settings"])

        # Drawing of bars.
        for bar in bars:
            elements["bars"].append(bar.draw_transverse(document=document, x=x, y=y))

        # Drawing of stirrups.
        for stirrup in stirrups:
            delta_x = self.cover - max(self.max_db_sup, self.max_db_inf) / 2 - stirrup.diameter
            delta_y = self.cover - self.max_db_inf / 2 - stirrup.diameter

            elements["stirrups"].append(stirrup.draw_transverse(document=document,
                                                                x=x + delta_x,
                                                                y=y + delta_y,
                                                                unifilar=unifilar))

        # Setting groups of elements in dictionary.
        elements["all_elements"] = (elements["concrete"]["all_elements"] +
                                    list(chain(*[bar_dict["all_elements"] for bar_dict in elements["bars"]])) +
                                    list(chain(*[st_dict["all_elements"] for st_dict in elements["stirrups"]])))

        return elements

    def draw_longitudinal_rebar_detailing(self,
                                          document: Drawing,
                                          x: float = None,
                                          y: float = None,
                                          unifilar: bool = True,
                                          beam_axes: bool = True,
                                          settings: dict = COLUMN_SET_LONG_REBAR) -> dict:
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
        :return: A dict of graphical entities representing the longitudinal rebar detailing.
        :rtype: dict
        """

        elements = {"text_elements": [],
                    "bars": [],
                    "barline_elements": [],
                    "beam_axes_elements": [],
                    "all_elements": []}

        def __draw_section_bars(bars: list = None,
                                spacing: float = settings["spacing"],
                                rebar_x: float = None,
                                rebar_y: float = None,
                                barline=True,
                                text_reference: str = None) -> tuple:

            bars_elements = []
            text_elements = []
            barline_elements = []

            if text_reference:
                text_elements += text(document=document,
                                      text=text_reference,
                                      height=settings["text_height"],
                                      point=(rebar_x + 0.02, rebar_y + self.height + spacing * 2))

            unique_bars_list = []
            for bar in bars:
                if bar.denomination not in unique_bars_list:
                    rebar_x += spacing + bar.box_height
                    bars_elements.append(bar.draw_longitudinal(document=document,
                                                               x=rebar_x,
                                                               y=rebar_y,
                                                               unifilar=unifilar,
                                                               dimensions=True,
                                                               settings=settings["bar_settings"]))
                    unique_bars_list.append(bar.denomination)

            if barline:
                barline_elements += rect(doc=document,
                                         width=0,
                                         height=self.height + self.depth * 4,
                                         x=rebar_x + spacing,
                                         y=rebar_y - spacing,
                                         sides=(0, 1, 0, 0))

            rebar_x += spacing

            return text_elements, bars_elements, barline_elements, rebar_x, rebar_y

        group, rebar_x, rebar_y = [], x, y
        if self.as_sup:
            barline = True if self.as_right or self.bars_as_left or self.bars_as_inf else False
            elements_tuple = __draw_section_bars(bars=self.bars_as_sup,
                                                 spacing=settings["spacing"],
                                                 rebar_x=rebar_x,
                                                 rebar_y=rebar_y,
                                                 barline=barline,
                                                 text_reference="As sup.")

            text_elements, bars, barline_elements, rebar_x, rebar_y = elements_tuple

            elements["text_elements"].extend(text_elements)
            elements["bars"].extend(bars)
            elements["barline_elements"].extend(barline_elements)

        if self.as_right:
            barline = True if self.bars_as_left or self.bars_as_inf else False
            elements_tuple = __draw_section_bars(bars=self.bars_as_right,
                                                 spacing=settings["spacing"],
                                                 rebar_x=rebar_x,
                                                 rebar_y=rebar_y,
                                                 barline=barline,
                                                 text_reference="As right.")

            text_elements, bars, barline_elements, rebar_x, rebar_y = elements_tuple

            elements["text_elements"].extend(text_elements)
            elements["bars"].extend(bars)
            elements["barline_elements"].extend(barline_elements)

        if self.as_left:
            barline = True if self.bars_as_inf else False
            elements_tuple = __draw_section_bars(bars=self.bars_as_left,
                                                 spacing=settings["spacing"],
                                                 rebar_x=rebar_x,
                                                 rebar_y=rebar_y,
                                                 barline=barline,
                                                 text_reference="As left.")

            text_elements, bars, barline_elements, rebar_x, rebar_y = elements_tuple

            elements["text_elements"].extend(text_elements)
            elements["bars"].extend(bars)
            elements["barline_elements"].extend(barline_elements)

        if self.as_inf:
            elements_tuple = __draw_section_bars(bars=self.bars_as_inf,
                                                 spacing=settings["spacing"],
                                                 rebar_x=rebar_x,
                                                 rebar_y=rebar_y,
                                                 barline=False,
                                                 text_reference="As inf.")

            text_elements, bars, barline_elements, rebar_x, rebar_y = elements_tuple

            elements["text_elements"].extend(text_elements)
            elements["bars"].extend(bars)
            elements["barline_elements"].extend(barline_elements)

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

        # Setting groups of elements in dictionary.
        elements["all_elements"] = (elements["text_elements"] +
                                    list(chain(*[bar_dict["all_elements"] for bar_dict in elements["bars"]])) +
                                    elements["barline_elements"] +
                                    elements["beam_axes_elements"])

        return elements

    def draw_transverse_rebar_detailing(self, document: Drawing,
                                        x: float = None,
                                        y: float = None,
                                        y_section: float = None,
                                        unifilar: bool = False,
                                        dimensions: bool = True,
                                        settings: dict = COLUMN_SET_TRANSVERSE_REBAR) -> list:
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
        :param settings: Dict with column longitudinal rebar drawing settings.
        :type settings: dict
        :return: A dict of graphical entities representing the transverse rebar detailing.
        :rtype: dict
        """
        if y_section is None:
            y_section = self.height / 2

        # Checking if x given is in beam length.
        if not 0 <= y_section <= self.height:
            return []

        elements = {"stirrups": []}

        stirrups = self.__elements_section(elements=self.stirrups,
                                           y=y_section)

        group = []
        for stirrup in stirrups:
            elements["stirrups"].append(stirrup.draw_transverse(document=document,
                                                                x=x,
                                                                y=y,
                                                                unifilar=unifilar,
                                                                dimensions=dimensions))

        # Setting groups of elements in dictionary.
        elements["all_elements"] = (list(chain(*[st_dict["all_elements"] for st_dict in elements["stirrups"]])))

        return elements

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
        list_bars, list_denom, list_pos, list_quantity = gen_symmetric_list(dictionary=bars,
                                                                            nomenclature=nomenclature,
                                                                            number_init=number_init)

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
                delta_x = self.cover - db_max / 2 + (db_max / 2 - db / 2)
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
                                denomination=list_denom[i],
                                position=list_pos[i],
                                quantity=list_quantity[i]))

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
        n = 0
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
                                    anchor=stirrup[3],
                                    direction=Direction.VERTICAL,
                                    position="{0}S{1}".format(self.nomenclature, n)))
            n += 1

        return entities

    def draw_table_rebar_detailing(self,
                                   document: Drawing,
                                   x: float = None,
                                   y: float = None) -> dict:
        # Getting data.
        data = self.extract_data()

        # Creating table.
        table = CADTable(data=data, labels=["POSITION", "DIAMETER", "SPACING", "QUANTITY", "LENGTH", "TOTAL LENGTH",
                                            "WEIGHT"])

        # Drawing table.
        elements = table.draw_table(document=document, x=x, y=y)

        return elements

    def extract_data(self) -> list:
        data = []
        position_list = []
        for element in (self.all_bars + self.stirrups):
            if element.position not in position_list:
                position = element.position
                diameter = element.diameter
                spacing = "{0}".format(element.spacing) if element.element_type == ElementTypes.STIRRUP else "-"
                quantity = element.quantity if element.element_type == ElementTypes.STIRRUP else self.positions[element.position]["quantity"]
                length = "{0:.2f}".format(float(element.length))
                total_length = "{0:.2f}".format(element.quantity * element.length)

                weight = "{0:.2f}".format(element.quantity * element.weight)
                total_weight = 0

                data.append([position, diameter, spacing, quantity, length, total_length, weight])
                position_list.append(element.position)

        return data
