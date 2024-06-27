import cv2
import numpy as np

class Approach2:
    def __init__(self, image: np.ndarray) -> None:
        """
        Initialize the class with an image

        Args:
            image (numpy.ndarray): The input image expected in BGR format.
        """
        self.image = image

    def enhance_contrast(self) -> np.ndarray:
        """
        Enhance the contrast of an image stored in the instance variable `self.image`. This method
        checks if the image is already in grayscale; if not, it converts it to grayscale. Then, it
        applies Contrast Limited Adaptive Histogram Equalization (CLAHE) to improve the contrast.

        Returns:
            np.ndarray: The contrast-enhanced grayscale image.
        """
        # Check if the image is already in grayscale; if not, convert it to grayscale
        if len(self.image.shape) > 2:
            # Assuming the image could have 3 channels (BGR) or 4 channels (BGRA)
            if len(self.image.shape) == 3:
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            else:
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGRA2GRAY)
        else:
            # Image is already grayscale
            gray = self.image

        # Create a CLAHE object with parameters for contrast limiting and grid size
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # Apply CLAHE to the grayscale image to enhance contrast
        enhanced_image = clahe.apply(gray)

        return enhanced_image

    def white_balance(self) -> np.ndarray:
        """
        Adjusts the white balance of an image stored in the instance variable `self.image` by
        normalizing each color channel to their 99th percentile value. This approach ensures
        that the brightest colors are adjusted to pure white, effectively reducing color
        cast from uneven lighting conditions.

        Returns:
            np.ndarray: The white-balanced image as an 8-bit unsigned integer array.
        """
        # Handle BGRA images by converting them to BGR
        if self.image.shape[2] == 4:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)

        # Convert image to double precision for accurate calculations
        double_img = self.image.astype(np.float64)

        # Find the maximum values in each channel at the 99th percentil
        max_values = np.percentile(double_img, 99, axis=(0, 1))

        # Scale the image based on these maximum values to adjust white balance
        balanced_img = (double_img / max_values * 255).clip(0, 255).astype(np.uint8)

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
    approach2 = Approach2(image)
    approach2.process_image()
