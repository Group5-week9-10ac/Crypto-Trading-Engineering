import "./App.css";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavbarPage";
import CreatebackPage from "./components/CreateBacktestPage";
import SignUpPage from "./components/SignUpPage";
import LoginPage from "./components/LoginPage";
import HomePage from "./components/HomePage";
import PrivateRoutes from "./utils/PrivateRoute";

function App() {
  return (
    <>
      <NavBar />

      <Routes>
        <Route element={<PrivateRoutes />}>
          <Route path="/createbacktest" element={<CreatebackPage />} />
        </Route>
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </>
  );
}

export default App;
