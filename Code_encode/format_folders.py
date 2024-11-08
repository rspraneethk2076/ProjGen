import os
import shutil
import re
import argparse
import zipfile

def split_text(text):
    pattern = r'(?<=\n)(?=#.*\/)'
    parts = re.split(pattern, text)
    formatted_parts = [part.strip() for part in parts]
    
    return formatted_parts

def format_raw_file(filepath,project_name):
    root_dir=os.path.join("D:/Downloads/genMaya/projects",project_name)
    with open(filepath,'r') as f:
        content =f.read()
    
    codeparts=split_text(content)
    for section in codeparts:
        if section.strip() :
            header,code=section.strip().split('\n',1)
            file_path=os.path.join(root_dir,header.strip())

            dir_name =os.path.dirname(file_path)
            os.makedirs(dir_name,exist_ok=True)
            
            with open(file_path,'w') as f:
                f.write(code.strip())

            print(f'folder {file_path} formating is done')
            
def merge_folders(base_dir):
    # Get a list of all folders in the base directory (projects directory)
    projects = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    for project in projects:
        project_path = os.path.join(base_dir, project)

        # Get a list of all subfolders within the project
        subfolders = [f for f in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, f))]

        # Separate subfolders with #{some_name} and {some_name}
        for folder in subfolders:
            if folder.startswith('#'):
                # Get the equivalent folder without the '#' prefix
                clean_folder_name = folder[1:]  # Remove '#' from folder name
                clean_folder_path = os.path.join(project_path, clean_folder_name)
                hashed_folder_path = os.path.join(project_path, folder)

                # Check if the folder without '#' exists
                if os.path.exists(clean_folder_path):
                    # Merge the contents of both folders
                    print(f"Merging {folder} into {clean_folder_name} in project {project}")

                    for item in os.listdir(hashed_folder_path):
                        item_path = os.path.join(hashed_folder_path, item)
                        dest_path = os.path.join(clean_folder_path, item)

                        if os.path.isdir(item_path):
                            # Recursively merge subfolders
                            shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
                        else:
                            # Copy individual files
                            shutil.copy2(item_path, dest_path)
                    
                    # Optionally, remove the #{some_name} folder after merging
                    shutil.rmtree(hashed_folder_path)



def clean_requirements(requirements_file):
    # Read the requirements and remove duplicates
    with open(requirements_file, 'r') as file:
        lines = [line.split('==')[0].strip() for line in file.readlines()]  # Remove version specifications

    # Remove duplicates by converting to a set, then back to a list
    unique_packages = list(set(lines))

    # Write the cleaned requirements back to the file
    with open(requirements_file, 'w') as file:
        for package in unique_packages:
            if package:  # Check if the line is not empty
                file.write(package + '\n')


def renamefoldernames(base_dir ):
    for project in os.listdir(base_dir):
        project_path = os.path.join(base_dir, project)

        # Check if it's a directory
        if os.path.isdir(project_path):
            # Iterate through each folder inside the project
            for folder in os.listdir(project_path):
                folder_path = os.path.join(project_path, folder)
                # Check if it's a directory
                if os.path.isdir(folder_path):
                    # Remove '#' from the folder name
                    new_folder_name = folder.replace('#', '')
                    new_folder_path = os.path.join(project_path, new_folder_name)

                    # Rename the folder
                    os.rename(folder_path, new_folder_path)


def zip_folder(source_folder, destination_folder, zip_name):

    zip_path = os.path.join(destination_folder, zip_name)
    

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)

                zipf.write(file_path, os.path.relpath(file_path, source_folder))
    print(f"Folder '{source_folder}' has been zipped successfully to '{zip_path}'.")

def main(project_name):
    format_raw_file(f"D:/Downloads/genMaya/files/{project_name}_flask_app.txt",project_name)
    shutil.copy("D:/Downloads/genMaya/files/run_project.bat",os.path.join("run_project.bat","D:/Downloads/genMaya/projects",project_name))
    merge_folders("D:/Downloads/genMaya/projects")
    renamefoldernames("D:/Downloads/genMaya/projects")
    clean_requirements(f"D:/Downloads/genMaya/projects/{project_name}/src/requirements.txt")
    zip_folder(f"D:/Downloads/genMaya/projects/{project_name}","D:/Downloads/genMaya/zip_files",f"{project_name}.zip")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project file by removing specific text.")
    parser.add_argument("project_name", type=str, help="The name of the project file to process")
    
    args = parser.parse_args()
    main(args.project_name)

