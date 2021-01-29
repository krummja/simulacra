
def argb_from_color(col):
    return (col & 0xFF000000) >> 24, (col & 0xFF0000) >> 16, (col & 0xFF00) >> 8, col & 0xFF

def subtile_from_cell(x, y):
    return (x * 2, y)

def tile_from_subtile(x, y):
    return (x * 2, y * 2)

def subtile_from_tile(x, y):
    return (x // 2, y // 2)

def cell_from_subtile(x, y):
    return (x // 2, y)

def subtile_dimensions_from_tile(w, h):
    return (w * 2, h * 2)

def cell_dimensions_from_subtile(w, h):
    return (w * 2, h)
