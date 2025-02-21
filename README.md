Python script for converting 32x18 pngs into levels for [boxsmasher](https://github.com/rollerozxa/boxsmasher) by ROllerozxa.

Rellies on [Pillow](https://pillow.readthedocs.io/en/stable/) image library for Python.

! This script is not a perfect tool, customization needs to be added manually, and output must be manually copied each time.

### Prerequisites

- A (Unix) computer with ability to run LÖVE and development version of boxsmasher
- Baisic knowledge of the Unix commandline and file system
- working Python3 with [Pillow](https://pillow.readthedocs.io/en/stable/) library
- a pixelart editor

## Creating a Level

Create a 32x18 `.png` using a [pixelart editor of your choice](https://lospec.com/pixel-art-software-list/), I recommend [local ones](https://www.piskelapp.com/), over browser versions as they are easier to save.

By default: (cand be changed, see "Configuration" section)

- Red (255,0,0,255) are 1x1 boxes

- Dark Red (200,0,0,255) are for solid full boxes

- Green (255,0,0,255) is the throwBoundary

- Blue (255,0,0,255) is the solid terrain

## Running

Have [Pillow](https://pillow.readthedocs.io/en/stable/) installed

`python3 converter.py` or explore `converter.ipynb` notebook

pngs should be RGBA

## Configuration

To configure edit the constants in `converter.py`

`author = "your-name-here"`

`totalBalls = 3` or however many balls you want

color designations - the types of objects your colors represent.

```py
color_designations = [ # (RGBA, type, [additional, single-block])
    [(255,0,0,255),'boxclusters',['',False]],
    [(200,0,0,255),'boxclusters',['',True]],
    [(0,255,0,255),'throwBoundary',['',False]],
    [(0,0,255,255),'terrain',['',False]]
    # ...
]
```

The first must be a tuple with 4 values for RGBA colro channels.

The second is the type, which must exactly match the keywords `boxclusters`, `throwBoundary`, or `terrain`. (Note that you can/should have only one throwBoundary)

The third are specific qualities of the group. `''` is a free space for special qualitie such as `friction = <float between 0.0 and 1.0>`, `restitution = 2` (how bouncy it is), or `colour = { 209, 156, 56 }` (see [level 24 on in boxsmasher](https://github.com/rollerozxa/boxsmasher/blob/master/levels/24.lua))

The True/False value indicates whether you want the color to be a cluster of 1x1 boxes or a solid whole. Note: terrain and throwBoundary ignore this, and will always be whole.

## TODO

Proper converter still under construction.

A JavaScript version and plugins for pixel art editors might come later.
