import { Box } from "@mui/material";


export default function Popup({
  onClose,
  event,
}: {
  onClose: () => void;
  event: any;
}) {

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
          <h4>Trainer:</h4>
          {event?.extendedProps?.trainer?.map((trainer: any) => (
            <p>{trainer}</p>
          ))}
        </div>
        <div style={{ float: "left", marginLeft: "5vw" }}>
          <h4>Azubis:</h4>
          <div>
            {event?.extendedProps?.gruppe?.azubis.map((azubi: any) => (
              <p style={{ margin: 0 }}>{azubi.name}</p>
            ))}
          </div>
        </div>
        <div>
            Raum: {event?.extendedProps?.raum}
        </div>
        <div>
            Zeitspanne: {event?.startStr.split("T")[0]} - {event?.endStr.split("T")[0]}
        </div>
      </Box>
    </>
  );
}
