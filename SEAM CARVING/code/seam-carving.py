'''
    Run: python3 seam-carving.py Arch.jpg Arch-seamed.png
'''

import sys

from energy import compute_energy
from seam_v2 import compute_vertical_seam_v2, visualize_seam_on_image
from util import Colour, read_image_to_array, write_array_to_image


def remove_seam_from_image(image, seam_xs):
    new_pixels = [
        [p for x, p in enumerate(row) if x != seam_xs[y]]
        for (y, row) in enumerate(image)
    ]

    return new_pixels


def remove_n_lowest_seams_from_image(image, num_seams_to_remove):
    for i in range(num_seams_to_remove):
        print(f'Removing seam {i + 1}/{num_seams_to_remove}')

        print('  Computing energy...')
        energy_data = compute_energy(image)
        print('  Finding the lowest-energy seam...')
        seam_xs, _ = compute_vertical_seam_v2(energy_data)

        print(f'  Saving intermediate result to intermediate-{i}.png...')
        visualized_pixels = visualize_seam_on_image(image, seam_xs)
        write_array_to_image(visualized_pixels, f'intermediate-{i}.png')

        print('  Removing the lowest-energy seam...')
        image = remove_seam_from_image(image, seam_xs)

    return image

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'USAGE: {__file__} <input> <num-seams-to-remove> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    num_seams_to_remove = int(sys.argv[2])
    output_filename = sys.argv[3]

    print(f'Reading {input_filename}...')
    pixels = read_image_to_array(input_filename)

    print(f'Saving {output_filename}')
    resized_pixels = \
        remove_n_lowest_seams_from_image(pixels, num_seams_to_remove)
    write_array_to_image(resized_pixels, output_filename)


