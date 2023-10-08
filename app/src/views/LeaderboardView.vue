<script setup lang="ts">
import { getHighscore, getLatestScores, getScore, getTopKScores } from "@/api";
import AxiosErrorWidget from "@/components/AxiosErrorWidget.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import GlobalLeaderboard from "@/components/GlobalLeaderboard.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import UserLeaderboard from "@/components/UserLeaderboard.vue";
import UserResults from "@/components/UserResults.vue";
import type { Score } from "@/game";
import { useGameStore } from "@/stores/game";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const LATEST_K = 10;
const TOP_K = 10;

const route = useRoute();
const router = useRouter();
const gameStore = useGameStore();

const loading = ref(true);
const error = ref();

const username = ref<string>(route.query.user as string);
const score = ref<Score>();
const topKScores = ref<Score[]>();
const latestScores = ref<Score[]>();
const personalHighScore = ref<Score>();
const globalHighScore = ref<Score>();

const scoreId = computed(() => parseInt(route.query.score_id as string));

const scoreIdProvided = computed(() => route.query.user != undefined);

onMounted(fetchScores);

async function fetchScores() {
    try {
        loading.value = true;

        // Array of promises to wait for
        const promises: Promise<any>[] = [];

        // Global leaderboards
        promises.push(
            getTopKScores(TOP_K).then((x) => {
                const scores = x.data;
                topKScores.value = scores;
                globalHighScore.value = scores.length > 0 ? scores[0] : undefined;
            })
        );

        // If score ID provided, fetch user-specific data
        if (scoreIdProvided.value) {
            // Gets the score referred to by score_id
            const getScorePromise = getScore(scoreId.value).then((x) => (score.value = x.data));
            promises.push(getScorePromise);
            // Get personal latest scores
            promises.push(
                getScorePromise
                    .then((score) => getLatestScores(score.user_id, LATEST_K))
                    .then((x) => (latestScores.value = x.data))
            );
            // Get personal high score
            promises.push(
                getScorePromise
                    .then((score) => getHighscore(score.user_id))
                    .then((x) => (personalHighScore.value = x.data))
            );
        }

        // Wait for all results
        await Promise.all(promises);
    } catch (e) {
        error.value = e;
        console.error(e);
    } finally {
        loading.value = false;
    }
}

async function resetGame() {
    await gameStore.reset();
    router.push({ name: "login" });
}
</script>

<template>
    <Fullscreen center style="padding-bottom: 5em">
        <main v-if="error" class="error">
            <AxiosErrorWidget :error="error"></AxiosErrorWidget>
        </main>
        <main v-else-if="loading" class="loading">
            <LoadingSpinner>Getting latest high scores...</LoadingSpinner>
        </main>
        <main v-else class="leaderboard">
            <UserResults
                v-if="score && personalHighScore && globalHighScore"
                :score="score"
                :personal-high-score="personalHighScore"
                :global-high-score="globalHighScore"
                :username="username"
            ></UserResults>

            <h1 v-else>General Leaderboard</h1>

            <hr />

            <div class="tables">
                <template v-if="scoreIdProvided">
                    <h2>Your latest scores</h2>
                    <UserLeaderboard v-if="latestScores" :scores="latestScores"></UserLeaderboard>
                </template>
                <h2>Top {{ TOP_K }} players</h2>
                <GlobalLeaderboard :scores="topKScores"></GlobalLeaderboard>
            </div>

            <hr />

            <div>
                <button @click="resetGame()" class="reset input-huge">Play Again!</button>
            </div>
        </main>
    </Fullscreen>
</template>

<style lang="scss" scoped>
@import "@/assets/components.scss";

.leaderboard {
    max-width: 100vw;
    padding: var(--padding);
}

h1 {
    margin: var(--padding) 0;
    line-height: 1;
    font-size: var(--font-size-huge);
    word-wrap: break-word;
    max-width: 80vw;
}

h2 {
    font-size: var(--font-size-large);
}

.reset {
    min-width: min(80vw, 20em);
}

@import "@/assets/base.scss";

@media screen and (max-width: $bp-mobile) {
    .leaderboard {
        padding: var(--padding-lg);
    }
}
</style>
