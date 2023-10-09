<script setup lang="ts">
import { computed, ref } from "vue";

interface Button {
    text: string;
    role?: "confirm" | "cancel" | "button";
    action?: (c: Context) => void;
    class?: string;
}

type DefaultButton = "confirm" | "cancel";

const defaultButtons: { [key in DefaultButton]: Button } = {
    confirm: {
        text: "Confirm",
        role: "confirm",
        action: confirm,
    },
    cancel: {
        text: "Cancel",
        role: "cancel",
        action: cancel,
    },
};

interface Props {
    buttons: (Button | DefaultButton)[];
}

const props = withDefaults(defineProps<Props>(), {
    buttons: () => ["cancel", "confirm"],
    btnClasses: () => ({}),
});

const fullButtons = computed(() =>
    props.buttons.map((x) => {
        if (typeof x == "string") return defaultButtons[x];
        else return x;
    })
);

const emit = defineEmits<{
    (e: "confirm"): void;
    (e: "cancel"): void;
    (e: "open"): void;
    (e: "close"): void;
    (e: "toggle", state: boolean): void;
}>();

const isOpen = ref<boolean>(false);

function toggle(state?: boolean) {
    if (state == undefined) state = !isOpen.value;
    isOpen.value = state;
    emit("toggle", state);
}

const open = () => toggle(true);
const close = () => toggle(false);

function confirm() {
    toggle(false);
    emit("confirm");
}

function cancel() {
    toggle(false);
    emit("cancel");
}

const context = { toggle, open, close, confirm, cancel, isOpen };
type Context = typeof context;

function handleButtonClicked(btn: Button) {
    if (btn.role == "confirm") confirm();
    if (btn.role == "cancel") cancel();

    if (btn.action) btn.action(context);
}

defineExpose({ toggle, open, close });
</script>

<template>
    <div class="modal-base">
        <Transition
            class="animate__animated"
            style="animation-duration: 200ms"
            enter-active-class="animate__fadeIn"
            leave-active-class="animate__fadeOut"
        >
            <div v-if="isOpen" class="modal-background"></div>
        </Transition>
        <Transition
            class="animate__animated"
            style="animation-duration: 200ms"
            enter-active-class="animate__zoomIn"
            leave-active-class="animate__zoomOut"
        >
            <div v-if="isOpen" class="modal-frame">
                <div class="modal-content">
                    <slot></slot>
                </div>
                <div class="modal-buttons">
                    <button
                        v-for="(btn, idx) of fullButtons"
                        :key="idx"
                        :class="btn.class"
                        @click="handleButtonClicked(btn)"
                    >
                        {{ btn.text }}
                    </button>
                </div>
            </div>
        </Transition>
    </div>
</template>

<style lang="scss" scoped>
.modal-base {
    position: fixed;
    inset: 0;
    display: flex;
    flex-direction: column;
    // justify-content: center;
    padding-top: 20vh;
    align-items: center;
    pointer-events: none;
}

.modal-background {
    z-index: 100;
    position: fixed;
    inset: 0;
    background-color: #0004;
    backdrop-filter: blur(2px);
}

.modal-frame {
    pointer-events: all;
    z-index: 101;
    background-color: var(--color-background);
    border-radius: var(--br);
    border: var(--border-width) solid rgba(var(--color-text-rgb), 0.1);
    padding: var(--padding-lg);
    box-shadow: 0 0 30px var(--color-shadow);
}

.modal-buttons {
    margin-top: var(--gap-lg);
    display: flex;
    gap: var(--gap);
    justify-content: flex-end;
}
</style>
