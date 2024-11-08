
import argparse


def remove_text_before_third_occurrence(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    parts = content.split("#src/app.py")
    

    if len(parts) > 3:

        new_content = "#src/app.py" + "#src/app.py".join(parts[3:])
    else:

        new_content = content

    with open(file_path, 'w') as file:
        file.write(new_content)



def remove_text_after_bat_occurrence(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    count = 0
    result_lines = []

    for line in lines:
        if "#src/run_project.bat" in line:
            count += 1
            if count == 1:
                
                break
        result_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(result_lines)


def main(project_name):
    remove_text_before_third_occurrence(f'D:/Downloads/genMaya/files/{project_name}_flask_app.txt')
    remove_text_after_bat_occurrence(f'D:/Downloads/genMaya/files/{project_name}_flask_app.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project file by removing specific text.")
    parser.add_argument("project_name", type=str, help="The name of the project file to process")
    
    args = parser.parse_args()
    main(args.project_name)