import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Azubis from "./pages/Azubis";
import AzubiGroup from "./pages/AzubiGroup.tsx";
import Trainers from "./pages/Trainers";
import "./App.css";
import Modules from "./pages/Modules";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/azubis" element={<Azubis />} />
        <Route path="/azubis/group/:groupId" element={<AzubiGroup />} />
        <Route path="/trainers" element={<Trainers />} />
        <Route path="/modules" element={<Modules />} />
      </Routes>
    </>
  );
}

export default App;
