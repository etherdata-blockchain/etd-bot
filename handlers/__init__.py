from .help_handler import help_handler
from .stats_handler import stats_handler
from .image_handler import image_handler
from .devices_handler import device_handler
from .balance_handler import balance_handler

HANDLERS = [
    help_handler,
    image_handler,
    stats_handler,
    help_handler,
    balance_handler,
    device_handler
]
