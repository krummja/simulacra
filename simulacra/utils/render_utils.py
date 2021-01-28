
def argb_from_color(col):
    return (col & 0xFF000000) >> 24, (col & 0xFF0000) >> 16, (col & 0xFF00) >> 8, col & 0xFF

def cell_to_tile(x, y):
    return (x * 2, y)

def tile_to_pixel(x, y):
    return (x * 2, y * 2)

def pixel_to_tile(x, y):
    return (x // 2, y // 2)

def tile_to_cell(x, y):
    return (x // 2, y)
