import React from "react";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

const LoggedInLinks = () => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link  active" to="/createbacktest">
          Create Backtest
        </Link>
      </li>
      <li className="nav-item">
        <a className="nav-link active" href="#">
          Log Out
        </a>
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

const NavBar = () => {
  // const [logged] = useAuth();

  const logged = true;

  return (
    <Navbar bg="dark" data-bs-theme="dark" style={{ marginTop: "20px" }}>
      <Container>
        <Navbar.Brand href="/">Home</Navbar.Brand>
        <Nav className="me-auto">
          {logged ? <LoggedInLinks /> : <LoggedOutLinks />}
        </Nav>
      </Container>
    </Navbar>
  );
};

export default NavBar;
