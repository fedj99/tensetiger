import { getWordList } from "@/api";
import { wordFormKeys, type Word, type WordFormKey } from "@/words";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useGameStore = defineStore("game", () => {
    const score = ref(0);
    const progress = ref(0);
    const wordCount = ref(0);
    const words = ref<Word[]>([]);
    const currentWord = computed(() => words.value[progress.value]);
    const shownKey = ref<WordFormKey>("form_infinitive");

    function next() {
        progress.value++;
        shownKey.value = wordFormKeys[Math.floor(Math.random() * wordFormKeys.length)];
    }

    async function reset() {
        const res = await getWordList();
        words.value = res.data;
        wordCount.value = words.value.length;
        progress.value = -1;
        score.value = 0;
        // Set random shown value
        next();
    }

    function resume(words_: Word[], wordCount_: number, progress_: number, points_: number) {
        // Simply resume round
        words.value = words_;
        wordCount.value = wordCount_;
        progress.value = progress_ - 1;
        score.value = points_;
        // Set random shown value
        next();
    }

    function addPoints(points: number) {
        score.value += points;
    }

    function deductPoints(points: number) {
        score.value -= points;
    }

    return {
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
    };
});
