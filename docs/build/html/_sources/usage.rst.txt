Usage
=====

For the following examples, we will use variable 'doc'as an instance of ezdxf.new().

.. code:: python

   import ezdxf


Creating a new document
-----------------------

Pass the setup parameter as True to use the dimensions and text styles from the ezdxf module. By default, etacad
uses them.

.. code:: python

    doc = ezdxf.new("R2010", setup=True)


Creating a Beam instance
------------------------
.. currentmodule:: etacad.beam

Create a simple concrete beam with :class:`Beam` class.

.. code:: python

    # Importing Beam class.
    from etacad import Beam

    # Creating a basic Beam instance.
    beam = Beam(width=0.2,
                height=0.35,
                length=4,
                x=1,
                y=2,
                as_sup={0.008: 2},
                as_inf={0.012: 2, 0.008: 1},
                stirrups_db=0.008,
                stirrups_sep=0.15,
                cover=0.025)

The `x` and `y` parameters correspond to the default point where the drawings will be plotted unless specified when
executing the drawing methods.


.. _beam-bars-label:

Beam bars
^^^^^^^^^

You can add more steel bars by specifying their diameter as the key and the quantity as the dictionary values. These
will be symmetrically arranged along the width or effective height of the section. You can add bars vertically using
the parameters `as_right` and `as_left`. The cover is considered at the bar's centerline.

.. code:: python

    beam = Beam(width=0.2,
                height=0.35,
                length=4,
                as_sup={0.01: 2, 0.008: 1},
                as_right={0.008: 2},
                as_inf={0.012: 2, 0.008: 1},
                as_left={0.008: 2},
                stirrups_db=0.008,
                stirrups_sep=0.15,
                cover=0.025)  # The cover is considered at the bar's centerline.

You can also add an anchorage length for the bars using `anchor_sup`, `anchor_right`, `anchor_inf`, and `anchor_left`,
passing a single value for all the bars on the side or a list specifying a value for each bar.


.. _beam-stirrups-label:

Beam stirrups
^^^^^^^^^^^^^

The stirrups are handled differently than the bars. You can specify a single diameter and spacing (as in the previous
example), which will distribute the stirrups along the beam, or you can provide a list of diameters, requiring
additional parameters such as the X coordinate where each stirrup begins and the reinforcement length. Additionally,
you can provide a list of the anchorage lengths for each stirrup or a float for all stirrups.

.. code:: python

    beam = Beam(width=0.2,
                height=0.35,
                length=4,
                as_sup={0.01: 2, 0.008: 1},
                as_inf={0.012: 2, 0.008: 1},
                stirrups_db=[0.008, 0.01, 0.008],
                stirrups_sep=[0.15, 0.1, 0.15],
                stirrups_length=[0.6, 2, 0.6],
                stirrups_anchor=0.125,
                stirrups_x=[0.2, 1, 3.2],
                cover=0.025)


Beam columns intersections
^^^^^^^^^^^^^^^^^^^^^^^^^^

Intersections of the columns can be taken into account; we need to introduce three additional parameters:
`columns`, `columns_pos`, and `columns_symbol`, the latter being optional.

.. code:: python

    beam = Beam(width=0.2,
                height=0.35,
                length=4,
                as_sup={0.008: 2},
                as_inf={0.012: 2, 0.008: 1},
                stirrups_db=0.008,
                stirrups_sep=0.15,
                columns=[(0.2, 0.35), (0.25, 0.35)],
                columns_pos=[0, 3.65],
                columns_symbol=["C1", "C2"],
                cover=0.025)


Longitudinal drawing of the beam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Beam class offers methods for drawing longitudinal and cross sections, which are customizable through the method
parameters and the `settings` parameter.
Each method returns a dictionary that may or may not contain other nested dictionaries (depending on the method and
class). The keys that do not have dictionaries contain a list of DXF entities.

.. code:: python

    beam.draw_longitudinal(document=doc,
                           x=2,
                           y=1,
                           unifilar_bars=False)

See more about the parameters of the :meth:`Beam.draw_longitudinal` function for further details.

 
Transversal drawing of the beam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_transverse(document=doc,
                         x=2,
                         y=1,
                         unifilar=False)

