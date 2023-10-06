<script setup lang="ts">
import { gameConfig, type Result } from "@/game";
import {
    emptyAnswer,
    wordFormKeys,
    wordFormNames,
    type Answer,
    type Word,
    type WordFormKey,
} from "@/words";
import { computed, nextTick, ref, watch } from "vue";

const props = defineProps<{
    word?: Word;
    shownKey: WordFormKey;
    progress: number;
    wordCount: number;
    result?: Result;
}>();

const emit = defineEmits<{
    (e: "submit", word: Word, shownKey: WordFormKey, answer: Answer): void;
    (e: "revealHint"): void;
    (e: "next"): void;
}>();

const editableWords = ref<Answer>(emptyAnswer());
const hintRevealed = ref<boolean>(false);
const submitDisabled = ref<boolean>(false);

const inputFields = ref<HTMLInputElement[]>([]);
const nextButton = ref<HTMLButtonElement>();

const hintStyle = computed(() => {
    if (hintRevealed.value) {
        return {};
    } else {
        return {
            "text-security": "disc",
            "-webkit-text-security": "disc",
        };
    }
});

watch(
    [() => props.word, () => props.shownKey],
    ([word, shownKey]) => {
        // Focus first field
        if (inputFields.value?.length) inputFields.value[0].focus();
        // Reset some buttons
        hintRevealed.value = false;
        submitDisabled.value = false;
        // Reset field contents
        if (!word) {
            // Set all to empty
            for (const key in editableWords.value) editableWords.value[key as WordFormKey] = "";
        } else {
            // Show only shownKey, others are empty
            for (const key in editableWords.value) {
                const castKey = key as WordFormKey;
                if (key == shownKey) editableWords.value[castKey] = word[castKey];
                else editableWords.value[castKey] = "";
            }
        }
    },
    { immediate: true }
);

function submit() {
    if (!props.word) return;
    submitDisabled.value = true;
    emit("submit", props.word, props.shownKey, editableWords.value);

    nextTick(() => {
        nextButton.value?.focus();
    });
}

function revealHint() {
    hintRevealed.value = true;
    emit("revealHint");
}
</script>

<template>
    <form v-if="word" autocomplete="off" class="form" action="" @submit.prevent="submit()">
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
            <div class="control-group">
                <input
                    :value="hintRevealed ? word.translation : 'Translation'"
                    readonly
                    type="text"
                    autocomplete="off"
                    name="translation"
                    id="translation"
                    :style="hintStyle"
                />
                <div class="controls">
                    <button
                        v-if="!hintRevealed"
                        type="button"
                        class="button-small"
                        @click="revealHint()"
                    >
                        Reveal Hint (-{{ gameConfig.hintRevealedPenalty }} points)
                    </button>
                </div>
            </div>
        </div>

        <input type="submit" value="Check" style="flex: 1" :disabled="submitDisabled" />

        <Transition>
            <div
                v-if="result"
                class="result-overlay"
                :class="result?.hasMistakes ? 'wrong' : 'correct'"
            >
                <template v-if="!result">
                    <h1>Oops...</h1>
                    <p>Something went wrong, as there isn't currently a result.</p>
                </template>
                <template v-else-if="result.hasMistakes">
                    <h1 class="heading">Incorrect <i class="ri-ghost-line"></i></h1>
                    <div class="mistakes">
                        <span>You said:</span>
                        <span>Correct:</span>
                        <template v-for="(mistake, key) in result.mistakes" :key="key">
                            <template v-if="mistake">
                                <input
                                    type="text"
                                    readonly
                                    :value="mistake.actual"
                                    class="wrong"
                                    tabindex="-1"
                                />
                                <input
                                    type="text"
                                    readonly
                                    :value="mistake.expected"
                                    tabindex="-1"
                                />
                            </template>
                            <template v-else>
                                <input
                                    type="text"
                                    readonly
                                    :value="result.word[key]"
                                    class="correct"
                                    tabindex="-1"
                                />
                                <input
                                    type="text"
                                    readonly
                                    :value="result.word[key]"
                                    tabindex="-1"
                                />
                            </template>
                        </template>
                    </div>
                </template>
                <template v-else>
                    <h1 class="heading">Correct! <i class="ri-sparkling-fill"></i></h1>
                    <p>All your answers were correct. Good job!</p>
                </template>
                <span class="spacer"></span>
                <button
                    type="button"
                    ref="nextButton"
                    class="button-contrast"
                    @click="$emit('next')"
                >
                    Next <kbd><i class="ri-corner-down-left-fill"></i></kbd>
                </button>
            </div>
        </Transition>
    </form>
</template>

<style lang="scss" scoped="">
@import "@/assets/main.scss";

.form {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    gap: var(--gap-lg);
    border: var(--border-width) solid rgba(var(--color-text-rgb), 0.1);
    border-radius: var(--br);
    padding: var(--padding);
    margin: var(--padding) 0;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.12);
    overflow: hidden;
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

input[type="text"],
input[type="password"] {
    border: var(--border-width) solid transparent;
    transition: all 200ms;
    min-height: 2.5em;
}

input[type="text"].active {
    border: var(--border-width) dotted rgba(var(--color-text-rgb), 0.3);

    &:focus {
        border-color: transparent;
    }
}

.control-group {
    position: relative;

    .controls {
        position: absolute;
        inset: 0;
        display: flex;
        justify-content: flex-end;
        padding: 5px;

        button {
            font-size: 11pt;
            font-weight: normal;
        }
    }
}

.result-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: var(--padding);
    padding: var(--padding-lg);
    border-radius: var(--br);
    border: var(--border-width) solid #0002;
    max-height: 20em;
    clip-path: circle(200% at top right);

    background-color: #fff;

    * {
        margin: 0;
    }

    .spacer {
        flex: 1;
    }

    .heading {
        margin-top: 1rem;
    }

    button {
        align-self: stretch;
    }

    --white: 255, 255, 255;

    &.correct {
        background-color: var(--color-success);
        color: var(--color-success-contrast);
        .button-contrast {
            @include button-style-outlined(var(--white), var(--color-success-contrast), 0.2, #fff6);
        }
    }

    &.wrong {
        background-color: var(--color-danger);
        color: var(--color-danger-contrast);

        .button-contrast {
            @include button-style-outlined(var(--white), var(--color-danger-contrast), 0.2, #fff6);
        }

        .heading {
            font-size: var(--font-size-large);
            font-weight: 400;
            margin: 0;
        }
    }
}

// Mistakes
.mistakes {
    overflow-y: auto;
    display: grid;
    grid-template-rows: 1fr 1fr;
    grid-template-columns: max-content repeat(3, minmax(0, 1fr));
    grid-auto-flow: column;
    gap: var(--gap);
    align-items: center;

    span {
        font-weight: bold;
    }

    input {
        pointer-events: none;
        color: #20201f;
        font-weight: bold;
        background-color: #fff3;
        border: var(--border-width) solid #fff6;

        &.correct {
            color: #004e03;
        }

        &.wrong {
            text-decoration: underline wavy red;
            color: #8b0000;
        }
    }
}

// Transitions
.v-enter-active,
.v-leave-active {
    transition: clip-path 400ms cubic-bezier(0.165, 0.84, 0.44, 1);
}

.v-enter-from,
.v-leave-to {
    clip-path: circle(0 at top right);
}
</style>
