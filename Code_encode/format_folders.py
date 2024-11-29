import os
import shutil
import re
import argparse
import zipfile
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_function import logger

def split_text(text):
    logger.debug("Splitting text into sections based on pattern.")
    pattern = r'(?<=\n)(?=#.*\/)'
    parts = re.split(pattern, text)
    formatted_parts = [part.strip() for part in parts]
    logger.debug(f"Text split into {len(formatted_parts)} parts.")
    return formatted_parts

def format_raw_file(filepath, project_name):
    logger.info(f"Formatting raw file: {filepath} for project: {project_name}")
    root_dir = os.path.join("C:/Users/HP/Downloads/GenMaya3s/projects", project_name)
    with open(filepath, 'r') as f:
        content = f.read()
    logger.debug("Raw file content loaded.")

    codeparts = split_text(content)
    for section in codeparts:
        if section.strip():
            header, code = section.strip().split('\n', 1)
            file_path = os.path.join(root_dir, header.strip())
            dir_name = os.path.dirname(file_path)
            os.makedirs(dir_name, exist_ok=True)
            logger.debug(f"Creating directories: {dir_name}")

            with open(file_path, 'w') as f:
                f.write(code.strip())
            logger.info(f"Formatted and saved section to: {file_path}")

def merge_folders(base_dir):
    logger.info(f"Starting to merge folders in base directory: {base_dir}")
    projects = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    logger.debug(f"Found projects: {projects}")

    for project in projects:
        project_path = os.path.join(base_dir, project)
        subfolders = [f for f in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, f))]
        logger.debug(f"Processing project: {project} with subfolders: {subfolders}")

        for folder in subfolders:
            if folder.startswith('#'):
                clean_folder_name = folder[1:]
                clean_folder_path = os.path.join(project_path, clean_folder_name)
                hashed_folder_path = os.path.join(project_path, folder)

                if os.path.exists(clean_folder_path):
                    logger.info(f"Merging folder: {folder} into {clean_folder_name} in project {project}")
                    for item in os.listdir(hashed_folder_path):
                        item_path = os.path.join(hashed_folder_path, item)
                        dest_path = os.path.join(clean_folder_path, item)

                        if os.path.isdir(item_path):
                            shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item_path, dest_path)
                    shutil.rmtree(hashed_folder_path)
                    logger.info(f"Merged and removed folder: {hashed_folder_path}")

def clean_requirements(requirements_file):
    logger.info(f"Cleaning requirements file: {requirements_file}")
    with open(requirements_file, 'r') as file:
        lines = [line.split('==')[0].strip() for line in file.readlines()]
    unique_packages = list(set(lines))
    logger.debug(f"Found {len(unique_packages)} unique packages.")

    with open(requirements_file, 'w') as file:
        for package in unique_packages:
            if package:
                file.write(package + '\n')
    logger.info(f"Cleaned requirements file saved: {requirements_file}")

def renamefoldernames(base_dir):
    logger.info(f"Renaming folder names in base directory: {base_dir}")
    for project in os.listdir(base_dir):
        project_path = os.path.join(base_dir, project)
        if os.path.isdir(project_path):
            for folder in os.listdir(project_path):
                folder_path = os.path.join(project_path, folder)
                if os.path.isdir(folder_path):
                    new_folder_name = folder.replace('#', '')
                    new_folder_path = os.path.join(project_path, new_folder_name)
                    os.rename(folder_path, new_folder_path)
                    logger.info(f"Renamed folder: {folder_path} to {new_folder_path}")

def zip_folder(source_folder, destination_folder, zip_name):
    logger.info(f"Zipping folder: {source_folder} to {destination_folder} with name: {zip_name}")
    zip_path = os.path.join(destination_folder, zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source_folder))
    logger.info(f"Folder '{source_folder}' zipped successfully to '{zip_path}'.")

def main(project_name):
    logger.info(f"Starting main function for project: {project_name}")
    try:
        format_raw_file(f"C:/Users/HP/Downloads/GenMaya3s/files/{project_name}_flask_app.txt", project_name)
        shutil.copy("C:/Users/HP/Downloads/GenMaya3s/files/run_project.bat",
                    os.path.join("C:/Users/HP/Downloads/GenMaya3s/projects", project_name))
        logger.info(f"Copied run_project.bat to project directory.")
        
        merge_folders("C:/Users/HP/Downloads/GenMaya3s/projects")
        renamefoldernames("C:/Users/HP/Downloads/GenMaya3s/projects")
        clean_requirements(f"C:/Users/HP/Downloads/GenMaya3s/projects/{project_name}/src/requirements.txt")
        zip_folder(f"C:/Users/HP/Downloads/GenMaya3s/projects/{project_name}",
                   "C:/Users/HP/Downloads/GenMaya3s/zip_files", f"{project_name}.zip")
        logger.info("Main function completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project file by removing specific text.")
    parser.add_argument("project_name", type=str, help="The name of the project file to process")
    args = parser.parse_args()
    logger.info(f"Script started with project: {args.project_name}")
    main(args.project_name)