<script setup lang="ts">
import { useGameStore } from "@/stores/game";

const gameStore = useGameStore();
</script>

<template>
    <div class="box">
        <span class="prefix">Your score:</span>
        <span class="score">{{ gameStore.score }}</span>
        <span class="suffix">pts.</span>
    </div>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";
.box {
    color: var(--color-accent-secondary);
    display: flex;
    gap: var(--padding-lg);
    align-items: baseline;
    justify-content: center;
}
.prefix,
.suffix {
    line-height: 1em;
}
.score {
    font-size: calc(1.5 * var(--font-size-huge));
    font-weight: bold;
    font-family: var(--font-default-serif);
}

@media screen and (max-width: $bp-mobile) {
    .prefix,
    .suffix {
        display: none;
    }

    .score {
        font-size: var(--font-size-huge);
    }
}
</style>
