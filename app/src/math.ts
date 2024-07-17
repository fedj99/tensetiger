export function lerp(min: number, max: number, frac: number, clamp: boolean = true) {
    const res = min + (max - min) * frac;

    if (clamp) {
        return Math.min(Math.max(res, min), max);
    }

    return res;
}
