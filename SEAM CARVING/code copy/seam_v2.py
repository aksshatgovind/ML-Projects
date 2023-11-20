'''
    Run: python3 seam_v2.py Arch.jpg Arch-seam-2.png
'''

import sys

from energy import compute_energy
from util import Colour, read_image_to_array, write_array_to_image


class SeamEnergyWithBackPointer:

    def __init__(self, energy, x_coordinate_in_previous_row=None):
        self.energy = energy
        self.x_coordinate_in_previous_row = x_coordinate_in_previous_row

    
def compute_vertical_seam_v2(energy_data):
    
    m_grid = [[None for _ in row] for row in energy_data]

    h = len(energy_data)
    w = len(energy_data[0])

    for x in range(w):
        m_grid[0][x] = SeamEnergyWithBackPointer(energy_data[0][x])

    for y in range(1, h):
        for x in range(w):
            x_min = x - 1 if x > 0 else 0
            x_max = x + 1 if x < w - 1 else w - 1

            min_x_parent = min(
                range(x_min, x_max + 1),
                key=lambda x_candidate: m_grid[y - 1][x_candidate].energy
            )

            m_grid[y][x] = SeamEnergyWithBackPointer(
                energy_data[y][x] + m_grid[y - 1][min_x_parent].energy,
                min_x_parent
            )

    min_end_x = min(enumerate(m_grid[h - 1]), key=lambda m: m[1].energy)[0]
    seam_energy = m_grid[-1][min_end_x].energy

    seam_xs = []
    last_x = min_end_x
    for y in range(h - 1, -1, -1):
        seam_xs.append(last_x)
        last_x = m_grid[y][last_x].x_coordinate_in_previous_row

    seam_xs.reverse()

    return (seam_xs, seam_energy)

def visualize_seam_on_image(pixels, seam_xs):
    h = len(pixels)
    w = len(pixels[0])

    new_pixels = [[p for p in row] for row in pixels]

    for y, seam_x in enumerate(seam_xs):
        min_x = max(seam_x - 2, 0)
        max_x = min(seam_x + 2, w - 1)

        for x in range(min_x, max_x + 1):
            new_pixels[y][x] = Colour(255, 0, 0)

    return new_pixels

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_to_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)

    print('Finding the lowest-energy seam...')
    seam_xs, min_seam_energy = compute_vertical_seam_v2(energy_data)

    print(f'Saving {output_filename}')
    visualized_pixels = visualize_seam_on_image(pixels, seam_xs)
    write_array_to_image(visualized_pixels, output_filename)

    print()
    print(f'Minimum seam energy was {min_seam_energy} at x = {seam_xs[-1]}')

