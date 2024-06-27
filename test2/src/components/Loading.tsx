import React from "react";
import { ClipLoader } from "react-spinners";
import Box from "@mui/material/Box";


const Loading = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "80vh",
        backgroundColor: "background.default",
        color: "text.primary",
      }}
    >
      <div>
        <p>Loading, please wait...</p>
      </div>
      <ClipLoader
        color="#2f89fc"
        loading={true}
        size={100}
        cssOverride={{ display: "block", margin: "0 auto", borderColor: "#2f89fc" }}
      />
    </Box>
  );
};

export default Loading;
