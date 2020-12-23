from __future__ import annotations

import bearlibterminal as blt
from bearlibterminal import terminal


terminal.open()
terminal.print(2, 1, "Hello world!")
terminal.refresh()
while terminal.read() != terminal.TK_CLOSE:
    pass
terminal.close()