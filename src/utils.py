import os


def read_files_to_dict(directory_path):
    content_dict = {}
    # List all files in the given directory
    for filename in os.listdir(directory_path):
        # Check if the file is a text file
        if filename.endswith(".txt"):
            # Construct full file path
            file_path = os.path.join(directory_path, filename)
            # Read the contents of the file
            with open(file_path, "r") as file:
                content = file.read()
                # Use the filename without extension as the key
                key = os.path.splitext(filename)[0]
                content_dict[key] = content
    return content_dict


def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content
