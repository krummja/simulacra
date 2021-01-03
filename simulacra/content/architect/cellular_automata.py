from __future__ import annotations

import numpy as np
from numpy.fft import fft2, ifft2


def fft_convolve2d(board, kernel):
    board_ft = fft2(board)
    kernel_ft = fft2(kernel)
    height, width = board_ft.shape

    convolution = np.real(ifft2(board_ft * kernel_ft))
    convolution = np.roll(convolution, -(int(height / 2) + 1), axis=0)
    convolution = np.roll(convolution, -(int(width / 2) + 1), axis=1)
    return convolution.round()


class Automata:

    def __init__(self, shape, density, neighborhood, rule) -> None:
        self.board = np.random.uniform(0, 1, shape)
        self.board = self.board < density

        n_height, n_width = neighborhood.shape
        self.kernel = np.zeros(shape)
        self.kernel[(shape[0] - n_height - 1) // 2 : (shape[0] + n_height) // 2,
                    (shape[1] - n_width - 1) // 2 : (shape[1] + n_width) // 2] = neighborhood

        self.rule = rule

    def update_board(self, intervals=1):
        for _ in range(intervals):
            convolution = fft_convolve2d(self.board, self.kernel)
            shape = convolution.shape
            new_board = np.zeros(shape, dtype=np.int)
            new_board[np.where(np.in1d(convolution, self.rule[0]).reshape(shape) \
                               & (self.board == 1))] = 1
            new_board[np.where(np.in1d(convolution, self.rule[1]).reshape(shape) \
                               & (self.board == 0))] = 1
            self.board = new_board

    def generate(self, iterations):
        self.update_board(iterations)


class Conway(Automata):
    def __init__(self, shape, density):
        neighborhood = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        rule = [[2, 3], [3]]
        Automata.__init__(self, shape, density, neighborhood, rule)


class Life34(Automata):
    def __init__(self, shape, density):
        neighborhood = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        rule = [[3, 4], [3, 4]]
        Automata.__init__(self, shape, density, neighborhood, rule)


class Amoeba(Automata):
    def __init__(self, shape, density):
        neighborhood = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        rule = [[1, 3, 5, 8], [3, 5, 7]]
        Automata.__init__(self, shape, density, neighborhood, rule)


class Anneal(Automata):
    def __init__(self, shape, density):
        neighborhood = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        rule = [[3, 5, 6, 7, 8],
                [4, 6, 7, 8]]
        Automata.__init__(self, shape, density, neighborhood, rule)


class Bugs(Automata):
    def __init__(self, shape, density):
        neighborhood = np.ones((11, 11))
        rule = [np.arange(34, 59), np.arange(34, 46)]
        Automata.__init__(self, shape, density, neighborhood, rule)
