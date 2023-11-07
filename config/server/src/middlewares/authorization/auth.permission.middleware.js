const jwt = require('jsonwebtoken'),
secret = require('../../config/env.config')['jwt_secret'];
const ADMIN_PERMISSION = require('../../config/env.config')['permissionLevels']['ADMIN'];

exports.minimumPermissionLevelRequired = (required_permission_level) => {
    return (req, res, next) => {
        console.log('permission level:' + req.jwt.permissionLevel)
        let user_permission_level = parseInt(req.jwt.permissionLevel);
        let userId = req.jwt.userId;
        console.log(user_permission_level);
        console.log(required_permission_level);
        if (user_permission_level & required_permission_level) {
            return next();
        } else {
            console.log('Niet voldoende rechten');
            return res.status(403).send();
        }
    };
};

exports.onlySameUserOrAdminCanDoThisAction = (req, res, next) => {
    let user_permission_level = parseInt(req.jwt.permissionLevel);
    let userId = req.jwt.userId;
    let paramsId = req.params.id;
    console.log('req.jwt.userid: ' + req.jwt.userId);
    console.log('req.params.id: ' + paramsId);
    console.log('req.params object' + req.params);
    if (req.params && req.params.id && userId == paramsId) {
        return next();
    } else {
        if (user_permission_level & ADMIN_PERMISSION) {
            return next();
        } else {
            console.log('user is geen admin en user_permission_level klopt niet');
            return res.status(403).send();
        }
    }

};

exports.sameUserCantDoThisAction = (req, res, next) => {
    let userId = req.jwt.userId;
    if (req.params.userId !== userId) {
        return next();
    } else {
        return res.status(400).send();
    }
};