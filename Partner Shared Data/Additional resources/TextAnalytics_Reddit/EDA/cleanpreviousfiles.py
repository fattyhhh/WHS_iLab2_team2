import os


# Remove previously saved files
def cleanpreviousfiles():
    """
    Remove previously saved CSV files in the current directory.
    """
    files = [f for f in os.listdir('.') if os.path.isfile(f)]  # List all files in the current directory
    for f in files:
        if f.endswith('.csv'):  # Check if the file has a .csv extension
            os.remove(f)  # Remove the file
