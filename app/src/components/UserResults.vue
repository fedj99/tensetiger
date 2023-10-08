<script setup lang="ts">
import type { Score } from "@/game";
import { computed } from "vue";

interface Props {
    score: Score;
    personalHighScore: Score;
    globalHighScore: Score;
    username: string;
}

const props = defineProps<Props>();

const greeting = computed(() => {
    if (props.score.score > 0) return "Good job";
    else return "Better luck next time";
});
const ending = computed(() => {
    if (props.score.score > 0) return "Impressive!";
    else return "You can do better than this...";
});
</script>

<template>
    <div class="user-results">
        <h1>
            {{ greeting }}, <span class="username">{{ username }}</span
            >!
        </h1>
        <p>You scored</p>
        <h1 class="score">{{ score?.score }}</h1>
        <p>points. {{ ending }}</p>

        <hr />

        <p v-if="score.score == personalHighScore.score && score.date == personalHighScore.date">
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
            <strong class="highscore">{{ personalHighScore?.score || "Loading..." }}</strong>
        </p>
    </div>
</template>

<style lang="scss" scoped>
.username {
    color: var(--color-accent-secondary);
}

.highscore {
    font-family: var(--font-default-serif);
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
</style>
