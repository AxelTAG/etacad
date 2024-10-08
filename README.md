# etacad

A package aimed to simpilfy drawings of structurals elements based on ezdxf library.


## Features

- Uses of ezdxf for create ".dxf" files with Python.
- Python Bar, Stirrup, Beam, Column classes for manipulate and draw elements.

## Coming features

- Slab class, Isoleted footing.

## Usage

```
import ezdxf
from etacad.beam import Beam
from etacad.column import Column

# Create a dxf document.
doc = ezdxf.new("R2010", setup=True)

# Create a beam.
beam = Beam(width=0.3,
            height=0.5,
            length=4,
            as_sup={0.012: 2, 0.008: 1},
            as_inf={0.016: 2, 0.01: 1},
            as_right={0.01: 4},
            as_left={0.01:4},
            anchor_sup=0.1,
            anchor_right=0,
            anchor_inf=0.1,
            anchor_left=0,
            stirrups_db=[0.008, 0.01, 0.008],
            stirrups_length=[0.6, 2, 0.6],
            stirrups_sep=[0.15, 0.10, 0.15],
            stirrups_x=[0.2, 1, 3.10],
            cover=0.03,
            columns=[[0.2, 0.5], [0.3, 0.5]],
            columns_pos=[0, 3.7])

# Draw longitudinal section.
beam.draw_longitudinal(document=doc, x=0, y=0, unifilar_bars=False)

# Draw transverse section.
beam.draw_transverse(document=doc, x=5, y=0, unifilar=False, x_section=2)
beam.draw_transverse(document=doc, x=7, y=0, unifilar=False, x_section=0.4)

# Draw longitudinal rebar detailing.
beam.draw_longitudinal_rebar_detailing(document=doc, x=0, y=-1)

# Draw transverse rebar detailing.
beam.draw_transverse_rebar_detailing(document=doc, x=6, y=0, x_section=2)
beam.draw_transverse_rebar_detailing(document=doc, x=8, y=0, x_section=0.4)

# Draw table rebar detailing.
beam.draw_table_rebar_detailing(document=doc, x=0, y=-7)

# Saving dxf file.
doc.saveas("beam.dxf")


# Create a dxf document.
doc1 = ezdxf.new("R2010", setup=True)

# Create a column.
column = Column(width=0.2,
                depth=0.2,
                height=6,
                as_sup={0.016: 2},
                as_inf={0.016: 2},
                stirrups_db=0.008,
                stirrups_sep=0.15,
                cover=0.03)

# Draw column longitudinal section.
column.draw_longitudinal(document=doc1, x=10, y=0, unifilar_bars=False)

# Draw column transverse section.
column.draw_transverse(document=doc1, x=10, y=-1, unifilar=False, y_section=2)

# Draw column longitudinal rebar detailing.
column.draw_longitudinal_rebar_detailing(document=doc1, x=11, y=0)

# Draw column transverse rebar detailing.
column.draw_transverse_rebar_detailing(document=doc1, x=11, y=-1, y_section=2)

# Draw column table rebar detailing.
column.draw_table_rebar_detailing(document=doc1, x=10, y=-7)

# Saving dxf file.
doc1.saveas("column.dxf")
```

## Links

- Documentation at: comming soon.
- Source code and issue tracking at: [GitHub](https://github.com/AxelTAG/etacad)
- Distribution at: [Pypi](https://pypi.org/project/etacad/)

## Support me:

- If you want to pay me for a beer, coffee, or something else: [C|_|](https://www.paypal.com/paypalme/KevinAxelTagliaferri)