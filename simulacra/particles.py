from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
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
        nsteps = int(dt/timestep)
        for step in range(nsteps):
            for particle in self.particles:
                # 1. Calculate the particle's direction
                norm = (particle.x ** 2 + particle.y ** 2) ** 0.5
                vx = (-particle.y) / norm
                vy = particle.x / norm
                
                # 2. Calculate the displacement
                dx = timestep * particle.ang_speed * vx
                dy = timestep * particle.ang_speed * vy
                particle.x += dx
                particle.y += dy
                
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
        X = [particle.x for particle in simulator.particles]
        Y = [particle.y for particle in simulator.particles]
    
        line.set_data(X, Y)
        return line,
    
    anim = animation.FuncAnimation(
        fig, animate, init_func=init, blit=True, interval=10
        )
    
    plt.show()
    

def run_visualization():
    particles = [Particle( 0.3,  0.5, +1 ),
                 Particle( 0.0, -0.5, -1 ),
                 Particle(-0.1, -0.4, +3 )]
    simulator = ParticleSimulator(particles)
    while True:
        visualize(simulator)

run_visualization()