import cv2
import numpy as np

class Approach1:
    def __init__(self, image: np.ndarray) -> None:
        """
        Initialize the class with an image

        Args:
            image (numpy.ndarray): The input image expected in BGR format.
        """
        self.image = image

    def enhance_contrast(self) -> np.ndarray:
        """
        Enhance the contrast of an image stored in the instance variable `self.image`. The method
        converts the image to grayscale (if not already), then applies histogram equalization
        to improve the contrast.

        Returns:
            numpy.ndarray: The contrast-enhanced grayscale image.
        """
        # Check if the image is already in grayscale; if not, convert it to grayscale
        if len(self.image.shape) > 2:
            if len(self.image.shape) == 3:
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            else:
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGRA2GRAY)
        else:
            gray = self.image

        # Apply histogram equalization to the grayscale image to enhance contrast
        eq = cv2.equalizeHist(gray)

        return eq

    def white_balance(self) -> np.ndarray:
        """
        Applies white balance correction to an image using the gray world assumption. This method
        adjusts the intensities of the image channels so that the average R, G, and B values across the
        image become approximately equal, simulating a neutral lighting condition.

        Returns:
            numpy.ndarray: The white-balanced BGR image.
        """
        if self.image.shape[2] == 4:
            # Convert BGRA to BGR
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)

        # Convert the image from 8-bit to 32-bit floating point for accurate calculations
        image = self.image.astype(np.float32)

        # Split the image into its Blue, Green, and Red components
        b, g, r = cv2.split(image)

        # Compute the average intensity for each channel
        avg_b = np.mean(b)
        avg_g = np.mean(g)
        avg_r = np.mean(r)

        # Calculate the average intensity of all channels (Gray world assumption)
        gray_value = (avg_b + avg_g + avg_r) / 3

        # Calculate correction factors for each channel to equalize the average intensities
        coeff_b = gray_value / avg_b
        coeff_g = gray_value / avg_g
        coeff_r = gray_value / avg_r

        # Scale each channel by its respective correction factor and clip the results to the valid range
        b = np.clip(b * coeff_b, 0, 255).astype(np.uint8)
        g = np.clip(g * coeff_g, 0, 255).astype(np.uint8)
        r = np.clip(r * coeff_r, 0, 255).astype(np.uint8)

        # Reassemble the corrected channels back into a single BGR image
        balanced_img = cv2.merge([b, g, r])

        return balanced_img

    def luminance_weight_map(self, img: np.ndarray) -> np.ndarray:
        """
        Calculate a luminance weight map from a given image. The method converts the image
        to the YUV color space and uses the luminance channel as weights, normalized to the range [0, 1].

        Args:
            img (numpy.ndarray): The input image. Expected to be in BGR format if it has 3 channels.

        Returns:
            numpy.ndarray: The normalized luminance weights of the image.
        """
        # Convert the image to the YUV color space
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

        # Y channel represents the luminance
        luminance = yuv[:, :, 0]

        # Normalize the luminance channel to use as weights
        luminance_weights = luminance / 255.0

        return luminance_weights

    def saliency_weight_map(self, img: np.ndarray) -> np.ndarray:
        """
        Generates a saliency weight map for an input image using the Laplacian of Gaussian method.
        This function highlights areas of significant intensity change, often corresponding to edges.

        Args:
            img (np.ndarray): An input image in BGR format.

        Returns:
            np.ndarray: A saliency weight map of the image, normalized to the range [0, 1].
        """
        # Convert the image to grayscale
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Use Laplacian of Gaussian for edge detection
        saliency = cv2.Laplacian(gray, cv2.CV_64F)

        # Get the absolute values to form the saliency map
        saliency = np.absolute(saliency)

        # Normalize the saliency map
        saliency = cv2.normalize(
            saliency, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F
        )

        return saliency

    def chromatic_weight_map(self, img: np.ndarray) -> np.ndarray:
        """
        Generates a chromatic weight map for an input image by normalizing the saturation channel
        of its HSV color space representation. This map emphasizes regions with higher color intensity,
        providing a measure of chromaticity.

        Args:
            img (np.ndarray): An input image in BGR format.

        Returns:
            np.ndarray: A chromatic weight map with values normalized between 0 and 1.
        """
        # Convert image to HSV to access the saturation channel
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]  # Saturation channel
        # Normalize the saturation channel to use as weights
        chromatic_weights = saturation / 255.0
        return chromatic_weights

    def apply_weight_maps(
        self,
        img: np.ndarray,
        luminance_map: np.ndarray,
        saliency_map: np.ndarray,
        chromatic_map: np.ndarray,
    ) -> np.ndarray:
        """
        Applies provided weight maps (luminance, saliency, and chromatic) to the lightness channel of
        an image converted to LAB color space. This method enhances the lightness channel by incorporating
        these weights, which reflect different perceptual features of the image.

        Args:
            img (np.ndarray): An input image in BGR format.
            luminance_map (np.ndarray): A weight map based on the luminance of the image.
            saliency_map (np.ndarray): A weight map based on the saliency of the image.
            chromatic_map (np.ndarray): A weight map based on the chromaticity of the image.

        Returns:
            np.ndarray: The processed image in BGR format, with modified lightness based on the applied weights.
        """
        # 1. Convert to LAB color space
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        # 2. Ensure weight maps have the same dimensions as the image
        luminance_map = cv2.resize(luminance_map, (img.shape[1], img.shape[0]))
        saliency_map = cv2.resize(saliency_map, (img.shape[1], img.shape[0]))
        chromatic_map = cv2.resize(chromatic_map, (img.shape[1], img.shape[0]))

        # 3. Normalize weight maps
        luminance_map = luminance_map.astype(np.float32) / 255.0
        saliency_map = saliency_map.astype(np.float32) / 255.0
        chromatic_map = chromatic_map.astype(np.float32) / 255.0

        # 4. Extract lightness (L), A, and B channels from LAB image
        l, a, b = cv2.split(img)

        # 5. Apply weight maps to lightness channel
        l = l * luminance_map + (1 - luminance_map) * l

        # 6. Merge weighted channels back to LAB
        # Check channel dimensions
        if l.shape != a.shape or l.shape != b.shape:
            # Resize channels if necessary
            l = cv2.resize(l, (a.shape[1], a.shape[0]))

        # Check channel depths
        if l.dtype != a.dtype or l.dtype != b.dtype:
            # Convert channels to a common depth if necessary
            l = l.astype(np.uint8)

        # Now merge the channels
        img = cv2.merge((l, a, b))

        # 7. Convert back to BGR for display or further processing
        img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)

        return img

    def fuse_images(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        weight_map1: np.ndarray,
        weight_map2: np.ndarray,
    ) -> np.ndarray:
        """
        Fuses two images with corresponding weight maps using simple averaging. This method
        is typically used to blend images based on specific features highlighted by the weight maps,
        resulting in a composite that selectively emphasizes areas from each source image.

        Args:
            image1 (np.ndarray): A NumPy array representing the first image (typically 3 channels for RGB).
            image2 (np.ndarray): A NumPy array representing the second image (typically 3 channels for RGB).
            weight_map1 (np.ndarray): A NumPy array representing the weight map for the first image.
            weight_map2 (np.ndarray): A NumPy array representing the weight map for the second image.

        Returns:
            np.ndarray: The fused image, which has the same dimensions and data type as the input images.
        """

        # Ensure all images have the same spatial dimensions
        if (
            image1.shape[:2] != image2.shape[:2]
            or weight_map1.shape[:2] != weight_map2.shape[:2]
        ):
            raise ValueError(
                "Images and weight maps must have the same spatial dimensions!"
            )

        # Reshape weight maps to match image channels (if necessary)
        if weight_map1.ndim < image1.ndim:
            weight_map1 = weight_map1.reshape(
                (weight_map1.shape[0], weight_map1.shape[1], 1)
            )
        if weight_map2.ndim < image2.ndim:
            weight_map2 = weight_map2.reshape(
                (weight_map2.shape[0], weight_map2.shape[1], 1)
            )

        # Simple averaging with weight maps
        fused_image = (image1 * weight_map1 + image2 * weight_map2) / (
            weight_map1 + weight_map2
        )

        # Clip pixel values to [0, 255] (assuming uint8 images)
        fused_image = np.clip(fused_image, 0, 255).astype(np.uint8)

        return fused_image

    def process_image(self) -> np.ndarray:
        """
        The processing steps are:
            1. Apply white balance and contrast enhancements to the original image.
            2. Generate chromatic, saliency, and luminance weight maps for both the contrast-enhanced and
            white-balanced images.
            3. Combine these maps with the original images to create enhanced versions.
            4. Fuse the two enhanced images into a final image based on luminance comparisons.
        """
        # Apply white balance and contrast enhancements
        white_balance_img = self.white_balance()
        contrast_img = self.enhance_contrast()

        # Generate weight maps for the contrast-enhanced image
        chromatic_map1 = self.chromatic_weight_map(contrast_img)
        saliency_map1 = self.saliency_weight_map(contrast_img)
        luminance_map1 = self.luminance_weight_map(contrast_img)

        # Generate weight maps for the white-balanced image
        chromatic_map2 = self.chromatic_weight_map(white_balance_img)
        saliency_map2 = self.saliency_weight_map(white_balance_img)
        luminance_map2 = self.luminance_weight_map(white_balance_img)

        # Apply weighted maps to enhance images
        enhanced_image1 = self.apply_weight_maps(
            contrast_img, luminance_map1, saliency_map1, chromatic_map1
        )
        enhanced_image2 = self.apply_weight_maps(
            white_balance_img, luminance_map2, saliency_map2, chromatic_map2
        )
        
        # Fuse the two enhanced images into the final image
        return self.fuse_images(
            enhanced_image1, enhanced_image2, luminance_map1, luminance_map2
        )

if __name__ == "__main__":
    path = "C:/Users/labra/Downloads/n01496331_10207.jpg"
    image = cv2.imread(path)
    approach1 = Approach1(image)
    approach1.process_image()
    