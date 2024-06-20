# etacad

A package aimed to simpilfy drawings of structurals elements based on ezdxf library.


## Features

- Uses of ezdxf for create ".dxf" files with Python.
- Python Element, Bar, Stirrup, Beam classes for manipulate.

## Usage

```
import ezdxf
from etacad import Beam

# Create a dxf document.
doc = ezdxf.new("R2000")

# Create a beam.
beam = Beam(width=0.3,
            height=0.5,
            length=4,
            as_sup={12: 2, 8: 1},
            as_inf={16: 2, 10: 1},
            as_right={10: 4}, as_left={10:4},
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
beam.draw_longitudinal(x=0, y=0, unifilar=False)

# Saving dxf file.
doc.saveas("beam.dxf")
```