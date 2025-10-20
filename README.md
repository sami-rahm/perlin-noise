# perlin-noise
pretty cool took me a few hrs to make

save image option in draw_full_perlin_grid, also change box resolution
change depth at the top with res

how it works: 

1. generates a grid of vectors in random directions
2. for any point in the grid you find the 4 surrounding grid points
3. compute the dot product of the point with each corner then interpolate them
