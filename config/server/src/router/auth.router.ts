import express from 'express';

const VerifyUserMiddleware = require('../middlewares/authorization/verify.user.middleware');
const AuthorizationController = require('../controllers/authorization.controller');
const AuthValidationMiddleware = require('../middlewares/authorization/auth.validation.middleware');

const router = express.Router();

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

export default router;