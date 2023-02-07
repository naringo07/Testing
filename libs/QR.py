
import cv2


def read_qr_code(image):
    """Read an image and return the QR code.
    
    Args:
        image (cv2 image): Image to analyze for QR Code
    
    Returns:
        qr (string): Value from QR code
    """
    
    try:
        detect = cv2.QRCodeDetector()
        value, points, _ = detect.detectAndDecode(image)
        return (value, points)
    except:
        return None