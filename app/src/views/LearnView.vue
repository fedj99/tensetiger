<script setup lang="ts">
import { postScore } from "@/api";
import AxiosErrorWidget from "@/components/AxiosErrorWidget.vue";
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
// import Logo from "@/components/Logo.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import Score from "@/components/Score.vue";
import WordForm from "@/components/WordForm.vue";
import { getResult, type Result } from "@/game";
import {
    LS_SCORE_KEY,
    LS_SHOWN_KEY,
    LS_WORD_COUNT_KEY,
    LS_WORD_PROGRESS_KEY,
    LS_WORDS_KEY,
    useGameStore,
} from "@/stores/game";
import { type Answer, type Word, type WordFormKey } from "@/words";
import { nextTick, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCookies } from "vue3-cookies";

const route = useRoute();
const router = useRouter();
const gameStore = useGameStore();

const loading = ref(true);
const error = ref(null);

const userName = ref<string>("");
const userId = ref<number>(-1);
const currentResult = ref<Result | undefined>(undefined);
const wordFormRef = ref<InstanceType<typeof WordForm> | null>(null);

// Watch when route changes, then get a new (or cached word list)
watch([() => route.params], () => loadOrFetchWordList(), { immediate: true });

// Watch parameters and persist to resume later
watch(
    [
        () => gameStore.words,
        () => gameStore.wordCount,
        () => gameStore.progress,
        () => gameStore.score,
        () => gameStore.shownKey,
    ],
    ([words, wordCount, progress, score, shownKey]) =>
        saveProgress(words, wordCount, progress, score, shownKey)
);

// Get current logged in user
onMounted(() => {
    const { cookies } = useCookies();
    userName.value = decodeURI(cookies.get("username"));
    userId.value = parseInt(decodeURI(cookies.get("user_id")));
    if (userName.value == "null") {
        alert("Please enter a username first");
        useRouter().push({ name: "login" });
    }
});

// Game methods
async function newRound() {
    try {
        // Get new list of words from API
        console.log("Fetching a fresh round");
        loading.value = true;
        await Promise.all([gameStore.reset(), gameStore.fetchGameConfig()]);
        // Watchers automatically save value
    } catch (e: any) {
        error.value = e;
    } finally {
        loading.value = false;
    }
}

async function resumeFromCache(
    words: string,
    wordCount: string,
    progress: string,
    score: string,
    shownKey: string
) {
    try {
        console.log(
            "Resuming game from cache, fetching game config",
            words,
            wordCount,
            progress,
            score,
            shownKey
        );
        loading.value = true;
        const _wordCount = parseInt(wordCount);
        const _progress = parseInt(progress);
        const _words = JSON.parse(words);
        const _score = parseInt(score);
        const _shownKey = shownKey as WordFormKey;

        // Load game config
        await gameStore.fetchGameConfig();

        // Resume game (needs to be done in any case to set state variables)
        gameStore.resume(_words, _wordCount, _progress, _score, _shownKey);
        // If already done, finish this round (and post the score)
        if (_progress >= _wordCount) {
            // Game was already over (?)
            endRound();
        }
    } catch (e: any) {
        error.value = e;
    } finally {
        loading.value = false;
    }
}

function loadOrFetchWordList() {
    // Check local storage first
    const cachedWords = localStorage.getItem(LS_WORDS_KEY);
    const cachedWordCount = localStorage.getItem(LS_WORD_COUNT_KEY);
    const cachedProgress = localStorage.getItem(LS_WORD_PROGRESS_KEY);
    const cachedPoints = localStorage.getItem(LS_SCORE_KEY);
    const cachedShownKey = localStorage.getItem(LS_SHOWN_KEY);

    // Load from local storage
    if (cachedWords && cachedWordCount && cachedProgress && cachedPoints && cachedShownKey) {
        resumeFromCache(cachedWords, cachedWordCount, cachedProgress, cachedPoints, cachedShownKey);
    } else {
        // Not cached, start a new round
        newRound();
    }

    nextTick(() => {
        setTimeout(() => {
            wordFormRef.value?.focusFirst();
            console.log("Round started");
        }, 200);
    });
}

