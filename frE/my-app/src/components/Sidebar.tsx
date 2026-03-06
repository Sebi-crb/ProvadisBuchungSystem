import { Button, Drawer } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function Sidebar() {

    const navigate = useNavigate();

  return (
    <div  style={{ width: "180px" }}>
      <Drawer
        variant="permanent"
        anchor="right"
        sx={{
          "& .MuiDrawer-paper": {
            width: "180px",
            flexShrink: 0,
            color: "white",
            backgroundColor: "#026291",
            boxSizing: "border-box",
          },
          color: "white",
        }}
      >
        <Button onClick={() => null} sx={{ color: "white", marginTop: 5 }}>
          User
        </Button>
        <Button
          onClick={() => navigate("/azubis")}
          sx={{ color: "white", marginTop: 10 }}
        >
          Azubi
        </Button>
        <Button
          onClick={() => navigate("/trainers")}
          sx={{ color: "white", marginTop: 5 }}
        >
          Trainer
        </Button>
        <Button
          onClick={() => navigate("/modules")}
          sx={{ color: "white", marginTop: 5 }}
        >
          Module
        </Button>
      </Drawer>
      </div>
  );
}