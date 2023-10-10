import { type AxiosError } from "axios";
import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

export const useErrorsStore = defineStore("errors", () => {
    const router = useRouter();

    const _error = ref<AxiosError | null>(null);
    const _status = ref<number>(0);

    const error = computed(() => _error);
    const status = computed(() => _status);

    function setError(err: AxiosError) {
        console.error(err);

        _status.value = err.response?.status || err.status || 0;
        _error.value = err;

        const route = { name: "generic-error" };
        if (_status.value == 400) route.name = "bad-request";
        else if (_status.value == 404) route.name = "not-found";
        else if (_status.value == 500) route.name = "internal-server-error";

        router.replace(route);
    }

    function unsetError() {
        _error.value = null;
    }

    return {
        error,
        status,
        setError,
        unsetError,
    };
});
