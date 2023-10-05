import type { Answer, Word, WordFormKey } from "./words";

const gameConfig = {
    incorrectAnswerPenalty: 0,
    correctAnswerAward: 5,
};

export function getPointsFor(word: Word, shownKey: WordFormKey, answer: Answer): number {
    let sum = 0;

    for (const key_ in answer) {
        const key = key_ as WordFormKey;
        if (key == shownKey) continue;
        if (word[key] != answer[key]) {
            // Wrong answer
            sum -= gameConfig.incorrectAnswerPenalty;
        } else {
            // Correct answer
            sum += word.difficulty * gameConfig.correctAnswerAward;
        }
    }

    return sum;
}
