from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import timeit
from random import uniform
from matplotlib import pyplot as plt
from matplotlib import animation


class Particle:
    
    def __init__(self, x, y, ang_speed):
        self.x = x
        self.y = y
        self.ang_speed = ang_speed


class ParticleSimulator:
    
    def __init__(self, particles) -> None:
        self.particles = particles
    
    def evolve(self, dt):
        timestep = 0.00001
        nsteps = int(dt / timestep)
        
        r_i = np.array([[p.x, p.y] for p in self.particles])
        ang_speed_i = np.array([p.ang_speed for p in self.particles])
        
        for step in range(nsteps):
            for particle in self.particles:
                norm = np.sqrt((r_i ** 2).sum(axis=1))
                
                v_i = r_i[:, [1, 0]]
                v_i[:, 0] *= -1
                v_i /= norm[:, np.newaxis]
                
                d_i = timestep * ang_speed_i[:, np.newaxis] * v_i
                r_i += d_i
            
            for i, p in enumerate(self.particles):
                p.x, p.y = r_i[i]


def visualize(simulator: ParticleSimulator):
    X = [particle.x for particle in simulator.particles]
    Y = [particle.y for particle in simulator.particles]
    
    fig = plt.figure()
    ax = plt.subplot(111, aspect='equal')
    line, = ax.plot(X, Y, 'ro')
    
    # Axis limits
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    
    def init():
        line.set_data([], [])
        return line,
    
    def animate(i):
        simulator.evolve(0.01)
        X = [particle.x for particle in simulator.particles]
        Y = [particle.y for particle in simulator.particles]
        line.set_data(X, Y)
        return line,
    
    anim = animation.FuncAnimation(
        fig, animate, init_func=init, blit=True, interval=10
        )
    
    plt.show()
    

def run_visualization():
    particles = [Particle(uniform(-1.0, 1.0),
                          uniform(-1.0, 1.0),
                          uniform(-1.0, 1.0))
                 for i in range(10)]
    simulator = ParticleSimulator(particles)
    visualize(simulator)


import fileinput
import cProfile

def profile():
    pr = cProfile.Profile()
    pr.enable()
    for line in fileinput.input():
        for i in range(10):
            y = int(line.strip()) + int(line.strip())
    pr.disable()
    pr.print_stats(sort='time')


if __name__ == '__main__':
    result = timeit.timeit('run_visualization()', setup='from __main__ import run_visualization', number=1)
    profile()