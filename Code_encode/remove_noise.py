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

remove_text_before_third_occurrence('D:/Downloads/genMaya/files/flask_app.txt')
remove_text_after_bat_occurrence('D:/Downloads/genMaya/files/flask_app.txt')
