<script setup lang="ts">
import {
    emptyAnswer,
    wordFormKeys,
    wordFormNames,
    type Answer,
    type Word,
    type WordFormKey,
} from "@/words";
import { ref, watch } from "vue";

const props = defineProps<{
    word?: Word;
    shownKey: WordFormKey;
    progress: number;
    wordCount: number;
}>();

const editableWords = ref<Answer>(emptyAnswer());

const inputFields = ref<HTMLInputElement[]>([]);

watch(
    [() => props.word, () => props.shownKey],
    ([word, shownKey]) => {
        if (inputFields.value?.length) inputFields.value[0].focus();
        if (!word) {
            for (const key in editableWords.value) editableWords.value[key as WordFormKey] = "";
        } else {
            for (const key in editableWords.value) {
                const castKey = key as WordFormKey;
                if (key == shownKey) editableWords.value[castKey] = word[castKey];
                else editableWords.value[castKey] = "";
            }
        }
    },
    { immediate: true }
);

const emit = defineEmits<{
    (e: "submit", word: Word, shownKey: WordFormKey, answer: Answer): void;
}>();

function submit() {
    if (!props.word) return;
    emit("submit", props.word, props.shownKey, editableWords.value);
}
</script>

<template>
    <form v-if="word" class="form" action="" @submit.prevent="submit()">
        <div v-for="key of wordFormKeys" :key="key" class="verb-form">
            <label :for="key">{{ wordFormNames[key] }}</label>
            <input
                v-model="editableWords[key]"
                :readonly="shownKey == key"
                required
                class="input-huge"
                type="text"
                :name="key"
                :id="key"
                :class="{ active: shownKey != key }"
                ref="inputFields"
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
    margin: var(--padding) 0;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.12);
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

input[type="text"] {
    border: var(--border-width) solid transparent;
    transition: all 200ms;
}

input[type="text"].active {
    border: var(--border-width) dotted rgba(var(--color-text-rgb), 0.3);

    &:focus {
        border-color: transparent;
    }
}
</style>
