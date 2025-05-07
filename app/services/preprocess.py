from PIL import Image
import numpy as np
import cv2

def preprocess_image(image_bytes: bytes) -> Image.Image:
    """
    Takes image bytes, processes it with OpenCV,
    and returns a clean PIL Image for model input.
    """
    # Convert bytes to NumPy array
    np_img = np.frombuffer(image_bytes, np.uint8)
    # Decode the image
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    # Convert BGR (OpenCV default) to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert to PIL image
    pil_img = Image.fromarray(img)
    return pil_img
