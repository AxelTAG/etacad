# -*- coding: utf-8 -*-

# Local imports.
from etacad.cadtable import CADTable
from etacad.concrete import Concrete
from etacad.converters import to_list
from etacad.drawing_utils import text
from etacad.globals import (Position, Axes, SlabTypes, Direction, ElementTypes, Orientation, CONCRETE_WEIGHT,
                            SLAB_SET_LONGITUDINAL, SLAB_SET_TRANSVERSE, SLAB_SET_LONG_REBBAR)
from etacad.spaced_bars import SpacedBars

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from itertools import chain


@define
class Slab:
    """
    Slab element, computes geometrics and physics props and manages dxf drawing methods (longitudinal, transversal,
    reinforcement detailing, etc.)

    :param length_x: Slab length along the X axis.
    :type length_x: float
    :param length_y: Slab length along the Y axis.
    :type length_y: float
    :param thickness: Slab thickness.
    :type thickness: float
    :param x: X-coordinate of the bottom left corner of the slab concrete shape.
    :type x: float
    :param y: Y-coordinate of the bottom left corner of the slab concrete shape.
    :type y: float
    :param direction: Direction of the slab (HORIZONTAL or VERTICAL).
    :type direction: Direction
    :param orientation: Slab orientation (TOP, RIGHT, DOWN, LEFT).
    :type orientation: Orientation
    :param as_sup_x_db: Superior X-direction rebar diameter.
    :type as_sup_x_db: list | float
    :param as_sup_y_db: Superior Y-direction rebar diameter.
    :type as_sup_y_db: list | float
    :param as_inf_x_db: Inferior X-direction rebar diameter.
    :type as_inf_x_db: list | float
    :param as_inf_y_db: Inferior Y-direction rebar diameter.
    :type as_inf_y_db: list | float
    :param as_sup_x_sp: Superior X-direction rebar spacing.
    :type as_sup_x_sp: list | float
    :param as_sup_y_sp: Superior Y-direction rebar spacing.
    :type as_sup_y_sp: list | float
    :param as_inf_x_sp: Inferior X-direction rebar spacing.
    :type as_inf_x_sp: list | float
    :param as_inf_y_sp: Inferior Y-direction rebar spacing.
    :type as_inf_y_sp: list | float
    :param as_sup_x_anchor: Superior X-direction rebar anchor lengths.
    :type as_sup_x_anchor: list | float
    :param as_sup_y_anchor: Superior Y-direction rebar anchor lengths.
    :type as_sup_y_anchor: list | float
    :param as_inf_x_anchor: Inferior X-direction reabar anchor lengths.
    :type as_inf_x_anchor: list | float
    :param as_inf_y_anchor: Inferior Y-direction rebar anchor lengths.
    :type as_inf_y_anchor: list | float
    :param as_sup_x_bend_longitud: Bend lengths of superior X bars.
    :type as_sup_x_bend_longitud: list | float
    :param as_sup_y_bend_longitud: Bend lengths of superior Y bars.
    :type as_sup_y_bend_longitud: list | float
    :param as_sup_x_bend_angle: Bend angles of superior X bars.
    :type as_sup_x_bend_angle: list | float
    :param as_sup_y_bend_angle: Bend angles of superior Y bars.
    :type as_sup_y_bend_angle: list | float
    :param as_sup_x_bend_height: Bend heights of superior X bars.
    :type as_sup_x_bend_height: list | float
    :param as_sup_y_bend_height: Bend heights of superior Y bars.
    :type as_sup_y_bend_height: list | float
    :param cover: Concrete cover for reinforcement.
    :type cover: float
    :param nomenclature: Prefix used in bar position identifiers.
    :type nomenclature: str
    :param number_init: Initial number used for bar position numbering.
    :type number_init: int | None
    :param description: Optional description of the slab element.
    :type description: str | None
    :param element_type: Type of the structural element (SLAB).
    :type element_type: ElementTypes

    :ivar length_x: Slab length along the X axis.
    :vartype length_x: float
    :ivar length_y: Slab length along the Y axis.
    :vartype length_y: float
    :ivar thickness: Slab thickness.
    :vartype thickness: float
    :ivar x: X-coordinate of the bottom left corner of the slab concrete shape.
    :vartype x: float
    :ivar y: Y-coordinate of the bottom left corner of the slab concrete shape.
    :vartype y: float
    :ivar direction: Direction of the slab (HORIZONTAL or VERTICAL).
    :vartype direction: Direction
    :ivar orientation: Slab orientation (TOP, RIGHT, DOWN, LEFT).
    :vartype orientation: Orientation

    :ivar as_sup_x_db: Superior X-direction rebar diameter.
    :vartype as_sup_x_db: list | float
    :ivar as_sup_y_db: Superior Y-direction rebar diameter.
    :vartype as_sup_y_db: list | float
    :ivar as_inf_x_db: Inferior X-direction rebar diameter.
    :vartype as_inf_x_db: list | float
    :ivar as_inf_y_db: Inferior Y-direction rebar diameter.
    :vartype as_inf_y_db: list | float
    :ivar as_sup_x_sp: Superior X-direction rebar spacing.
    :vartype as_sup_x_sp: list | float
    :ivar as_sup_y_sp: Superior Y-direction rebar spacing.
    :vartype as_sup_y_sp: list | float
    :ivar as_inf_x_sp: Inferior X-direction rebar spacing.
    :vartype as_inf_x_sp: list | float
    :ivar as_inf_y_sp: Inferior Y-direction rebar spacing.
    :vartype as_inf_y_sp: list | float
    :ivar as_sup_x_anchor: Superior X-direction rebar anchor lengths.
    :vartype as_sup_x_anchor: list | float
    :ivar as_sup_y_anchor: Superior Y-direction rebar anchor lengths.
    :vartype as_sup_y_anchor: list | float
    :ivar as_inf_x_anchor: Inferior X-direction reabar anchor lengths.
    :vartype as_inf_x_anchor: list | float
    :ivar as_inf_y_anchor: Inferior Y-direction rebar anchor lengths.
    :vartype as_inf_y_anchor: list | float
    :ivar as_sup_x_bend_longitud: Bend lengths of superior X bars.
    :vartype as_sup_x_bend_longitud: list | float
    :ivar as_sup_y_bend_longitud: Bend lengths of superior Y bars.
    :vartype as_sup_y_bend_longitud: list | float
    :ivar as_sup_x_bend_angle: Bend angles of superior X bars.
    :vartype as_sup_x_bend_angle: list | float
    :ivar as_sup_y_bend_angle: Bend angles of superior Y bars.
    :vartype as_sup_y_bend_angle: list | float
    :ivar as_sup_x_bend_height: Bend heights of superior X bars.
    :vartype as_sup_x_bend_height: list | float
    :ivar as_sup_y_bend_height: Bend heights of superior Y bars.
    :vartype as_sup_y_bend_height: list | float
    :ivar cover: Concrete cover for reinforcement.
    :ivar bars_as_sup_x: List of generated superior X-direction bars.
    :vartype bars_as_sup_x: list[SpacedBars]
    :ivar bars_as_sup_y: List of generated superior Y-direction bars.
    :vartype bars_as_sup_y: list[SpacedBars]
    :ivar bars_as_inf_x: List of generated inferior X-direction bars.
    :vartype bars_as_inf_x: list[SpacedBars]
    :ivar bars_as_inf_y: List of generated inferior Y-direction bars.
    :vartype bars_as_inf_y: list[SpacedBars]
    :vartype cover: float

    :ivar nomenclature: Prefix used in spaced bar position identifiers.
    :vartype nomenclature: str
    :ivar number_init: Initial number used for spaced bar position numbering.
    :vartype number_init: int | None
    :ivar description: Optional description of the slab element.
    :vartype description: str | None

    :ivar element_type: Type of the structural element (SLAB).
    :vartype element_type: ElementTypes
    :ivar concrete: Concrete element representing the slab volume.
    :vartype concrete: Concrete

    :ivar all_bars: All reinforcement bars of the slab.
    :vartype all_bars: list[SpacedBars]
    :ivar all_elements: All drawable elements (bars, annotations).
    :vartype all_elements: list

    :ivar positions: Dictionary of bar positions used in labeling.
    :vartype positions: dict
    :ivar max_db_sup_x: Maximum diameter in superior X bars.
    :vartype max_db_sup_x: float
    :ivar max_db_sup_y: Maximum diameter in superior Y bars.
    :vartype max_db_sup_y: float
    :ivar max_db_inf_x: Maximum diameter in inferior X bars.
    :vartype max_db_inf_x: float
    :ivar max_db_inf_y: Maximum diameter in inferior Y bars.
    :vartype max_db_inf_y: float
    :ivar max_db_hz: Maximum horizontal bar diameter.
    :vartype max_db_hz: float

    :ivar number_init_sup_x: Initial bar ID number for superior X bars.
    :vartype number_init_sup_x: int
    :ivar number_init_sup_y: Initial bar ID number for superior Y bars.
    :vartype number_init_sup_y: int
    :ivar number_init_inf_x: Initial bar ID number for inferior X bars.
    :vartype number_init_inf_x: int
    :ivar number_init_inf_y: Initial bar ID number for inferior Y bars.
    :vartype number_init_inf_y: int
    """
    # Geometric attributes.
    length_x: float = field(converter=float)
    length_y: float = field(converter=float)
    thickness: float = field(converter=float)
    x: float = field(default=0, converter=float)
    y: float = field(default=0, converter=float)
    direction: Direction = field(default=Direction.HORIZONTAL)
    orientation: Orientation = field(default=Orientation.BOTTOM)

    # Longitudinal steel attributes.
    as_sup_x_db: list | float = field(default=None, converter=to_list)
    as_sup_y_db: list | float = field(default=None, converter=to_list)
    as_inf_x_db: list | float = field(default=None, converter=to_list)
    as_inf_y_db: list | float = field(default=None, converter=to_list)

    as_sup_x_sp: list | float = field(default=None, converter=to_list)
    as_sup_y_sp: list | float = field(default=None, converter=to_list)
    as_inf_x_sp: list | float = field(default=None, converter=to_list)
    as_inf_y_sp: list | float = field(default=None, converter=to_list)

    max_db_sup_x: float = field(init=False)
    max_db_sup_y: float = field(init=False)
    max_db_inf_x: float = field(init=False)
    max_db_inf_y: float = field(init=False)
    max_db_hz: float = field(init=False)

    as_sup_x_anchor: list | float = field(default=None, converter=to_list)
    as_sup_y_anchor: list | float = field(default=None, converter=to_list)
    as_inf_x_anchor: list | float = field(default=None, converter=to_list)
    as_inf_y_anchor: list | float = field(default=None, converter=to_list)

    as_sup_x_bend_longitud: list | float = field(default=None, converter=to_list)
    as_sup_y_bend_longitud: list | float = field(default=None, converter=to_list)

    as_sup_x_bend_angle: list | float = field(default=None, converter=to_list)
    as_sup_y_bend_angle: list | float = field(default=None, converter=to_list)

    as_sup_x_bend_height: list | float = field(default=None, converter=to_list)
    as_sup_y_bend_height: list | float = field(default=None, converter=to_list)

    bars_as_sup_x: list | float = field(init=False)
    bars_as_sup_y: list | float = field(init=False)
    bars_as_inf_x: list | float = field(init=False)
    bars_as_inf_y: list | float = field(init=False)

    number_init_sup_x: int = field(init=False)
    number_init_sup_y: int = field(init=False)
    number_init_inf_x: int = field(init=False)
    number_init_inf_y: int = field(init=False)

    cover: float = field(default=0, converter=float)

    # Concrete attributes.
    concrete: Concrete = field(init=False)
    concrete_specific_weight: float = CONCRETE_WEIGHT

    # Entities groups.
    all_bars: list[SpacedBars] = field(init=False)
    all_elements: list = field(init=False)

    # Box attributes.
    _box_width: float = field(init=False)
    _box_height: float = field(init=False)

    # Position bar attributes.
    nomenclature: str = field(default="#")
    positions: dict = field(init=False)
    number_init: int = field(default=None)
    description: str = field(default=None)

    # Other attributes.
    element_type: ElementTypes = field(default=ElementTypes.SLAB)

    def __attrs_post_init__(self):
        # Longitudinal steel attributes.
        if self.number_init is None:
            self.number_init = 1

        # Superior X bars.
        (self.as_sup_x_db, self.max_db_sup_x, self.as_sup_x_anchor, self.number_init_sup_x, self.as_sup_x_bend_longitud,
         self.as_sup_x_bend_angle, self.as_sup_x_bend_height) = self.__asign_bar_vars(
            as_db=self.as_sup_x_db,
            as_anchor=self.as_sup_x_anchor,
            as_bend_length=self.as_sup_x_bend_longitud,
            as_bend_angle=self.as_sup_x_bend_angle,
            as_bend_height=self.as_sup_x_bend_height, )

        # Superior Y bars.
        (self.as_sup_y_db, self.max_db_sup_y, self.as_sup_y_anchor, self.number_init_sup_y, self.as_sup_y_bend_longitud,
         self.as_sup_y_bend_angle, self.as_sup_y_bend_height) = self.__asign_bar_vars(
            as_db=self.as_sup_y_db,
            as_anchor=self.as_sup_y_anchor,
            as_bend_length=self.as_sup_y_bend_longitud,
            as_bend_angle=self.as_sup_y_bend_angle,
            as_bend_height=self.as_sup_y_bend_height)

        # Inferior X bars.
        (self.as_inf_x_db, self.max_db_inf_x, self.as_inf_x_anchor, self.number_init_inf_x,
         _, _, _) = self.__asign_bar_vars(
            as_db=self.as_inf_x_db,
            as_anchor=self.as_inf_x_anchor)

        # Inferior Y bars.
        (self.as_inf_y_db, self.max_db_inf_y, self.as_inf_y_anchor, self.number_init_inf_y,
         _, _, _) = self.__asign_bar_vars(
            as_db=self.as_inf_y_db,
            as_anchor=self.as_inf_y_anchor)

        # Generate bars.
        self.bars_as_sup_x = self.__gen_bars(as_db=self.as_sup_x_db,
                                             as_sp=self.as_sup_x_sp,
                                             as_anchor=self.as_sup_x_anchor,
                                             as_position=Position.SUPERIOR,
                                             as_direction=Direction.HORIZONTAL,
                                             as_bend_length=self.as_sup_x_bend_longitud,
                                             as_bend_angle=self.as_sup_x_bend_angle,
                                             as_bend_height=self.as_sup_x_bend_height,
                                             as_number_init=self.number_init_sup_x)
        self.bars_as_sup_y = self.__gen_bars(as_db=self.as_sup_y_db,
                                             as_sp=self.as_sup_y_sp,
                                             as_anchor=self.as_sup_y_anchor,
                                             as_position=Position.SUPERIOR,
                                             as_direction=Direction.VERTICAL,
                                             as_bend_length=self.as_sup_y_bend_longitud,
                                             as_bend_angle=self.as_sup_y_bend_angle,
                                             as_bend_height=self.as_sup_y_bend_height,
                                             as_number_init=self.number_init_sup_y)
        self.bars_as_inf_x = self.__gen_bars(as_db=self.as_inf_x_db,
                                             as_sp=self.as_inf_x_sp,
                                             as_anchor=self.as_inf_x_anchor,
                                             as_position=Position.INFERIOR,
                                             as_direction=Direction.HORIZONTAL,
                                             as_number_init=self.number_init_inf_x)
        self.bars_as_inf_y = self.__gen_bars(as_db=self.as_inf_y_db,
                                             as_sp=self.as_inf_y_sp,
                                             as_anchor=self.as_inf_y_anchor,
                                             as_position=Position.INFERIOR,
                                             as_direction=Direction.VERTICAL,
                                             as_number_init=self.number_init_inf_y)

        # Concrete attributes.
        vertices = [(0, 0),
                    (0, self.length_y),
                    (self.length_x, self.length_y),
                    (self.length_x, 0)]

        self.concrete = Concrete(vertices=vertices,
                                 height=self.thickness,
                                 x=self.x,
                                 y=self.y,
                                 specific_weight=self.concrete_specific_weight)

        # Entities groups.
        self.all_bars = self.bars_as_sup_x + self.bars_as_sup_y + self.bars_as_inf_x + self.bars_as_inf_y
        self.all_elements = self.all_bars

        # Box attributes.
        self._box_width = self.length_x
        self._box_height = self.length_y

    @property
    def box_width(self) -> float:
        """Bounding box width (equal to length_x)."""
        return self._box_width

    @property
    def box_height(self) -> float:
        """Bounding box height (equal to length_y)."""
        return self._box_height

    def draw_longitudinal(self, document: Drawing,
                          x: float = None,
                          y: float = None,
                          concrete_shape: bool = True,
                          bars: bool = True,
                          bars_sup: bool = True,
                          bars_inf: bool = True,
                          one_bar: bool = False,
                          one_bar_position_sup: int = None,
                          one_bar_position_inf: int = None,
                          dimensions: bool = True,
                          description: bool = True,
                          unifilar_bars: bool = False) -> dict:
        """
        Draws the longitudinal view of the slab, including the concrete section and reinforcement bars.

        The method adds the concrete outline and/or longitudinal bars (superior and/or inferior)
        to the specified `ezdxf` drawing, with customizable display options. It returns a dictionary
        with categorized drawing elements.

        :param document: The `ezdxf` Drawing object where the elements will be rendered.
        :type document: Drawing
        :param x: X-coordinate of the left bottom corner of slab concrete shape. Defaults to slab's own X.
        :type x: float, optional
        :param y: Y-coordinate of the left bottom corner of slab concrete shape. Defaults to slab's own Y.
        :type y: float, optional
        :param concrete_shape: Whether to draw the concrete outline of the slab.
        :type concrete_shape: bool
        :param bars: Whether to draw reinforcement bars.
        :type bars: bool
        :param bars_sup: Whether to draw superior reinforcement bars.
        :type bars_sup: bool
        :param bars_inf: Whether to draw inferior reinforcement bars.
        :type bars_inf: bool
        :param one_bar: Whether to draw a single selected bar instead of the full set.
        :type one_bar: bool
        :param one_bar_position_sup: Position index for the superior bar to draw when `one_bar` is True.
        :type one_bar_position_sup: int, optional
        :param one_bar_position_inf: Position index for the inferior bar to draw when `one_bar` is True.
        :type one_bar_position_inf: int, optional
        :param dimensions: Whether to draw dimensions.
        :type dimensions: bool
        :param description: Whether to include denomination/description for each bar.
        :type description: bool
        :param unifilar_bars: If True, draws bars in unifilar (symbolic) representation.
        :type unifilar_bars: bool

        :return: Dictionary containing grouped drawing elements:
            - "concrete_elements": list of DXF elements related to the concrete section
            - "spaced_bars_elements": list of DXF elements related to spaced bars
            - "all_elements": flat list combining all drawable elements
        :rtype: dict
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {}
        concrete_dict = []
        spaced_bars_dict = []

        # Drawing concrete shape.
        if concrete_shape:
            concrete_dict = self.concrete.draw_transverse(document=document,
                                                          x=x,
                                                          y=y,
                                                          dimensions=dimensions,
                                                          dimensions_inner=False,
                                                          settings=SLAB_SET_LONGITUDINAL["concrete_settings"])

        # Drawing of bars.
        if bars:
            if bars_sup:
                for sp_bar in (self.bars_as_sup_x + self.bars_as_sup_y):
                    spaced_bars_dict.append(sp_bar.draw_longitudinal(
                        document=document,
                        x=x + (sp_bar.x - self.x),
                        y=y + (sp_bar.y - self.y),
                        unifilar=unifilar_bars,
                        dimensions=False,
                        reinforcement_dimensions=False,
                        description=description,
                        one_bar=one_bar,
                        one_bar_position=one_bar_position_sup,
                        settings=SLAB_SET_LONGITUDINAL["spaced_bars_settings"]))
            if bars_inf:
                for sp_bar in (self.bars_as_inf_x + self.bars_as_inf_y):
                    spaced_bars_dict.append(sp_bar.draw_longitudinal(
                        document=document,
                        x=x + (sp_bar.x - self.x),
                        y=y + (sp_bar.y - self.y),
                        unifilar=unifilar_bars,
                        dimensions=False,
                        reinforcement_dimensions=False,
                        description=description,
                        one_bar=one_bar,
                        one_bar_position=one_bar_position_inf,
                        settings=SLAB_SET_LONGITUDINAL["spaced_bars_settings"]))

        # Setting groups of elements in dictionary.
        elements["concrete_elements"] = concrete_dict
        elements["spaced_bars_elements"] = spaced_bars_dict
        elements["all_elements"] = (elements["concrete_elements"]["all_elements"] +
                                    list(chain(*[spbars["all_elements"] for spbars in spaced_bars_dict])))

        return elements

    def draw_transverse(self, document: Drawing,
                        x: float = None,
                        y: float = None,
                        axe_section: str = "x",
                        concrete_shape: bool = True,
                        bars: bool = True,
                        dimensions: bool = True,
                        descriptions: bool = True,
                        description_start_sup: int = 6,
                        description_start_inf: int = 9,
                        unifilar: bool = False,
                        settings: dict = SLAB_SET_TRANSVERSE) -> dict:
        """
        Draws the transverse section of the slab, including the concrete shape and reinforcement bars.

        This method generates the DXF elements representing a cross-sectional view of the slab along
        the selected axis ('x' or 'y'). It includes both transverse and longitudinal reinforcement bars,
        as well as optional dimensions and descriptions. It handles symbolic (unifilar) or detailed representation.

        :param document: The `ezdxf` Drawing object where the transverse view will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the left bottom corner of slab concrete shape. Defaults to slab's own X.
        :type x: float, optional
        :param y: Y-coordinate of the left bottom corner of slab concrete shape. Defaults to slab's own Y.
        :type y: float, optional
        :param axe_section: Section axis ("x" for right view or "y" for front view).
        :type axe_section: str
        :param concrete_shape: Whether to draw the concrete shape of the slab section.
        :type concrete_shape: bool
        :param bars: Whether to draw reinforcement bars.
        :type bars: bool
        :param dimensions: Whether to draw dimension lines.
        :type dimensions: bool
        :param descriptions: Whether to show bar descriptions.
        :type descriptions: bool
        :param description_start_sup: Initial number to use for upper transverse bar labels.
        :type description_start_sup: int
        :param description_start_inf: Initial number to use for lower transverse bar labels.
        :type description_start_inf: int
        :param unifilar: If True, draws symbolic (unifilar) bars; if False, uses detailed geometry.
        :type unifilar: bool
        :param settings: Dictionary of drawing settings for concrete and reinforcement bars.
        :type settings: dict

        :return: Dictionary containing grouped DXF elements:
            - "concrete": DXF elements related to the concrete shape.
            - "spaced_bars_elements": List of DXF elements for all reinforcement bars.
            - "all_elements": Flat list combining all the elements above for easier access.
        :rtype: dict
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {}
        concrete_dict = {}
        spaced_bars_dict = []

        # Drawing concrete.
        if concrete_shape:
            if axe_section == Axes.X.value:
                concrete_dict = self.concrete.draw_right_view(document=document,
                                                              x=x,
                                                              y=y,
                                                              dimensions=dimensions,
                                                              dimensions_inner=False,
                                                              settings=settings["concrete_settings"])
            if axe_section == Axes.Y.value:
                concrete_dict = self.concrete.draw_front_view(document=document,
                                                              x=x,
                                                              y=y,
                                                              dimensions=dimensions,
                                                              dimensions_inner=False,
                                                              settings=settings["concrete_settings"])

        # Drawing bars.
        if bars:
            # X axe section.
            sp_bars_lg_sup = self.bars_as_sup_y
            sp_bars_lg_inf = self.bars_as_inf_y
            sp_bars_tr_sup = self.bars_as_sup_x
            sp_bars_tr_inf = self.bars_as_inf_x
            db_max_lg_sup = self.max_db_sup_y
            db_max_lg_inf = self.max_db_inf_y
            anchor_lg_sup = any(self.as_sup_y_anchor)
            anchor_lg_inf = any(self.as_inf_y_anchor)
            rotate_angle = -90
            other_extreme = False
            inverter_coeficient = 1

            # Y axe section.
            if axe_section == "y":
                sp_bars_lg_sup, sp_bars_tr_sup = sp_bars_tr_sup, sp_bars_lg_sup
                sp_bars_lg_inf, sp_bars_tr_inf = sp_bars_tr_inf, sp_bars_lg_inf
                db_max_lg_sup = self.max_db_sup_x
                db_max_lg_inf = self.max_db_inf_x
                anchor_lg_sup = any(self.as_sup_x_anchor)
                anchor_lg_inf = any(self.as_inf_x_anchor)
                rotate_angle = 0
                other_extreme = False
                inverter_coeficient = -1

            # Transverse bar sections.
            # Superior.
            for i, sp_bar in enumerate(sp_bars_tr_sup):
                first_bar_index = 0
                last_bar_index = sp_bar.quantity - 1
                if axe_section == "y":
                    first_bar_index, last_bar_index = last_bar_index, first_bar_index

                x_coord, y_coord = x, y
                if unifilar:
                    y_coord += db_max_lg_sup / 2

                bar_displacements = {}
                if not unifilar and anchor_lg_sup:
                    bar_displacements[first_bar_index] = (0, db_max_lg_sup * inverter_coeficient)
                    if sp_bar.is_exact_reinforcement:
                        bar_displacements[last_bar_index] = (0, -db_max_lg_sup * inverter_coeficient)

                spaced_bars_dict.append(sp_bar.draw_transverse(document=document,
                                                               x=x_coord,
                                                               y=y_coord,
                                                               dimensions=False,
                                                               descriptions=descriptions,
                                                               description_start=description_start_sup + i * settings[
                                                                   "description_start_coefficient"],
                                                               bar_displacements=bar_displacements,
                                                               rotate_angle=rotate_angle,
                                                               other_extreme=other_extreme,
                                                               settings=settings["spaced_bars_settings"]))

            # Inferior.
            for i, sp_bar in enumerate(sp_bars_tr_inf):
                first_bar_index = 0
                last_bar_index = sp_bar.quantity - 1
                if axe_section == "y":
                    first_bar_index, last_bar_index = last_bar_index, first_bar_index

                x_coord, y_coord = x, y
                if unifilar:
                    y_coord -= db_max_lg_inf / 2

                bar_displacements = {}
                if not unifilar and anchor_lg_inf:
                    bar_displacements[first_bar_index] = (0, db_max_lg_inf * inverter_coeficient)
                    if sp_bar.is_exact_reinforcement:
                        bar_displacements[last_bar_index] = (0, -db_max_lg_inf * inverter_coeficient)

                spaced_bars_dict.append(sp_bar.draw_transverse(document=document,
                                                               x=x_coord,
                                                               y=y_coord,
                                                               dimensions=False,
                                                               descriptions=descriptions,
                                                               description_start=description_start_inf + i * settings[
                                                                   "description_start_coefficient"],
                                                               bar_displacements=bar_displacements,
                                                               rotate_angle=rotate_angle,
                                                               other_extreme=other_extreme,
                                                               settings=settings["spaced_bars_settings"]))

            # Longitudinal bars.
            # Superior.
            for sp_bar in sp_bars_lg_sup:
                x_coord = x + self.cover
                y_coord = y + self.thickness - self.cover - sp_bar.mandrel_radius - sp_bar.max_height_attribute - sp_bar.diameter / 2
                if unifilar:
                    y_coord += sp_bar.diameter / 2 + sp_bar.mandrel_radius

                if sp_bar.diameter == db_max_lg_sup:
                    spaced_bars_dict.append(sp_bar.bars[0].draw_longitudinal(document=document,
                                                                             x=x_coord,
                                                                             y=y_coord,
                                                                             dimensions=False,
                                                                             denomination=False,
                                                                             unifilar=unifilar,
                                                                             settings=settings["spaced_bars_settings"]))

            # Inferior.
            for sp_bar in sp_bars_lg_inf:
                x_coord = x + self.cover
                y_coord = y + self.cover - sp_bar.diameter / 2
                if unifilar:
                    y_coord += sp_bar.diameter / 2

                if sp_bar.diameter == db_max_lg_inf:
                    spaced_bars_dict.append(sp_bar.bars[0].draw_longitudinal(document=document,
                                                                             x=x_coord,
                                                                             y=y_coord,
                                                                             dimensions=False,
                                                                             denomination=False,
                                                                             unifilar=unifilar,
                                                                             settings=settings["spaced_bars_settings"]))
        if dimensions:
            # Dimensions are drawn at concrete shape.
            pass

        # Setting groups of elements in dictionary.
        elements["concrete_elements"] = concrete_dict
        elements["spaced_bars_elements"] = spaced_bars_dict
        elements["all_elements"] = (elements["concrete_elements"]["all_elements"] +
                                    list(chain(
                                        *[sp_dict["all_elements"] for sp_dict in elements["spaced_bars_elements"]])))

        return elements

    def draw_longitudinal_rebar_detailing(self,
                                          document: Drawing,
                                          x: float = None,
                                          y: float = None,
                                          unifilar: bool = False,
                                          settings: dict = SLAB_SET_LONG_REBBAR) -> dict:
        """
        Draws a detailed longitudinal reinforcement schedule for the slab.

        This method creates a vertical list of labeled reinforcement bars for both
        top (superior) and bottom (inferior) layers in the X and Y directions. Each
        group of bars is preceded by a label, and bars are spaced according to the
        settings provided. Bars are drawn symbolically or in full detail based on
        the `unifilar` flag.

        :param document: The `ezdxf` Drawing object where the detailing will be placed.
        :type document: Drawing
        :param x: X-coordinate of the top-left corner of the detailing layout. Defaults to the slab's own x.
        :type x: float, optional
        :param y: Y-coordinate of the top-left corner of the detailing layout. Defaults to the slab's own y.
        :type y: float, optional
        :param unifilar: If True, draws symbolic (unifilar) representations of the bars; otherwise, detailed.
        :type unifilar: bool
        :param settings: Dictionary containing configuration for text height, spacing, and bar styling.
        :type settings: dict

        :return: Dictionary containing grouped DXF elements:
            - "text_elements": DXF elements related to text labels.
            - "bars_elements": List of DXF elements for all reinforcement bars.
            - "all_elements": Flat list combining all the elements above for easier access.
        :rtype: dict
        """
        bars_elements = []
        text_elements = []
        elements = {}

        # Bars.
        rebbar_y = 0

        # TODO: evaluar la posibilidad de hacer una función para crear cada apartado de barras.
        # Superior bars.
        # X.
        if self.bars_as_sup_x:
            text_elements += text(document=document,
                                  text="As sup. x",
                                  height=settings["text_height"],
                                  point=(x, y - rebbar_y))
            rebbar_y += settings["text_height"] + settings["text_distance_vertical"]

            for sp_bar in self.bars_as_sup_x:
                bars_elements.append(sp_bar.bars[0].draw_longitudinal(document=document,
                                                                      x=x,
                                                                      y=y - rebbar_y,
                                                                      unifilar=unifilar,
                                                                      settings=settings["bar_settings"]))
                rebbar_y += sp_bar.bars[0].box_height + settings["spacing"]

        if self.bars_as_sup_y:
            text_elements += text(document=document,
                                  text="As sup. y",
                                  height=settings["text_height"],
                                  point=(x, y - rebbar_y))
            rebbar_y += settings["text_height"] + settings["text_distance_vertical"]

            for sp_bar in self.bars_as_sup_y:
                bars_elements.append(sp_bar.bars[0].draw_longitudinal(document=document,
                                                                      x=x,
                                                                      y=y - rebbar_y,
                                                                      unifilar=unifilar,
                                                                      settings=settings["bar_settings"]))
                rebbar_y += sp_bar.bars[0].box_height + settings["spacing"]

        if self.bars_as_inf_x:
            text_elements += text(document=document,
                                  text="As inf. x",
                                  height=settings["text_height"],
                                  point=(x, y - rebbar_y))
            rebbar_y += settings["text_height"] + settings["text_distance_vertical"]

            for sp_bar in self.bars_as_inf_x:
                bars_elements.append(sp_bar.bars[0].draw_longitudinal(document=document,
                                                                      x=x,
                                                                      y=y - rebbar_y,
                                                                      unifilar=unifilar,
                                                                      settings=settings["bar_settings"]))
                rebbar_y += sp_bar.bars[0].box_height + settings["spacing"]

        if self.bars_as_inf_y:
            text_elements += text(document=document,
                                  text="As inf. y",
                                  height=settings["text_height"],
                                  point=(x, y - rebbar_y))
            rebbar_y += settings["text_height"] + settings["text_distance_vertical"]

            for sp_bar in self.bars_as_inf_y:
                bars_elements.append(sp_bar.bars[0].draw_longitudinal(document=document,
                                                                      x=x,
                                                                      y=y - rebbar_y,
                                                                      unifilar=unifilar,
                                                                      settings=settings["bar_settings"]))

                rebbar_y += sp_bar.bars[0].box_height + settings["spacing"]

        # Setting groups of elements in dictionary.
        elements["bars_elements"] = bars_elements
        elements["text_elements"] = text_elements
        elements["all_elements"] = (elements["text_elements"] +
                                    list(chain(
                                        *[bar["all_elements"] for bar in elements["bars_elements"]])))

        return elements

    def draw_rebar_detailing_transverse(self) -> dict:
        pass

    def draw_table_rebar_detailing(self,
                                   document: Drawing,
                                   x: float = None,
                                   y: float = None) -> dict:
        """
        Draws a reinforcement detailing table for the slab.

        This method generates a tabular summary of the reinforcement bars used in the slab,
        including information such as position, diameter, spacing, quantity, individual length,
        total length, and weight. The table is created from internal slab data and inserted into
        the provided DXF document at the specified coordinates.

        :param document: The `ezdxf` Drawing object where the table will be drawn.
        :type document: Drawing
        :param x: X-coordinate of the bottom-left corner of the table. If not specified, defaults to the slab's own x.
        :type x: float, optional
        :param y: Y-coordinate of the bottom-left corner of the table. If not specified, defaults to the slab's own y.
        :type y: float, optional

        :return: Dictionary containing the generated DXF elements of the table.
        :rtype: dict
        """
        # Getting data.
        data = self.extract_data()

        # Creating table.
        table = CADTable(data=data, labels=["POSITION", "DIAMETER", "SPACING", "QUANTITY", "LENGTH", "TOTAL LENGTH",
                                            "WEIGHT"])

        # Drawing table.
        elements = table.draw_table(document=document, x=x, y=y)

        return elements

    def extract_data(self) -> list:
        """
        Extracts and formats reinforcement bar data for tabular representation.

        This method iterates over all reinforcement bars associated with the slab
        and gathers relevant properties such as position, diameter, spacing, quantity,
        length, total length, and weight. Numeric values like length, total length, and
        weight are formatted to two decimal places, while spacing is represented as a string.

        :return: A list of lists, where each inner list represents one row of bar data
                 with the following fields:
                 [POSITION, DIAMETER, SPACING, QUANTITY, LENGTH, TOTAL LENGTH, WEIGHT]
        :rtype: list
        """
        data = []
        for element in self.all_bars:
            position = element.position
            diameter = element.diameter
            spacing = "{0}".format(element.spacing)
            quantity = element.quantity
            length = "{0:.2f}".format(float(element.length))
            total_length = "{0:.2f}".format(element.quantity * element.length)
            weight = "{0:.2f}".format(element.weight)

            data.append([position, diameter, spacing, quantity, length, total_length, weight])

        return data

    def __asign_bar_vars(self,
                         as_db: list,
                         as_anchor: list,
                         as_bend_length: list = None,
                         as_bend_angle: list = None,
                         as_bend_height: list = None) -> tuple[list, float, list, int, list, list, list]:
        """
        Assigns and adjusts variables related to reinforcement bars, anchorage, and bar bends.

        If the list of bar diameters (`as_db`) is provided, the method calculates the maximum diameter
        and updates the internal bar counter (`self.number_init`). It then ensures the anchorage and
        bending-related lists (length, angle, and height) match the number of bars, repeating elements
        if necessary or defaulting to zero values when not provided.

        :param as_db: List of bar diameters.
        :type as_db: list
        :param as_anchor: List of anchorage values for each bar. If shorter than `as_db`, it is repeated.
                          If None, all anchorage values are set to 0.
        :type as_anchor: list
        :param as_bend_length: List of bend lengths for each bar. Can be None. If shorter, it is repeated.
        :type as_bend_length: list
        :param as_bend_angle: List of bend angles for each bar. Can be None. If shorter, it is repeated.
        :type as_bend_angle: list
        :param as_bend_height: List of bend heights for each bar. Can be None. If shorter, it is repeated.
        :type as_bend_height: list

        :return: A tuple containing:
                 - List of bar diameters (`as_db`)
                 - Maximum bar diameter (`max_db`)
                 - Adjusted list of anchorage values (`as_anchor`)
                 - Initial bar counter value (`number_init_as`)
                 - List of bend lengths (`as_bend_length`)
                 - List of bend angles (`as_bend_angle`)
                 - List of bend heights (`as_bend_height`)
        :rtype: tuple[list, float, list, int, list, list, list]
        """
        if not as_db:
            return [], 0, [], 0, [], [], []

        quantity = len(as_db)
        max_db = max(as_db)
        number_init_as = self.number_init or 0
        self.number_init = number_init_as + quantity

        def normalize_list(lst):
            if lst is None:
                return [0] * quantity
            if len(lst) != quantity:
                return lst[:1] * quantity
            return lst

        as_anchor = normalize_list(as_anchor)
        as_bend_length = normalize_list(as_bend_length)
        as_bend_angle = normalize_list(as_bend_angle)
        as_bend_height = normalize_list(as_bend_height)

        return as_db, max_db, as_anchor, number_init_as, as_bend_length, as_bend_angle, as_bend_height

    # TODO: Escribir función elements_section y refactorizar funciones de transversal acordemente.
    def __elements_section(self,
                           elements: list,
                           x: float) -> list:
        pass

    def __gen_bars(self,
                   as_db: list,
                   as_sp: list,
                   as_anchor: list,
                   as_position: Position,
                   as_direction: Direction,
                   as_number_init: int,
                   as_bend_length: list = None,
                   as_bend_angle: list = None,
                   as_bend_height: list = None) -> list[SpacedBars]:
        """
        Generates a list of spaced reinforcement bars based on provided geometry and layout parameters.

        This method calculates the position and orientation of each reinforcement bar
        within a concrete element, considering spacing, cover, direction, anchorage,
        and position (e.g., top or bottom of the section).

        :param as_db: List of bar diameters.
        :type as_db: list[float]
        :param as_sp: List of bar spacings corresponding to each bar.
        :type as_sp: list[float]
        :param as_anchor: List of anchorage lengths for each bar.
        :type as_anchor: list[float]
        :param as_position: Position of the reinforcement (e.g., superior or inferior).
        :type as_position: Position
        :param as_direction: Direction of the reinforcement bars (e.g., horizontal or vertical).
        :type as_direction: Direction
        :return: A list of SpacedBars objects representing the placed reinforcement bars.
        :rtype: list[SpacedBars]
        """

        def get_x_y_by_position(n_position: int,
                                n_bars: int) -> tuple[float, float, float, float]:
            """
                Calculates the start coordinates and transverse center for a reinforcement bar.

                Based on the position (top or bottom) and the direction of the reinforcement,
                this function computes the x and y coordinates for placing the longitudinal bar
                and the corresponding transverse center point.

                :param n_position: Index of the current bar being placed.
                :type n_position: int
                :param n_bars: Total number of bars to be placed.
                :type n_bars: int
                :return: Tuple of (x_long, y_long, x_transverse, y_transverse) coordinates.
                :rtype: tuple[float, float, float, float]
                """
            if as_position == Position.SUPERIOR:
                if as_direction == Direction.HORIZONTAL:  # Superior X.
                    x_long = self.x + self.cover
                    y_long = self.y + self.cover + (as_sp[n_position] / n_bars) * n_position - as_db[i] / 2
                    x_transverse = self.cover
                    y_transverse = self.thickness - self.cover - self.max_db_sup_y / 2
                    return x_long, y_long, x_transverse, y_transverse

                x_long = self.x + self.cover + (as_sp[n_position] / n_bars) * n_position - as_db[i] / 2  # Superior Y.
                y_long = self.y + self.cover
                x_transverse = self.cover
                y_transverse = self.thickness - self.cover - self.max_db_sup_x / 2 - as_db[i]
                return x_long, y_long, x_transverse, y_transverse

            if as_direction == Direction.HORIZONTAL:  # Inferior X.
                x_long = self.x + self.cover
                y_long = self.y + self.cover + (as_sp[n_position] / n_bars) * n_position - as_db[i] / 2
                x_transverse = self.cover
                y_transverse = self.cover + self.max_db_inf_y / 2 + as_db[i]
                return x_long, y_long, x_transverse, y_transverse

            x_long = self.x + self.cover + (as_sp[n_position] / n_bars) * n_position - as_db[i] / 2  # Inferior Y.
            y_long = self.y + self.cover
            x_transverse = self.cover
            y_transverse = self.cover + self.max_db_inf_x / 2
            return x_long, y_long, x_transverse, y_transverse

        if as_bend_height is None:
            as_bend_height = [0] * len(as_db)

        if as_bend_length is None:
            as_bend_length = [0] * len(as_db)

        if as_bend_angle is None:
            as_bend_angle = [0] * len(as_db)

        # Determination of util length and width.
        length = self.length_x - 2 * self.cover
        reinforcement_length = self.length_y - 2 * self.cover
        if as_direction == Direction.VERTICAL:
            length, reinforcement_length = reinforcement_length, length

        # Loop for generation of bars.
        total_bars = len(as_db)
        spaced_bars = []
        for i in range(total_bars):
            # Determination of x and y coordinates.
            x, y, x_tr, y_tr = get_x_y_by_position(n_position=i,
                                                   n_bars=total_bars)

            # Determination of mandrel radius.
            mandrel_radius = 0
            if as_direction == Direction.HORIZONTAL:
                mandrel_radius = self.as_inf_y_db[0] / 2
                if as_position == Position.SUPERIOR:
                    mandrel_radius = self.as_sup_y_db[0] / 2

            if as_direction == Direction.VERTICAL:
                mandrel_radius = self.as_inf_x_db[0] / 2
                if as_position == Position.SUPERIOR:
                    mandrel_radius = self.as_sup_x_db[0] / 2

            # Determination of orientation.
            orientation = Orientation.BOTTOM
            if as_position == Position.INFERIOR and not any(as_bend_length):
                orientation = Orientation.TOP

            # Setting description.
            description = f"{self.nomenclature}{as_number_init} Ø{as_db[i]}/ {as_sp[i]}m"
            position = f"{self.nomenclature}{as_number_init}"
            as_number_init += 1

            spaced_bars.append(SpacedBars(reinforcement_length=reinforcement_length - (as_sp[i] / total_bars) * i,
                                          length=length,
                                          diameter=as_db[i],
                                          spacing=as_sp[i],
                                          x=x,
                                          y=y,
                                          transverse_center=(x_tr, y_tr),
                                          direction=as_direction,
                                          orientation=orientation,
                                          left_anchor=as_anchor[i],
                                          right_anchor=as_anchor[i],
                                          mandrel_radius=mandrel_radius,
                                          bend_longitud=as_bend_length[i],
                                          bend_angle=as_bend_angle[i],
                                          bend_height=as_bend_height[i],
                                          description=description,
                                          position=position))

        return spaced_bars
