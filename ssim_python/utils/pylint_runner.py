import os

def run_pylint_on_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Running pylint on: {file_path}")
                os.system(f"pylint {file_path}")
