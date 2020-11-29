from __future__ import annotations
import time
import tcod

from config import *


class NoiseMachine:

    NOISE_OPTIONS = [
        ["perlin noise", tcod.NOISE_PERLIN, tcod.noise.SIMPLE],             # 0
        ["simplex noise", tcod.NOISE_SIMPLEX, tcod.noise.SIMPLE],           # 1
        ["wavelet noise", tcod.NOISE_WAVELET, tcod.noise.SIMPLE],           # 2
        ["perlin fbm", tcod.NOISE_PERLIN, tcod.noise.FBM],                  # 3
        ["perlin turbulence", tcod.NOISE_PERLIN, tcod.noise.TURBULENCE],    # 4
        ["simplex fbm", tcod.NOISE_SIMPLEX, tcod.noise.FBM],                # 5
        ["simplex turbulence", tcod.NOISE_SIMPLEX, tcod.noise.TURBULENCE],  # 6
        ["wavelet fbm", tcod.NOISE_WAVELET, tcod.noise.FBM],                # 7
        ["wavelet turbulence", tcod.NOISE_WAVELET, tcod.noise.TURBULENCE],  # 8
        ]

    def __init__(self):
        self.func = 3
        self.dx = 0.0
        self.dy = 0.0
        self.octaves = 2.0
        self.zoom = 4.0
        self.hurst = tcod.NOISE_DEFAULT_HURST
        self.lacunarity = tcod.NOISE_DEFAULT_LACUNARITY
        self.noise = self.get_noise()
        self.img = tcod.image_new(CONSOLE_WIDTH * 2, CONSOLE_HEIGHT * 2)

    @property
    def algorithm(self):
        return self.NOISE_OPTIONS[self.func][1]

    @property
    def implementation(self):
        return self.NOISE_OPTIONS[self.func][2]

    def get_noise(self):
        return tcod.noise.Noise(
            2,
            self.algorithm,
            self.implementation,
            self.hurst,
            self.lacunarity,
            self.octaves,
            seed=None,
            )

    def on_enter(self):
        tcod.sys_set_fps(0)

    def on_draw(self, consoles: Dict[str, Console]):
        self.dx = time.perf_counter() * 0.25
        self.dy = time.perf_counter() * 0.25
        for y in range(2 * CONSOLE_HEIGHT):
            for x in range(2 * CONSOLE_WIDTH):
                f = [
                    self.zoom * x / (2 * CONSOLE_WIDTH) + self.dx,
                    self.zoom * y / (2 * CONSOLE_HEIGHT) + self.dy
                    ]
                value = self.noise.get_point(*f)
                c = int((value + 1.0) / 2.0 * 255)
                c = max(0, min(c, 255))
                self.img.put_pixel(x, y, (c // 2, c // 2, c))

        rectw = 24
        recth = 13
        if self.implementation == tcod.noise.SIMPLE:
            recth = 10

        consoles['ROOT'].draw_semigraphics(self.img)
        # consoles['ROOT'].draw_rect(
        #     2, 2,
        #     rectw, recth,
        #     ch=0, fg=tcod.white, bg=tcod.grey,
        #     bg_blend=tcod.BKGND_COLOR_BURN
        #     )
        
        # consoles['ROOT'].print(
        #     2, 10,
        #     "Testing"
        # )

        # consoles['ROOT'].fg[2: 2 + rectw, 2: 2 + recth] = (
        #     consoles['ROOT'].fg[2: 2 + rectw, 2: 2 + recth] * tcod.grey / 255
        #     )