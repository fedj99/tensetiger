<script setup lang="ts">
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import Logo from "@/components/Logo.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import WordForm from "@/components/WordForm.vue";
import { getPointsFor } from "@/game";
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
    const points = getPointsFor(word, shownKey, answer);
    gameStore.addPoints(points);

    if (gameStore.progress >= gameStore.wordCount - 1) {
        endRound();
    }

    // Get next word
    gameStore.next();
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

                <Logo></Logo>

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
                    @submit="onSubmit"
                ></WordForm>

                <p>
                    Fill in the missing verb forms! If there are multiple correct forms, choose one.
                </p>
            </main>
        </Centered>
    </Fullscreen>
</template>

<style lang="scss" scoped="">
@import "@/assets/components.scss";

.main {
    width: min(90vw, 50em);
}

.player {
    font-size: var(--font-size-large);
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
