<script setup lang="ts">
import { computed, ref } from "vue";

const navbarShown = ref<boolean>(false);
const navbarMobileClass = computed(() => (navbarShown.value ? "mobile-shown" : "mobile-hidden"));
</script>

<template>
    <nav class="navbar" :class="navbarMobileClass">
        <div class="navbar-mobile-topbar">
            <span class="name">Bring Brang Brung</span>
            <button class="mobile-toggle-button" @click="navbarShown = !navbarShown">
                <i class="ri-menu-line"></i>
            </button>
        </div>
        <ul class="navbar-items" :class="navbarMobileClass">
            <li class="li-name">
                <span class="name">Bring Brang Brung</span>
            </li>
            <span class="sep">|</span>
            <li>
                <RouterLink :to="{ name: 'home' }" @click="navbarShown = false"
                    ><i class="ri-home-line"></i> Home</RouterLink
                >
            </li>
            <li>
                <RouterLink :to="{ name: 'learn' }" @click="navbarShown = false"
                    ><i class="ri-play-line"></i> Resume Round</RouterLink
                >
            </li>
            <li>
                <RouterLink :to="{ name: 'leaderboard' }" @click="navbarShown = false"
                    ><i class="ri-vip-crown-line"></i> Leaderboard</RouterLink
                >
            </li>
        </ul>
    </nav>
</template>

<style lang="scss" scoped>
@import "@/assets/base.scss";
@import "@/assets/main.scss";

.navbar-items {
    margin: 0;
    padding: 0;
    list-style-type: none;
    text-align: center;
    margin: var(--padding-lg);
    display: flex;
    gap: var(--gap-lg);
    justify-content: center;
    overflow: hidden;

    transition:
        max-height 200ms,
        background-color 200ms;
}

.name {
    font-family: var(--font-headings);
}

.navbar-mobile-topbar {
    display: none;
}

@media screen and (max-width: $bp-mobile) {
    .li-name {
        display: none;
    }

    .navbar-items {
        gap: var(--gap-sm);
    }

    .mobile-hidden .navbar-items {
        max-height: 0;
    }

    nav {
        transition:
            background-color 200ms,
            color 200ms;
    }

    nav.mobile-shown {
        background-color: var(--color-accent-primary);
        color: var(--color-contrast-primary);

        a {
            color: var(--color-contrast-primary);
        }
    }

    .mobile-shown .navbar-items {
        max-height: 30em;
    }

    .mobile-toggle-button {
        --color: 0, 0, 0;
        @include button-style-outlined-inv(var(--color), var(--color-text), 0, #0003);
        padding: var(--padding-sm);
        line-height: 1;
    }

    .navbar-mobile-topbar {
        display: block;
        margin: var(--padding-lg);
        position: relative;
        text-align: center;

        button {
            position: absolute;
            right: 0;
            top: 0;
        }
    }

    .navbar-items {
        flex-direction: column;
    }

    .sep {
        display: none;
    }
}
</style>
