import { use, useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import TrainerCard from "../components/Card";
import { Box, Dialog } from "@mui/material";
import { data } from "react-router-dom";

export default function Trainers() {

  const [trainers, setTrainers] = useState([]);


  useEffect(() => {
    fetch("/api/trainers")
      .then((response) => response.json())
      .then((data) => {
        setTrainers(data);
      });
  }, []);



  return (
    <>
      <Sidebar />
      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          gap: 3,
          padding: 4,
          justifyContent: "flex-start",
        }}
      >
        {trainers.map((trainer: any) => (
          <TrainerCard key={trainer.id} name={trainer.vorname + " " + trainer.nachname} id={trainer.id} />
        ))}
      </Box>

    </>
  );
}
