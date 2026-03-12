import { Autocomplete, Box, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../css/addPopup.css";

export default function AddPopup2({
  onClose,
  slot,
  mId,
  onSend,
}: {
  onClose: () => void;
  slot: any;
  mId: any;
  onSend: (slot: any) => void;
}) {

    useEffect(() => {
        console.log(slot.start)
        console.log(mId)
        fetch("/api/getTrainerForSlot", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({"start": slot.start, "moduleId" : mId}),
          });
    }, [])
  
  return (
    <>
      <Box
        onClick={onClose}
        sx={{
          position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: "rgba(161, 161, 161, 0.5)", zIndex: 1503,
        }}
      />
      <Box
        onClick={(e) => e.stopPropagation()}
        sx={{
          position: "fixed", top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: "#f3f3f3", padding: 3, borderRadius: 2,
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.2)",
          zIndex: 1504, maxWidth: "45vw", width: "90%", height: "60vh",
        }}
      >
        <h2>Trainer wählen</h2>
        
      </Box>
    </>
  );
}