import { Box, Stack, Typography } from "@mui/material";
import React from "react";

const details = () => {
  return (
    <Stack direction="column" gap={5} pb={5}>
      <section id="approach1"></section>
      <Typography variant="h3" sx={{ fontWeight: "bold" }}>
        Approach 1
      </Typography>
      <Stack direction="column" gap={3} px={3} py={1}>
        <Typography variant="body1">
          This approach involves initial enhancements to both contrast and white
          balance. For contrast, the image is converted to grayscale followed by
          histogram equalization. For white balance, corrections are made based
          on the gray world method, which assumes that the average of all colors
          in a scene naturally tends towards gray over the entire image. This is
          particularly useful in underwater settings where color casts can be
          prevalent due to varying depths and water conditions.
        </Typography>
        <Typography variant="body1">
          Furthermore, the approach uses luminance, saliency, and chromatic
          weight maps. These maps are designed to enhance different perceptual
          features of the image. Luminance weights help in adjusting brightness
          levels, saliency weights emphasize important features and edges, and
          chromatic weights enhance color vividness. Combined, these adjustments
          yield a well-balanced, visually pleasing image that significantly
          improves upon the original underwater photographs.
        </Typography>
        <img src="/assets/approach 1.png" alt="Approach 1" />
      </Stack>
      <section />
      <section id="approach2">
        <Typography variant="h3" sx={{ fontWeight: "bold" }}>
          Approach 2
        </Typography>
        <Stack direction="column" gap={3} px={3} py={1}>
          <Typography variant="body1">
            The second approach focuses on adaptive contrast enhancement and
            color normalization. Unlike traditional methods, this technique
            utilizes Contrast Limited Adaptive Histogram Equalization (CLAHE),
            which prevents over-amplification of noise by limiting
            contrastenhancement in homogeneous areas of the image. Additionally,
            color normalization adjusts each color channel to its 99th
            percentile, ensuring that the brightest colors are adjusted to pure
            white. This method effectively reduces the typical bluish or
            greenish cast seen in underwater images, leading to more natural and
            accurate color representation.
          </Typography>
          <img src="/assets/approach 2.png" alt="Approach 2" />
        </Stack>
      </section>
    </Stack>
  );
};

export default details;