See more about the parameters of the :meth:`Beam.draw_transverse` function for further details.


Longitudinal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_longitudinal_rebar_detailing(document=doc,
                                           x=2,
                                           y=1,
                                           unifilar=True)

See more about the parameters of the :meth:`Beam.draw_longitudinal_rebar_detailing` function for further details.


Transversal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_transverse_rebar_detailing(document=doc,
                                           x=2,
                                           y=1,
                                           unifilar=True)

See more about the parameters of the :meth:`Beam.draw_transverse_rebar_detailing` function for further details.


Table rebar detailing
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_table_rebar_detailing(document=doc,
                                    x=2,
                                    y=1)

See more about the parameters of the :meth:`Beam.draw_table_rebar_detailing` function for further details.


Creating a Column instance
--------------------------

.. currentmodule:: etacad.column

Create a simple concrete column with :class:`Column` class.

.. code:: python

    # Importing Column class.
    from etacad import Column

    # Creating a basic Column instance.
    column = Column(width=0.25,
                    depth=0.25,
                    height=6,
                    x=2,
                    y=2,
                    as_sup={0.012: 3},
                    as_right={0.012: 1},
                    as_inf={0.012: 2},
                    as_left={0.012: 1},
                    stirrups_db=0.008,
                    stirrups_sep=0.15,
                    cover=0.025)

The `x` and `y` parameters correspond to the default point where the drawings will be plotted unless specified when
executing the drawing methods.


Column bars
^^^^^^^^^^^

It works the same as the :ref:`Beam bars<beam-bars-label>` section. The consideration here is that symmetrical columns are
generally used, and all the bar parameters (as_sup, as_right, as_inf, as_left) should be utilized. It must be noted that
the bars at the edges apply to two faces of the section, as considered in this example.


Column stirrups
^^^^^^^^^^^^^^^

It works the same as the :ref:`Beam stirrups<beam-stirrups-label>` section.


Column beams intersections
^^^^^^^^^^^^^^^^^^^^^^^^^^

Intersections of the beams can be taken into account; we need to introduce three additional parameters:
`beams`, `beams_pos`, and `beams_symbol`, the latter being optional.

.. code:: python

    column = Column(width=0.25,
                    depth=0.25,
                    height=6,
                    x=2,
                    y=2,
                    as_sup={0.012: 3},
                    as_right={0.012: 1},
                    as_inf={0.012: 2},
                    as_left={0.012: 1},
                    stirrups_db=0.008,
                    stirrups_sep=0.15,
                    beams=[(0.25, 0.25), (0.25, 0.25)],
                    beams_pos=[0, 5.75],
                    beams_symbol=["B1", "B2"],
                    cover=0.025)


Longitudinal drawing of the column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Column class offers methods for drawing longitudinal and cross sections, which are customizable through the method
parameters and the `settings` parameter.
Each method returns a dictionary that may or may not contain other nested dictionaries (depending on the method and
class). The keys that do not have dictionaries contain a list of DXF entities.

.. code:: python

    column.draw_longitudinal(document=doc,
                             x=3,
                             y=1,
                             unifilar_bars=False)

See more about the parameters of the :meth:`Column.draw_longitudinal` function for further details.


Transversal drawing of the column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_transverse(document=doc,
                           x=5,
                           y=1,
                           unifilar=False)

See more about the parameters of the :meth:`Column.draw_transverse` function for further details.


Longitudinal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_longitudinal_rebar_detailing(document=doc,
                                             x=2,
                                             y=1,
                                             unifilar=True)

See more about the parameters of the :meth:`Column.draw_longitudinal_rebar_detailing` function for further details.


Transversal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_transverse_rebar_detailing(document=doc,
                                           x=6,
                                           y=1,
                                           unifilar=True)

See more about the parameters of the :meth:`Column.draw_transverse_rebar_detailing` function for further details.


Table rebar detailing
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_table_rebar_detailing(document=doc,
                                      x=2,
                                      y=1)

See more about the parameters of the :meth:`Column.draw_table_rebar_detailing` function for further details.


Creating a Slab instance
--------------------------

