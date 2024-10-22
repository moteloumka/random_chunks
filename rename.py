import os
import random

def generate_random_number():
    """Generates a random 6-digit number as a string."""
    return f"{random.randint(100000, 999999)}"

def rename_files_in_directory(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Loop through all the files and rename them with a random 6-digit number
    for filename in files:
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):  # Only process files, not directories
            file_extension = os.path.splitext(filename)[1]
            # Generate a new random 6-digit number
            new_filename = f"{generate_random_number()}{file_extension}"
            new_file_path = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    directory = "workspace/Data/Videos/nik_light_videos/"  # Replace with your directory path
    rename_files_in_directory(directory)
