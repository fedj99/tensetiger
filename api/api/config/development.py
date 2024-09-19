from .default import GAME_CONFIG

APP_NAME = "tensetiger-dev"
DB_HOST = "postgres"
DB_USER = "tensetiger_dev"
DB_DATABASE = "tensetiger_dev"

GAME_CONFIG.update(
    {
        "wordCount": 4,
        "streakCheckpoints": [
            {"streak": 1, "points": 5},
            {"streak": 2, "points": 12},
            {"streak": 3, "points": 20},
            {"streak": 4, "points": 30},
        ],
        "minTimeBonusSeconds": 45,
        "maxTimeBonusSeconds": 15,
    }
)
