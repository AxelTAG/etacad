# -*- coding: utf-8 -*-

# Local imports.
from etacad.cadtable import CADTable
from etacad.concrete import Concrete
from etacad.converters import to_list
from etacad.drawing_utils import delimit_axe, dim_linear, rect, text
from etacad.globals import (Position, Axes, SlabTypes, Direction, ElementTypes, Orientation, CONCRETE_WEIGHT,
                            SLAB_SET_LONGITUDINAL, SLAB_SET_TRANSVERSE, SLAB_SET_LONG_REBBAR,
                            SLAB_SET_TRANSVERSE_REBBAR)
from etacad.spaced_bars import SpacedBars

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs
from itertools import chain


@define
class Slab:
    """
    Slab element, computes geometrics and physics props and manages dxf drawing methods (longitudinal, transversal,
    reinforcement detailing, etc.)
    """
    # Geometric attributes.
    length_x: float = field(converter=float)
    length_y: float = field(converter=float)
    thickness: float = field(converter=float)
    slab_type: int = field(default=SlabTypes.RECTANGULAR)
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
    as_inf_x_bend_longitud: list | float = field(default=None, converter=to_list)
    as_inf_y_bend_longitud: list | float = field(default=None, converter=to_list)

    as_sup_x_bend_angle: list | float = field(default=None, converter=to_list)
    as_sup_y_bend_angle: list | float = field(default=None, converter=to_list)
    as_inf_x_bend_angle: list | float = field(default=None, converter=to_list)
    as_inf_y_bend_angle: list | float = field(default=None, converter=to_list)

    as_sup_x_bend_height: list | float = field(default=None, converter=to_list)
    as_sup_y_bend_height: list | float = field(default=None, converter=to_list)
    as_inf_x_bend_height: list | float = field(default=None, converter=to_list)
    as_inf_y_bend_height: list | float = field(default=None, converter=to_list)

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

    # Crossing beams attributes.
    beams: list = field(default=None)  # Maybe not in use.
    beams_pos: list = field(default=None)  # Maybe not in use.
    beams_symbol: list = field(default=None)  # Maybe not in use.

    # Entities groups.
    all_bars: list[SpacedBars] = field(init=False)
    all_elements: list = field(init=False)

    # Box attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)

    # Position bar attributes.
    nomenclature: str = field(default="#")
    positions: dict = field(init=False)

    # Slab attributes.
    denomination: str = field(default=None)
    number_init: int = field(default=None)
    element_type: ElementTypes = field(default=ElementTypes.SLAB)

    def __attrs_post_init__(self):
        # Longitudinal steel attributes.
        if self.number_init is None:
            self.number_init = 0

        # Superior X bars.
        (self.as_sup_x_db, self.max_db_sup_x, self.as_sup_x_anchor, self.number_init_sup_x, self.as_sup_x_bend_longitud,
         self.as_sup_x_bend_angle, self.as_sup_x_bend_height) = self.__asign_bar_vars(
            as_db=self.as_sup_x_db,
            as_anchor=self.as_sup_x_anchor,
            as_bend_length=self.as_sup_x_bend_longitud,
            as_bend_angle=self.as_sup_x_bend_angle,
            as_bend_height=self.as_sup_x_bend_height)

        # Superior Y bars.
        (self.as_sup_y_db, self.max_db_sup_y, self.as_sup_y_anchor, self.number_init_sup_y, self.as_sup_y_bend_longitud,
         self.as_sup_y_bend_angle, self.as_sup_y_bend_height) = self.__asign_bar_vars(
            as_db=self.as_sup_y_db,
            as_anchor=self.as_sup_y_anchor,
            as_bend_length=self.as_sup_y_bend_longitud,
            as_bend_angle=self.as_sup_y_bend_angle,
            as_bend_height=self.as_sup_y_bend_height)

        # Inferior X bars.
        (self.as_inf_x_db, self.max_db_inf_x, self.as_inf_x_anchor, self.number_init_inf_x, self.as_inf_x_bend_longitud,
         self.as_inf_x_bend_angle, self.as_inf_x_bend_height) = self.__asign_bar_vars(
            as_db=self.as_inf_x_db,
            as_anchor=self.as_inf_x_anchor,
            as_bend_length=self.as_inf_x_bend_longitud,
            as_bend_angle=self.as_inf_x_bend_angle,
            as_bend_height=self.as_inf_x_bend_height)

        # Inferior Y bars.
        (self.as_inf_y_db, self.max_db_inf_y, self.as_inf_y_anchor, self.number_init_inf_y, self.as_inf_y_bend_longitud,
         self.as_inf_y_bend_angle, self.as_inf_y_bend_height) = self.__asign_bar_vars(
            as_db=self.as_inf_y_db,
            as_anchor=self.as_inf_y_anchor,
            as_bend_length=self.as_inf_y_bend_longitud,
            as_bend_angle=self.as_inf_y_bend_angle,
            as_bend_height=self.as_inf_y_bend_height)

        # Generate bars.
        self.bars_as_sup_x = self.__gen_bars(as_db=self.as_sup_x_db,
                                             as_sp=self.as_sup_x_sp,
                                             as_anchor=self.as_sup_x_anchor,
                                             as_position=Position.SUPERIOR,
                                             as_direction=Direction.HORIZONTAL,
                                             as_bend_length=self.as_sup_x_bend_longitud,
                                             as_bend_angle=self.as_sup_x_bend_angle,
                                             as_bend_height=self.as_sup_x_bend_height)
        self.bars_as_sup_y = self.__gen_bars(as_db=self.as_sup_y_db,
                                             as_sp=self.as_sup_y_sp,
                                             as_anchor=self.as_sup_y_anchor,
                                             as_position=Position.SUPERIOR,
                                             as_direction=Direction.VERTICAL,
                                             as_bend_length=self.as_sup_y_bend_longitud,
                                             as_bend_angle=self.as_sup_y_bend_angle,
                                             as_bend_height=self.as_sup_y_bend_height)
        self.bars_as_inf_x = self.__gen_bars(as_db=self.as_inf_x_db,
                                             as_sp=self.as_inf_x_sp,
                                             as_anchor=self.as_inf_x_anchor,
                                             as_position=Position.INFERIOR,
                                             as_direction=Direction.HORIZONTAL,
                                             as_bend_length=self.as_inf_x_bend_longitud,
                                             as_bend_angle=self.as_inf_x_bend_angle,
                                             as_bend_height=self.as_inf_x_bend_height)
        self.bars_as_inf_y = self.__gen_bars(as_db=self.as_inf_y_db,
                                             as_sp=self.as_inf_y_sp,
                                             as_anchor=self.as_inf_y_anchor,
                                             as_position=Position.INFERIOR,
                                             as_direction=Direction.VERTICAL,
                                             as_bend_length=self.as_inf_y_bend_longitud,
                                             as_bend_angle=self.as_inf_y_bend_angle,
                                             as_bend_height=self.as_inf_y_bend_height)

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
        self.box_width = self.length_x
        self.box_height = self.length_y

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
                          denomination: bool = False,
                          unifilar_bars: bool = False) -> dict:
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
                        dimensions=dimensions,
                        reinforcement_dimensions=False,
                        denomination=denomination,
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
                        dimensions=dimensions,
                        reinforcement_dimensions=False,
                        denomination=denomination,
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
                        x_section: float = None,
                        y_section: float = None,
                        axe_section: str = "x",
                        concrete_shape: bool = True,
                        bars: bool = True,
                        dimensions: bool = True,
                        denomination: bool = False,
                        unifilar: bool = True,
                        settings: dict = SLAB_SET_TRANSVERSE) -> dict:
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {}
        concrete_dict = []
        spaced_bars_dict = []

        # Drawing concrete.
        if concrete_shape:
            if axe_section == Axes.X.value:
                concrete_dict += self.concrete.draw_right_view(document=document,
                                                               x=x,
                                                               y=y,
                                                               dimensions=dimensions,
                                                               dimensions_inner=False,
                                                               settings=settings["concrete_settings"])
            if axe_section == Axes.Y.value:
                concrete_dict += self.concrete.draw_front_view(document=document,
                                                               x=x,
                                                               y=y,
                                                               dimensions=dimensions,
                                                               dimensions_inner=False,
                                                               settings=settings["concrete_settings"])

        # Drawing bars.
        if bars:
            sp_bars_lg_sup = self.bars_as_sup_y
            sp_bars_lg_inf = self.bars_as_inf_y
            sp_bars_tr_sup = self.bars_as_sup_x
            sp_bars_tr_inf = self.bars_as_inf_x
            db_max_lg_sup = self.max_db_sup_y
            db_max_lg_inf = self.max_db_inf_y
            anchor_lg_sup = any(self.as_sup_y_anchor)
            anchor_lg_inf = any(self.as_inf_y_anchor)
            rotate_angle = -90

            if axe_section == "y":
                sp_bars_lg_sup, sp_bars_tr_sup = sp_bars_tr_sup, sp_bars_lg_sup
                sp_bars_lg_inf, sp_bars_tr_inf = sp_bars_tr_inf, sp_bars_lg_inf
                db_max_lg_sup = self.max_db_sup_x
                db_max_lg_inf = self.max_db_inf_x
                anchor_lg_sup = any(self.as_sup_x_anchor)
                anchor_lg_inf = any(self.as_inf_x_anchor)
                rotate_angle = 0

            # Transverse bar sections.
            for sp_bar in sp_bars_tr_sup:
                x_coord, y_coord = x, y
                if unifilar:
                    y_coord += db_max_lg_sup / 2

                bar_displacements = {}
                if not unifilar and anchor_lg_sup:
                    bar_displacements[sp_bar.quantity - 1] = (0, -db_max_lg_sup)
                    if sp_bar.is_exact_reinforcement:
                        bar_displacements[0] = (0, db_max_lg_sup)

                spaced_bars_dict.append(sp_bar.draw_transverse(document=document,
                                                               x=x_coord,
                                                               y=y_coord,
                                                               dimensions=False,
                                                               bar_displacements=bar_displacements,
                                                               rotate_angle=rotate_angle,
                                                               settings=settings["spaced_bars_settings"]))

            for sp_bar in sp_bars_tr_inf:
                x_coord, y_coord = x, y
                if unifilar:
                    y_coord -= db_max_lg_inf / 2

                bar_displacements = {}
                if not unifilar and anchor_lg_inf:
                    print(anchor_lg_inf)
                    bar_displacements[sp_bar.quantity - 1] = (0, -db_max_lg_inf)
                    if sp_bar.is_exact_reinforcement:
                        bar_displacements[0] = (0, db_max_lg_inf)

                spaced_bars_dict.append(sp_bar.draw_transverse(document=document,
                                                               x=x_coord,
                                                               y=y_coord,
                                                               dimensions=False,
                                                               bar_displacements=bar_displacements,
                                                               rotate_angle=rotate_angle,
                                                               settings=settings["spaced_bars_settings"]))

            # Longitudinal bars.
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
            pass

        return elements

    def draw_rebbar_detailing_longitudinal(self):
        pass

    def draw_rebbar_detailing_transverse(self):
        pass

    def draw_rebbar_detailing_table(self):
        pass

    def data(self):
        pass

    # TODO: Escribir función elements_section y refactorizar funciones de transversal acordemente.
    def __elements_section(self,
                           elements: list,
                           x: float) -> list:
        pass

    def extract_data(self):
        pass

    def __asign_bar_vars(self,
                         as_db: list,
                         as_anchor: list,
                         as_bend_length: list,
                         as_bend_angle: list,
                         as_bend_height: list) -> tuple[list, float, list, int, list, list, list]:
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

    def __gen_bars(self,
                   as_db: list,
                   as_sp: list,
                   as_anchor: list,
                   as_bend_length: list,
                   as_bend_angle: list,
                   as_bend_height: list,
                   as_position: Position,
                   as_direction: Direction) -> list[SpacedBars]:
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
                                          bend_height=as_bend_height[i]))

        return spaced_bars


