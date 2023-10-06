<script setup lang="ts">
import type { Score } from "@/game";

interface Props {
    scores: Score[];
    showRank?: boolean;
}

withDefaults(defineProps<Props>(), { showRank: false });

function formatDate(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleString(["de-CH"], {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        timeZone: "GMT",
    });
}

function formatDateShort(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleDateString(["de-CH"], {
        month: "numeric",
        day: "numeric",
    });
}
</script>

<template>
    <table>
        <thead>
            <tr>
                <th v-if="showRank">#</th>
                <th>Player</th>
                <th>Date</th>
                <th>Points</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(score, idx) of scores" :key="score.id">
                <td v-if="showRank">{{ idx + 1 }}</td>
                <td style="color: var(--color-accent-secondary)">{{ score.username }}</td>
                <td>{{ formatDateShort(score.date) }}</td>
                <td style="color: var(--color-accent-primary)">{{ score.score }}</td>
            </tr>
        </tbody>
    </table>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";

@media screen and (max-width: $bp-mobile) {
    table,
    tr {
        width: 100%;
    }
}
</style>
