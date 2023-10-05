export interface Word {
    id: number;
    form_infinitive: string;
    form_simple_past: string;
    form_past_participle: string;
    translation: string;
    difficulty: number;
}

export interface Answer {
    form_infinitive: string;
    form_simple_past: string;
    form_past_participle: string;
}

export type WordFormKey = "form_infinitive" | "form_simple_past" | "form_past_participle";
export const wordFormKeys: WordFormKey[] = [
    "form_infinitive",
    "form_simple_past",
    "form_past_participle",
];
export const wordFormNames = {
    form_infinitive: "Infinitive",
    form_simple_past: "Simple Past",
    form_past_participle: "Past Participle",
};

export function emptyAnswer(): Answer {
    return {
        form_infinitive: "",
        form_simple_past: "",
        form_past_participle: "",
    };
}
