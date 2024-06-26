import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { useForm } from 'react-hook-form';
import { loginUser } from '../services/apiService'; // Import the loginUser function
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const { register, handleSubmit, reset, formState: { errors } } = useForm();
    const [show, setShow] = useState(false);
    const [serverResponse, setServerResponse] = useState('');
    const navigate = useNavigate();

    const submitForm = async (data) => {
        try {
            const response = await loginUser(data.username, data.password);
            localStorage.setItem('jwtToken', response.token); // Store JWT token
            navigate('/'); // Redirect to home or another protected route
        } catch (error) {
            console.error('Error logging in:', error);
            setServerResponse('Invalid username or password.');
            setShow(true);
        }
        reset();
    };

    return (
        <div className="container">
            <div className="form">
                {show && (
                    <Alert variant="danger" onClose={() => setShow(false)} dismissible>
                        <p>{serverResponse}</p>
                    </Alert>
                )}
                <h1>Login</h1>
                <form>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Your username"
                            {...register("username", { required: true })}
                        />
                        {errors.username && <small style={{ color: "red" }}>Username is required</small>}
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Your password"
                            {...register("password", { required: true })}
                        />
                        {errors.password && <small style={{ color: "red" }}>Password is required</small>}
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={handleSubmit(submitForm)}>Login</Button>
                    </Form.Group>
                    <br />
                </form>
            </div>
        </div>
    );
};

export default LoginPage;

