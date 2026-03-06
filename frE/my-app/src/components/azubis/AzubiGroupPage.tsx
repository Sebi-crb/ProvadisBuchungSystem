import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Container from "@mui/material/Container";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Paper from "@mui/material/Paper";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
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
const moduleData = data.Module as Record<string, { title: string }>;

export default function AzubiGroupPage() {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [modalAzubi, setModalAzubi] = useState<Azubi | null>(null);
  const [search, setSearch] = useState("");

  const gid = groupId ?? "";
  const gruppe = gruppen[gid];

  const filteredAzubis = useMemo(() => {
    if (!gruppe) {
      return [];
    }
    const term = search.trim().toLowerCase();
    if (!term) {
      return gruppe.azubis;
    }
    return gruppe.azubis.filter((a) =>
      a.name.toLowerCase().includes(term)
    );
  }, [gruppe, search]);

  function openModul(modulId: string) {
    navigate(`/modules?modul=${modulId}`);
    setModalAzubi(null);
  }

  if (!gruppe) {
    return (
      <Box
        sx={{
          position: "fixed",
          inset: 0,
          bgcolor: "#f6f7f9",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <AppBar position="sticky" sx={{ bgcolor: "#026291" }}>
          <Toolbar>
            <IconButton color="inherit" edge="start" onClick={() => navigate("/azubis")}>
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="h6" sx={{ ml: 1 }}>
              Azubis
            </Typography>
          </Toolbar>
        </AppBar>
        <Box sx={{ p: 3 }}>
          <Typography>Gruppe nicht gefunden.</Typography>
        </Box>
      </Box>
    );
  }

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
          <IconButton color="inherit" edge="start" onClick={() => navigate("/azubis")}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h6" sx={{ ml: 1 }}>
            Gruppe {gid}
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth={false} sx={{ py: 3, px: { xs: 2, md: 6 }, display: "flex", justifyContent: "center" }}>
        <Box sx={{ width: "100%", maxWidth: 800 }}>
          <AzubiSearchField
            value={search}
            onChange={setSearch}
            placeholder="Azubi in dieser Gruppe suchen..."
          />

          <Paper sx={{ borderRadius: 2, mt: 2 }}>
            <List dense disablePadding>
              {filteredAzubis.map((a) => (
                <ListItemButton key={a.id} onClick={() => setModalAzubi(a)}>
                  <ListItemText
                    primary={a.name}
                    secondary={`${a.unternehmen} • Ausbildungsjahr ${a.ausbildungsjahr}`}
                  />
                </ListItemButton>
              ))}
            </List>
          </Paper>
        </Box>
      </Container>

      <Dialog open={!!modalAzubi} onClose={() => setModalAzubi(null)} fullWidth maxWidth="sm">
        {modalAzubi && (
          <>
            <DialogTitle>{modalAzubi.name}</DialogTitle>
            <DialogContent>
              <Typography sx={{ mt: 0.5 }}>
                <strong>Unternehmen:</strong> {modalAzubi.unternehmen}
              </Typography>
              <Typography sx={{ mt: 0.5 }}>
                <strong>Ausbildungsjahr:</strong> {modalAzubi.ausbildungsjahr}
              </Typography>

              <Typography sx={{ mt: 2, mb: 1 }}>
                <strong>Abgeschlossene Module</strong>
              </Typography>

              <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                {modalAzubi.abgeschlosseneModule.map((mid) => (
                  <Chip
                    key={mid}
                    label={moduleData[mid]?.title || `Modul ${mid}`}
                    onClick={() => openModul(mid)}
                    sx={{ bgcolor: "#026291", color: "white" }}
                  />
                ))}
              </Box>
            </DialogContent>
          </>
        )}
      </Dialog>
    </Box>
  );
}

