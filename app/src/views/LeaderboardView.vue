<script setup lang="ts">
import { getHighscore, getLatestScores, getScore, getTopKScores } from "@/api";
import AxiosErrorWidget from "@/components/AxiosErrorWidget.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import GlobalLeaderboard from "@/components/GlobalLeaderboard.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import UserLeaderboard from "@/components/UserLeaderboard.vue";
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

const username = ref(route.query.user);
const score = ref<Score>();
const topKScores = ref<Score[]>();
const latestScores = ref<Score[]>();
const personalHighScore = ref<Score>();
const globalHighScore = ref<Score>();

const scoreId = computed(() => parseInt(route.query.score_id as string));
const greeting = computed(() => {
    if (!score.value) return "Loading...";
    if (score.value.score > 0) return "Good job";
    else return "Better luck next time";
});
const ending = computed(() => {
    if (!score.value) return "Loading...";
    if (score.value.score > 0) return "Impressive!";
    else return "You can do better than this...";
});

onMounted(fetchScores);

async function fetchScores() {
    try {
        loading.value = true;
        const [scoreRes, topKRes] = await Promise.all([
            getScore(scoreId.value),
            getTopKScores(TOP_K),
        ]);
        score.value = scoreRes.data as Score;
        topKScores.value = topKRes.data as Score[];
        globalHighScore.value = topKScores.value.length > 0 ? topKScores.value[0] : undefined;
        username.value = score.value.username;
        const [latestRes, highscoreRes] = await Promise.all([
            getLatestScores(score.value.user_id, LATEST_K),
            getHighscore(score.value.user_id),
        ]);
        latestScores.value = latestRes.data as Score[];
        personalHighScore.value = highscoreRes.data as Score;
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
            <h1>
                {{ greeting }}, <span class="username">{{ username }}</span
                >!
            </h1>
            <p>You scored</p>
            <h1 class="score">{{ score?.score }}</h1>
            <p>points. {{ ending }}</p>

            <hr />

            <template v-if="score && personalHighScore && globalHighScore">
                <p
                    v-if="
                        score.score == personalHighScore.score &&
                        score.date == personalHighScore.date
                    "
                >
                    <template
                        v-if="
                            score.score == globalHighScore.score &&
                            score.user_id == globalHighScore.user_id &&
                            score.date == globalHighScore.date
                        "
                    >
                        🎉🎉🎉 <strong>NEW HIGH SCORE!!!</strong> 🎉🎉🎉
                    </template>
                    <template v-else> 🎉 <strong>New personal record!</strong> 🎉 </template>
                </p>
                <p v-else>
                    Previous personal record:
                    <strong class="highscore">{{
                        personalHighScore?.score || "Loading..."
                    }}</strong>
                </p>
            </template>
            <p v-else>High score loading...</p>

            <hr />

            <div class="tables">
                <h2>Your latest scores</h2>
                <UserLeaderboard v-if="latestScores" :scores="latestScores"></UserLeaderboard>
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

.username {
    color: var(--color-accent-secondary);
}

.highscore {
    font-family: var(--font-default-serif);
    font-size: var(--font-size-large);
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

.score {
    margin: 0;
    line-height: 1;
    font-size: 72pt;
}

p {
    margin: var(--padding) 0;
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
