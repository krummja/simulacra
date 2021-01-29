
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

def draw_box(console, x, y, w, h):
    # upper border
    border = '┌' + '─' * (w) + '┐'
    console.puts(x - 1, y - 1, border)
    # sides
    for i in range(h):
        console.puts(x - 1, y + i, '│')
        console.puts(x + w, y + i, '│')
    # lower border
    border = '└' + '─' * (w) + '┘'
    console.puts(x - 1, y + h, border)
