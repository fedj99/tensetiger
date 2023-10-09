<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

type Theme = "light" | "dark";

const LS_THEME_KEY = "theme";

// What the user requested
const userPreference = ref<Theme | undefined>(undefined);
// The actual theme, should be derived from userPreference
const darkModeEnabled = ref<boolean>(false);
const theme = computed(() => (darkModeEnabled.value ? "dark" : "light"));

// Change the theme on document body when theme changed
watch(theme, (newTheme, oldTheme) => {
    document.documentElement.dataset["theme"] = newTheme;
});

watch(userPreference, setThemeAuto);

function setTheme(theme: Theme) {
    // For now theme is only controlled by a toggle switch
    darkModeEnabled.value = theme == "dark";
}

function setThemeAuto() {
    // Set theme. If no page preference is saved, use user preference
    const cachedTheme = localStorage.getItem(LS_THEME_KEY);
    if (cachedTheme) {
        // Use saved theme
        const theme = JSON.parse(cachedTheme);
        setTheme(theme);
    } else if (userPreference.value) {
        // Use user preference
        setTheme(userPreference.value);
    } else {
        // Use default
        setTheme("light");
    }
}

function addThemeEventListener(prefersColorScheme: string, theme: Theme) {
    matchMedia(`(prefers-color-scheme: ${prefersColorScheme})`).addEventListener("change", (e) => {
        if (e.matches) {
            userPreference.value = theme;
            setThemeAuto();
        }
    });
}

function setUserPreference(prefersColorScheme: string, theme: Theme) {
    if (matchMedia(`(prefers-color-scheme: ${prefersColorScheme})`).matches)
        userPreference.value = theme;
}

function savePagePreference(e: Event) {
    let theme: Theme = "light";
    if ((e.target as HTMLInputElement).checked) theme = "dark";
    localStorage.setItem(LS_THEME_KEY, JSON.stringify(theme));
}

// Set user preference from media query
onMounted(() => {
    // Set up some listeners
    // Set up event listeners to check for user preference changes
    addThemeEventListener("light", "light");
    addThemeEventListener("dark", "dark");
    // Events are fired only on change, so set user preference manually on load
    setUserPreference("light", "light");
    setUserPreference("dark", "dark");
});
</script>

<template>
    <span class="switcher-frame">
        <input
            id="theme-select"
            v-model="darkModeEnabled"
            type="checkbox"
            name="theme-select"
            @input="savePagePreference"
        />
        <label for="theme-select" class="switcher-toggle" :class="theme">
            <span class="slider" :class="theme">
                <i class="ri-sun-line light"></i>
                <i class="ri-moon-line dark"></i>
            </span>
        </label>
    </span>
</template>

<style lang="scss" scoped>
#theme-select {
    width: 0;
    height: 0;
    visibility: hidden;
}

.switcher-toggle {
    --size: 20px;
    --pad: 3px;

    width: calc(2.25 * (var(--size) + 2 * var(--pad)));
    padding: 0;
    display: inline-block;
    border: var(--border-width) solid rgba(var(--color-text-rgb), 0.4);
    border-radius: 200px;
    position: relative;
    background-color: rgba(var(--color-text-rgb), 0.1);

    .slider {
        display: block;
        height: var(--size);
        width: var(--size);
        font-size: var(--size);
        line-height: 1;
        padding: 5px;
        box-sizing: content-box;
        background-color: var(--color-text);
        color: var(--color-background);
        border-radius: 200px;
        transition: all 200ms;

        i {
            position: absolute;
            opacity: 0;
            transition:
                opacity 300ms,
                color 200ms;
        }

        &.light i.light {
            opacity: 1;
        }

        &.dark i.dark {
            opacity: 1;
        }
    }
}

input:checked + .switcher-toggle .slider {
    margin-left: 100%;
    transform: translateX(-100%);
}
</style>
