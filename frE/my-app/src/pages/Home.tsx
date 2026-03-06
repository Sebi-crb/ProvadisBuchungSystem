import { useNavigate } from "react-router-dom";
import Calendar from "../components/Calendar";
import data from "../responses/Homepage.json";
import Sidebar from "../components/Sidebar";
import { Box } from "@mui/material";

export default function Home() {
  const navigate = useNavigate();
  console.log(data);
  let termine = data.termine;
  return (
<Box sx={{ display: "flex", flexDirection: "row" }}>
  <Calendar termine={termine} gruppen={data.gruppen} />
  <Sidebar />
</Box>
  );
}
