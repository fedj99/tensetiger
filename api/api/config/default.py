import os

APP_NAME = "tensetiger-default"
MIGRATIONS_DIR = "migrations"
FRONTEND_ROOT = "frontend"
GAME_CONFIG = {
    "wordCount": 10,
    "incorrectAnswerPenalty": 1,
    "correctAnswerAward": 5,
    "noParticipleAnswers": [
        "(no participle)",
        "(kein participle)",
        "(no simple past)",
        "(kein simple past)",
        "(nothing)",
    ],
    "hintRevealedPenalty": 3,
    "streakCheckpoints": [
        {"streak": 4, "points": 5},
        {"streak": 6, "points": 10},
        {"streak": 8, "points": 15},
        {"streak": 10, "points": 30},
    ],
}
