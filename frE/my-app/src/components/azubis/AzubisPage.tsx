import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import data from "../../responses/azubiPageSrc.json";
import AzubiSearchField from "./AzubiSearchField";

type Azubi = {
  id: number;
  name: string;
  unternehmen: string;
  abgeschlosseneModule: string[];
  ausbildungsjahr: string;
};

const gruppen = data.Gruppen as Record<string, { azubis: Azubi[] }>;

export default function AzubisPage() {
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  const gruppenIds = useMemo(() => Object.keys(gruppen), []);

  const filteredGruppen = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) {
      return gruppenIds;
    }
    return gruppenIds.filter((gid) => {
      if (gid.toLowerCase().includes(term)) {
        return true;
      }
      return gruppen[gid].azubis.some((a) =>
        a.name.toLowerCase().includes(term)
      );
    });
  }, [search, gruppenIds]);

  return (
    <Box
      sx={{
        position: "fixed",
        inset: 0,
        bgcolor: "#f6f7f9",
        overflow: "auto",
      }}
    >
      <AppBar position="sticky" sx={{ bgcolor: "#026291" }}>
        <Toolbar>
          <IconButton color="inherit" edge="start" onClick={() => navigate("/home")}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h6" sx={{ ml: 1 }}>
            Azubis
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth={false} sx={{ py: 3, px: { xs: 2, md: 6 }, display: "flex", justifyContent: "center" }}>
        <Box sx={{ width: "100%", maxWidth: 1100 }}>
          <AzubiSearchField
            value={search}
            onChange={setSearch}
            placeholder="Gruppe oder Azubi suchen..."
          />

          <Box
            sx={{
              mt: 2,
              display: "grid",
              gridTemplateColumns: {
                xs: "1fr",
                sm: "repeat(2, 1fr)",
                md: "repeat(3, 1fr)",
              },
              gap: 2,
            }}
          >
            {filteredGruppen.map((gid) => {
              const azubis = gruppen[gid].azubis;
              const years = Array.from(
                new Set(azubis.map((a) => a.ausbildungsjahr))
              ).sort();
              return (
                <Paper
                  key={gid}
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    cursor: "pointer",
                    "&:hover": { boxShadow: 4 },
                  }}
                  onClick={() => navigate(`/azubis/group/${gid}`)}
                >
                  <Typography variant="h6">Gruppe {gid}</Typography>
                  <Typography sx={{ mt: 0.5, color: "text.secondary" }}>
                    {azubis.length} Azubis
                  </Typography>
                  <Typography sx={{ mt: 0.5, color: "text.secondary" }}>
                    Ausbildungsjahre: {years.join(", ")}
                  </Typography>
                </Paper>
              );
            })}
          </Box>
        </Box>
      </Container>
    </Box>
  );
}
