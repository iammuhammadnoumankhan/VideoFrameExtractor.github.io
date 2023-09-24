import streamlit as st
import cv2
import os
import zipfile
from tempfile import TemporaryDirectory
import yaml


# Function to extract frames from a video at a specific FPS
def extract_frames_at_fps(video_path, output_folder, target_fps=60):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    # Get the frame rate of the video
    video_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculate the frame extraction interval based on the target FPS
    frame_interval = int(video_fps / target_fps)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop when we reach the end of the video
        if not ret:
            break

        # Check if the frame should be saved based on the frame interval
        if frame_count % frame_interval == 0:
            # Save the frame as an image
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()

# Streamlit app
def main():
    st.title("Video Frame Extractor")

    # Step 1: Upload video
    uploaded_video = st.file_uploader("Step 1: Upload a video file", type=["mp4", "avi", "mkv", "avi", "webm"])

    if uploaded_video:
        st.video(uploaded_video)

        # Step 2: Set frames per second (FPS)
        target_fps = st.number_input("Step 2: Set frames per second (FPS)", value=DEFAULT, min_value=MIN, max_value=MAX)

        # Step 3: Process video and extract frames
        if st.button("Step 3: Process and Extract Frames"):
            with TemporaryDirectory(prefix="video_frame") as temp_dir:
                temp_output_folder = os.path.join(temp_dir, "output_images")

                #get the video path from the uploaded file object
                video_path = os.path.join(temp_dir, uploaded_video.name)
                with open(video_path, "wb") as video_file:
                    video_file.write(uploaded_video.read())

                extract_frames_at_fps(video_path, temp_output_folder, target_fps)

                # Step 4: Create a zip folder and download
                st.write("Step 4: Downloading...")
                with zipfile.ZipFile("output_images.zip", "w") as zipf:
                    for root, _, files in os.walk(temp_output_folder):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_output_folder))

                st.download_button("Download Images (ZIP)", "output_images.zip")

if __name__ == "__main__":
    with open("Config.yaml", 'r') as file:
            my_file = yaml.safe_load(file)
        
    MAX = my_file["MAX"]
    DEFAULT = my_file["DEFAULT"]
    MIN = my_file["MIN"]
    main()