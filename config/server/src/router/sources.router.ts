import express from 'express';
import { getSources, updateSources } from '../controllers/sources.controller';
const PermissionMiddleware = require('../middlewares/authorization/auth.permission.middleware');
const ValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');
const config = require('../config/env.config');

const ADMIN = config.permissionLevels.ADMIN;
const PAID = config.permissionLevels.PAID_USER;
const FREE = config.permissionLevels.NORMAL_USER;

const router = express.Router();

router.get('/', getSources);

router.put('/', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(ADMIN),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    updateSources
]);

export default router;