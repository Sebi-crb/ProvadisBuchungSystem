import { Box, Button } from "@mui/material";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AddPopup from "./AddPopup";

export default function Popup({
  onClose,
  event,
}: {
  onClose: () => void;
  event: any;
}) {
  const navigate = useNavigate();
  const formattedEventStructure = {
    titel: event.title,
    start: event.start,
    end: event.end,
    groupId: event.extendedProps.groupId,
  };
  const [showAddPopup, setShowAddPopup] = useState(false);

  const [trainer, setTrainer] = useState(null);
  const [gruppe, setGruppe] = useState(null);

  useEffect(() => {
    let moduleId = event.extendedProps.moduleId;
    const kurse = JSON.parse(sessionStorage.getItem("kurse"));
    let kursData = kurse[moduleId];

    fetch("/api/trainers")
      .then((res) => res.json())
      .then((data) => {
        data.forEach((trainerIndex) => {
          if (trainerIndex.id == event.extendedProps.trainerId) {
            console.log(trainerIndex);
            setTrainer(trainerIndex);
          }
        });
      })
      .catch((err) => console.error("Fetch error:", err));

    fetch("/api/gruppen")
      .then((res) => res.json())
      .then((data) => {
        data.forEach((gruppenIndex) => {
          if (gruppenIndex.id == event.extendedProps.groupId) {
            setGruppe(gruppenIndex);
          }
        });
      })
      .catch((err) => console.error("Fetch error:", err));
  }, []);

  function addNewEvent() {
    setShowAddPopup(true);
  }

  function writeNewEventToDB() {}

  return (
    <>
      {showAddPopup && (
        <AddPopup
          onClose={() => setShowAddPopup(false)}
          event={null}
          onSend={writeNewEventToDB}
        />
      )}
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
        <h2>{event?.title}</h2>
        <div style={{ float: "right", marginRight: "5vw" }}>
          <h4
            onClick={() => navigate("/trainers")}
            style={{
              cursor: "pointer",
              color: "#1976d2",
              display: "inline-block",
              textDecoration: "underline",
            }}
            onMouseOver={(e) => (e.currentTarget.style.textDecoration = "none")}
            onMouseOut={(e) =>
              (e.currentTarget.style.textDecoration = "underline")
            }
          >
            Trainer:
          </h4>
          <br></br>
          {trainer ? `${trainer.vorname} ${trainer.nachname}` : "Laden..."}{" "}
        </div>
        <div style={{ float: "left", marginLeft: "5vw" }}>
          <h4
            onClick={() => navigate("/azubis")}
            style={{
              cursor: "pointer",
              color: "#1976d2",
              display: "inline-block",
              textDecoration: "underline",
            }}
            onMouseOver={(e) => (e.currentTarget.style.textDecoration = "none")}
            onMouseOut={(e) =>
              (e.currentTarget.style.textDecoration = "underline")
            }
          >
            Gruppe:
          </h4>
          <div>
            {gruppe && (
              <p key={gruppe.id}>
                <a href={`/azubis/group/${gruppe.id}`}>{gruppe.name}</a>
              </p>
            )}
          </div>
        </div>
        <div>Raum: {event?.extendedProps?.raum}</div>
        <div>
          Zeitspanne: {event?.startStr.split("T")[0]} -{" "}
          {event?.endStr.split("T")[0]}
        </div>
        <Button
          sx={{ marginTop: "400px" }}
          variant="outlined"
          onClick={() => addNewEvent()}
        >
          Bearbeiten
        </Button>
      </Box>
    </>
  );
}
