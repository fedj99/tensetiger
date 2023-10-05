import type { Answer, Word, WordFormKey } from "./words";

const gameConfig = {
    incorrectAnswerPenalty: 1,
    correctAnswerAward: 5,
    noParticipleAnswers: ["(no participle)", "(kein participle)", "(nothing)"],
};

export interface Mistake {
    expected: string;
    actual: string;
}
export interface Result {
    points: number;
    mistakes: Mistake[];
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
    const mistakes: Mistake[] = [];

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
            mistakes.push({ expected, actual });
        }
    }

    return { points, mistakes, hasMistakes: mistakes.length > 0 };
}
