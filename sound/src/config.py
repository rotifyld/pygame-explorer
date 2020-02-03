from attrdict import AttrDict

Config = AttrDict({
    'game': {
        'caption': 'Sound',
        'height': 600,
        'width': 800,
        'cell_size': 10,
        'fps': 40,
        'epsilon': 0.01
    },
    'box': {
        'width': 800,
        'height': 600
    },
    'particle': {
        'color': (255, 255, 255),
        'r': 4,
        'v_max': 5
    },
    'simulation': {
        'num_particles': 10
    }
})
