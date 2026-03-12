import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import UserIcon from "@mui/icons-material/Person";
import Typography from "@mui/material/Typography";
import AddHolidayPopup from "./AddHolidayPopup";
import { useState } from "react";

export default function TrainerCard({ name, id }: { name: string; id: string }) {
  const [showPopup, setShowPopup] = useState(false);

  const isAdmin = sessionStorage.getItem("role") === "admin";

  return (
    <>
      {showPopup && (
        <AddHolidayPopup
          onClose={() => setShowPopup(false)}
          event={{ name, id }}
        />
      )}

      <Card
        sx={{
          maxWidth: 345,
          width: "30vw",
          borderRadius: 4,
          boxShadow: "0px 4px 20px rgba(5, 4, 5, 0.5)",
          cursor: isAdmin ? "pointer" : "default",
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
          "&:hover": isAdmin
            ? {
                transform: "translateY(-6px)",
                boxShadow: "0px 10px 30px rgba(4, 4, 5, 0.5)",
              }
            : {},
        }}
        {...(isAdmin && {
          onClick: () => {
            setShowPopup(true);
          },
        })}
      >
        <CardMedia
          component="div"
          sx={{
            height: 140,
            backgroundColor: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <UserIcon sx={{ fontSize: 60, color: "gray" }} />
        </CardMedia>

        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {name}
          </Typography>
        </CardContent>

        <CardActions />
      </Card>
    </>
  );
}
