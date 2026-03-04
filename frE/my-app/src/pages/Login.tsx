import { Button } from "@mui/material";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

export default function Login() {
  return (
    <>
      <Box
        component="section"
        sx={{
          backgroundColor: "#026291",
          width: "20vw",
          height: "40vh",
          boxShadow: "5px 10px 12px rgba(0, 0, 0, 0.1)",
        }}
      >
        <h2 style={{ marginTop: "5px" }}>Login</h2>
        <TextField
          id="username"
          label="Username"
          variant="outlined"
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
        <input type="submit" value="Login" />
      </Box>
    </>
  );
}
