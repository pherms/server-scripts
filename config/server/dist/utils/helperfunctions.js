"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.exclude = void 0;
const exclude = (user, keys) => {
    return Object.fromEntries(Object.entries(user).filter(([key]) => !keys.includes(key)));
};
exports.exclude = exclude;
//# sourceMappingURL=helperfunctions.js.map