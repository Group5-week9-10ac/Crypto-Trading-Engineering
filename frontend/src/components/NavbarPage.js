import React from "react";
import { Link, useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

const handleLogout = (navigate) => {
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken');
  navigate('/login'); // Use navigate instead of window.location.href
};

const LoggedInLinks = ({ navigate }) => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/createbacktest">
          Create Backtest
        </Link>
      </li>
      <li className="nav-item">
        <button className="nav-link active" onClick={() => handleLogout(navigate)}>
          Log Out
        </button>
      </li>
    </>
  );
};

const LoggedOutLinks = () => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/signup">
          Sign Up
        </Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link active" to="/login">
          Login
        </Link>
      </li>
    </>
  );
};

const NavbarPage = () => {
  const token = localStorage.getItem('token');
  const logged = !!token;
  const navigate = useNavigate();

  return (
    <Navbar bg="dark" variant="dark" style={{ marginTop: "20px" }}>
      <Container>
        <Navbar.Brand href="/">Home</Navbar.Brand>
        <Nav className="me-auto">
          {logged ? <LoggedInLinks navigate={navigate} /> : <LoggedOutLinks />}
        </Nav>
      </Container>
    </Navbar>
  );
};

export default NavbarPage;
