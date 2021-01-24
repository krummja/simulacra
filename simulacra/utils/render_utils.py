
def argb_from_color(col):
    return (col & 0xFF000000) >> 24, (col & 0xFF0000) >> 16, (col & 0xFF00) >> 8, col & 0xFF
