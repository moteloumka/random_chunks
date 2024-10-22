import cv2
import os
import argparse

argparser = argparse.ArgumentParser(description="Extract frames from a video file")
argparser.add_argument("video_file", help="Path to the video file")

video_file = argparser.parse_args().video_file

def save_frames_from_video(video_path):
    # Get the video file name without the extension
    file_name = os.path.splitext(os.path.basename(video_path))[0]

    # Create the output directory
    output_dir = f"/workspace/Data/Images/{file_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get the frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    success = True
    second = 0

    while success:
        # Set the frame position at frame count
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        success, frame = cap.read()

        if success:
            # Save the frame for each second
            frame_filename = f"{second:06d}.jpg"
            frame_output_path = os.path.join(output_dir, frame_filename)
            cv2.imwrite(frame_output_path, frame)

            # Increment the second counter
            second += 2

        # Move to the next second's frame
        frame_count += fps

    # Release the video capture object
    cap.release()
    print(f"Frames saved in {output_dir}")

# Example usage
if __name__ == "__main__":
    #video_file = "path_to_your_video_file.mp4"  # Replace with your video file path
    save_frames_from_video(video_file)
