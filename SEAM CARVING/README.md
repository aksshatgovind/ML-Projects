# SEAM CARVING


## Content Aware Image Resizing

Resizing an image based on the contents of the image so the result looks natural

## How does seam carving work?

* An energy map (edge detection) is generated from the provided image.
* The algorithm tries to find the least important parts of the image taking into account the lowest energy values.
* Using a dynamic programming approach the algorithm will generate individual seams across the image from top to down, or from left to right (depending on the horizontal or vertical resizing) and will allocate for each seam a custom value, the least important pixels having the lowest energy cost and the most important ones having the highest cost.
* We traverse the image from the second row to the last row and compute the cumulative minimum energy for all possible connected seams for each entry.
* The minimum energy level is calculated by summing up the current pixel value with the lowest value of the neighboring pixels obtained from the previous row.
* We traverse the image from top to bottom and compute the minimum energy level. For each pixel in a row we compute the energy of the current pixel plus the energy of one of the three possible pixels above it.
* Find the lowest cost seam from the energy matrix starting from the last row and remove it.
* Repeat the process.




# Example

* Original image 
![original](https://user-images.githubusercontent.com/883386/35481925-de130752-0435-11e8-9246-3950679b4fd6.jpg) 
* Seamed image 
![broadway_tower_edit](https://user-images.githubusercontent.com/883386/35498110-a4a03328-04d5-11e8-9bf1-f526ef033d6a.jpg) 
