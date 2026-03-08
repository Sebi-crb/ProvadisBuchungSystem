import { Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function Popup({
  onClose,
  event,
}: {
  onClose: () => void;
  event: any;
}) {
  const navigate = useNavigate();

  console.log("infopopup", event);
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
          {event?.extendedProps?.trainer?.map(
            (trainerName: string, index: number) => (
              <p key={index}>{trainerName}</p>
            ),
          )}
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
            {event?.extendedProps?.group?.map((g: { name: string, id: string }) => (
              <p key={g.id}>
                <a href={`/azubis/group/${g.id}`}>
                  {g.name}
                </a>
              </p>
            ))}
          </div>
        </div>
        <div>Raum: {event?.extendedProps?.raum}</div>
        <div>
          Zeitspanne: {event?.startStr.split("T")[0]} -{" "}
          {event?.endStr.split("T")[0]}
        </div>
      </Box>
    </>
  );
}
