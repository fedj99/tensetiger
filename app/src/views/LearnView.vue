<script setup lang="ts">
import { getWordList } from "@/api";
import Centered from "@/components/Centered.vue";
import Fullscreen from "@/components/Fullscreen.vue";
import Logo from "@/components/Logo.vue";
import WordForm from "@/components/WordForm.vue";
import type { Word } from "@/words";
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const LS_WORDS_KEY = "words";
const LS_WORD_COUNT_KEY = "word-count";
const LS_WORD_PROGRESS_KEY = "word-progress";

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const error = ref(null);
const words = ref<Word[]>([]);
const wordCount = ref<number>(0);
const progress = ref<number>(0);

const userName = computed(() => route.query.username);
const currentWord = computed(() => words.value[progress.value]);

watch([() => route.params], () => fetchWordList(), { immediate: true });

async function newRound() {
    try {
        loading.value = true;
        // Load new round
        const wordList = await getWordList();
        loading.value = false;

        // Start round
        words.value = wordList.data;
        wordCount.value = words.value?.length;
        progress.value = 0;
    } catch (e: any) {
        error.value = e;
    }
}

function resumeRound(words_: Word[], wordCount_: number, progress_: number) {
    // Simply resume round
    words.value = words_;
    wordCount.value = wordCount_;
    progress.value = progress_;
}

function fetchWordList() {
    const cachedWords = localStorage.getItem(LS_WORDS_KEY);
    const cachedWordCount = localStorage.getItem(LS_WORD_COUNT_KEY);
    const cachedProgress = localStorage.getItem(LS_WORD_PROGRESS_KEY);

    if (cachedWords && cachedWordCount && cachedProgress) {
        const wordCount = parseInt(cachedWordCount);
        const progress = parseInt(cachedProgress);
        const words = JSON.parse(cachedWords);

        if (progress < wordCount - 1) {
            // Resume game
            resumeRound(words, wordCount, progress);
        }
    }

    // Start a new round
    newRound();
}

function onSubmit(key: string, value: string) {
    progress.value++;

    if (progress.value == wordCount.value) {
        endRound();
    }
}

function endRound() {
    // Post score and get score ID back
    // Then go to leaderboards with score ID, where all results are fetched
    const scoreId = 0;
    router.push({ name: "leaderboard", query: { username: userName.value, scoreId } });
}

function setWord() {}
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
                <p>Fill in the missing verb form! If there are multiple, choose one.</p>

                <WordForm
                    :word="currentWord"
                    :progress="progress"
                    :word-count="wordCount"
                    @submit="onSubmit"
                ></WordForm>
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
