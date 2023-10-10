import axios from "axios";
import { type GameConfig, type Score } from "./rules";
import type { Word } from "./words";

interface User {
    id: number;
    username: string;
    last_logon: string;
}

if (!import.meta.env.VITE_API_URL || import.meta.env.VITE_API_URL == "")
    throw "Please specify VITE_API_URL environment variable";

console.log("API URL set to ", import.meta.env.VITE_API_URL);

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
});

export function login(username: string, password: string) {
    return api.post<{
        success: boolean;
        user: User;
    }>("/login", { username, password });
}

export function logout() {
    return api.post("/logout");
}

export function getUser(id: number) {
    return api.get<User>(`/users/${id}`);
}

export function getWordList() {
    return api.get<Word[]>("/words/batch");
}

export function getGameConfig() {
    return api.get<GameConfig>("/game-config");
}

export function postScore(userId: number, username: string, score: number) {
    return api.post("/scores", { user_id: userId, username, score });
}

export function getScore(scoreId: number) {
    return api.get<Score>(`/scores/${scoreId}`);
}

export function getTopKScores(k: number = 5) {
    return api.get<Score[]>("/scores/topk", { params: { k } });
}

export function getLatestScores(userId: number, k: number = 5) {
    return api.get<Score[]>("/scores/latest", { params: { user_id: userId, k } });
}

export function getHighscore(userId: number) {
    return api.get<Score>("/scores/highscore", { params: { user_id: userId } });
}
