import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "http://<error>",
});

export function getWordList(count: number = 5) {
    return api.get("/words", {
        params: { count },
    });
}
