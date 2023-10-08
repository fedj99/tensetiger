<script setup lang="ts">
import "@/chartjs";
import type { Score } from "@/game";
import { type ChartData, type ChartOptions } from "chart.js";
import { DateTime } from "luxon";
import { computed, ref, type CSSProperties } from "vue";
import { Scatter } from "vue-chartjs";

interface Props {
    scores: Score[];
}

const props = defineProps<Props>();

const scoresReversed = computed(() => {
    const copy = [...props.scores];
    copy.reverse();
    return copy;
});

const chartData = computed(() => {
    const config: ChartData<"scatter", number[]> = {
        labels: scoresReversed.value.map((x) =>
            DateTime.fromRFC2822(x.date, { setZone: true }).toLocaleString({
                dateStyle: "short",
                timeStyle: "short",
            })
        ),
        datasets: [
            {
                data: scoresReversed.value.map((x) => x.score),
                label: "Your score",
                fill: "origin",
                showLine: true,
                borderColor: getCSSVariable("--color-accent-primary"),
                pointBackgroundColor: getCSSVariable("--color-accent-primary"),
                backgroundColor: `rgba(${getCSSVariable("--color-accent-primary-rgb")}, 0.2`,
            },
        ],
    };
    return config;
});
const chartOptions = ref<ChartOptions<"scatter">>({
    responsive: true,
    scales: {
        x: {
            type: "category",
        },
    },
});
const chartStyles = ref<CSSProperties>({
    height: "300px",
    width: "100%",
    position: "relative",
});

function getCSSVariable(name: string) {
    return getComputedStyle(document.documentElement).getPropertyValue(name);
}
</script>

<template>
    <Scatter
        v-if="scores.length > 0"
        id="personal-performance-graph"
        :data="chartData"
        :options="chartOptions"
        :style="chartStyles"
    ></Scatter>
    <div v-else>No scores yet</div>
</template>

<style lang="scss" scoped></style>
