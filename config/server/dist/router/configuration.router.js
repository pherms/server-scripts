"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const configuration_controller_1 = require("../controllers/configuration.controller");
const PermissionMiddleware = require('../middlewares/authorization/auth.permission.middleware');
const ValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');
const config = require('../config/env.config');
const ADMIN = config.permissionLevels.ADMIN;
const PAID = config.permissionLevels.PAID_USER;
const FREE = config.permissionLevels.NORMAL_USER;
const router = express_1.default.Router();
router.get('/', configuration_controller_1.getConfiguration);
router.put('/', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(ADMIN),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    configuration_controller_1.updateConfiguration
]);
exports.default = router;
//# sourceMappingURL=configuration.router.js.map