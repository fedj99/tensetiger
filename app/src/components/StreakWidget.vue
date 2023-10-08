<script setup lang="ts">
import { useGameStore } from "@/stores/game";

const gameStore = useGameStore();
</script>

<template>
    <div class="streak-base">
        <span
            ><strong>{{ gameStore.streak }}</strong
            >&times; 🔥 +<strong>{{ gameStore.currentStreakBonus }}</strong> pts.</span
        >
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
}
</style>
