import type { Answer, Word, WordFormKey } from "./words";

export const gameConfig = {
    incorrectAnswerPenalty: 1,
    correctAnswerAward: 5,
    noParticipleAnswers: ["(no participle)", "(kein participle)", "(nothing)"],
    hintRevealedPenalty: 3,
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

export function isCorrect(expected: string, actual: string) {
    const normalize = (str: string) => str.trim().toLowerCase();
    const separate = (str: string) => str.split(",");

    if (gameConfig.noParticipleAnswers.includes(normalize(expected))) {
        // No participle, decide what should be correct
        const actualNormalized = normalize(actual);
        return gameConfig.noParticipleAnswers.includes(actualNormalized);
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

export function getResult(word: Word, shownKey: WordFormKey, answer: Answer): Result {
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
        if (isCorrect(expected, actual)) {
            // Correct answer
            points += word.difficulty * gameConfig.correctAnswerAward;
        } else {
            // Wrong answer
            points -= gameConfig.incorrectAnswerPenalty;
            mistakes[key] = { expected, actual };
            hasMistakes = true;
        }
    }

    return { points, word, mistakes, hasMistakes };
}
