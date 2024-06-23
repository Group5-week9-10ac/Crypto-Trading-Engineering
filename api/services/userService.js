const User = require('../models/User');

async function createUser(username, password) {
    try {
        const user = await User.create({
            username,
            password_hash: hashPassword(password),
        });
        return user;
    } catch (error) {
        console.error('Error creating user:', error);
        throw error;
    }
}

async function findUserByUsername(username) {
    try {
        const user = await User.findOne({
            where: { username },
        });
        return user;
    } catch (error) {
        console.error('Error finding user by username:', error);
        throw error;
    }
}

module.exports = {
    createUser,
    findUserByUsername,
};
