import os

# Define the path to the file
file_path = "/flag"

try:
    # Get file statistics (this works even if the file is not readable by you)
    file_stat = os.stat(file_path)
    
    # Output the file size
    print("File size:", file_stat.st_size, "bytes")

except FileNotFoundError:
    print(f"File {file_path} does not exist.")
except PermissionError:
    print(f"You do not have permission to access the file {file_path}.")
