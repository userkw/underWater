import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { Box, Button, Stack, Typography } from "@mui/material";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";
import ClearIcon from "@mui/icons-material/Clear";
import toast from "react-hot-toast";
import { Loading, UploadFile, Popup, ImageCadre } from "@/components";

type filtredImageType = {
  approach1: string;
  approach2: string;
};

const index = () => {
  const [imageUrl, setImageUrl] = useState<string | ArrayBuffer | null>(null);
  const [filtredImageUrl, setFiltredImageUrl] = useState<filtredImageType>({
    approach1: "",
    approach2: "",
  });
  const [goodRespense, isGoodRespense] = useState<boolean>(false);
  const [error, isError] = useState<boolean>(false);
  const [open, setOpen] = useState(false);
  const router = useRouter();

  // Dialog Popup Control
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  // End Dialog Popup Control

  useEffect(() => {
    const uploadImage = async () => {
      console.log(imageUrl);
      if (!imageUrl) return;
      fetch("http://127.0.0.1:5000/filter-image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: imageUrl }),
      })
        .then((response) => response.json())
        .then((data) => {
          isError(false);
          console.log("Success:", data);
          setFiltredImageUrl({
            approach1: data.approach1,
            approach2: data.approach2,
          });
          setTimeout(() => isGoodRespense(true), 2000);
        })
        .catch((error) => {
          console.error("Upload error:", error);
          isError(true);
        });
    };
    uploadImage();
  }, [imageUrl]);

  useEffect(() => {
    if (error) {
      toast.error("An error ocupied please later");
      setTimeout(() => window.location.reload(), 1000);
    }
  }, [error]);

  //
  const handleImageChange = (image: string | ArrayBuffer | null) => {
    setImageUrl(image);
  };

  return (
    <>
      {imageUrl == null ? (
        <>
          <Stack direction={{ xs: "column", md: "row" }} gap={4}>
            {/* Left side */}
            <Stack
              direction={"column"}
              justifyContent={"center"}
              alignItems={"center"}
              flex={1}
              gap={4}
              minHeight={{ md: "80vh" }}
            >
              <Box>
                <img
                  src="/assets/gif/spongebob.gif"
                  alt="Description of the GIF"
                  width="350"
                  height="auto"
                />
              </Box>
              {/* Text */}
              <Typography
                variant={"h3"}
                fontFamily={"poppins"}
                fontWeight={700}
                color={"#40514e"}
                align="center"
                sx={{ lineHeight: 1.6, w: { sm: "90%", md: "70%" } }}
              >
                Filter Your{" "}
                <Typography
                  variant={"h3"}
                  component={"span"}
                  fontFamily={"poppins"}
                  fontWeight={700}
                  color={"#2f89fc"}
                  p={1}
                  sx={{ boxShadow: 3, lineHeight: 1.6 }}
                >
                  Under Water
                </Typography>{" "}
                Image
              </Typography>
            </Stack>

            <Box
              className="flex items-center justify-center"
              minHeight={{ md: "80vh" }}
              flex={1}
            >
              <UploadFile onImageChange={handleImageChange} />
            </Box>
          </Stack>
        </>
      ) : (
        <Box>
          {goodRespense ? (
            <Box
              minHeight={"80vh"}
              position={"relative"}
              sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                gap: 4,
              }}
            >
              {/* Reload Button */}
              <Button
                sx={{ position: "absolute", right: "10px", top: "10px" }}
                onClick={() => router.reload()}
              >
                <ClearIcon fontSize="large" sx={{ cursor: "pointer" }} />
              </Button>

              {/* Images */}
              <Stack
                direction={{ xs: "column", md: "row" }}
                gap={5}
                justifyContent={"space-between"}
              >
                <ImageCadre imageUrl={imageUrl} title="Original Image" />
                <ImageCadre
                  imageUrl={filtredImageUrl.approach1}
                  title="Approach 1 Result"
                />
                <ImageCadre
                  imageUrl={filtredImageUrl.approach2}
                  title="Approach 2 Result"
                />
              </Stack>

              {/* Download Button */}
              <Box className="flex items-center justify-center">
                <Button
                  component="label"
                  variant="contained"
                  tabIndex={-1}
                  startIcon={<CloudDownloadIcon />}
                  onClick={handleClickOpen}
                  sx={{ px: 3, py: 2 }}
                >
                  <Typography
                    variant="body1"
                    fontFamily={"poppins"}
                    fontWeight={500}
                    fontSize={20}
                    align="center"
                    sx={{ width: "100%" }}
                  >
                    Download Filtred Image
                  </Typography>
                </Button>
              </Box>

              {/* Popup */}
              <Popup
                open={open}
                handleClose={handleClose}
                filtredImage={filtredImageUrl}
              />
            </Box>
          ) : (
            <Loading />
          )}
        </Box>
      )}
    </>
  );
};

export default index;
