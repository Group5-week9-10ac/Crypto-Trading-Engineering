import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { signupUser } from '../services/apiService'; // Import the signupUser function

const SignUpPage = () => {
    const { register, handleSubmit, reset, formState: { errors } } = useForm();
    const [showAlert, setShowAlert] = useState(false);
    const [alertMessage, setAlertMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const submitForm = async (data) => {
        if (data.password !== data.confirmPassword) {
            setAlertMessage('Passwords do not match');
            setShowAlert(true);
            return;
        }

        setIsLoading(true);

        const body = {
            username: data.username,
            email: data.email,
            password: data.password
        };

        try {
            const response = await signupUser(body.username, body.email, body.password);
            setAlertMessage(response.message);
            setShowAlert(true);
            reset(); // Reset form fields on successful signup
        } catch (error) {
            console.error('Error signing up:', error);
            if (error.response) {
                // Handle HTTP error response from server
                setAlertMessage(error.response.data.message || 'An error occurred during signup. Please try again.');
            } else if (error.request) {
                // Handle network error (no response received)
                setAlertMessage('Network error. Please try again later.');
            } else {
                // Handle other errors
                setAlertMessage('An unexpected error occurred. Please try again.');
            }
            setShowAlert(true);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="form">
                <h1>Sign Up</h1>
                {showAlert && (
                    <Alert variant={alertMessage.includes('success') ? 'success' : 'danger'} onClose={() => setShowAlert(false)} dismissible>
                        <p>{alertMessage}</p>
                    </Alert>
                )}
                <form>
                    <Form.Group>
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text"
                            placeholder="Your username"
                            {...register("username", { required: true, maxLength: 25 })}
                        />
                        {errors.username && <p style={{ color: "red" }}>Username is required</p>}
                        {errors.username?.type === "maxLength" && <p style={{ color: "red" }}>Max characters should be 25</p>}
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email"
                            placeholder="Your email"
                            {...register("email", { required: true, maxLength: 80 })}
                        />
                        {errors.email && <p style={{ color: "red" }}>Email is required</p>}
                        {errors.email?.type === "maxLength" && <p style={{ color: "red" }}>Max characters should be 80</p>}
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password"
                            placeholder="Your password"
                            {...register("password", { required: true, minLength: 8 })}
                        />
                        {errors.password && <p style={{ color: "red" }}>Password is required</p>}
                        {errors.password?.type === "minLength" && <p style={{ color: "red" }}>Min characters should be 8</p>}
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control type="password"
                            placeholder="Your password"
                            {...register("confirmPassword", { required: true, minLength: 8 })}
                        />
                        {errors.confirmPassword && <p style={{ color: "red" }}>Confirm Password is required</p>}
                        {errors.confirmPassword?.type === "minLength" && <p style={{ color: "red" }}>Min characters should be 8</p>}
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={handleSubmit(submitForm)} disabled={isLoading}>{isLoading ? 'Signing up...' : 'Sign Up'}</Button>
                    </Form.Group>
                    <br />
                    <Form.Group>
                        <small>Already have an account? <Link to='/login'>Log In</Link></small>
                    </Form.Group>
                    <br />
                </form>
            </div>
        </div>
    );
};

export default SignUpPage;
