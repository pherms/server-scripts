const crypto = require('crypto');
// import { db } from '../../utils/db.server';
const db = require('../../utils/db.server').db;

exports.hasAuthValidFields = (req, res, next) => {
    let errors = [];

    if (req.body) {
        if (!req.body.emailAddress) {
            errors.push('Email adres is leeg');
        }
        if (!req.body.password) {
            errors.push('Password is niet ingevuld');
        }

        if (errors.length) {
            return res.status(400).send({errors: errors.join(',')});
        } else {
            return next();
        }
    } else {
        return res.status(400).send({errors: 'Ontbrekende email en password'});
    }
};

exports.isPasswordAndUserMatch = async (req, res, next) => {
    await db.user.findMany({
        where: {
            emailAddress: req.body.emailAddress,
        }
    })
    .then((user) => {
        if(!user[0]) {
            res.status(400).send({});
        } else {
            let passwordFields = user[0].password.split('$');
            let salt = passwordFields[0];
            let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
            if (hash === passwordFields[1]) {
                req.body = {
                    userId: user[0].id,
                    emailAddress: user[0].emailAddress,
                    permissionLevel: user[0].permissionLevel,
                    provider: 'email',
                    name: user[0].firstName + ' ' + user[0].lastName,
                };
                return next();
            } else {
                return res.status(400).send({errors: ['Invalid email or password']});
            }
        }
    });
};