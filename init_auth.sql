-- Create a table for users and their credentials
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role_id INTEGER REFERENCES roles(role_id)
);

-- Insert initial users relevant to your application
INSERT INTO users (username, password, email, full_name, role_id)
VALUES ('admin', 'hashedpassword', 'admin@example.com', 'Admin User', 1);

-- Create roles for access control
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- Insert initial roles
INSERT INTO roles (role_name) VALUES ('admin'), ('user'), ('guest');

-- Grant privileges to roles
CREATE ROLE authenticated_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO authenticated_user;

CREATE ROLE guest_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO guest_user;

-- Assign roles to users
ALTER ROLE authenticated_user IN DATABASE ${POSTGRES_DB} TO admin;
