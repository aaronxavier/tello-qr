# Tello ArUco Marker Detection

This project enables real-time ArUco marker detection using a DJI Tello drone's video stream. It processes the video feed to identify and track ArUco markers, providing detection counts and visual feedback.

## Features

- Real-time video streaming from DJI Tello drone
- ArUco marker detection and tracking
- Detection counter for unique markers
- Visual overlay of detected markers
- Console output of marker IDs and detection counts

## Prerequisites

- Python 3.x
- OpenCV (cv2)
- NumPy
- DJI Tello drone
- WiFi connection to the Tello drone

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/tello-qr.git
cd tello-qr
```

2. Install required dependencies:
```bash
pip install opencv-python numpy
```

## Usage

1. Connect to your Tello drone's WiFi network

2. Run the program:
```bash
python stream.py
```

3. The program will:
   - Initialize the video stream
   - Begin detecting ArUco markers
   - Display the video feed with marker annotations
   - Show detection count on screen
   - Print marker IDs to console

4. To exit the program:
   - Type 'bye' in the console
   - Or press Ctrl+C

## ArUco Marker Specifications

The program uses the 6x6 ArUco dictionary (DICT_6X6_250) which supports:
- 6x6 bit markers
- Up to 250 different marker IDs
- Good balance between detection reliability and marker size

## Output

The program provides two types of output:
1. Visual feedback:
   - Video stream with detected markers highlighted
   - Detection counter displayed in top-left corner
2. Console output:
   - Marker IDs as they are detected
   - Total detection count

## Notes

- The detection counter increments only for new markers
- A marker must leave the frame and return to be counted again
- The video stream is automatically resized for better performance
- The program uses UDP streaming on port 11111

## Troubleshooting

If you encounter issues:
1. Ensure you're connected to the Tello's WiFi network
2. Check that the Tello is powered on and in range
3. Verify that port 11111 is not blocked by your firewall
4. Make sure you have sufficient lighting for marker detection

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Aaron Xavier
