import streamlit as st
from datetime import timedelta
import av
import json
import logging
from PIL import Image, ImageDraw
from ultralytics import YOLO
import io

# Setup logging
logging.basicConfig(level=logging.INFO)

# Model Path
model_path = r"C:\Users\KAMAL\Desktop\Advait\best.pt"  # Update this path to the location of your model
model = YOLO(model_path)  # Load a custom model

threshold = 0.5

def format_timestamp(seconds):
    # Convert seconds to timedelta and format as HH:MM:SS
    td = timedelta(seconds=seconds)
    return str(td)

def detect_logos(frames):
    pepsi_pts = []
    cocacola_pts = []

    try:
        for i, (img, timestamp) in enumerate(frames):
            logging.info(f"Processing frame {i+1}/{len(frames)} at timestamp {timestamp}")
            results = model(img)  # Run inference

            for result in results:
                boxes = result.boxes  # Boxes object for bounding box outputs

                for box in boxes:
                    # Extract the bounding box and confidence
                    x1, y1, x2, y2 = box.xyxy[0].tolist()  # Convert to list
                    score = box.conf[0].item()  # Convert to float
                    class_id = int(box.cls[0].item())  # Convert to int

                    if score > threshold:
                        class_name = result.names[class_id].upper()
                        width = x2 - x1
                        height = y2 - y1
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        frame_center_x = img.width / 2
                        frame_center_y = img.height / 2
                        distance_from_center = ((center_x - frame_center_x) ** 2 + (center_y - frame_center_y) ** 2) ** 0.5

                        # Draw the bounding box on the image
                        draw = ImageDraw.Draw(img)
                        draw.rectangle([x1, y1, x2, y2], outline='red', width=3)

                        formatted_timestamp = format_timestamp(timestamp)
                        entry = {
                            "timestamp": formatted_timestamp,
                            "size": {"width": width, "height": height},
                            "distance_from_center": distance_from_center
                        }

                        if class_name == 'PEPSI':
                            pepsi_pts.append(entry)
                        elif class_name == 'COCA-COLA':
                            cocacola_pts.append(entry)
        logging.info("Logo detection completed.")
    except Exception as e:
        logging.error(f"Error during logo detection: {e}")

    return pepsi_pts, cocacola_pts, frames

def generate_output_json(pepsi_pts, cocacola_pts):
    # Convert all values to strings for JSON serialization
    def to_serializable(obj):
        if isinstance(obj, (list, dict)):
            return obj
        elif hasattr(obj, 'tolist'):
            return obj.tolist()  # Convert numpy arrays or tensors
        elif hasattr(obj, 'item'):
            return obj.item()  # Convert single element tensors
        else:
            return str(obj)  # Convert other non-serializable objects to string

    output = {
        "Pepsi_pts": [entry["timestamp"] for entry in pepsi_pts],
        "CocaCola_pts": [entry["timestamp"] for entry in cocacola_pts],
        "Pepsi_details": [ {k: to_serializable(v) for k, v in entry.items()} for entry in pepsi_pts ],
        "CocaCola_details": [ {k: to_serializable(v) for k, v in entry.items()} for entry in cocacola_pts ]
    }
    
    return output

def detect_logo_in_image(image):
    results = model(image)  # Run inference
    pepsi_pts = []
    cocacola_pts = []

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs

        for box in boxes:
            # Extract the bounding box and confidence
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Convert to list
            score = box.conf[0].item()  # Convert to float
            class_id = int(box.cls[0].item())  # Convert to int

            if score > threshold:
                class_name = result.names[class_id].upper()
                width = x2 - x1
                height = y2 - y1
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                frame_center_x = image.width / 2
                frame_center_y = image.height / 2
                distance_from_center = ((center_x - frame_center_x) ** 2 + (center_y - frame_center_y) ** 2) ** 0.5

                # Draw the bounding box on the image
                draw = ImageDraw.Draw(image)
                draw.rectangle([x1, y1, x2, y2], outline='red', width=3)

                entry = {
                    "size": {"width": width, "height": height},
                    "distance_from_center": distance_from_center
                }

                if class_name == 'PEPSI':
                    pepsi_pts.append(entry)
                elif class_name == 'COCA-COLA':
                    cocacola_pts.append(entry)

    return pepsi_pts, cocacola_pts, image

