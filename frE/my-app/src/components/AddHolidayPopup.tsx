import { Box, Button } from "@mui/material";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../css/addPopup.css";

export default function AddHolidayPopup({
  onClose,
  event,
  id,
}: {
  onClose: () => void;
  event: any;
  id: string;
}) {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(startDate);

  function writeHoliday() {
    const newHoliday = {
      start: startDate.toISOString().split("T")[0],
      end: endDate.toISOString().split("T")[0],
      trainerId: event.id,
    };
    fetch("/api/setHolidays", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newHoliday),
    });
  }

  return (
    <>
      <Box
        onClick={onClose}
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: "rgba(161, 161, 161, 0.5)",
          zIndex: 1299,
        }}
      />
      <Box
        onClick={(e) => e.stopPropagation()}
        sx={{
          position: "fixed",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: "#f3f3f3",
          padding: 3,
          borderRadius: 2,
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.2)",
          zIndex: 1300,
          maxWidth: "45vw",
          width: "90%",
          height: "60vh",
        }}
      >
        <>
          <h2>Urlaub für {event.name} eintragen</h2>
          <p>Von</p>
          <DatePicker
            selected={startDate}
            onChange={(date: Date | null) => {
              if (date) setStartDate(date);
            }}
            filterDate={(date) => date.getDay() !== 0 && date.getDay() !== 6}
          />
          <p>Bis</p>
          <DatePicker
            selected={endDate}
            onChange={(date: Date | null) => {
              if (date) setEndDate(date);
            }}
            filterDate={(date) => date.getDay() !== 0 && date.getDay() !== 6}
            highlightDates={[startDate]}
          />
          <div style={{ marginTop: "20px" }}>
            <Button variant="contained" onClick={() => writeHoliday()}>
              Eintragen
            </Button>
          </div>
        </>
      </Box>
    </>
  );
}
