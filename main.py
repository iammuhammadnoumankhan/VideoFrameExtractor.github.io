import os
import cv2

# Function to extract frames from a video
def extract_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop when we reach the end of the video
        if not ret:
            break

        # Save the frame as an image
        # frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        # cv2.imwrite(frame_filename, frame)

        #CHECK IF THE FRAME IS MULTIPLE 
        if frame_count % 2 == 0:
            #save the frame
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()

# Specify the path to your video and output folder
video_path = input("Enter File Directory: ")        #"Input\\4.mp4"
# video_path = r"C:\Users\owlsense.intern\Desktop\NOUMAN\Scrape frames from video\Input\1.mp4"
output_folder = "Output\\"

# Call the function to extract frames
extract_frames(video_path, output_folder)

print(f"Images extracted and saved in {output_folder}")
