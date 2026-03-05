import { Button } from "@mui/material";
import Drawer from "@mui/material/Drawer";
import { useNavigate } from "react-router-dom";
import Calendar from "../components/Calendar";
import data from "../responses/Homepage.json";

export default function Home() {
  const navigate = useNavigate();
    console.log(data);
    let termine = data.termine;
  return (
    <div>
      <Drawer
        variant="permanent"
        anchor="right"
        sx={{
          "& .MuiDrawer-paper": {
            width: "10vw",
            color: "white",
            backgroundColor: "#026291",
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
      </Drawer>

      <Calendar termine={termine} gruppen={data.Gruppen} />
    </div>
  );
}
