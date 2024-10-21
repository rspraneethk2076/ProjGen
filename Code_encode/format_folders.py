import os
import shutil
project_name="project1"
def format_raw_file(filepath,project_name):
    root_dir="D:/Downloads/genMaya/projects"+project_name
    with open(filepath,'r') as f:
        content =f.read()
    
    codeparts=content.split('#')
    for section in codeparts:
        if section.strip():
            header,code=section.strip().split('\n',1)
            file_path=os.path.join(root_dir,header.strip())

            dir_name =os.path.dirname(file_path)
            os.makedirs(dir_name,exist_ok=True)
            
            with open(file_path,'w') as f:
                f.write(code.strip())

            print(f'folder {file_path} formating is done')


format_raw_file("D:/Downloads/genMaya/files/flask_app.txt",project_name)
shutil.copy("D:/Downloads/genMaya/files/run_project.bat",os.path.join("run_project.bat","D:/Downloads/genMaya/projects"+project_name))