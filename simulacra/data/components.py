from components.physics import Physics
from components.inventory import Inventory


test_container = {
    'PHYSICS': {'weight': 10.0, 'size': 'average'},
    'INVENTORY': {}
}


component_templates = {
    'PHYSICS': Physics,
    'INVENTORY': Inventory,
    'test_container': test_container
}