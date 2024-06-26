import React from "react";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

const Portfoliolink = () => (
  <>
    <Nav.Item>
      <Link className="nav-link" to="/createbacktest">
        Create Backtest
      </Link>
    </Nav.Item>
    <Nav.Item>
      <Link className="nav-link" to="/modern_portfolio">
        Portfolio
      </Link>
    </Nav.Item>
    <Nav.Item>
      <Link className="nav-link" to="/forecast">
        forecast
      </Link>
    </Nav.Item>

    <Nav.Item>
      <a className="nav-link" href="#" onClick={() => console.log("Log Out")}>
        Log Out
      </a>
    </Nav.Item>
  </>
);

const LoggedInLinks = () => (
  <>
    <Nav.Item>
      <Link className="nav-link" to="/createbacktest">
        Create Backtest
      </Link>
    </Nav.Item>
    <Nav.Item>
      <a className="nav-link" href="#" onClick={() => console.log("Log Out")}>
        Log Out
      </a>
    </Nav.Item>
  </>
);


const LoggedOutLinks = () => (
  <>
    <Nav.Item>
      <Link className="nav-link" to="/signup">
        Sign Up
      </Link>
    </Nav.Item>
    <Nav.Item>
      <Link className="nav-link" to="/login">
        Login
      </Link>
    </Nav.Item>
  </>
);

const NavBar = () => {
  const logged = false; // Replace with actual authentication logic

  return (
    <Navbar bg="dark" variant="dark" style={{ marginTop: "20px" }}>
      <Container>
        <Navbar.Brand as={Link} to="/">
          Home
        </Navbar.Brand>
        <Nav className="me-auto">
          {logged ? <LoggedInLinks /> : <LoggedOutLinks />}
          <Portfoliolink />
        </Nav>
      </Container>
    </Navbar>
  );
};

export default NavBar;
