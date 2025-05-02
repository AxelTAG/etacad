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
    beam = Beam(width=.2,
                height=.35,
                length=4,
                x=1,
                y=2,
                as_sup={.008: 2},
                as_inf={.012: 2, .008: 1},
                stirrups_db=.008,
                stirrups_sep=.15,
                cover=.025)

The `x` and `y` parameters correspond to the default point where the drawings will be plotted unless specified when
executing the drawing methods.


.. _beam-bars-label:

Beam bars
^^^^^^^^^

You can add more steel bars by specifying their diameter as the key and the quantity as the dictionary values. These
will be symmetrically arranged along the width or effective height of the section. You can add bars vertically using
the parameters `as_right` and `as_left`. The cover is considered at the bar's centerline.

.. code:: python

    beam = Beam(width=.2,
                    height=.35,
                    length=4,
                    as_sup={.01: 2, .008: 1},
                    as_right={.008: 2},
                    as_inf={.012: 2, .008: 1},
                    as_left={.008: 2},
                    stirrups_db=.008,
                    stirrups_sep=.15,
                    cover=.025)  # The cover is considered at the bar's centerline.

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

    beam = Beam(width=.2,
                height=.35,
                length=4,
                as_sup={.01: 2, .008: 1},
                as_inf={.012: 2, .008: 1},
                stirrups_db=[.008, .01, .008],
                stirrups_sep=[.15, .1, .15],
                stirrups_length=[.6, 2, .6],
                stirrups_anchor=.125,
                stirrups_x=[.2, 1, 3.2],
                cover=0.025)


Beam columns intersections
^^^^^^^^^^^^^^^^^^^^^^^^^^

Intersections of the columns can be taken into account; we need to introduce three additional parameters:
`columns`, `columns_pos`, and `columns_symbol`, the latter being optional.

.. code:: python

    beam = Beam(width=.2,
                height=.35,
                length=4,
                as_sup={.008: 2},
                as_inf={.012: 2, .008: 1},
                stirrups_db=.008,
                stirrups_sep,
                columns=[(.2, .35), (.25, .35)],
                columns_pos=[0, 3.65],
                columns_symbol=["C1", "C2"],
                cover=.025)


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
                           unfilar_bars=False)

See more about the parameters of the :meth:`Beam.draw_longitudinal` function for further details.

 
Transversal drawing of the beam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_transverse(document=doc,
                         x=2,
                         y=1,
                         unfilar_bars=False)

See more about the parameters of the :meth:`Beam.draw_transverse` function for further details.


Longitudinal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_longitudinal_rebar_detailing(document=doc,
                                           x=2,
                                           y=1,
                                           unfilar_bars=True)

See more about the parameters of the :meth:`Beam.draw_longitudinal_rebar_detailing` function for further details.


Transversal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_transverse_rebar_detailing(document=doc,
                                           x=2,
                                           y=1,
                                           unfilar_bars=True)

See more about the parameters of the :meth:`Beam.draw_transverse_rebar_detailing` function for further details.


Table rebar detailing
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    beam.draw_transverse_rebar_detailing(document=doc,
                                         x=2,
                                         y=1,
                                         unfilar_bars=True)

See more about the parameters of the :meth:`Beam.draw_transverse_rebar_detailing` function for further details.


Creating a Column instance
--------------------------

.. currentmodule:: etacad.column

Create a simple concrete column with :class:`Column` class.

.. code:: python

    # Importing Column class.
    from etacad import Column

    # Creating a basic Column instance.
    column = Column(width=.25,
                    depth=.25,
                    height=6,
                    x=2,
                    y=2,
                    as_sup={.012: 3},
                    as_right={.012: 1},
                    as_inf={.012: 2},
                    as_left={.012: 1},
                    stirrups_db=.008,
                    stirrups_sep=.15,
                    cover=.025)

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

    column = Column(width=.25,
                    depth=.25,
                    height=6,
                    x=2,
                    y=2,
                    as_sup={.012: 3},
                    as_right={.012: 1},
                    as_inf={.012: 2},
                    as_left={.012: 1},
                    stirrups_db=.008,
                    stirrups_sep=.15,
                    beams=[(.25, .25), (.25, .25)],
                    beams_pos=[0, 5.75],
                    columns_symbol=["B1", "B2"],
                    cover=.025)


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
                             unfilar_bars=False)

See more about the parameters of the :meth:`Column.draw_longitudinal` function for further details.


Transversal drawing of the column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_transverse(document=doc,
                           x=5,
                           y=1,
                           unfilar_bars=False)

See more about the parameters of the :meth:`Column.draw_transverse` function for further details.


Longitudinal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_longitudinal_rebar_detailing(document=doc,
                                             x=2,
                                             y=1,
                                             unfilar_bars=True)

See more about the parameters of the :meth:`Column.draw_longitudinal_rebar_detailing` function for further details.


Transversal rebar detailing drawing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_transverse_rebar_detailing(document=doc,
                                           x=6,
                                           y=1,
                                           unfilar_bars=True)

See more about the parameters of the :meth:`Column.draw_transverse_rebar_detailing` function for further details.


Table rebar detailing
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    column.draw_transverse_rebar_detailing(document=doc,
                                           x=2,
                                           y=1,
                                           unfilar_bars=True)

See more about the parameters of the :meth:`Column.draw_transverse_rebar_detailing` function for further details.
