from attrdict import AttrDict

Config = AttrDict({
    'game': {
        'caption': 'Sound',
        'width': 800,
        'height': 600,
        'cell_size': 10,
        'fps': 40,
        'epsilon': 0.01
    },
    'box': {
        'x_low': 20,
        'x_high': 780,
        'y_low': 20,
        'y_high': 580,
    },
    'particle': {
        'color': (255, 255, 255),
        'r': 2,
        'v_max': 10
    },
    'simulation': {
        'num_particles': 1000
    },
    'debug': 0
})
