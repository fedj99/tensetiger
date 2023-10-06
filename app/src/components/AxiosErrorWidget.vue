<script setup lang="ts">
import ErrorBaseView from "@/views/errors/ErrorBaseView.vue";
import { AxiosError } from "axios";

defineProps<{
    error: AxiosError;
}>();
</script>

<template>
    <ErrorBaseView>
        <h3>{{ error.message || "Error" }}</h3>
        <p class="sans fs-reg">Aw, shucks! Something went wrong on our end.</p>

        <details class="sans fs-reg">
            <summary>Show Error Details</summary>

            <pre>
                {{ JSON.stringify(error, null, 2) }}
            </pre>
        </details>
    </ErrorBaseView>
</template>

<style lang="scss" scoped>
.fs-reg {
    font-size: var(--font-size-regular);
}

.sans {
    font-family: var(--font-default-sans);
}

pre {
    width: min(90vw, 40em);
}
</style>
