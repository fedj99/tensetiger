<script setup lang="ts">
import { getHighscore, getLatestScores, getScore, getTopKScores } from "@/api";
import AxiosErrorWidget from "@/components/AxiosErrorWidget.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import ScoreTable from "@/components/ScoreTable.vue";
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

onMounted(async () => {
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
        loading.value = false;
    } catch (e) {
        console.log(e);
        error.value = e;
    }
});

async function resetGame() {
    await gameStore.reset();
    router.push({ name: "login" });
}
</script>

<template>
    <Fullscreen center style="padding-bottom: 5em">
        <div v-if="loading && !error" class="loading">Loading...</div>
        <div v-else-if="error" class="error">
            <AxiosErrorWidget :error="error"></AxiosErrorWidget>
        </div>
        <div v-else class="leaderboard">
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
                <div>
                    <h2>Your latest scores</h2>
                    <ScoreTable v-if="latestScores" :scores="latestScores"></ScoreTable>
                    <div v-else>No scores yet</div>
                </div>

                <div>
                    <h2>Top {{ TOP_K }} players</h2>
                    <ScoreTable v-if="topKScores" :scores="topKScores" show-rank></ScoreTable>
                    <div v-else>No scores yet</div>
                </div>
            </div>

            <hr />

            <div>
                <button @click="resetGame()" class="reset input-huge">Play Again!</button>
            </div>
        </div>
    </Fullscreen>
</template>

<style lang="scss" scoped>
@import "@/assets/components.scss";

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

.tables {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2em;
}

.reset {
    width: 100%;
}

@import "@/assets/base.scss";

@media screen and (max-width: $bp-mobile) {
    .leaderboard {
        padding: var(--padding-lg);
    }

    .tables {
        width: 100%;
        flex-direction: column;
        align-items: stretch;
    }
}
</style>
