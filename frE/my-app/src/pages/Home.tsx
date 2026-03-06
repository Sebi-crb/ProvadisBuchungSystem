import { useNavigate } from "react-router-dom";
import Calendar from "../components/Calendar";
import data from "../responses/Homepage.json";
import Sidebar from "../components/Sidebar";

export default function Home() {
  const navigate = useNavigate();
  console.log(data);
  let termine = data.termine;
  return (
    <div>
      <Sidebar/>
      <Calendar termine={termine} gruppen={data.Gruppen} />
    </div>
  );
}
