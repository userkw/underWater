import React, { useEffect, useRef, useState } from "react";
import { Button, Card, CardActions, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import toast from "react-hot-toast";

const UploadFile = ({ onImageChange }: any) => {
  const inputRef = useRef<any>(null);
  const [imageUrl, setImageUrl] = useState<string | ArrayBuffer | null>(null);
  const imageExtensions = ["jpeg", "png", "jpg"];

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    e.preventDefault();
    console.log("File has been added");
    const file = e.target.files ? e.target.files[0] : null;
    if (file) {
      const fileSplited = file.name.split(".");
      const fileExtension = fileSplited[fileSplited.length - 1];
      if (e.target.files && file) {
        if (imageExtensions.includes(fileExtension)) {
          const reader = new FileReader();
          reader.onload = (event) => {
            setImageUrl(event.target?.result as string);
            onImageChange(event.target?.result as string);
          };
          reader.onerror = (error) => {
            console.error("Error reading file:", error);
          };
          reader.readAsDataURL(file);
        } else {
          toast.error(
            "File extension error (your image should have .png, .jpeg, .jpg) "
          );
        }
      }
    }
  }

  function openFileExplorer() {
    inputRef.current.value = "";
    inputRef.current.click();
  }
  return (
    <>
      <form>
        <Card
          sx={{
            width: 400,
            minHeight: 250,
            borderRadius: "16px",
            boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.3)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          <CardActions sx={{ justifyContent: "center", padding: 1 }}>
            <input
              placeholder="fileInput"
              className="hidden"
              ref={inputRef}
              type="file"
              multiple={false}
              onChange={handleChange}
              accept="image/*"
            />
            <Button
              component="label"
              variant="contained"
              tabIndex={-1}
              startIcon={<CloudUploadIcon />}
              onClick={openFileExplorer}
              sx={{ px: 2, py: 1 }}
            >
              <Typography
                variant="body1"
                fontFamily={"poppins"}
                fontWeight={500}
                fontSize={20}
                align="center"
                sx={{ width: "100%" }}
              >
                Upload Your Image
              </Typography>
            </Button>
          </CardActions>
          <CardActions sx={{ justifyContent: "center", padding: 1 }}>
            <Typography
              variant="body1"
              fontFamily={"poppins"}
              fontWeight={500}
              fontSize={16}
              color={"#40514e"}
              align="center"
              sx={{ width: "100%" }}
            >
              Or
            </Typography>
          </CardActions>

          <CardActions sx={{ justifyContent: "center", padding: 1 }}>
            <Typography
              variant="body1"
              fontFamily={"poppins"}
              fontWeight={500}
              fontSize={18}
              color={"#40514e"}
              align="center"
              sx={{ width: "100%" }}
            >
              Drag and Drop an image
            </Typography>
          </CardActions>
        </Card>
      </form>
    </>
  );
};

export default UploadFile;
