"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const dotenv = __importStar(require("dotenv"));
const express_1 = __importDefault(require("express"));
const http_1 = __importDefault(require("http"));
const body_parser_1 = __importStar(require("body-parser"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const compression_1 = __importDefault(require("compression"));
const cors_1 = __importDefault(require("cors"));
const user_router_1 = __importDefault(require("./router/user.router"));
const auth_router_1 = __importDefault(require("./router/auth.router"));
const configuration_router_1 = __importDefault(require("./router/configuration.router"));
const sources_router_1 = __importDefault(require("./router/sources.router"));
dotenv.config();
if (!process.env.PORT) {
    process.exit(1);
}
const PORT = parseInt(process.env.PORT, 10);
const app = (0, express_1.default)();
const corsOptions = {
    // origin: "*",
    origin: true,
    optionsSuccessStatus: 200,
    credentials: true
};
// app.use(cors({
//     credentials: true,
//     origin: true,
// }));
app.use((0, cors_1.default)(corsOptions));
app.use((0, compression_1.default)());
app.use((0, cookie_parser_1.default)());
app.use((0, body_parser_1.urlencoded)({
    extended: true
}));
app.use(body_parser_1.default.json());
app.use('/api/v1/auth', auth_router_1.default);
app.use('/api/v1/users', user_router_1.default);
app.use('/api/v1/configuration', configuration_router_1.default);
app.use('/api/v1/sources', sources_router_1.default);
const server = http_1.default.createServer(app);
server.listen(PORT, () => {
    console.log(`Listening on port: ${PORT}`);
});
//# sourceMappingURL=index.js.map