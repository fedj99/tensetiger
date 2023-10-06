import { getGameConfig, getWordList } from "@/api";
import { type GameConfig } from "@/game";
import { wordFormKeys, type Word, type WordFormKey } from "@/words";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const LS_WORDS_KEY = "words";
export const LS_WORD_COUNT_KEY = "word-count";
export const LS_WORD_PROGRESS_KEY = "word-progress";
export const LS_SCORE_KEY = "points";
export const LS_SHOWN_KEY = "shown-key";

export const useGameStore = defineStore("game", () => {
    const _config = ref<GameConfig>();
    const score = ref(0);
    const progress = ref(0);
    const wordCount = ref(0);
    const words = ref<Word[]>([]);
    const currentWord = computed(() => words.value[progress.value]);
    const shownKey = ref<WordFormKey>("form_infinitive");

    const config = computed(() => {
        if (_config.value == undefined) throw "Game config not loaded";
        return _config.value;
    });

    function next(shownKey_: WordFormKey | undefined = undefined) {
        progress.value++;
        if (shownKey_) shownKey.value = shownKey_;
        else shownKey.value = wordFormKeys[Math.floor(Math.random() * wordFormKeys.length)];
    }

    async function reset() {
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

        const res = await getWordList();
        words.value = res.data;
        wordCount.value = words.value.length;
        progress.value = -1;
        score.value = 0;
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

    function addPoints(points: number) {
        score.value += points;
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
        next,
        reset,
        resume,
        addPoints,
        deductPoints,
        fetchGameConfig,
    };
});
