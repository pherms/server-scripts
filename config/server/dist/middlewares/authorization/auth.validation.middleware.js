const jwt = require('jsonwebtoken'),
    secret = require('../../config/env.config.js').jwt_secret,
    crypto = require('crypto');

exports.verifyRefreshBodyField = (req, res, next) => {
    if (req.body && req.body.refresh_token) {
        return next();
    } else {
        return res.status(400).send({error: 'Need to pass refresh_token field'});
    }
};

exports.validRefreshNeeded = (req, res, next) => {
    let b = Buffer.from(req.body.refresh_token, 'base64');
    let refresh_token = b.toString();
    let hash = crypto.createHmac('sha512', req.jwt.refreshKey).update(req.jwt.userId + secret).digest("base64");
    if (hash === refresh_token) {
        req.body = req.jwt;
        return next();
    } else {
        return res.status(400).send({error: 'Invalid refresh token'});
    }
};

exports.validJWTNeeded = (req, res, next) => {
    console.log(req.headers);
    if (req.headers['authentication']) {
        try {
            let authorization = req.headers['authentication'].split(' ');
            console.log(authorization);
            if (authorization[0] !== 'Bearer') {
                return res.status(401).send();
            } else {
                req.jwt = jwt.verify(authorization[1], secret);
                return next();
            }
        } catch (error) {
            return res.status(403).send(error);
        }
    } else {
        return res.status(401).send();
    }
};