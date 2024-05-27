export const exclude = (user: Record<string, any>, keys: string[]): Record<string, any> => {
    return Object.fromEntries(
        Object.entries(user).filter(([key]) => !keys.includes(key))
    );
};