import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Container from "@mui/material/Container";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

type Modul = {
  id: number;
  name: string;
  dauer: string;
  beschreibung: string;
  pcKennzeichnung: boolean;
  verpflichtendeVorgängermodule: (string | number)[];
  optionaleVorgängermodule: (string | number)[];
  zuordnungLernjahr: string;
};

export default function ModulesPage() {
  const [searchParams] = useSearchParams();
  const modulParam = searchParams.get("modul");
  const refs = useRef<Record<string, HTMLDivElement | null>>({});
  const navigate = useNavigate();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [moduleData, setModuleData] = useState<Record<string, Modul>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/modules")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        // API may return an array or an object keyed by id
        const normalized: Record<string, Modul> = Array.isArray(data)
          ? Object.fromEntries(data.map((m: Modul) => [String(m.id), m]))
          : data;
        setModuleData(normalized);
      })
      .catch((err) => {
        console.error("Error fetching modules:", err);
        setError("Module konnten nicht geladen werden.");
      })
      .finally(() => setLoading(false));
  }, []);

  const modulIds = Object.keys(moduleData);

  useEffect(() => {
    if (modulParam && refs.current[modulParam]) {
      refs.current[modulParam]?.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [modulParam, moduleData]);

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
            Module
          </Typography>
        </Toolbar>
      </AppBar>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 8 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 8 }}>
          <Typography color="error">{error}</Typography>
        </Box>
      )}

      {!loading && !error && (
        <Container maxWidth={false} sx={{ py: 3, px: { xs: 2, md: 6 }, display: "flex", justifyContent: "center", minHeight: 0 }}>
          <Box
            sx={{
              width: "100%",
              maxWidth: 1100,
              display: "grid",
              gridTemplateColumns: {
                xs: "1fr",
                sm: "repeat(2, 1fr)",
                md: "repeat(3, 1fr)",
              },
              gap: 2,
              pb: 2,
              alignContent: "start",
            }}
          >
            {modulIds.map((id) => {
              const m = moduleData[id];
              const isHighlight = modulParam === id;
              return (
                <Paper
                  key={id}
                  ref={(el) => {
                    refs.current[id] = el;
                  }}
                  onClick={() => setSelectedId(id)}
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    cursor: "pointer",
                    border: isHighlight ? "2px solid #026291" : "1px solid #e0e0e0",
                    bgcolor: isHighlight ? "#e3f2fd" : "#fff",
                    minWidth: 0,
                    "&:hover": { boxShadow: 4 },
                  }}
                >
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    {id}. {m.name}
                  </Typography>
                  <Typography sx={{ mt: 0.5, color: "text.secondary" }}>
                    {m.dauer} Tage · Lernjahr: {m.zuordnungLernjahr} · PC: {m.pcKennzeichnung ? "ja" : "nein"}
                  </Typography>
                  <Typography
                    sx={{
                      mt: 1,
                      fontSize: "0.875rem",
                      color: "text.secondary",
                      display: "-webkit-box",
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: "vertical",
                      overflow: "hidden",
                    }}
                  >
                    {m.beschreibung}
                  </Typography>
                </Paper>
              );
            })}
          </Box>
        </Container>
      )}

      <Dialog open={!!selectedId} onClose={() => setSelectedId(null)} fullWidth maxWidth="sm">
        {selectedId && moduleData[selectedId] && (
          <>
            <DialogTitle>
              {selectedId}. {moduleData[selectedId].name}
            </DialogTitle>
            <DialogContent>
              <Typography sx={{ mt: 0.5 }}>
                Dauer: {moduleData[selectedId].dauer} Tage
              </Typography>
              <Typography sx={{ mt: 0.5 }}>
                Lernjahr: {moduleData[selectedId].zuordnungLernjahr}
              </Typography>
              <Typography sx={{ mt: 0.5 }}>
                PC erforderlich: {moduleData[selectedId].pcKennzeichnung ? "ja" : "nein"}
              </Typography>
              <Typography sx={{ mt: 2 }}>{moduleData[selectedId].beschreibung}</Typography>

              {moduleData[selectedId].verpflichtendeVorgängermodule.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography sx={{ fontWeight: 600 }}>Verpflichtende Vorgänger-Module:</Typography>
                  <Box sx={{ mt: 0.5 }}>
                    {moduleData[selectedId].verpflichtendeVorgängermodule
                      .map((vid) => `${vid}. ${moduleData[String(vid)]?.name ?? ""}`)
                      .join(", ")}
                  </Box>
                </Box>
              )}

              {moduleData[selectedId].optionaleVorgängermodule.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography sx={{ fontWeight: 600 }}>Optionale Vorgänger-Module:</Typography>
                  <Box sx={{ mt: 0.5 }}>
                    {moduleData[selectedId].optionaleVorgängermodule
                      .map((vid) => `${vid}. ${moduleData[String(vid)]?.name ?? ""}`)
                      .join(", ")}
                  </Box>
                </Box>
              )}
            </DialogContent>
          </>
        )}
      </Dialog>
    </Box>
  );
}