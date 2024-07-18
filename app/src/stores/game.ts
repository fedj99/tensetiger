import { getGameConfig, getWordList } from "@/api";
import { invlerp, lerp } from "@/math";
import { defaultGameConfig, type GameConfig, type Result } from "@/rules";
import { wordFormKeys, type Word, type WordFormKey } from "@/words";
import { DateTime } from "luxon";
import { defineStore } from "pinia";
import { computed, ref, watch } from "vue";

export const LS_GAME_STATE_KEY = "game-state";

export interface GameState {
    words: Word[];
    wordCount: number;
    progress: number;
    score: number;
    streak: number;
    shownKey: WordFormKey;
    hintRevealed: boolean;
    startTime: string;
    elapsedSeconds: number;
    endTime: string | undefined;
}

export const useGameStore = defineStore("game", () => {
    const _config = ref<GameConfig>();
    const score = ref(0);
    const progress = ref(0);
    const wordCount = ref(0);
    const words = ref<Word[]>([]);
    const currentWord = computed(() => words.value[Math.min(progress.value, wordCount.value - 1)]); // Never go over boundaries
    const shownKey = ref<WordFormKey>("form_infinitive");
    const hintRevealed = ref<boolean>(false);
    const streak = ref<number>(0);
    const startTime = ref<DateTime>(DateTime.now());
    const endTime = ref<DateTime>();
    const elapsedSeconds = ref<number>(0);

    const config = computed(() => {
        return _config.value || defaultGameConfig;
    });
    const currentStreakBonus = computed(() =>
        Math.max(
            0, // In case there is no streak, return 0 (all checkpoints will be higher)
            ...config.value.streakCheckpoints
                .filter((x) => streak.value >= x.streak)
                .map((x) => x.points)
        )
    );
    const currentTimeBonus = computed(() => {
        if (!startTime.value) return 0;

        // Find the fraction between max and min time, with 1.0 being min time and 0.0 being max time
        const { minTimeBonusSeconds: minSeconds, maxTimeBonusSeconds: maxSeconds } = config.value;
        const frac = 1 - invlerp(minSeconds, maxSeconds, elapsedSeconds.value);
        console.log("frac", frac);

        // Compute the bonus points
        const { minTimeBonusPoints: minPoints, maxTimeBonusPoints: maxPoints } = config.value;
        const bonusPoints = Math.round(lerp(minPoints, maxPoints, frac));

        return bonusPoints;
    });

    // Set up a watcher function to save the state when it changes
    watch([words, wordCount, progress, score, streak, shownKey, hintRevealed], () => saveState());

    let counterHandle: number | undefined = undefined;

    function next() {
        progress.value++;
        shownKey.value = wordFormKeys[Math.floor(Math.random() * wordFormKeys.length)];
        hintRevealed.value = false;
    }

    function clearCache() {
        console.log("Clearing cached game...");
        // Clear the cache
        localStorage.removeItem(LS_GAME_STATE_KEY);
    }

    function startCounter() {
        stopCounter();
        counterHandle = setInterval(handleCounterUpdate, 1000);
    }

    function stopCounter() {
        if (counterHandle != undefined) {
            clearInterval(counterHandle);
        }
    }

    function hasSavedGameState() {
        return localStorage.getItem(LS_GAME_STATE_KEY) != undefined;
    }

    function saveState() {
        const state: GameState = {
            words: words.value,
            wordCount: wordCount.value,
            progress: progress.value,
            score: score.value,
            streak: streak.value,
            shownKey: shownKey.value,
            hintRevealed: hintRevealed.value,
            startTime: startTime.value.toISO() || "undefined",
            elapsedSeconds: elapsedSeconds.value,
            endTime: endTime.value?.toISO() || undefined,
        };
        console.log("Saving game state");
        localStorage.setItem(LS_GAME_STATE_KEY, JSON.stringify(state));
    }

    function loadState() {
        const cacheItem = localStorage.getItem(LS_GAME_STATE_KEY);
        if (!cacheItem) return false;

        const state: GameState = JSON.parse(cacheItem);
        console.log("Loading game state:", state);

        words.value = state.words;
        wordCount.value = state.wordCount;
        progress.value = state.progress;
        score.value = state.score;
        streak.value = state.streak;
        shownKey.value = state.shownKey;
        hintRevealed.value = state.hintRevealed;
        startTime.value = DateTime.fromISO(state.startTime);
        endTime.value = state.endTime ? DateTime.fromISO(state.endTime) : undefined;
        elapsedSeconds.value = state.elapsedSeconds;

        return true;
    }

    async function reset() {
        clearCache();

        const res = await getWordList();
        words.value = res.data;
        wordCount.value = words.value.length;
        progress.value = -1;
        score.value = 0;
        streak.value = 0;
        startTime.value = DateTime.now();
        endTime.value = undefined;

        // Set random shown value
        next();

        handleCounterUpdate();
        startCounter();
    }

    function resume() {
        startCounter();
    }

    function addPoints(result: Result) {
        score.value += result.points;
        // Increase streak by default
        streak.value++;
        // Check if streak has ended. A streak ends either when the user makes a mistake or the last
        // round is played (i.e. there are no more rounds)
        if (result.hasMistakes) {
            // Streak bonus is only applied at end of streak, calculate bonus based on streak
            console.log("Awarding streak bonus:", currentStreakBonus.value);
            score.value += currentStreakBonus.value;

            // Reset streak
            console.log("Resetting streak");
            streak.value = 0;
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

    function finish() {
        // If there currently still is a streak, award the points
        console.log("current time bonus", currentTimeBonus.value);
        score.value += currentStreakBonus.value;
        score.value += currentTimeBonus.value;

        stopCounter();
    }

    function handleCounterUpdate() {
        if (!startTime.value) {
            elapsedSeconds.value = 0;
        } else {
            // Get the number of seconds passed since beginning
            elapsedSeconds.value = Math.round(
                DateTime.now().diff(startTime.value, "seconds").seconds
            );
        }
    }

    return {
        config,
        score,
        progress,
        wordCount,
        words,
        currentWord,
        shownKey,
        hintRevealed,
        startTime,
        endTime,
        elapsedSeconds,
        streak,
        currentStreakBonus,
        currentTimeBonus,
        hasSavedGameState,
        next,
        reset,
        clearCache,
        resume,
        addPoints,
        deductPoints,
        fetchGameConfig,
        finish,
        loadState,
        saveState,
    };
});
