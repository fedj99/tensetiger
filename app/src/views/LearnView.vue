<script setup lang="ts">
import { postScore } from "@/api";
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import Score from "@/components/Score.vue";
import StreakWidget from "@/components/StreakWidget.vue";
import WordForm from "@/components/WordForm.vue";
import { getResult, type Result } from "@/rules";
import { useErrorsStore } from "@/stores/errors";
import { useGameStore } from "@/stores/game";
import { type Answer, type Word, type WordFormKey } from "@/words";
import { nextTick, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCookies } from "vue3-cookies";

const route = useRoute();
const router = useRouter();
const gameStore = useGameStore();
const errorsStore = useErrorsStore();

const loading = ref(true);
const loadingMessage = ref("Loading...");

const userName = ref<string>("");
const userId = ref<number>(-1);
const currentResult = ref<Result | undefined>(undefined);
const wordFormRef = ref<InstanceType<typeof WordForm> | null>(null);
const showPlayer = false;

// Watch when route changes, then get a new (or cached word list)
watch([() => route.params], () => startRound(), { immediate: true });

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
async function openNewRound() {
    // Get new list of words from API
    console.log("Fetching a fresh round");
    await Promise.all([gameStore.reset(), gameStore.fetchGameConfig()]);
    // Watchers automatically save value
}

async function resumeFromCache() {
    console.log("Resuming game from cache, fetching game config");
    loading.value = true;

    // Load game config
    await gameStore.fetchGameConfig();

    // Resume game (needs to be done in any case to set state variables)
    gameStore.resume();
    // If already done, finish this round (and post the score)
    if (gameStore.progress >= gameStore.wordCount) {
        // Game was already over (?)
        console.warn("Inconsistent state, loaded finished game from cache");
        endRound();
    }
}

async function startRound() {
    loading.value = true;
    loadingMessage.value = "Loading verb forms...";

    try {
        // Check local storage first
        const loaded = gameStore.loadState();

        // Load from local storage
        if (loaded) {
            await resumeFromCache();
        } else {
            // Not cached, start a new round
            await openNewRound();
        }

        console.log("Game config:", gameStore.config);

        nextTick(() => {
            setTimeout(() => {
                wordFormRef.value?.focusFirst();
                console.log("Round started");
            }, 200);
        });
    } catch (e: any) {
        errorsStore.setError(e);
    } finally {
        loading.value = false;
    }
}

async function endRound() {
    try {
        // Signal to the game store that the round has finished
        gameStore.finish();
        console.log("Ending round. Points achieved:", gameStore.score);
        // Post score and get score ID back
        loading.value = true;
        loadingMessage.value = "Submitting your results...";
        const res = await postScore(userId.value, userName.value, gameStore.score);
        // When the score has been posted, it's safe to delete
        await gameStore.clearCache();
        // Then go to leaderboards with score ID, where all results are fetched
        router.push({
            name: "leaderboard",
            query: { user_id: userId.value, score_id: res.data.score_id.toString() },
        });
    } catch (e: any) {
        errorsStore.setError(e);
        console.error(e);
    } finally {
        loading.value = false;
    }
}

// Button handlers
function onSubmit(word: Word, shownKey: WordFormKey, answer: Answer) {
    console.log("Submit", shownKey, answer);
    // Compute points
    const result = getResult(gameStore.config, word, shownKey, answer);
    gameStore.addPoints(result);

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
            <main v-if="loading">
                <LoadingSpinner>{{ loadingMessage }}</LoadingSpinner>
            </main>
            <main v-else class="main">
                <div v-if="showPlayer" class="player">
                    <span> You are playing as: </span>
                    <strong>{{ userName }}</strong>
                    <RouterLink
                        :to="{ name: 'home' }"
                        class="button"
                        style="margin-left: 10px; font-size: var(--font-size-small)"
                        >Change
                    </RouterLink>
                </div>

                <Score></Score>
                <StreakWidget v-if="gameStore.currentStreakBonus > 0"></StreakWidget>
                <!-- <Logo></Logo> -->

                <ProgressBar
                    :total="gameStore.wordCount"
                    :progress="gameStore.progress"
                ></ProgressBar>

                <hr />

                <WordForm
                    ref="wordFormRef"
                    :game-config="gameStore.config"
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

                <div class="rules par">
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
@import "@/assets/base.scss";

.main {
    width: min(100%, 50em);
    margin: auto;
    padding: var(--padding-lg);
}

.par {
    max-width: max-content;
    margin: auto;
}

.rules {
    list-style: "👉";
    line-height: 1.5em;

    &:is(ul) li {
        padding-left: 0.5em;
    }
}

[data-theme="dark"] .rules {
    list-style: "👉";
}

.player {
    font-size: var(--font-size-large);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--gap);
}

@media screen and (max-width: $bp-mobile) {
    .player {
        font-size: var(--font-size-regular);
        flex-wrap: wrap;
        margin-top: var(--gap);

        a {
            flex: 1;
        }
    }

    .rules {
        text-align: left;

        ul {
            padding-left: 1em;
        }
    }
}
</style>
