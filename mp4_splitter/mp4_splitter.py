import subprocess
import os
import shutil

def is_ffmpeg_available():
    """Check if FFmpeg is installed and available in the system PATH."""
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

def split_video(file_input):
    try:
        # Check if FFmpeg is available
        if not is_ffmpeg_available():
            print("Error: FFmpeg is not installed or not available in the system PATH.")
            print("Please install FFmpeg from https://ffmpeg.org/download.html and try again.")
            return

        # Check if the input is a full path or just a file name
        if os.path.isabs(file_input):
            file_path = file_input  # Full path
        else:
            file_path = os.path.join(os.getcwd(), file_input)  # File in the same folder as script

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_input}' not found.")
            return

        # Get the file name and extension
        file_name_no_ext, file_extension = os.path.splitext(file_input)

        # Use FFmpeg to get the duration of the video
        result = subprocess.run(
            ['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        duration = float(result.stdout.decode().strip())
        midpoint = duration / 2

        # Generate output file names
        part1_path = f"{file_name_no_ext}_part1{file_extension}"
        part2_path = f"{file_name_no_ext}_part2{file_extension}"

        # Split the video into two parts using FFmpeg (suppress output)
        subprocess.run(['ffmpeg', '-i', file_path, '-t', str(midpoint), '-c', 'copy', part1_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(['ffmpeg', '-i', file_path, '-ss', str(midpoint), '-c', 'copy', part2_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        print(f"Video split successfully into '{part1_path}' and '{part2_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Ask the user for the file input (file name or full path)
file_input = input("Enter the name of your MP4 file (or full file path): ")
split_video(file_input)
