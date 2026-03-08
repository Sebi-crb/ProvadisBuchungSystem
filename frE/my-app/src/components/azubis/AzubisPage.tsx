import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import AzubiSearchField from "./AzubiSearchField";

type Azubi = {
  id: number;
  vorname: string;
  nachname: string;
  unternehmen: string;
  attendedModules: string[];
  ausbildungsJahr: number;
  block: string;
};

type Gruppe = {
  id: number;
  namen: string;
  block: string;
  attendedModules: string[];
  azubis: Azubi[];
};

export default function AzubisPage() {
  const [gruppen, setGruppen] = useState<Gruppe[]>([]);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/api/gruppenAndAzubis")
      .then((response) => response.json())
      .then((data: Gruppe[]) => {
        setGruppen(data);
      });
  }, []);

  const filteredGruppen = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) {
      return gruppen;
    }
    return gruppen.filter((gruppe) => {
      if (gruppe.namen.toLowerCase().includes(term)) {
        return true;
      }
      if (gruppe.block.toLowerCase().includes(term)) {
        return true;
      }
      return gruppe.azubis.some(
        (a) =>
          a.vorname.toLowerCase().includes(term) ||
          a.nachname.toLowerCase().includes(term),
      );
    });
  }, [search, gruppen]);

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
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => navigate("/home")}
          >
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h6" sx={{ ml: 1 }}>
            Azubis
          </Typography>
        </Toolbar>
      </AppBar>

      <Container
        maxWidth={false}
        sx={{
          py: 3,
          px: { xs: 2, md: 6 },
          display: "flex",
          justifyContent: "center",
        }}
      >
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
            {filteredGruppen.map((gruppe) => {
              const years = Array.from(
                new Set(gruppe.azubis.map((a) => a.ausbildungsJahr)),
              ).sort();
              return (
                <Paper
                  key={gruppe.id}
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    cursor: "pointer",
                    "&:hover": { boxShadow: 4 },
                  }}
                  onClick={() => navigate(`/azubis/group/${gruppe.id}`)}
                >
                  <Typography variant="h6">{gruppe.namen}</Typography>
                  <Typography sx={{ mt: 0.5, color: "text.secondary" }}>
                    Block {gruppe.block}
                  </Typography>
                  <Typography sx={{ mt: 0.5, color: "text.secondary" }}>
                    {gruppe.azubis.length} Azubis
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
