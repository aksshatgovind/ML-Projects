'''
    Run: python3 energy.py Arch.jpg Arch-energy-map.png
'''

import sys
from util import Colour, read_image_to_array, write_array_to_image


def energy_at(pixels, x, y):
    h = len(pixels)
    w = len(pixels[0])

    x0 = x if x == 0 else x - 1
    x1 = x if x == w - 1 else x + 1

    dxr = pixels[y][x0].r - pixels[y][x1].r
    dxg = pixels[y][x0].g - pixels[y][x1].g
    dxb = pixels[y][x0].b - pixels[y][x1].b
    dx = dxr * dxr + dxg * dxg + dxb * dxb

    y0 = y if y == 0 else y - 1
    y1 = y if y == h - 1 else y + 1

    dyr = pixels[y0][x].r - pixels[y1][x].r
    dyg = pixels[y0][x].g - pixels[y1][x].g
    dyb = pixels[y0][x].b - pixels[y1][x].b
    dy = dyr * dyr + dyg * dyg + dyb * dyb

    return dx + dy


def compute_energy(pixels):
    energy = [[0 for _ in row] for row in pixels]

    for y, row in enumerate(pixels):
        for x, _ in enumerate(row):
            energy[y][x] = energy_at(pixels, x, y)

    return energy


def energy_data_to_colors(energy_data):
    colors = [[0 for _ in row] for row in energy_data]

    max_energy = max(
        energy
        for row in energy_data
        for energy in row
    )

    for y, row in enumerate(energy_data):
        for x, energy in enumerate(row):
            energy_normalized = round(energy / max_energy * 255)
            colors[y][x] = Colour(
                energy_normalized,
                energy_normalized,
                energy_normalized
            )

    return colors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f'Reading {input_file}...')
    pixels = read_image_to_array(input_file)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)
    energy_pixels = energy_data_to_colors(energy_data)

    print(f'Saving {output_file}')
    write_array_to_image(energy_pixels, output_file)