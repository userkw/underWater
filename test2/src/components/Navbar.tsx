import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Box } from "@mui/material";
import toast from "react-hot-toast";
import { useRouter } from "next/router";

const Navbar: React.FC = () => {
  const router = useRouter();
  return (
    <Box sx={{ boxShadow: 3, zIndex: 100 }}>
      <AppBar
        position="static"
        sx={{
          backgroundColor: "white",
        }}
      >
        <Toolbar sx={{ height: "10vh", justifyContent: "center" }}>
          <Typography variant="h5" sx={{flexGrow: 1,  color: "black" }}>
            <a href="/">
              Under Water Filter
            </a>
          </Typography>

          <Button
            sx={{ color: "black", fontWeight: "bold" }}
            onClick={() => {
              toast.success("Apply a filter to your photo now");
              router.push("/");
            }}
          >
            Image Filter
          </Button>
          <Button
            sx={{ color: "black", fontWeight: "bold" }}
            onClick={() =>
              toast.error("Video Filter is not available at this time")
            }
          >
            Video Filter
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
