import { Autocomplete, Box, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import "react-datepicker/dist/react-datepicker.css";
import "../css/addPopup.css";
import BookCours from "./BookCourse";

export default function PickRoom({
  onClose,
  slot,
  trainer,
  mId,
  group,
  onSend,
}: {
  onClose: () => void;
  slot: any;
  trainer: any;
  mId: any;
  group: any;
  onSend: (slot: any) => void;
}) {

    const [rooms, setRooms] = useState([]);

    useEffect(() => {
        console.log(trainer)
    fetch("/api/getRoomForSlot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "start": slot.start, "moduleId": mId }),
    })
    .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json(); 
    })
    .then((data) => {
        console.log("Success:", data);
        setRooms(data)
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}, [])

function bookCourse(room){
        fetch("/api/book_course", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "start": slot.start, "moduleId": mId, "roomId": room.id, "groupId": group.id, "trainerId": trainer.id }),
    })
    .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json(); 
    })
    .then((data) => {
        console.log("Success:", data);
        setRooms(data)
    })
    .catch((error) => {
        console.error("Error:", error);
    });
    
}
  
  return (
    <>
      <Box
        onClick={onClose}
        sx={{
          position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: "rgba(161, 161, 161, 0.5)", zIndex: 1600,
        }}
      />
      <Box
        onClick={(e) => e.stopPropagation()}
        sx={{
          position: "fixed", top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: "#f3f3f3", padding: 3, borderRadius: 2,
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.2)",
          zIndex: 1601, maxWidth: "45vw", width: "90%", height: "60vh",
        }}
      >
        <h2>Raum wählen</h2>
        <div
  style={{
    display: "flex",
    flexWrap: "wrap",
    gap: "12px",
    marginTop: "12px",
  }}
>
          {rooms.map((room, index) => (
    <button
      key={index}
      style={{
        padding: "8px 14px",
        borderRadius: "6px",
        border: "1px solid #ccc",
        background: "rgb(53, 111, 236)",
        cursor: "pointer",
      }}
      onClick={()=> {bookCourse(room)}}
    >
      {room.name} 
    </button>
  ))}
  </div>
      </Box>
    </>
  );
}