import { Autocomplete, Box, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../css/addPopup.css";
import AddPopup2 from "./AddPopup2";

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
  const [group, setGroup] = useState<{ label: string; id: number } | null>(null); 

  const [trainerOptions, setTrainerOptions] = useState<{ label: string }[]>([]);
  const [groupOptions, setGroupOptions] = useState<{ label: string; id: number }[]>([]);
  const [moduleOptions, setModuleOptions] = useState<{ label: string; id: number }[]>([]);
  const [slots, setSlots] = useState([])

  const [showPopup2, setShowPopup2] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState();

  function saveEvent() {
    if (!modul || !group) return;
    const newEvent = {
      title: modul.label,
      start: new Date(startDate).setHours(8, 0, 0, 0), 
      end: new Date(endDate).setHours(16, 30, 0, 0),
      extendedProps: {
        modulId: modul.id,
        trainer: trainer,
        group: group.id,
      },
    };
    onSend(newEvent);
    onClose();
  }

  useEffect(() => {
    fetch("/api/trainers")
      .then((res) => res.json())
      .then((data) => {
        setTrainerOptions(data.map((t: any) => ({ label: `${t.vorname} ${t.nachname}` })));
      });

    fetch("/api/gruppen")
      .then((res) => res.json())
      .then((data) => {
        setGroupOptions(data.map((g: any) => ({ label: g.name, id: g.id })));
      });
  }, []);


  useEffect(() => {
    if (!group) return;

    fetch("/api/modules")
      .then((res) => res.json())
      .then((data) => {
        const allModules: { label: string; id: number }[] = Object.values(data).map((m: any) => ({
          label: m.name,
          id: m.id,
        }));

        fetch(`/api/getAllowedModules/${group.id}`)
          .then((res) => res.json())
          .then((allowedIds: number[]) => {
            const filtered = allModules.filter((m) => allowedIds.includes(m.id));
            setModuleOptions(filtered);
            setModul(null); 
          });
      });
  }, [group]);

  useEffect(() => {
    if (!group || !modul) return;

    fetch(`/api/getGroupModuleTimeSlot/${group.id}/${modul.id}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("slots", data);
        setSlots(data)
      });
  }, [group, modul]);


  function openNextPopup(slot){
    setSelectedSlot(slot)
    setShowPopup2(true);
  }

  return (
    <>
    {showPopup2 &&( <AddPopup2 group={group} onClose={() => setShowPopup2(false)} slot={selectedSlot} mId={modul.id}/>)}
      <Box
        onClick={onClose}
        sx={{
          position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: "rgba(161, 161, 161, 0.5)", zIndex: 1500,
        }}
      />
      <Box
        onClick={(e) => e.stopPropagation()}
        sx={{
          position: "fixed", top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: "#f3f3f3", padding: 3, borderRadius: 2,
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.2)",
          zIndex: 1501, maxWidth: "45vw", width: "90%", height: "60vh",
        }}
      >
        <h2>Neuen Kurs Eintragen</h2>
        <div
  style={{
    display: "flex",
    flexWrap: "wrap",
    gap: "12px",
    marginTop: "12px",
  }}
>
  {slots.map((slot, index) => (
    <button
      key={index}
      style={{
        padding: "8px 14px",
        borderRadius: "6px",
        border: "1px solid #ccc",
        background: "rgb(53, 111, 236)",
        cursor: "pointer",
      }}
      onClick={()=> openNextPopup(slot)}
    >
      {slot.start} - {slot.end}
    </button>
  ))}
</div>
        <div style={{marginTop: "40px"}}>
          <Autocomplete
            disablePortal options={groupOptions} sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Group" />}
            onChange={(_, newValue) => setGroup(newValue)}
          />
        </div>
        <div>
          <Autocomplete
            multiple disablePortal options={trainerOptions} sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Trainer" />}
            onChange={(_, newValue) => setTrainer(newValue.map((o) => o.label))}
          />
        </div>
        <div>
          <Autocomplete
            disablePortal options={moduleOptions} sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Modul" />}
            value={modul} 
            onChange={(_, newValue) => setModul(newValue)}
          />
        </div>
        <Button
          variant="contained" sx={{ backgroundColor: "#0C2F6F" }}
          onClick={saveEvent}
          disabled={!group || !modul} 
        >
          Speichern
        </Button>
      </Box>
    </>
  );
}