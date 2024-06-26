import React from "react";
import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavbarPage";
import CreatebackPage from "./components/CreateBacktestPage";
import SignUpPage from "./components/SignUpPage";
import LoginPage from "./components/LoginPage";
import HomePage from "./components/HomePage";
import PrivateRoute from "./utils/PrivateRoute";

function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/createbacktest" element={<PrivateRoute component={CreatebackPage} />} />
      </Routes>
    </>
  );
}

export default App;


