#!/usr/bin/env python3
import math
import sys

from PIL import Image, ImageDraw, ImageFont


ALPHABET = "+-=ABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"
DEBUG = False
DEBUG_COLOR = 127
DEGREES = (-112.5, -67.5, -22.5, 22.5, 67.5, 112.5, 157.5, -157.5)
FONT = ImageFont.truetype("/Library/Fonts/Microsoft/Georgia", 32)
FRAME_DURATION = 250
HIDDEN_COLOR = 1
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
MESSAGE_X_POSITION = 167
VISIBLE_COLOR = 255

BOUNDING_BOX_CENTER = [IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2]
BOUNDING_BOX_HALF_WIDTH = 320
BOUNDING_BOX = [
    (
        BOUNDING_BOX_CENTER[0] - BOUNDING_BOX_HALF_WIDTH,
        BOUNDING_BOX_CENTER[1] - BOUNDING_BOX_HALF_WIDTH,
    ),
    (
        BOUNDING_BOX_CENTER[0] + BOUNDING_BOX_HALF_WIDTH,
        BOUNDING_BOX_CENTER[1] + BOUNDING_BOX_HALF_WIDTH,
    ),
]

rotation_multiplier = 0


def circle_point(degree):
    radians = degree * math.pi / 180
    return (
        math.cos(radians) * BOUNDING_BOX_HALF_WIDTH + BOUNDING_BOX_CENTER[0],
        math.sin(radians) * BOUNDING_BOX_HALF_WIDTH + BOUNDING_BOX_CENTER[1],
    )


def draw_character(draw, character, dim=0, rotation=0):
    color = 255
    points = []
    for i, bit in enumerate(to_bit_array([character], 8)):
        if bit:
            points.append(circle_point(DEGREES[i] - rotation * rotation_multiplier))
    if len(points) > 2:
        draw.polygon(points, fill=color)
    elif len(points) == 2:
        draw.line(points, fill=color, width=3)
    elif points:
        draw_point(draw, points[0], 3, fill=color)


def draw_image(image, index, character, *previous_characters):
    draw = ImageDraw.Draw(image)
    draw.text(
        (MESSAGE_X_POSITION, IMAGE_HEIGHT - 40),
        f"FLAG ALPHABET: {ALPHABET}",
        fill=HIDDEN_COLOR,
        font=FONT,
    )
    if DEBUG:
        draw.ellipse(BOUNDING_BOX, outline=DEBUG_COLOR, width=2)
        draw.text((90, 0), str(index), fill=DEBUG_COLOR, font=FONT)
        draw.text((180, 0), f"{character:08b}", fill=DEBUG_COLOR, font=FONT)

    for i, (previous_character, dim) in enumerate(previous_characters):
        rotation = index - (len(previous_characters) - i)
        draw_character(draw, previous_character, dim=dim, rotation=rotation)
    draw_character(draw, character, dim=0, rotation=index)
    #draw_character(draw, 0xFF, dim=0, rotation=index)
    return image


def draw_point(draw, coordinates, radius, fill):
    box = [
        (coordinates[0] - radius, coordinates[1] - radius),
        (coordinates[0] + radius, coordinates[1] + radius),
    ]
    draw.ellipse(box, fill=fill)


def from_bit_array(array, bits_per_character):
    characters = []
    for x in range(0, len(array), bits_per_character):
        character = 0
        for bit in array[x : x + bits_per_character]:
            character = (character << 1) | bit
        characters.append(character)
    return characters


def main():
    global rotation_multiplier

    if len(sys.argv) != 2:
        print("Usage: puzzle.py FLAG")
        return 1
    flag = sys.argv[1]
    if not flag or len(flag) % 8 != 0:
        print("FLAG must be set and its length be a multiple of 8")
        return 1

    try:
        indexed = [ALPHABET.index(x) for x in flag]
    except ValueError:
        print(f"FLAG characters must be one of: {ALPHABET}")
        return 1

    bit_array = to_bit_array(indexed, 5)
    assert indexed == from_bit_array(bit_array, 5)
    translated = from_bit_array(bit_array, 8)

    rotation_multiplier = 45. / len(translated)


    image = Image.new(mode="L", size=(IMAGE_WIDTH, IMAGE_HEIGHT))
    images = []
    for index, character in enumerate(translated):
        images.append(
            draw_image(
                image.copy(),
                index,
                character,
            )
        )
    images[0].save(
        "puzzle.gif",
        append_images=images[1:],
        duration=FRAME_DURATION,
        loop=0,
        save_all=True,
    )


def to_bit_array(characters, bits_per_character):
    array = []
    mask = 1 << (bits_per_character - 1)
    for character in characters:
        for _ in range(bits_per_character):
            array.append(int(character & mask == mask))
            character = character << 1
    return array


if __name__ == "__main__":
    sys.exit(main())
