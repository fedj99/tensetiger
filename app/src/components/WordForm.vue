<script setup lang="ts">
import type { Word } from "@/words";

const props = defineProps<{
    word?: Word;
    progress: number;
    wordCount: number;
}>();

const emit = defineEmits<{
    (e: "submit", key: string, value: string): void;
}>();

function submit() {
    emit("submit", "", "");
}
</script>

<template>
    <form v-if="word" class="form" action="" @submit.prevent="submit()">
        <div class="verb-form">
            <label for="form_infinitive">Infinitive</label>
            <input
                :value="word.form_infinitive"
                readonly
                class="input-huge"
                type="text"
                name="form_infinitive"
                id="form_infinitive"
            />
        </div>

        <div class="verb-form">
            <label for="form_simple_past">Simple past</label>
            <input
                :value="word.form_simple_past"
                readonly
                class="input-huge"
                type="text"
                name="form_simple_past"
                id="form_simple_past"
            />
        </div>

        <div class="verb-form">
            <label for="form_present_perfect">Present perfect</label>
            <input
                :value="word.form_past_participle"
                readonly
                class="input-huge"
                type="text"
                name="form_present_perfect"
                id="form_present_perfect"
            />
        </div>

        <div class="verb-form translation">
            <label for="translation">German translation</label>
            <input
                :value="word.translation"
                readonly
                type="text"
                name="translation"
                id="translation"
            />
        </div>

        <input
            type="submit"
            :value="progress < wordCount - 1 ? 'Next' : 'Finish'"
            style="flex: 1"
        />
    </form>
</template>

<style lang="scss" scoped="">
.form {
    display: flex;
    flex-wrap: wrap;
    gap: var(--gap-lg);
    border: var(--border-width) solid rgba(var(--color-text-rgb), 0.1);
    border-radius: var(--br);
    padding: var(--padding);
    margin: var(--padding);
}

.verb-form {
    flex: 1;

    label,
    input {
        display: block;
        width: 100%;
        text-align: left;
    }

    label {
        text-transform: uppercase;
        opacity: 0.5;
        margin-bottom: 0.6em;
    }

    &.translation {
        flex-basis: 100%;
        margin-top: 1em;
    }
}
</style>
