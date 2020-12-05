import timeit

if __name__ == '__main__':
    result = timeit.repeat('run_visualization()',
                           setup='from particle_tests import run_visualization',
                           number=1, 
                           repeat=1)