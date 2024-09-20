<script setup lang="ts">
import type { LeaderboardScore } from "@/rules";
import ScoreTable from "./ScoreTable.vue";

interface Props {
    scores?: LeaderboardScore[];
}

defineProps<Props>();
</script>

<template>
    <ScoreTable v-if="scores" :scores="scores" date-format="short"></ScoreTable>
    <div v-else>No scores yet</div>
</template>

<style lang="scss" scoped></style>