.. currentmodule:: etacad.slab

Create a simple concrete slab with :class:`Slab` class.

.. code:: python

    # Importing Slab class.
    from etacad import Slab

    # Creating a basic Slab instance.
    slab = Slab(length_x=6,
               length_y=4,
               thickness=0.15,
               x=1,
               y=1)

The `x` and `y` parameters correspond to the default point where the drawings will be plotted unless specified when
executing the drawing methods.


Slab reinforcement
^^^^^^^^^^^^^^^^^^

Adds steel bars to the slab by assigning values to the parameters as_sup_x_*, as_sup_y_*, as_inf_x_*, and as_inf_y_*.
You can define the position of the reinforcement (top or bottom), the bar diameter, the spacing between bars, and their
anchorage length.

You can also add a concrete cover using the cover parameter.

.. code:: python

    # Creating a basic Slab instance.
    slab = Slab(length_x=6,
                length_y=4,
                thickness=0.15,
                x=1,
                y=1
                as_inf_x_db=0.006,
                as_inf_y_db=0.008,
                as_inf_x_sp=12,
                as_inf_y_sp=12,
                as_inf_x_anchor=0.05,
                as_inf_y_anchor=0.075,
                cover=0.025)

If you need more than two bar diameters in the same position (top/bottom, x/y), you must provide the corresponding
parameters as a list.

.. code:: python

    # Creating a basic Slab instance with reinforcement.
    slab = Slab(length_x=6,
                length_y=4,
                thickness=0.15,
                x=1,
                y=1,
                as_inf_x_db=0.006,
                as_inf_y_db=[0.008, 0.006],
                as_inf_x_sp=12,
                as_inf_y_sp=24,
                as_inf_x_anchor=0.05,
                as_inf_y_anchor=[0.075, 0.05],
                cover=0.025)


Longitudinal drawing of the column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Slab class offers methods for drawing longitudinal and cross sections, which are customizable through the method
parameters and the `settings` parameter.
Each method returns a dictionary that may or may not contain other nested dictionaries (depending on the method and
class). The keys that do not have dictionaries contain a list of DXF entities.

The draw_longitudinal() method will draw a top view of the slab (in future updates, it will be renamed to draw_top_view).
The method includes several parameters that enable or disable parts of the drawing according to user preferences.
The most notable parameter is one_bar, which indicates that only one bar from each position should be drawn.

.. code:: python

    # Drawing top view of slab.
    slab.draw_longitudinal(document=doc,
                           x=2,
                           y=2,
                           one_bar=False)

With the one_bar_position_* parameters, you can specify the position of the bar to be drawn.
The unifilar_bars parameter indicates whether you want to draw the bars as single-line representations (unifilar).

.. code:: python

    slab.draw_longitudinal(document=doc,
                           x=2,
                           y=2,
                           one_bar=False,
                           one_bar_position_sup=4,
                           one_bar_position_inf=6,
                           unifilar_bars=True)

See more about the parameters of the :meth:`Slab.draw_longitudinal` function for further details.


Transversal drawing of the column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cross-sections of the slab can be drawn along both the X and Y axes. This is specified using the axe_section parameter.
You can also enable the drawing of single-line (unifilar) bars.

.. code:: python

    slab.draw_transverse(document=doc,
                         x=4,
                         y=1,
                         axe_section="x",
                         concrete_shape=True,
                         unifilar=False)

See more about the parameters of the :meth:`Slab.draw_transverse` function for further details.


Longitudinal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A simple bar detailing can also be drawn.

.. code:: python

    slab.draw_longitudinal_rebar_detailing(document=doc,
                                           x=3,
                                           y=1,
                                           unifilar=True)

See more about the parameters of the :meth:`Slab.draw_longitudinal_rebar_detailing` function for further details.

Table rebar detailing
^^^^^^^^^^^^^^^^^^^^^

A reinforcement quantity table can also be drawn, just like in the Beam and Column classes.

.. code:: python

    slab.draw_table_rebar_detailing(document=doc,
                                    x=2,
                                    y=1)

See more about the parameters of the :meth:`Slab.draw_table_rebar_detailing` function for further details.
