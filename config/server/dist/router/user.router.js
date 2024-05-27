"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const user_controller_1 = require("../controllers/user.controller");
const PermissionMiddleware = require('../middlewares/authorization/auth.permission.middleware');
const ValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');
const config = require('../config/env.config');
const ADMIN = config.permissionLevels.ADMIN; // Admin level
const PAID = config.permissionLevels.PAID_USER; // User met hogere permissies
const FREE = config.permissionLevels.NORMAL_USER; // Standaard gebruiker
const router = express_1.default.Router();
router.post('/', user_controller_1.createUser);
router.get('/:emailAddress', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    user_controller_1.getUserByEmail
]);
router.get('/:userId', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    user_controller_1.getUserByID
]);
router.get('/', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    user_controller_1.getAllUsers
]);
router.patch('/:userId', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    user_controller_1.updateUserById
]);
router.delete('/:userId', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(ADMIN),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    user_controller_1.deleteUserById
]);
exports.default = router;
//# sourceMappingURL=user.router.js.map