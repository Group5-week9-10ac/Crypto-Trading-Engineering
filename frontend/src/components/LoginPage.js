import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { loginUser } from '../services/apiService';

const LoginPage = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async (data) => {
    setIsLoading(true);

    try {
      const response = await loginUser(data.username, data.password);
      console.log('Login success:', response);
    } catch (error) {
      console.error('Error logging in:', error);
      if (error.response) {
        setAlertMessage(error.response.data.message || 'An error occurred during login. Please try again.');
      } else if (error.request) {
        setAlertMessage('Network error. Please try again later.');
      } else {
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
        <h1>Login</h1>
        {showAlert && (
          <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>
            <p>{alertMessage}</p>
          </Alert>
        )}
        <form onSubmit={handleSubmit(onSubmit)}>
          <Form.Group>
            <Form.Label>Username or Email</Form.Label>
            <Form.Control type="text"
              placeholder="Your username or email"
              {...register("username", { required: true })}
            />
            {errors.username && <p style={{ color: "red" }}>Username or Email is required</p>}
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
          <Button type="submit" variant="primary" disabled={isLoading}>{isLoading ? 'Logging in...' : 'Log In'}</Button>
          <br />
          <Form.Group>
            <small>Don't have an account? <Link to='/signup'>Sign Up</Link></small>
          </Form.Group>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;


