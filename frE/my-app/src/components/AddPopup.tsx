import { Autocomplete, Box, Button, TextField } from "@mui/material";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../css/addPopup.css";

export default function AddPopup({
  onClose,
  event,
  onSend,
}: {
  onClose: () => void;
  event: any;
  onSend: (event: any) => void;
}) {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(startDate);
  const [modul, setModul] = useState("");
  const [trainer, setTrainer] = useState("");
  const [group, setGroup] = useState("");

  const modules = [{ label: "Modul 1" }, { label: "Modul 2" }];
  const trainers = [{ label: "Trainer 1" }, { label: "Trainer 2" }];
  const groups = [{ label: "Gruppe 1" }, { label: "Gruppe 2" }];

  function saveEvent() {
    const newEvent = {
      title: modul,
      start: startDate.toDateString().split("T"),
      end: endDate.toDateString().split("T"),
      extendedProps: {
        trainer: [trainer],
        group: group,
      },
    };
    onSend(newEvent);
    console.log("Neuer Kurs:", newEvent);
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
        <h2>Neuen Kurs Eintragen</h2>
        <div>
          <h4>Start</h4>
          <DatePicker
            selected={startDate}
            onChange={(date: any) => {
              setStartDate(date);
            }}
            className="datepicker"
          />
        </div>
        <div>
          <h4>Ende</h4>
          <DatePicker
            selected={endDate}
            onChange={(date: any) => setEndDate(date)}
            className="datepicker"
            highlightDates={[startDate]}
          />
        </div>
        <div>
          <Autocomplete
            disablePortal
            options={modules}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Modul" />}
            onChange={(value: any) => setModul(value.target.innerText)}
          />
        </div>
        <div>
          <Autocomplete
            multiple
            disablePortal
            options={trainers}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Trainer" />}
            onChange={(value: any) => setTrainer(value.target.innerText)}
          />
        </div>
        <div>
          <Autocomplete
            disablePortal
            options={groups}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Group" />}
            onChange={(value: any) => setGroup(value.target.innerText)}
          />
        </div>
        <Button
          variant="contained"
          sx={{ backgroundColor: "#0C2F6F" }}
          onClick={() => {
            saveEvent();
          }}
        >
          Speichern
        </Button>
      </Box>
    </>
  );
}
