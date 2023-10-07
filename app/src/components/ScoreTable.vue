<script setup lang="ts">
import type { Score } from "@/game";

interface Props {
    scores: Score[];
    showRank?: boolean;
    showPlayer?: boolean;
    dateFormat?: "short" | "long";
}

const props = withDefaults(defineProps<Props>(), {
    showRank: true,
    showPlayer: true,
    dateFormat: "long",
});

function formatDateLong(dateString: string) {
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

function formatDate(dateString: string) {
    if (props.dateFormat == "short") return formatDateShort(dateString);
    else if (props.dateFormat == "long") return formatDateLong(dateString);
}
</script>

<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th v-if="showRank">#</th>
                    <th>Date</th>
                    <th v-if="showPlayer">Player</th>
                    <th>Points</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(score, idx) of scores" :key="score.id">
                    <td v-if="showRank">{{ idx + 1 }}</td>
                    <td>{{ formatDate(score.date) }}</td>
                    <td v-if="showPlayer" style="color: var(--color-accent-secondary)">
                        {{ score.username }}
                    </td>
                    <td style="color: var(--color-accent-primary)">{{ score.score }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";

@media screen and (max-width: $bp-mobile) {
    .table-container {
        // overflow-x: auto;
        max-width: 80vw;
        overflow-x: auto;

        table {
            width: 100%;

            th,
            td {
                word-wrap: break-word;
            }
        }
    }
}
</style>
