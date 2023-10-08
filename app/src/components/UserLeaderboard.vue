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

const chartData = computed(() => {
    const config: ChartData<"scatter", number[]> = {
        labels: props.scores.map((x) => DateTime.fromRFC2822(x.date).toFormat("d. MMM T")),
        datasets: [
            {
                data: props.scores.map((x) => x.score),
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
        id="personal-performance-graph"
        :data="chartData"
        :options="chartOptions"
        :style="chartStyles"
        v-if="scores.length > 0"
    ></Scatter>
    <div v-else>No scores yet</div>
</template>

<style lang="scss" scoped></style>
