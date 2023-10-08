<script setup lang="ts">
import { type GameConfig, type Result } from "@/rules";
import { useGameStore } from "@/stores/game";
import {
    emptyAnswer,
    wordFormKeys,
    wordFormNames,
    type Answer,
    type Word,
    type WordFormKey,
} from "@/words";
import { computed, nextTick, ref, watch } from "vue";
import Modal from "./Modal.vue";

const props = defineProps<{
    gameConfig: GameConfig;
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

defineExpose({ focusFirst });

const gameStore = useGameStore();

const editableWords = ref<Answer>(emptyAnswer());
const submitDisabled = ref<boolean>(false);

const inputFields = ref<HTMLInputElement[]>([]);
const nextButton = ref<HTMLButtonElement>();
const revealHintModal = ref<InstanceType<typeof Modal>>();

const hintStyle = computed(() => {
    if (gameStore.hintRevealed) {
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
        // Reset some buttons
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
    gameStore.hintRevealed = true;
    emit("revealHint");
}

function focusFirst() {
    // Focus first field
    if (inputFields.value?.length) inputFields.value[0].focus();
}
</script>

<template>
    <form v-if="word" autocomplete="off" class="form" action="" @submit.prevent="submit()">
        <div v-for="key of wordFormKeys" :key="key" class="verb-form">
            <label :for="key">{{ wordFormNames[key] }}</label>
            <input
                :id="key"
                ref="inputFields"
                v-model="editableWords[key]"
                :readonly="shownKey == key"
                required
                class="input-huge"
                type="text"
                :name="key"
                :class="{ active: shownKey != key }"
            />
        </div>

        <div class="verb-form translation">
            <label for="translation">German translation</label>
            <div class="control-group">
                <input
                    id="translation"
                    :value="gameStore.hintRevealed ? word.translation : 'Translation'"
                    readonly
                    type="text"
                    autocomplete="off"
                    name="translation"
                    :style="hintStyle"
                    tabindex="-1"
                />
                <div class="controls">
                    <button
                        v-if="!gameStore.hintRevealed"
                        type="button"
                        class="button-small danger"
                        @click="revealHintModal?.open()"
                    >
                        Reveal
                    </button>
                </div>
            </div>
        </div>

        <input type="submit" value="Check" style="flex: 1" :disabled="submitDisabled" />

        <Transition>
            <div
                v-if="result"
                class="result-overlay"
                :class="result.hasMistakes ? 'wrong' : 'correct'"
            >
                <template v-if="result.hasMistakes">
                    <div class="toprow">
                        <h1 class="heading">Incorrect <i class="ri-ghost-line"></i></h1>
                        <strong>{{ result.word.translation }}</strong>
                    </div>
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
                                    autocapitalize="off"
                                    autocorrect="off"
                                />
                                <input
                                    type="text"
                                    readonly
                                    :value="mistake.expected"
                                    tabindex="-1"
                                    autocapitalize="off"
                                    autocorrect="off"
                                />
                            </template>
                            <template v-else>
                                <input
                                    type="text"
                                    readonly
                                    :value="result.word[key]"
                                    class="correct"
                                    tabindex="-1"
                                    autocapitalize="off"
                                    autocorrect="off"
                                />
                                <input
                                    type="text"
                                    readonly
                                    :value="result.word[key]"
                                    tabindex="-1"
                                    autocapitalize="off"
                                    autocorrect="off"
                                />
                            </template>
                        </template>
                    </div>
                </template>
                <template v-else>
                    <h1 class="heading">Correct! <i class="ri-sparkling-fill"></i></h1>
                    <p>
                        <strong>{{ result.word.translation }}</strong> &mdash;
                        {{ result.word.form_infinitive }} / {{ result.word.form_simple_past }} /
                        {{ result.word.form_past_participle }}
                    </p>
                    <p>All your answers were correct. Good job!</p>
                </template>
                <span class="spacer"></span>
                <button
                    ref="nextButton"
                    type="button"
                    class="button-contrast"
                    @click="$emit('next')"
                >
                    Next <kbd><i class="ri-corner-down-left-fill"></i></kbd>
                </button>
            </div>
        </Transition>

        <div class="bonus-points">
            <Transition
                class="animate__animated animate__fast"
                enter-active-class="animate__bounceIn"
                leave-active-class="animate__bounceOut"
            >
                <div v-if="!result && word?.difficulty != 1" class="bonus-points-badge">
                    <strong>{{ word?.difficulty }}&times;</strong> points!
                </div>
            </Transition>
        </div>
    </form>

    <Modal
        ref="revealHintModal"
        :buttons="['cancel', { text: 'Show Hint', role: 'confirm', class: 'danger' }]"
        @confirm="revealHint()"
        >Reveal translation?
        <strong class="color-danger">(-{{ gameConfig.hintRevealedPenalty }} points)</strong></Modal
    >
</template>

<style lang="scss" scoped="">
@import "@/assets/main.scss";
@import "@/assets/base.scss";

.bonus-points {
    position: absolute;
    top: -8pt;
    left: -8pt;
    right: -8pt;
    display: flex;
    justify-content: flex-end;

    @media screen and (max-width: $bp-mobile) {
        justify-content: center;
        top: -12pt;
    }

    .bonus-points-badge {
        background-color: var(--color-success);
        color: var(--color-success-contrast);
        padding: var(--padding-sm) var(--padding);
        border-radius: var(--br-sm);
        box-shadow: 0 0 10px var(--color-shadow-strong);
        font-size: var(--font-size-small);
        text-transform: uppercase;
        pointer-events: none;
    }
}

.form {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    gap: var(--gap-lg);
    border: var(--border-width) solid rgba(var(--color-text-rgb), 0.1);
    border-radius: var(--br);
    padding: var(--padding);
    margin: var(--padding) 0;
    box-shadow: 0 0 30px var(--color-shadow);
}

.verb-form {
    flex: 1;
    position: relative;

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

    @media screen and (max-width: $bp-mobile) {
        label {
            position: absolute;
            top: -9pt;
            line-height: 1;
            border: 2px solid #0003;
            left: 8pt;
            border-radius: var(--br-sm);
            padding: 1pt 5pt;
            background-color: var(--color-background);
            width: max-content;
            font-size: var(--font-size-small);
            opacity: 1;
        }
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
    // max-height: 20em;
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

// Mobile
@import "@/assets/base.scss";

@media screen and (max-width: $bp-mobile) {
    .form {
        flex-direction: column;
    }

    // .control-group .controls {
    //     position: relative;
    //     padding: var(--padding) 0;

    //     button {
    //         flex: 1;
    //     }
    // }

    .mistakes {
        grid-auto-flow: row;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .result-overlay .heading {
        font-size: var(--font-size-huge);
    }
}
</style>
