import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username === "user" && password === "user") {
      localStorage.setItem("role", "user");
      navigate("/home");
    } else if (username === "admin" && password === "admin") {
      localStorage.setItem("role", "admin");
      navigate("/home");
    } else {
      alert("Ungültige Anmeldedaten");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        width: "100%",
      }}
    >
      <Box
        component="form"
        onSubmit={handleLogin}
        sx={{
          backgroundColor: "#026291",
          width: "20vw",
          minWidth: "300px",
          height: "40vh",
          boxShadow: "5px 10px 12px rgba(0, 0, 0, 0.1)",
          padding: "20px",
          borderRadius: "8px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <h2 style={{ marginTop: "5px" }}>Login</h2>
        <TextField
          id="username"
          label="Username"
          variant="outlined"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          sx={{
            margin: "20px",
            "& .MuiOutlinedInput-root": {
              "& fieldset": { borderColor: "white" },
              "&:hover fieldset": { borderColor: "white" },
              "&.Mui-focused fieldset": { borderColor: "white" },
            },
            "& .MuiInputLabel-root": { color: "rgba(255,255,255,0.8)" },
            "& .MuiInputLabel-root.Mui-focused": { color: "white" },
            "& .MuiOutlinedInput-input": { color: "white" },
          }}
        />
        <TextField
          id="password"
          label="Password"
          type="password"
          variant="outlined"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{
            margin: "20px",
            "& .MuiOutlinedInput-root": {
              "& fieldset": { borderColor: "white" },
              "&:hover fieldset": { borderColor: "white" },
              "&.Mui-focused fieldset": { borderColor: "white" },
            },
            "& .MuiInputLabel-root": { color: "rgba(255,255,255,0.8)" },
            "& .MuiInputLabel-root.Mui-focused": { color: "white" },
            "& .MuiOutlinedInput-input": { color: "white" },
          }}
        />
        <Button
          type="submit"
          variant="contained"
          sx={{
            marginTop: "20px",
            backgroundColor: "white",
            color: "#026291",
            "&:hover": { backgroundColor: "#f0f0f0" },
          }}
        >
          Login
        </Button>
      </Box>
    </Box>
  );
}
