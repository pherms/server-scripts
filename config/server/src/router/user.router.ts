import express from "express";
import { createUser, getAllUsers, getUserByEmail, updateUserById, deleteUserById } from "../controllers/user.controller";
const PermissionMiddleware = require('../middlewares/authorization/auth.permission.middleware');
const ValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');
const config = require('../config/env.config');

const ADMIN = config.permissionLevels.ADMIN;
const PAID = config.permissionLevels.PAID_USER;
const FREE = config.permissionLevels.NORMAL_USER;

const router = express.Router();

router.post('/', createUser);

router.get('/', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    getAllUsers
]);
router.get('/:emailAddress', [
    // ValidationMiddleware.validJWTNeeded,
    // PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    // PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    getUserByEmail
]);
router.put('/:id', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(FREE),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    updateUserById
]);
router.delete('/:id', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    deleteUserById
]);

export default router;
