import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "http://<error>",
    withCredentials: true,
});

export function login(username: string) {
    return api.post("/login", { username });
}

export function getWordList(count: number = 5) {
    return api.get("/words", {
        params: { count },
    });
}
