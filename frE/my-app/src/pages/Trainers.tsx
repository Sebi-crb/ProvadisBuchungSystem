import { useEffect } from "react";
import Sidebar from "../components/Sidebar";

export default function Trainers() {
  useEffect(() => {
    fetch("/api/trainers")
      .then((response) => response.json())
      .then((data) => {
        console.log("Rohdaten der Trainer:", data);
      });
  }, []);

  return (
    <>
    <Sidebar/>
    </>
  );
}