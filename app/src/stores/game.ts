import { getGameConfig, getWordList } from "@/api";
import { defaultGameConfig, type GameConfig, type Result } from "@/game";
import { wordFormKeys, type Word, type WordFormKey } from "@/words";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const LS_WORDS_KEY = "words";
export const LS_WORD_COUNT_KEY = "word-count";
export const LS_WORD_PROGRESS_KEY = "word-progress";
export const LS_SCORE_KEY = "score";
export const LS_SHOWN_KEY = "shown-key";

export const useGameStore = defineStore("game", () => {
    const _config = ref<GameConfig>();
    const score = ref(0);
    const progress = ref(0);
    const wordCount = ref(0);
    const words = ref<Word[]>([]);
    const currentWord = computed(() => words.value[Math.min(progress.value, wordCount.value - 1)]); // Never go over boundaries
    const shownKey = ref<WordFormKey>("form_infinitive");
    const streak = ref<number>(0);
    const currentStreakBonus = computed(() =>
        Math.max(
            0, // In case there is no streak, return 0 (all checkpoints will be higher)
            ...config.value.streakCheckpoints
                .filter((x) => streak.value >= x.streak)
                .map((x) => x.points)
        )
    );
    const config = computed(() => {
        return _config.value || defaultGameConfig;
    });

    function next(shownKey_: WordFormKey | undefined = undefined) {
        progress.value++;
        if (shownKey_) shownKey.value = shownKey_;
        else shownKey.value = wordFormKeys[Math.floor(Math.random() * wordFormKeys.length)];
    }

    async function clearCache() {
        console.log("Clearing cached game...");
        // Clear the cache
        for (const key of [
            LS_SCORE_KEY,
            LS_SHOWN_KEY,
            LS_WORDS_KEY,
            LS_WORD_COUNT_KEY,
            LS_WORD_PROGRESS_KEY,
        ]) {
            localStorage.removeItem(key);
        }
    }

    async function reset() {
        clearCache();

        const res = await getWordList();
        words.value = res.data;
        wordCount.value = words.value.length;
        progress.value = -1;
        score.value = 0;
        streak.value = 0;
        // Set random shown value
        next();
    }

    function resume(
        words_: Word[],
        wordCount_: number,
        progress_: number,
        score_: number,
        shownKey_: WordFormKey
    ) {
        // Simply resume round
        words.value = words_;
        wordCount.value = wordCount_;
        progress.value = progress_ - 1;
        score.value = score_;
        shownKey.value = shownKey_;
        // Set random shown value
        next(shownKey_);
    }

    function addPoints(result: Result) {
        score.value += result.points;
        // Increase streak by default
        streak.value++;
        // Check if streak has ended. A streak ends either when the user makes a mistake or the last
        // round is played (i.e. there are no more rounds)
        if (result.hasMistakes || progress.value >= wordCount.value - 1) {
            // Streak bonus is only applied at end of streak, calculate bonus based on streak
            console.log("Awarding streak bonus:", currentStreakBonus.value);
            score.value += currentStreakBonus.value;

            // Reset streak if necessary
            if (result.hasMistakes) {
                console.log("Resetting streak");
                streak.value = 0;
            }
        }
    }

    function deductPoints(points: number) {
        score.value -= points;
    }

    async function fetchGameConfig() {
        const res = await getGameConfig();
        _config.value = res.data;
        return _config.value;
    }

    return {
        config,
        score,
        progress,
        wordCount,
        words,
        currentWord,
        shownKey,
        streak,
        currentStreakBonus,
        next,
        reset,
        clearCache,
        resume,
        addPoints,
        deductPoints,
        fetchGameConfig,
    };
});
