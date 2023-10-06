<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
    defineProps<{
        total: number;
        progress: number;
    }>(),
    { total: 0, progress: 0 }
);

const fillRatio = computed(() => props.progress / props.total);
const fillPercent = computed(() => fillRatio.value * 100);
</script>

<template>
    <div class="container">
        <div class="pb">
            <div class="pb-filler" :style="{ width: `${fillPercent}%` }"></div>
            <span class="text">Progress: {{ progress }} / {{ total }}</span>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.container {
    width: 100%;
}

.pb {
    position: relative;
    width: 100%;
    height: 2em;
    border: var(--border-width) solid rgba(var(--color-accent-secondary-rgb), 0.6);
    border-radius: var(--br);
    margin-top: 1em;

    display: flex;
    justify-content: center;
    align-items: center;

    box-shadow: 0 0 1.5rem rgba(var(--color-accent-secondary-rgb), 0.2);
    .text {
        font-weight: bold;
        color: var(--color-accent-secondary);
        z-index: 1;
    }
    .pb-filler {
        position: absolute;
        inset: 0;
        width: 0;
        height: 100%;
        background-color: rgba(var(--color-accent-secondary-rgb), 0.3);
        transition: width 400ms cubic-bezier(0.165, 0.84, 0.44, 1);
    }
}
</style>
