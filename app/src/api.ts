import axios from "axios";

if (!import.meta.env.VITE_API_URL || import.meta.env.VITE_API_URL == "")
    throw "Please specify VITE_API_URL environment variable";

console.log("API URL set to ", import.meta.env.VITE_API_URL);

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
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

export function getGameConfig() {
    return api.get("/game-config");
}

export function postScore(userId: number, username: string, score: number) {
    return api.post("/scores", { user_id: userId, username, score });
}

export function getScore(scoreId: number) {
    return api.get(`/scores/${scoreId}`);
}

export function getTopKScores(k: number = 5) {
    return api.get("/scores/topk", { params: { k } });
}

export function getLatestScores(userId: number, k: number = 5) {
    return api.get("/scores/latest", { params: { user_id: userId, k } });
}

export function getHighscore(userId: number) {
    return api.get("/scores/highscore", { params: { user_id: userId } });
}
