import { Autocomplete, Box, TextField } from "@mui/material";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../css/addPopup.css";

export default function AddPopup({
  onClose,
  event,
}: {
  onClose: () => void;
  event: any;
}) {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(startDate);

    const modules = [
        { label: "Modul 1" },
        { label: "Modul 2" },
    ]
    const trainer = [
        { label: "Trainer 1" },
        { label: "Trainer 2" },
    ]
    const group = [
        { label: "Gruppe 1" },
        { label: "Gruppe 2" },
    ]

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
            onChange={(date: any) => setStartDate(date)}
            className="datepicker"
          />
        </div>
        <div>
          <h4>Ende</h4>
          <DatePicker
            selected={endDate}
            onChange={(date: any) => setEndDate(date)}
            className="datepicker"
          />
        </div>
        <div>
          <Autocomplete
            disablePortal
            options={modules}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Modul" />}
          />
        </div>
        <div>
                      <Autocomplete
            disablePortal
            options={trainer}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Trainer" />}
          />
        </div>
        <div>
                                  <Autocomplete
            disablePortal
            options={group}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Group" />}
          />
        </div>
      </Box>
    </>
  );
}