function saveProgress(
    words: Word[],
    wordCount: number,
    progress: number,
    score: number,
    shownKey: WordFormKey
) {
    console.log("Saving progress");
    localStorage.setItem(LS_WORDS_KEY, JSON.stringify(words));
    localStorage.setItem(LS_WORD_COUNT_KEY, wordCount.toString());
    localStorage.setItem(LS_WORD_PROGRESS_KEY, progress.toString());
    localStorage.setItem(LS_SCORE_KEY, score.toString());
    localStorage.setItem(LS_SHOWN_KEY, shownKey);
}

async function endRound() {
    try {
        console.log("Ending round. Points achieved:", gameStore.score);
        // Post score and get score ID back
        loading.value = true;
        const res = await postScore(userId.value, userName.value, gameStore.score);
        // When the score has been posted, it's safe to delete
        gameStore.clearCache();
        // Then go to leaderboards with score ID, where all results are fetched
        router.push({
            name: "leaderboard",
            query: { user: userName.value, score_id: res.data.score_id.toString() },
        });
    } catch (e: any) {
        error.value = e;
    } finally {
        loading.value = false;
    }
}

// Button handlers
function onSubmit(word: Word, shownKey: WordFormKey, answer: Answer) {
    console.log("Submit", shownKey, answer);
    // Compute points
    const result = getResult(gameStore.config, word, shownKey, answer);
    gameStore.addPoints(result.points);

    // Set the result so the word widget shows the info
    currentResult.value = result;

    // Get next word
    gameStore.next();
}

function onNext() {
    console.log("Next");
    // Hide result
    currentResult.value = undefined;

    if (gameStore.progress >= gameStore.wordCount) {
        endRound();
    }

    // Focus input
    wordFormRef.value?.focusFirst();
}

function onHintRevealed() {
    gameStore.deductPoints(gameStore.config.hintRevealedPenalty);
}
</script>

<template>
    <Fullscreen>
        <Centered>
            <main v-if="loading && !error">Loading...</main>
            <main v-else-if="error">
                <AxiosErrorWidget :error="error"></AxiosErrorWidget>
            </main>
            <main v-else class="main">
                <div class="player">
                    <span>
                        You are playing as: <strong>{{ userName }}</strong>
                    </span>
                    <RouterLink
                        :to="{ name: 'home' }"
                        class="button"
                        style="margin-left: 10px; font-size: var(--font-size-small)"
                        >Change
                    </RouterLink>
                </div>

                <Score :score="gameStore.score"></Score>
                <!-- <Logo></Logo> -->

                <ProgressBar
                    :total="gameStore.wordCount"
                    :progress="gameStore.progress"
                ></ProgressBar>

                <hr />

                <WordForm
                    :game-config="gameStore.config"
                    :word="gameStore.currentWord"
                    :shown-key="gameStore.shownKey"
                    :progress="gameStore.progress"
                    :word-count="gameStore.wordCount"
                    :result="currentResult"
                    @submit="onSubmit"
                    @reveal-hint="onHintRevealed"
                    @next="onNext"
                    ref="wordFormRef"
                ></WordForm>

                <hr />

                <div class="par">
                    <strong>Fill in the missing verb forms!</strong>
                    <ul class="rules">
                        <li>If there are multiple correct verb forms, choose one.</li>
                        <li>If a verb form does not exist, write <code>(nothing)</code>.</li>
                        <li>You will lose points if you answer incorrectly!</li>
                    </ul>
                </div>
            </main>
        </Centered>
    </Fullscreen>
</template>

<style lang="scss" scoped="">
@import "@/assets/components.scss";

.main {
    width: min(90vw, 50em);
}

.par {
    max-width: max-content;
    margin: auto;
}

.rules {
    list-style: "👉🏿";
    line-height: 1.5em;

    &:is(ul) li {
        padding-left: 0.5em;
    }
}

.player {
    font-size: var(--font-size-large);
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
