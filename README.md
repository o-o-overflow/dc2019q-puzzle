# puzzle

## Install requirements

```sh
pip install -r requirements.txt
```

## Build the large-sized gif

```sh
./puzzle.py "FLAG"
```

## Minimize gif size

1. Open gif with tool like gimp.
2. Adjust the colormap such that the color (1, 1, 1) is also the color (0, 0, 0)
3. Re-export as an interlaced animated gif (accept existing timings).
