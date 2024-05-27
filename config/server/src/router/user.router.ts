import express from "express";
import { createUser, getAllUsers, getUserByEmail, getUserByID, updateUserById, deleteUserById } from "../controllers/user.controller";
const PermissionMiddleware = require('../middlewares/authorization/auth.permission.middleware');
const ValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');
const config = require('../config/env.config');

const ADMIN = config.permissionLevels.ADMIN; // Admin level
const PAID = config.permissionLevels.PAID_USER; // User met hogere permissies
const FREE = config.permissionLevels.NORMAL_USER; // Standaard gebruiker

const router = express.Router();

router.post('/', createUser);

router.get('/:emailAddress', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    getUserByEmail
]);
router.get('/:userId', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    getUserByID
]);
router.get('/', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    getAllUsers
]);
router.patch('/:userId', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(PAID),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    updateUserById
]);
router.delete('/:userId', [
    ValidationMiddleware.validJWTNeeded,
    PermissionMiddleware.minimumPermissionLevelRequired(ADMIN),
    PermissionMiddleware.onlySameUserOrAdminCanDoThisAction,
    deleteUserById
]);

export default router;
