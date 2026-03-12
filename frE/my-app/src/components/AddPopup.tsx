import { Autocomplete, Box, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
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
  const [modul, setModul] = useState<{ label: string; id: number } | null>(null);
  const [trainer, setTrainer] = useState<string[]>([]);
  const [group, setGroup] = useState<{ label: string; id: number }[]>([]);

  const [trainerOptions, setTrainerOptions] = useState<{ label: string }[]>([]);
  const [groupOptions, setGroupOptions] = useState<{ label: string; id: number }[]>([]);
  const [moduleOptions, setModuleOptions] = useState<{ label: string; id: number }[]>([]);

  function saveEvent() {
    const newEvent = {
      title: modul?.label ?? "",
      start: startDate.setHours(8, 0, 0, 0),
      end: endDate.setHours(16, 30, 0, 0),
      extendedProps: {
        modulId: modul?.id,
        trainer: trainer,
        group: group.map((g) => g.id),
      },
    };
    onSend(newEvent);
    console.log("Neuer Kurs:", newEvent);
    onClose();
  }

  useEffect(() => {
    fetch("/api/trainers")
      .then((response) => response.json())
      .then((data) => {
        const formattedTrainers = data.map((trainer: any) => ({
          label: trainer.vorname + " " + trainer.nachname,
        }));
        setTrainerOptions(formattedTrainers);
      });
      fetch("/api/modules/1")
      .then((response) => response.json())
      .then((data) => {
        console.log("allowedModules", data)
      });

    fetch("/api/gruppen")
      .then((response) => response.json())
      .then((data) => {
        const formattedGroups = data.map((group: any) => ({
          label: group.name,
          id: group.id,
        }));
        setGroupOptions(formattedGroups);
      });

    fetch("/api/modules")
      .then((response) => response.json())
      .then((data) => {
        // API returns an object keyed by id, not an array — use Object.values()
        const formattedModules = Object.values(data).map((m: any) => ({
          label: m.name,
          id: m.id,
        }));
        setModuleOptions(formattedModules);
      });
  }, []);

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
          zIndex: 1500,
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
          zIndex: 1501,
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
            onChange={(date: any) => setStartDate(date)}
            filterDate={(date) => date.getDay() !== 0 && date.getDay() !== 6}
          />
        </div>
        <div>
          <h4>Ende</h4>
          <DatePicker
            selected={endDate}
            onChange={(date: any) => setEndDate(date)}
            filterDate={(date) => date.getDay() !== 0 && date.getDay() !== 6}
            highlightDates={[startDate]}
          />
        </div>
        <div>
          <Autocomplete
            disablePortal
            options={moduleOptions}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Modul" />}
            onChange={(_, newValue) => {
              setModul(newValue); // store full object so MUI can render the selected label
            }}
          />
        </div>
        <div>
          <Autocomplete
            multiple
            disablePortal
            options={trainerOptions}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Trainer" />}
            onChange={(_, newValue) => {
              setTrainer(newValue.map((option) => option.label));
            }}
          />
        </div>
        <div>
          <Autocomplete
            multiple
            disablePortal
            options={groupOptions}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Group" />}
            onChange={(_, newValue) => {
              setGroup(newValue);
            }}
          />
        </div>
        <Button
          variant="contained"
          sx={{ backgroundColor: "#0C2F6F" }}
          onClick={saveEvent}
        >
          Speichern
        </Button>
      </Box>
    </>
  );
}