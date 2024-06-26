import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { useForm } from 'react-hook-form';
import { signupUser } from '../services/apiService'; // Correct import

const SignupPage = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async (data) => {
    setIsLoading(true);

    try {
      const response = await signupUser(data.username, data.email, data.password);
      // Handle successful signup, e.g., store tokens
      console.log('Signup success:', response);
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
          <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>
            <p>{alertMessage}</p>
          </Alert>
        )}
        <form onSubmit={handleSubmit(onSubmit)}>
          <Form.Group>
            <Form.Label>Username</Form.Label>
            <Form.Control type="text"
              placeholder="Your username"
              {...register("username", { required: true })}
            />
            {errors.username && <p style={{ color: "red" }}>Username is required</p>}
          </Form.Group>
          <br />
          <Form.Group>
            <Form.Label>Email</Form.Label>
            <Form.Control type="email"
              placeholder="Your email"
              {...register("email", { required: true })}
            />
            {errors.email && <p style={{ color: "red" }}>Email is required</p>}
          </Form.Group>
          <br />
          <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control type="password"
              placeholder="Your password"
              {...register("password", { required: true })}
            />
            {errors.password && <p style={{ color: "red" }}>Password is required</p>}
          </Form.Group>
          <br />
          <Button type="submit" variant="primary" disabled={isLoading}>{isLoading ? 'Signing up...' : 'Sign Up'}</Button>
        </form>
      </div>
    </div>
  );
};

export default SignupPage;

