# Real-time Object Detection using MSCOCO and SSD

This project utilizes the MSCOCO dataset and SSD (Single Shot MultiBox Detector) for real-time object detection using a webcam.

## Requirements

- Python 3.x
- OpenCV (cv2)
- Pre-trained SSD model
- MSCOCO dataset

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aksshatgovind/ML-Projects/tree/main/OBJECT%20DETECTION.git
    ```

2. Install required Python packages:
    ```bash
    pip install opencv-python
    ```

## Usage

1. Run the script:
    ```bash
    python code.ipynb
    ```

2. The webcam feed will start, and objects detected by the model will be outlined and labeled in real-time.

3. Press 'q' to exit the application.

## Notes

- Ensure that the webcam is connected and accessible.
- Adjust the confidence threshold (`confThreshold`) as needed for your application.
- The script currently supports detecting up to 80 classes defined in the MSCOCO dataset.

## Credits

- The code for object detection is based on the SSD implementation.
- Pre-trained SSD models can be obtained from various sources, including TensorFlow Object Detection API.
- MSCOCO dataset provides a wide range of object classes for training and evaluation.
