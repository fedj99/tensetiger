<script setup lang="ts">
import { useGameStore } from "@/stores/game";
import { Duration } from "luxon";
import { computed } from "vue";

const gameStore = useGameStore();

const elapsedTime = computed(() => {
    const duration = Duration.fromObject({ seconds: gameStore.elapsedSeconds });
    return duration.toFormat("m:ss");
});
</script>

<template>
    <div class="streak-base">
        <span> ⏱️ {{ elapsedTime }} </span>
    </div>
</template>

<style lang="scss">
.streak-base {
    padding: var(--padding-sm) var(--padding-huge);
    background-color: var(--color-success);
    border-radius: var(--br-sm);
    box-shadow: 0 0 10px var(--color-shadow-strong);
    color: var(--color-success-contrast);
    display: inline-block;
    min-width: 6.5rem;
    font-variant-numeric: tabular-nums;
}
</style>
