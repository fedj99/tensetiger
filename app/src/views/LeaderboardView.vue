<script setup lang="ts">
import { getHighscore, getLatestScores, getScore, getTopKScores, getUser } from "@/api";
import Fullscreen from "@/components/Fullscreen.vue";
import GlobalLeaderboard from "@/components/GlobalLeaderboard.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import UserLeaderboard from "@/components/UserLeaderboard.vue";
import UserResults from "@/components/UserResults.vue";
import type { Score } from "@/rules";
import { useErrorsStore } from "@/stores/errors";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useCookies } from "vue3-cookies";

const LATEST_K = 10;
const TOP_K = 10;

const route = useRoute();
const { cookies } = useCookies();

const errorsStore = useErrorsStore();

const loading = ref(true);

const username = ref<string>(route.query.username as string);
const score = ref<Score>();
const topKScores = ref<Score[]>();
const latestScores = ref<Score[]>();
const personalHighScore = ref<Score>();
const globalHighScore = ref<Score>();

const scoreId = computed(() => parseInt(route.query.score_id as string));

const scoreIdProvided = computed(() => route.query.score_id != undefined);
const queryUserId = computed(() => route.query.user_id);
const queryUserName = computed(() => route.query.username);

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

        // If score_id is passed as query parameters, we fetch the score and set the user_id
        // Otherwise, check query parameters for user id
        // Finally, try to get user from cookies
        const loggedInUserId = cookies.get("user_id");
        const loggedInUsername = cookies.get("username");
        let userId: number | undefined = undefined;

        if (scoreIdProvided.value) {
            const gameScore = await getScore(scoreId.value).then((x) => x.data);
            userId = gameScore.user_id;
            score.value = gameScore;
            username.value = gameScore.username;
        } else if (queryUserId.value) {
            userId = parseInt(queryUserId.value as string);
            if (!queryUserName.value) {
                username.value = await getUser(userId).then((x) => x.data.username);
            } else {
                username.value = queryUserName.value as string;
            }
        } else if (loggedInUserId) {
            userId = parseInt(loggedInUserId);
            username.value = loggedInUsername;
        }

        // If userId was determined, show personal information
        if (userId) {
            // Get personal latest scores
            promises.push(
                getLatestScores(userId, LATEST_K).then((res) => (latestScores.value = res.data))
            );
            // Get personal high score
            promises.push(getHighscore(userId).then((res) => (personalHighScore.value = res.data)));
        }

        // Wait for all results
        await Promise.all(promises);
    } catch (e: any) {
        errorsStore.setError(e);
        console.error(e);
    } finally {
        loading.value = false;
    }
}
</script>

<template>
    <Fullscreen center style="padding-bottom: 5em">
        <main v-if="loading" class="loading">
            <LoadingSpinner>Getting latest high scores...</LoadingSpinner>
        </main>
        <main v-else class="leaderboard">
            <UserResults
                v-if="personalHighScore && globalHighScore"
                :score="score"
                :personal-high-score="personalHighScore"
                :global-high-score="globalHighScore"
                :username="username"
            ></UserResults>

            <h1 v-else>General Leaderboard</h1>

            <hr />

            <div class="tables">
                <template v-if="latestScores">
                    <h2>Your latest scores</h2>
                    <UserLeaderboard v-if="latestScores" :scores="latestScores"></UserLeaderboard>
                </template>
                <h2>Top {{ TOP_K }} players</h2>
                <GlobalLeaderboard :scores="topKScores"></GlobalLeaderboard>
            </div>

            <hr />

            <div>
                <RouterLink :to="{ name: 'home' }" class="button reset button-huge"
                    >Play Again!</RouterLink
                >
            </div>
        </main>
    </Fullscreen>
</template>

<style lang="scss" scoped>
main {
    width: min(100%, 50em);
    margin: auto;
}

.leaderboard {
    max-width: 100vw;
    padding: var(--padding);
}

h1 {
    margin: var(--padding) 0;
    line-height: 1;
    font-size: var(--font-size-huge);
    overflow-wrap: break-word;
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
