import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Stack,
  Typography,
} from "@mui/material";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";
import React from "react";

type filtredImageType = {
  approach1: string;
  approach2: string;
};

type PopupProps = {
  open: boolean;
  handleClose: () => void;
  filtredImage: filtredImageType;
};

const Popup = ({ open, handleClose, filtredImage }: PopupProps) => {
  //  Download Image
  const downloadImage = (image: string) => {
    const link = document.createElement("a");
    link.href = image;

    var date = new Date();
    var dateString =
      date.getFullYear() +
      "-" +
      (date.getMonth() + 1).toString().padStart(2, "0") +
      "-" +
      date.getDate().toString().padStart(2, "0") +
      "_" +
      date.getHours().toString().padStart(2, "0") +
      "-" +
      date.getMinutes().toString().padStart(2, "0") +
      "-" +
      date.getSeconds().toString().padStart(2, "0");

    link.download = `enhanced_${dateString}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      aria-labelledby="form-dialog-title"
      sx={{ "& .MuiDialog-paper": { width: "600px" } }}
    >
      <DialogTitle id="form-dialog-title">Choose an Approach</DialogTitle>
      <DialogContent>
        <Stack direction="row" justifyContent="space-between" my={2}>
          <Button
            component="label"
            variant="contained"
            disabled={filtredImage.approach1 === ""}
            tabIndex={-1}
            startIcon={<CloudDownloadIcon />}
            onClick={() => downloadImage(filtredImage.approach1)}
            sx={{ p: 1 }}
          >
            <Typography
              variant="body1"
              fontFamily={"poppins"}
              fontWeight={300}
              fontSize={14}
              align="center"
              sx={{ width: "100%" }}
            >
              Approach 1
            </Typography>
          </Button>
          <a
            target="_blank"
            style={{
              textDecoration: "underline",
              cursor: "pointer",
              color: "blue",
            }}
            href="/details#approach1"
          >
            more details {">"}
          </a>
        </Stack>
        <Stack direction="row" justifyContent="space-between">
          <Button
            component="label"
            variant="contained"
            disabled={filtredImage.approach2 === ""}
            tabIndex={-1}
            startIcon={<CloudDownloadIcon />}
            onClick={() => downloadImage(filtredImage.approach2)}
            sx={{ p: 1 }}
          >
            <Typography
              variant="body1"
              fontFamily={"poppins"}
              fontWeight={300}
              fontSize={14}
              align="center"
              sx={{ width: "100%" }}
            >
              Approach 2
            </Typography>
          </Button>
          <a
            target="_blank"
            style={{
              textDecoration: "underline",
              cursor: "pointer",
              color: "blue",
            }}
            href="/details#approach2"
          >
            more details {">"}
          </a>
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          Cancel
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default Popup;
