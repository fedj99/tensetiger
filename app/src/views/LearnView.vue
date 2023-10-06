<script setup lang="ts">
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
// import Logo from "@/components/Logo.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import Score from "@/components/Score.vue";
import WordForm from "@/components/WordForm.vue";
import { gameConfig, getResult, type Result } from "@/game";
import { useGameStore } from "@/stores/game";
import { type Answer, type Word, type WordFormKey } from "@/words";
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCookies } from "vue3-cookies";

const LS_WORDS_KEY = "words";
const LS_WORD_COUNT_KEY = "word-count";
const LS_WORD_PROGRESS_KEY = "word-progress";
const LS_POINTS_KEY = "points";

const route = useRoute();
const router = useRouter();
const gameStore = useGameStore();

const loading = ref(true);
const error = ref(null);

const userName = ref<string>("");
const currentResult = ref<Result | undefined>(undefined);

watch([() => route.params], () => fetchWordList(), { immediate: true });

onMounted(() => {
    userName.value = useCookies().cookies.get("username");
    if (!userName.value) {
        alert("Please enter a username first");
        useRouter().push({ name: "login" });
    }
});

async function newRound() {
    try {
        loading.value = true;
        await gameStore.reset();
        loading.value = false;
    } catch (e: any) {
        error.value = e;
    }
}

function fetchWordList() {
    const cachedWords = localStorage.getItem(LS_WORDS_KEY);
    const cachedWordCount = localStorage.getItem(LS_WORD_COUNT_KEY);
    const cachedProgress = localStorage.getItem(LS_WORD_PROGRESS_KEY);
    const cachedPoints = localStorage.getItem(LS_POINTS_KEY);

    if (cachedWords && cachedWordCount && cachedProgress && cachedPoints) {
        const wordCount = parseInt(cachedWordCount);
        const progress = parseInt(cachedProgress);
        const words = JSON.parse(cachedWords);
        const points = parseInt(cachedPoints);

        if (progress < wordCount - 1) {
            // Resume game
            gameStore.resume(words, wordCount, progress, points);
        }
    }

    // Start a new round
    newRound();
}

function onSubmit(word: Word, shownKey: WordFormKey, answer: Answer) {
    // Compute points
    const result = getResult(word, shownKey, answer);
    console.log("Result:", result);
    gameStore.addPoints(result.points);

    // Set the result so the word widget shows the info
    currentResult.value = result;

    // if (result.hasMistakes) {
    //     const mistakeToString = (mistake: Mistake) => {
    //         if (mistake.actual.includes(",")) {
    //             return `Some of your answers ("${mistake.actual}") are not correct (should be one of "${mistake.expected}")`;
    //         } else if (mistake.expected.includes(",")) {
    //             return `Your answered "${mistake.actual}" which is not one of "${mistake.expected}"`;
    //         }
    //         return `Your answered "${mistake.actual}" but the correct answer is "${mistake.expected}"`;
    //     };

    //     const lines = ["You have some mistakes :(", "", ...result.mistakes.map(mistakeToString)];
    //     const text = lines.join("\n");
    //     alert(text);
    // }
}

function onNext() {
    // Hide result
    currentResult.value = undefined;

    if (gameStore.progress >= gameStore.wordCount - 1) {
        endRound();
    }

    // Get next word
    gameStore.next();
}

function onHintRevealed() {
    gameStore.deductPoints(gameConfig.hintRevealedPenalty);
}

function endRound() {
    // Post score and get score ID back
    // Then go to leaderboards with score ID, where all results are fetched
    const scoreId = 0;
    router.push({ name: "leaderboard", query: { username: userName.value, scoreId } });
}
</script>

<template>
    <Fullscreen>
        <Centered>
            <main class="main">
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
                    :word="gameStore.currentWord"
                    :shown-key="gameStore.shownKey"
                    :progress="gameStore.progress"
                    :word-count="gameStore.wordCount"
                    :result="currentResult"
                    @submit="onSubmit"
                    @reveal-hint="onHintRevealed"
                    @next="onNext"
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
