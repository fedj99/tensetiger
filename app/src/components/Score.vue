<script setup lang="ts">
const props = defineProps<{
    score: number;
}>();
</script>

<template>
    <div class="box">
        <span class="prefix">Your score:</span>
        <span class="score">{{ score }}</span>
        <span class="suffix">pts.</span>
    </div>
</template>

<style lang="scss" scoped>
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
</style>
