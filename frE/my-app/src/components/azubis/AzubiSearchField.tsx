import SearchIcon from "@mui/icons-material/Search";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

type Props = {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
};

export default function AzubiSearchField({ value, onChange, placeholder }: Props) {
  return (
    <TextField
      fullWidth
      size="small"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      InputProps={{
        startAdornment: (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              mr: 1,
              color: "text.secondary",
            }}
          >
            <SearchIcon fontSize="small" />
          </Box>
        ),
      }}
    />
  );
}

