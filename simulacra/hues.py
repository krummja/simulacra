from __future__ import annotations

from typing import Dict, Optional, Tuple

import tcod

Color = Tuple[int, int, int]


COLOR: Dict[str, Color] = {
    'maroon': (128, 0, 0),                          #  rgb(128, 0, 0),
    'dark red': (139, 0, 0),                        #  rgb(139, 0, 0),
    'brown': (165, 42, 42),                         #  rgb(165, 42, 42),
    'firebrick': (178, 34, 34),                     #  rgb(178, 34, 34),
    'crimson': (220, 20, 60),                       #  rgb(220, 20, 60),
    'red': (255, 0, 0),                             #  rgb(255, 0, 0),
    'tomato': (255, 99, 71),                        #  rgb(255, 99, 71),
    'coral': (255, 127, 80),                        #  rgb(255, 127, 80),
    'indian red': (205, 92, 92),                    #  rgb(205, 92, 92),
    'light coral': (240, 128, 128),                 #  rgb(240, 128, 128),
    'dark salmon': (233, 150, 122),                 #  rgb(233, 150, 122),
    'orange red': (255, 69, 0),                     #  rgb(255, 69, 0),
    'dark orange': (255, 140, 0),                   #  rgb(255, 140, 0),
    'orange': (255, 165, 0),                        #  rgb(255, 165, 0),
    'gold': (255, 215, 0),                          #  rgb(255, 215, 0),
    'dark golden rod': (184, 134, 11),              #  rgb(184, 134, 11),
    'golden rod': (218, 165, 32),                   #  rgb(218, 165, 32),
    'pale golden rod': (238, 232, 170),             #  rgb(238, 232, 170),
    'dark khaki': (189, 183, 107),                  #  rgb(189, 183, 107),
    'olive': (128, 128, 0),                         #  rgb(128, 128, 0),
    'yellow': (255, 255, 0),                        #  rgb(255, 255, 0),
    'yellow green': (154, 205, 50),                 #  rgb(154, 205, 50),
    'dark olive green': (85, 107, 47),              #  rgb(85, 107, 47),
    'olive drab': (107, 142, 35),                   #  rgb(107, 142, 35),
    'rain forest': (105, 115, 45),                  #  rgb(105, 115, 45),
    'lawn green': (124, 252, 0),                    #  rgb(124, 252, 0),
    'chart reuse': (127, 255, 0),                   #  rgb(127, 255, 0),
    'green yellow': (173, 255, 47),                 #  rgb(173, 255, 47),
    'dark green': (0, 100, 0),                      #  rgb(0, 100, 0),
    'green': (0, 128, 0),                           #  rgb(0, 128, 0),
    'forest green': (34, 139, 34),                  #  rgb(34, 139, 34),
    'ever green': (50, 70, 0),                      #  rgb(50, 70, 0),
    'lime': (0, 255, 0),                            #  rgb(0, 255, 0),
    'lime green': (50, 205, 50),                    #  rgb(50, 205, 50),
    'dark dark green': (75, 75, 60),                #  rgb(75, 75, 60),
    'light green': (144, 238, 144),                 #  rgb(144, 238, 144),
    'kelly green': (50, 200, 100),                  #  rgb(50, 200, 100),
    'pale green': (152, 251, 152),                  #  rgb(152, 251, 152),
    'dark sea green': (143, 188, 143),              #  rgb(143, 188, 143),
    'medium spring green': (0, 250, 154),           #  rgb(0, 250, 154),
    'spring green': (0, 255, 127),                  #  rgb(0, 255, 127),
    'sea green': (46, 139, 87),                     #  rgb(46, 139, 87),
    'medium aqua marine': (102, 205, 170),          #  rgb(102, 205, 170),
    'medium sea green': (60, 179, 113),             #  rgb(60, 179, 113),
    'blue stone': (30, 110, 90),                    #  rgb(30, 110, 90),
    'light sea green': (32, 178, 170),              #  rgb(32, 178, 170),
    'dark slate gray': (47, 79, 79),                #  rgb(47, 79, 79),
    'teal': (0, 128, 128),                          #  rgb(0, 128, 128),
    'dark cyan': (0, 139, 139),                     #  rgb(0, 139, 139),
    'aqua': (0, 255, 255),                          #  rgb(0, 255, 255),
    'cyan': (0, 255, 255),                          #  rgb(0, 255, 255),
    'light cyan': (224, 255, 255),                  #  rgb(224, 255, 255),
    'dark turquoise': (0, 206, 209),                #  rgb(0, 206, 209),
    'turquoise': (64, 224, 208),                    #  rgb(64, 224, 208),
    'medium turquoise': (72, 209, 204),             #  rgb(72, 209, 204),
    'pale turquoise': (175, 238, 238),              #  rgb(175, 238, 238),
    'aqua marine': (127, 255, 212),                 #  rgb(127, 255, 212),
    'powder blue': (176, 224, 230),                 #  rgb(176, 224, 230),
    'cadet blue': (95, 158, 160),                   #  rgb(95, 158, 160),
    'steel blue': (70, 130, 180),                   #  rgb(70, 130, 180)
    'corn flower blue': (100, 149, 237),            #  rgb(100, 149, 237),
    'deep sky blue': (0, 191, 255),                 #  rgb(0, 191, 255),
    'dodger blue': (30, 144, 255),                  #  rgb(30, 144, 255),
    'light blue': (173, 216, 230),                  #  rgb(173, 216, 230),
    'sky blue': (135, 206, 250),                    #  rgb(135, 206, 250),
    'midnight blue': (25, 25, 112),                 #  rgb(25, 25, 112),
    'navy': (0, 0, 128),                            #  rgb(0, 0, 128),
    'dark blue': (0, 0, 139),                       #  rgb(0, 0, 139),
    'medium blue': (0, 0, 205),                     #  rgb(0, 0, 205),
    'blue': (0, 0, 255),                            #  rgb(0, 0, 255),
    'royal blue': (65, 105, 225),                   #  rgb(65, 105, 225),
    'blue violet': (138, 43, 226),                  #  rgb(138, 43, 226),
    'indigo': (75, 0, 130),                         #  rgb(75, 0, 130),
    'dark slate blue': (72, 61, 139),               #  rgb(72, 61, 139),
    'slate blue': (106, 90, 205),                   #  rgb(106, 90, 205),
    'medium slate blue': (123, 104, 238),           #  rgb(123, 104, 238),
    'medium purple': (147, 112, 219),               #  rgb(147, 112, 219),
    'dark magenta': (139, 0, 139),                  #  rgb(139, 0, 139),
    'dark violet': (148, 0, 211),                   #  rgb(148, 0, 211),
    'dark orchid': (153, 50, 204),                  #  rgb(153, 50, 204),
    'medium orchid': (186, 85, 211),                #  rgb(186, 85, 211),
    'purple': (128, 0, 128),                        #  rgb(128, 0, 128),
    'thistle': (216, 191, 216),                     #  rgb(216, 191, 216),
    'plum': (221, 160, 221),                        #  rgb(221, 160, 221),
    'violet': (238, 130, 238),                      #  rgb(238, 130, 238),
    'magenta': (255, 0, 255),                       #  rgb(255, 0, 255),
    'orchid': (218, 112, 214),                      #  rgb(218, 112, 214),
    'medium violet red': (199, 21, 133),            #  rgb(199, 21, 133),
    'pale violet red': (219, 112, 147),             #  rgb(219, 112, 147),
    'deep pink': (255, 20, 147),                    #  rgb(255, 20, 147),
    'hot pink': (255, 105, 180),                    #  rgb(255, 105, 180),
    'light pink': (255, 182, 193),                  #  rgb(255, 182, 193),
    'pink': (255, 192, 203),                        #  rgb(255, 192, 203),
    'antique white': (250, 235, 215),               #  rgb(250, 235, 215),
    'beige': (245, 245, 220),                       #  rgb(245, 245, 220),
    'bisque': (255, 228, 196),                      #  rgb(255, 228, 196),
    'blanched almond': (255, 235, 205),             #  rgb(255, 235, 205),
    'wheat': (245, 222, 179),                       #  rgb(245, 222, 179),
    'corn silk': (255, 248, 220),                   #  rgb(255, 248, 220),
    'lemon chiffon': (255, 250, 205),               #  rgb(255, 250, 205),
    'light golden rod yellow': (250, 250, 210),     #  rgb(250, 250, 210),
    'light yellow': (255, 255, 224),                #  rgb(255, 255, 224),
    'saddle brown': (139, 69, 19),                  #  rgb(139, 69, 19),
    'sienna': (160, 82, 45),                        #  rgb(160, 82, 45),
    'chocolate': (210, 105, 30),                    #  rgb(210, 105, 30),
    'peru': (205, 133, 63),                         #  rgb(205, 133, 63),
    'sandy brown': (244, 164, 96),                  #  rgb(244, 164, 96),
    'burly wood': (222, 184, 135),                  #  rgb(222, 184, 135),
    'tan': (210, 180, 140),                         #  rgb(210, 180, 140),
    'rosy brown': (188, 143, 143),                  #  rgb(188, 143, 143),
    'moccasin': (255, 228, 181),                    #  rgb(255, 228, 181),
    'navajo white': (255, 222, 173),                #  rgb(255, 222, 173),
    'peach puff': (255, 218, 185),                  #  rgb(255, 218, 185),
    'misty rose': (255, 228, 225),                  #  rgb(255, 228, 225),
    'lavender blush': (255, 240, 245),              #  rgb(255, 240, 245),
    'linen': (250, 240, 230),                       #  rgb(250, 240, 230),
    'old lace': (253, 245, 230),                    #  rgb(253, 245, 230),
    'papaya whip': (255, 239, 213),                 #  rgb(255, 239, 213),
    'sea shell': (255, 245, 238),                   #  rgb(255, 245, 238),
    'mint cream': (245, 255, 250),                  #  rgb(245, 255, 250),
    'slate gray': (112, 128, 144),                  #  rgb(112, 128, 144),
    'light slate gray': (119, 136, 153),            #  rgb(119, 136, 153),
    'light steel blue': (176, 196, 222),            #  rgb(176, 196, 222),
    'lavender': (230, 230, 250),                    #  rgb(230, 230, 250),
    'floral white': (255, 250, 240),                #  rgb(255, 250, 240),
    'alice blue': (240, 248, 255),                  #  rgb(240, 248, 255),
    'ghost white': (248, 248, 255),                 #  rgb(248, 248, 255),
    'honeydew': (240, 255, 240),                    #  rgb(240, 255, 240),
    'ivory': (255, 255, 240),                       #  rgb(255, 255, 240),
    'azure': (240, 255, 255),                       #  rgb(240, 255, 255),
    'snow': (255, 250, 250),                        #  rgb(255, 250, 250),
    'black': (0, 0, 0),                             #  rgb(0, 0, 0),
    'charcoal': (75, 75, 75),                       #  rgb(75, 75, 75),
    'nero': (40, 40, 40),                           #  rgb(40, 40, 40),
    'wood bark': (38, 26, 26),                      #  rgb(38, 26, 26),
    'midnight express': (15, 15, 30),               #  rgb(15, 15, 30),
    'dark chocolate': (100, 65, 50),                #  rgb(100, 65, 50),
    'roman coffee': (120, 100, 85),                 #  rgb(120, 100, 85),
    'eclipse': (60, 60, 60),                        #  rgb(60, 60, 60),
    'dim gray': (105, 105, 105),                    #  rgb(105, 105, 105),
    'gray': (128, 128, 128),                        #  rgb(128, 128, 128),
    'dark gray': (169, 169, 169),                   #  rgb(169, 169, 169),
    'silver': (192, 192, 192),                      #  rgb(192, 192, 192),
    'light gray': (211, 211, 211),                  #  rgb(211, 211, 211),
    'gainsboro': (220, 220, 220),                   #  rgb(220, 220, 220),
    'white smoke': (245, 245, 245),                 #  rgb(245, 245, 245),
    'white': (255, 255, 255),                       #  rgb(255, 255, 255),
    }


class Colors:

    def __init__(self, color_dict: Dict[str, Color]) -> None:
        for k, v in color_dict.items():
            k = k.replace(" ", "_")
            self.__setattr__(k, v)


# Alright so it turns out that if an individual color channel's value is non-zero,
# it gets parsed as a string of length one. That means that I can easily manage the
# addition of extra characters for length parsing.
def set_color(
        fg: Optional[Tuple[int, int, int]] = None,
        bg: Optional[Tuple[int, int, int]] = None
    ) -> str:
    """Return the control codes used to change the text color."""
    string = ""
    if fg:
        string += f"{tcod.COLCTRL_FORE_RGB:c}{fg[0]:c}{fg[1]:c}{fg[2]:c}"
    if bg:
        string += f"{tcod.COLCTRL_BACK_RGB:c}{bg[0]:c}{bg[1]:c}{bg[2]:c}"
    return string

RESET = f"{tcod.COLCTRL_STOP:c}"
