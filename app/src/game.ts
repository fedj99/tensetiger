import type { Answer, Word, WordFormKey } from "./words";

export interface StreakCheckpoint {
    streak: number;
    points: number;
}

export interface GameConfig {
    wordCount: number;
    incorrectAnswerPenalty: number;
    correctAnswerAward: number;
    noParticipleAnswers: string[];
    hintRevealedPenalty: number;
    streakCheckpoints: StreakCheckpoint[];
}

export const defaultGameConfig: GameConfig = {
    wordCount: -1,
    incorrectAnswerPenalty: 0,
    correctAnswerAward: 0,
    noParticipleAnswers: [],
    hintRevealedPenalty: 0,
    streakCheckpoints: [],
};

export interface Mistake {
    expected: string;
    actual: string;
}
export type Mistakes = {
    [key in WordFormKey]: Mistake | undefined;
};
export interface Result {
    points: number;
    word: Word;
    mistakes: Mistakes;
    hasMistakes: boolean;
}

export interface Score {
    id: number;
    date: string;
    user_id: number;
    username: string;
    score: number;
}

export function isCorrect(gc: GameConfig, expected: string, actual: string) {
    const normalize = (str: string) => str.trim().toLowerCase();
    const separate = (str: string) => str.split(",");

    if (gc.noParticipleAnswers.includes(normalize(expected))) {
        // No participle, decide what should be correct
        const actualNormalized = normalize(actual);
        return gc.noParticipleAnswers.includes(actualNormalized);
    }

    const choices = separate(expected).map(normalize);

    if (actual.includes(",")) {
        // Multiple answers
        const given = separate(actual).map(normalize);
        for (const ans of given) {
            if (!choices.includes(ans)) return false;
        }
        return true;
    } else {
        const actualNormalized = actual.trim().toLowerCase();
        return choices.includes(actualNormalized);
    }
}

export function getResult(
    gc: GameConfig,
    word: Word,
    shownKey: WordFormKey,
    answer: Answer
): Result {
    let points = 0;
    let hasMistakes = false;
    const mistakes: Mistakes = {
        form_infinitive: undefined,
        form_simple_past: undefined,
        form_past_participle: undefined,
    };

    for (const key_ in answer) {
        const key = key_ as WordFormKey;
        if (key == shownKey) continue;
        const expected = word[key];
        const actual = answer[key];
        if (isCorrect(gc, expected, actual)) {
            // Correct answer
            points += word.difficulty * gc.correctAnswerAward;
        } else {
            // Wrong answer
            points -= gc.incorrectAnswerPenalty;
            mistakes[key] = { expected, actual };
            hasMistakes = true;
        }
    }

    return { points, word, mistakes, hasMistakes };
}
