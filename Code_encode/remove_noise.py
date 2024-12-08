import argparse
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import FILES_DIR
from log_function import logger


def remove_text_before_third_occurrence(file_path):
    logger.info(f"Starting to remove text before the third occurrence of '#src/app.py' in file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        logger.debug("File content read successfully.")

        parts = content.split("#src/app.py")
        logger.debug(f"File split into {len(parts)} parts based on '#src/app.py'.")

        if len(parts) > 3:
            new_content = "#src/app.py" + "#src/app.py".join(parts[3:])
            logger.info("Text after the third occurrence retained.")
        else:
            new_content = content
            logger.info("Less than three occurrences found. No changes made.")

        with open(file_path, 'w') as file:
            file.write(new_content)
        logger.info(f"Updated content written back to file: {file_path}")
    except Exception as e:
        logger.error(f"Error occurred in remove_text_before_third_occurrence: {e}")


def remove_text_after_bat_occurrence(file_path):
    logger.info(f"Starting to remove text after the first occurrence of '#src/run_project.bat' in file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        logger.debug("File lines read successfully.")

        count = 0
        result_lines = []

        for line in lines:
            if "#src/run_project.bat" in line:
                count += 1
                if count == 1:
                    logger.info("First occurrence of '#src/run_project.bat' found. Stopping text retention.")
                    break
            result_lines.append(line)

        with open(file_path, 'w') as file:
            file.writelines(result_lines)
        logger.info(f"Updated content written back to file: {file_path}")
    except Exception as e:
        logger.error(f"Error occurred in remove_text_after_bat_occurrence: {e}")


def main(project_name):
    logger.info(f"Main function started for project: {project_name}")
    try:
        file_path = os.path.join(FILES_DIR, f'{project_name}_flask_app.txt')
        remove_text_before_third_occurrence(file_path)
        remove_text_after_bat_occurrence(file_path)
        logger.info("Main function completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")


if __name__ == "__main__":
    logger.info("Script execution started.")
    parser = argparse.ArgumentParser(description="Process a project file by removing specific text.")
    parser.add_argument("project_name", type=str, help="The name of the project file to process")
    args = parser.parse_args()
    logger.debug(f"Parsed arguments: project_name={args.project_name}")
    main(args.project_name)