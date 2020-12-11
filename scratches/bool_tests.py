

class Particle:
    
    def __init__(self, alive: bool):
        self.is_alive = alive
        
    def __bool__(self) -> bool:
        return self.is_alive
    
particles = [Particle(False), Particle(False), Particle(False)]
print(any(particles))