if __name__ == "__main__":
    import ezdxf

    doc = ezdxf.new(setup=True)
    slab = Slab(
        length_x=4.05,
        length_y=6.05,
        thickness=0.18,
        x=10,
        y=10,
        as_sup_x_db=[0.012],
        as_sup_x_sp=[0.18],
        as_sup_y_db=[0.01],
        as_sup_y_sp=[0.18],
        as_inf_x_db=[0.016],
        as_inf_x_sp=[0.18],
        as_inf_y_db=[0.02],
        as_inf_y_sp=[0.18],
        as_inf_x_anchor=[0.05],
        as_sup_x_anchor=[0.05],
        # as_inf_y_anchor=[0.1],
        # as_inf_x_bend_longitud=[2],
        # as_inf_x_bend_angle=[45],
        # as_inf_x_bend_height=[0.1],
        # as_inf_y_bend_longitud=[4],
        # as_inf_y_bend_angle=[45],
        # as_inf_y_bend_height=[0.1],
        cover=0.025
    )

    slab.draw_longitudinal(document=doc, x=10, y=10, unifilar_bars=True, one_bar=True)
    slab.draw_transverse(document=doc, x=10, y=9.5, unifilar=True, axe_section="y")
    slab.draw_transverse(document=doc, x=10, y=9, unifilar=True, axe_section="x")

    slab.draw_longitudinal(document=doc, x=20, y=10, one_bar=False, unifilar_bars=False)
    slab.draw_transverse(document=doc, x=20, y=9.5, unifilar=False, axe_section="y")
    slab.draw_transverse(document=doc, x=20, y=9, unifilar=False, axe_section="x")

    doc.saveas(filename="c:/users/beta/desktop/test_slab.dxf")
