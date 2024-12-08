import requests
import traceback
import logging

server_url = "http://127.0.0.1:5001"
routes = ["/"]

# Function to get the last 4 lines from the log file
def get_last_log_lines(log_file, num_lines=4):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
            return lines[-num_lines:]  # Return the last 'num_lines' lines
    except FileNotFoundError:
        return ["Log file not found.\n"]
    except Exception as e:
        return [f"Error reading log file: {e}\n"]

# Function to test routes and capture logs
def test_routes(server_url, routes, log_file="D:/Downloads/genMaya/projects/hema/app.log"):
    logs_per_route = {}

    for route in routes:
        url = f"{server_url}{route}"
        print(f"Testing route: {url}")

        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error requesting {url}: {e}")
        
        # Fetch the last 4 lines of the log file
        last_log_lines = get_last_log_lines(log_file)
        logs_per_route[route] = "".join(last_log_lines)  # Store in dictionary

    return str(logs_per_route)

# Run the test
logs = test_routes(server_url, routes)

# Print the results
for route, log_content in logs.items():
    print(f"Logs for {route}:\n{log_content}")
