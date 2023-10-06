from . import add_prefix

APP_NAME = "b3-default"
MIGRATIONS_DIR = add_prefix("migrations")
FRONTEND_ROOT = add_prefix("frontend")
GAME_CONFIG = {
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
}
