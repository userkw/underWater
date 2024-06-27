import { Box, Stack, Typography } from "@mui/material";
import React from "react";

const ImageCadre = ({ imageUrl, title }: any) => {
  return (
    <Stack direction={"column"} gap={2}>
      <Typography
        variant={"h5"}
        fontFamily={"poppins"}
        fontWeight={500}
        color={"#40514e"}
        align="center"
        sx={{ lineHeight: 1.2, w: { sm: "90%", md: "70%" } }}
      >
        {title}
      </Typography>

      {/* Original Image */}
      <Box
        sx={{
          width: { xs: "200px", md: "300px" },
          height: { xs: "200px", md: "300px" },
          overflow: "hidden",
          border: "1px solid #ccc",
          padding: "4px",
        }}
      >
        <img
          src={imageUrl.toString()}
          alt="Your Image"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        />
      </Box>
    </Stack>
  );
};

export default ImageCadre;
