# puzzle

## Install requirements

```sh
pip install -r requirements.txt
```

## Build the large-sized gif

```sh
./puzzle.py "FLAG"
```

## Collapse color map

1. Open gif with tool like gimp.
2. Adjust the colormap such that all 3 colors are black (I couldn't quickly figure out how to get
   this directly working in pillow).
3. Re-export as an interlaced animated gif (accept existing timings).
