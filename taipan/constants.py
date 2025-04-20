# Game constants
DEBUG = True

# Battle constants
GENERIC = 1
LI_YUEN = 2

BATTLE_NOT_FINISHED = 0
BATTLE_WON = 1
BATTLE_INTERRUPTED = 2
BATTLE_FLED = 3
BATTLE_LOST = 4

# Input constants
BACKSPACE = 8
DELETE = 127
ESCAPE = 27
NEWLINE = 10

# Animation and timing constants
ANIMATION_PAUSE = 0.1
M_PAUSE = 3000  # Medium pause (3 seconds)
L_PAUSE = 5000  # Long pause (5 seconds)

if DEBUG:
    M_PAUSE = 500
    L_PAUSE = 1000
    ANIMATION_PAUSE = 0.1

# Game state constants
STARTING_YEAR = 1860
STARTING_MONTH = 1
STARTING_PORT = 1

# Ship constants
STARTING_CAPACITY = 60
STARTING_HOLD = 0
STARTING_GUNS = 0
STARTING_DAMAGE = 0

# Financial constants
STARTING_CASH = 0
STARTING_BANK = 0
STARTING_DEBT = 0
STARTING_BOOTY = 0

# Combat constants
BASE_ENEMY_HEALTH = 20.0
BASE_ENEMY_DAMAGE = 0.5

# Warehouse constants
MAX_WAREHOUSE_CAPACITY = 10000

# Item indices
OPIUM = 0
SILK = 1
ARMS = 2
GENERAL = 3

# Port indices
AT_SEA = 0
HONG_KONG = 1
SHANGHAI = 2
NAGASAKI = 3
SAIGON = 4
MANILA = 5
SINGAPORE = 6
BATAVIA = 7

# Status text indices
CRITICAL = 0
POOR = 1
FAIR = 2
GOOD = 3
PRIME = 4
PERFECT = 5

status_texts = ["Critical", "  Poor", "  Fair", "  Good", " Prime", "Perfect"]

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