def main():
    st.sidebar.title("Upload Files")
    st.sidebar.write("Upload a video or image file to detect Pepsi and Coca-Cola logos.")

    uploaded_video = st.sidebar.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
    video_button = st.sidebar.button("Upload Video") 

    uploaded_image = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    image_button = st.sidebar.button("Upload Image")

    st.title("Logo Detection in Video and Image")

    if uploaded_video is not None and video_button:
        if 'video_processed' not in st.session_state:
            # Convert uploaded file to a format that `av` can read
            video_bytes = uploaded_video.read()
            video_stream = io.BytesIO(video_bytes)
            container = av.open(video_stream)

            frames = []
            timestamps = []

            # Show a message while processing the frames
            with st.spinner("Processing frames and detecting logos..."):
                for i, frame in enumerate(container.decode(video=0)):
                    timestamp = float(frame.pts * frame.time_base)
                    formatted_timestamp = format_timestamp(timestamp)
                    timestamps.append(formatted_timestamp)
                    img = frame.to_image()
                    frames.append((img, timestamp))

            st.write(f"Extracted {len(frames)} frames from the video.")

            if len(frames) > 0:
                # Detect logos
                st.write("Detecting logos...")
                pepsi_pts, cocacola_pts, frames_with_boxes = detect_logos(frames)
                
                # Generate JSON output
                st.write("Generating JSON output...")
                output_json = generate_output_json(pepsi_pts, cocacola_pts)
                st.session_state['output_json'] = json.dumps(output_json, indent=4)
                
                # Create a video with bounding boxes
                st.write("Creating video with detected logos...(The video might be a little glitchy or inaccurate but the output.json file has all the outputs in proper order)")
                video_with_boxes = io.BytesIO()
                output_container = av.open(video_with_boxes, mode='w', format='mp4')
                stream = output_container.add_stream('h264', rate=30)
                stream.width = 640
                stream.height = 480
                stream.pix_fmt = 'yuv420p'
                
                for img, timestamp in frames_with_boxes:
                    img = img.resize((640, 480))
                    frame = av.VideoFrame.from_image(img)
                    packet = stream.encode(frame)
                    output_container.mux(packet)
                packet = stream.encode(None)
                output_container.mux(packet)
                output_container.close()

                st.session_state['video_with_boxes'] = video_with_boxes
                st.session_state['pepsi_pts'] = pepsi_pts
                st.session_state['cocacola_pts'] = cocacola_pts
            else:
                st.error("No frames extracted. Please upload a valid video file.")
        else:
            st.write("Video has already been processed.")
            
    if 'output_json' in st.session_state:
        st.download_button("Download JSON Output", st.session_state['output_json'], file_name="output.json", mime="application/json")
        st.button("Show JSON", on_click=lambda: st.json(json.loads(st.session_state['output_json'])))

    if 'video_with_boxes' in st.session_state:
        st.video(st.session_state['video_with_boxes'], format="video/mp4")

    st.write("Or upload an image to detect logos:")

    if uploaded_image is not None and image_button:
        image = Image.open(uploaded_image)
        pepsi_pts, cocacola_pts, image_with_boxes = detect_logo_in_image(image)
        st.image(image_with_boxes, caption='Processed Image', use_column_width=True)

        output_json_image = {
            "Pepsi_pts": [entry for entry in pepsi_pts],
            "CocaCola_pts": [entry for entry in cocacola_pts]
        }

        st.download_button(
            label="Download JSON Output for Image",
            data=json.dumps(output_json_image, indent=4),
            file_name="output_image.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()