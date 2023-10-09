from .default import GAME_CONFIG

APP_NAME = "b3-dev"
DB_HOST = "localhost"
DB_USER = "b3_dev"
DB_DATABASE = "b3_dev"

GAME_CONFIG.update(
    {
        "wordCount": 4,
        "streakCheckpoints": [
            {"streak": 1, "points": 5},
            {"streak": 2, "points": 12},
            {"streak": 3, "points": 20},
            {"streak": 4, "points": 30},
        ],
    }
)
