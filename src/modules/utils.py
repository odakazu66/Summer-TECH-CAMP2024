# Function to load QSS from a file
def load_stylesheet(qss_file_path):
    with open(qss_file_path, "r") as file:
        return file.read()