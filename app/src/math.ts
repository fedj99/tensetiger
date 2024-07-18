export function lerp(min: number, max: number, frac: number, clamp: boolean = true) {
    const res = min + (max - min) * frac;

    if (clamp) {
        return Math.min(Math.max(res, min), max);
    }

    return res;
}

export function invlerp(min: number, max: number, value: number, clamp: boolean = true) {
    const res = (value - min) / (max - min);

    if (clamp) {
        return Math.min(Math.max(res, 0), 1);
    }

    return res;
}
