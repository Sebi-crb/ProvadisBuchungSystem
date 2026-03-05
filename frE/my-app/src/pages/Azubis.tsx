import { Fab } from "@mui/material";
import { useNavigate } from "react-router-dom";
import data from "../responses/Azubis.json";

export default function Azubis() {
  function openAzubiDetails(azubiKey: any) {
    console.log("Azubi:", azubiKey);
  }
  const navigate = useNavigate();

  return (
    <>
      <Fab
        onClick={() => navigate("/home")}
        color="primary"
        sx={{
          position: "absolute",
          top: 10,
          left: 10,
        }}
      >
        {"<-"}
      </Fab>
      {data.groups.map((group, groupIndex) => (
        <div key={groupIndex}>
          <h2>
            Group {group.gruppenId} - Block {group.block}
          </h2>
          {group.azubis.map((azubi, azubiIndex) => (
            <div
              key={azubiIndex}
              onClick={() => {
                openAzubiDetails(azubiIndex);
              }}
            >
              <div style={{ margin: 5 }}>
                <p style={{ margin: 0 }}> {azubi.name}</p>
                <p style={{ margin: 0 }}>{azubi.unternehmen}</p>
                <p style={{ margin: 0 }}>
                  {" "}
                  {"lehrjahr " + azubi.ausbildungsjahr}
                </p>
              </div>
            </div>
          ))}
        </div>
      ))}
    </>
  );
}
