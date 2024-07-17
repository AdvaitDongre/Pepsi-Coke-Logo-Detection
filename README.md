# Pepsi-Coke-Logo-Detection

Custom Made Dataset: https://universe.roboflow.com/advait-dongre/pepsi-cocacola-images

Here’s a comprehensive `README.md` file that you can use for your project. This file includes detailed instructions for setting up and running your Streamlit application on both Windows and Linux systems.


# Logo Detection in Video and Image

This project is a Streamlit application that detects Pepsi and Coca-Cola logos in videos and images. The application uses the YOLO (You Only Look Once) object detection model to identify and locate the logos, and it outputs the results in both visual and JSON formats.

## File Structure

```
Advait
├── models
├── sample
├── train
├── best.pt
├── coca.mp4
├── extracting_frames.py
├── output.json
├── requirements.txt
```

## Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Step-by-Step Guide

#### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/AdvaitDongre/Pepsi-Coke-Logo-Detection/
cd Pepsi-Coke-Logo-Detection
```

#### Create and Activate a Virtual Environment

It is recommended to create a virtual environment to manage dependencies.

##### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

##### On Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install the Requirements

```bash
pip install -r requirements.txt
```

## Running the Application

### Step-by-Step Guide

1. Ensure your model file (`best.pt`) is in the project directory.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the Streamlit application.

```bash
streamlit run extracting_frames.py
```

## Usage

### Upload Files

- **Video File**: Upload a video file (mp4, mov, avi) to detect Pepsi and Coca-Cola logos in the video.
- **Image File**: Upload an image file (jpg, jpeg, png) to detect Pepsi and Coca-Cola logos in the image.

### Output

- **JSON Output**: Download the JSON file containing the detection details.
- **Processed Video/Image**: View the video or image with the detected logos highlighted by bounding boxes.

## Example Output

### JSON Format

```json
{
    "Pepsi_pts": ["00:00:01", "00:00:03"],
    "CocaCola_pts": ["00:00:02"],
    "Pepsi_details": [
        {
            "timestamp": "00:00:01",
            "size": {"width": 50, "height": 100},
            "distance_from_center": 30.0
        },
        {
            "timestamp": "00:00:03",
            "size": {"width": 60, "height": 110},
            "distance_from_center": 35.0
        }
    ],
    "CocaCola_details": [
        {
            "timestamp": "00:00:02",
            "size": {"width": 55, "height": 105},
            "distance_from_center": 32.0
        }
    ]
}
```

## Troubleshooting

### Common Issues

- **Model Not Found**: Ensure the `best.pt` file is in the project directory and the path is correctly set in the script.
- **Dependency Errors**: Make sure all dependencies are installed by running `pip install -r requirements.txt`.

### Logs

Check the logs for more information on errors or issues:

```bash
streamlit run extracting_frames.py
```

Logs will be displayed in the terminal where you ran the Streamlit command.

## Contributing

Contributions are welcome! Please create a pull request with a clear description of your changes.
