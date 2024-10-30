import os
import shutil
import re
project_name="project1"


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


format_raw_file("D:/Downloads/genMaya/files/flask_app.txt",project_name)
shutil.copy("D:/Downloads/genMaya/files/run_project.bat",os.path.join("run_project.bat","D:/Downloads/genMaya/projects",project_name))
merge_folders("D:/Downloads/genMaya/projects")
renamefoldernames("D:/Downloads/genMaya/projects")
clean_requirements("D:/Downloads/genMaya/projects/project1/src/requirements.txt")