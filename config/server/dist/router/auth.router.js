"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const VerifyUserMiddleware = require('../middlewares/authorization/verify.user.middleware');
const AuthorizationController = require('../controllers/authorization.controller');
const AuthValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');
const router = express_1.default.Router();
router.post('/', [
    VerifyUserMiddleware.hasAuthValidFields,
    VerifyUserMiddleware.isPasswordAndUserMatch,
    AuthorizationController.login
]);
router.post('/refresh', [
    AuthValidationMiddleware.validJWTNeeded,
    AuthValidationMiddleware.verifyRefreshBodyField,
    AuthValidationMiddleware.validRefreshNeeded,
    AuthorizationController.login
]);
exports.default = router;
//# sourceMappingURL=auth.router.js.map