# ipc_inter_channel_phase_example.py
#
# This script is a client-side example demonstrating how to use Inter-Process Communication (IPC)
# to command the Audio Analysis Tool (AAT) to perform an inter-channel phase analysis.
#
# It performs the following steps:
# 1. Connects to the running AAT application's IPC server.
# 2. Clears any previously loaded files in the AAT application.
# 3. Loads a reference audio file and one or more target audio files into the AAT.
# 4. Sends a command to perform an 'intel_channel_phase' analysis between the files.
# 5. Receives the analysis results, which include the plot data.
# 6. If plot data is received, it saves the data locally on the client-side as both a CSV and a JSON file.
#
# Prerequisites:
# - The main AAT application must be running.
# - The 'pandas' library is required for client-side CSV saving (`pip install pandas`).

import socket
import json
import os
import time
import pandas as pd  # pandas is excellent for robust CSV handling.

# --- IPC Server Configuration ---
# These should match the settings in the AAT application.
HOST = '127.0.0.1'
PORT = 12345


def send_ipc_command(sock, command, recv_timeout=60.0):
    """
    Sends a command to the IPC server and waits for a response.

    Args:
        sock (socket.socket): The connected client socket.
        command (dict): The command to send, formatted as a Python dictionary.
        recv_timeout (float): Max time in seconds to wait for a response.

    Returns:
        dict or None: The JSON response from the server as a dictionary, or None on error.
    """
    original_timeout = sock.gettimeout()
    try:
        sock.settimeout(recv_timeout)
        message = json.dumps(command).encode('utf-8')
        
        # Send message length first (4 bytes, big-endian)
        sock.sendall(len(message).to_bytes(4, 'big'))
        # Send the actual message
        sock.sendall(message)
        print(f"CLIENT: Sent command -> {command.get('action')}")
        
        # Receive response length
        response_len_bytes = sock.recv(4)
        if not response_len_bytes:
            print("CLIENT ERROR: Connection closed by server while waiting for response length.")
            return None
            
        response_len = int.from_bytes(response_len_bytes, 'big')
        
        # Receive the full response data
        response_data = b''
        while len(response_data) < response_len:
            packet = sock.recv(response_len - len(response_data))
            if not packet:
                print("CLIENT ERROR: Connection closed by server while receiving response data.")
                return None
            response_data += packet
            
        response_dict = json.loads(response_data.decode('utf-8'))
        print(f"CLIENT: Received response <- {response_dict.get('status', 'UNKNOWN')}")
        return response_dict
        
    except socket.timeout:
        print(f"CLIENT ERROR: Socket timed out after {recv_timeout}s waiting for response for action '{command.get('action')}'.")
        return {"status": "error", "message": "Socket timeout"}
    except Exception as e:
        print(f"CLIENT ERROR: An exception occurred in send_ipc_command for action '{command.get('action')}': {e}")
        return {"status": "error", "message": str(e)}
    finally:
        sock.settimeout(original_timeout)


def save_plot_data_to_json_file(plot_data_list, json_filepath):
    """
    Saves a list of plot data series to a JSON file.

    Args:
        plot_data_list (list): A list of dictionaries, where each dict represents a data series.
        json_filepath (str): The full path for the output JSON file.

    Returns:
        bool: True on success, False on failure.
    """
    print(f"CLIENT: Attempting to save plot data to JSON: '{os.path.basename(json_filepath)}'...")
    try:
        with open(json_filepath, 'w', encoding='utf-8') as jsonf:
            json.dump(plot_data_list, jsonf, indent=4)
        print(f"CLIENT: Successfully saved plot data to JSON.")
        return True
    except Exception as e:
        print(f"CLIENT ERROR: Failed to save plot data to JSON: {e}")
        return False


def save_plot_data_to_csv_client_side(plot_data_list, csv_filepath):
    """
    Saves a list of plot data series to a CSV file using the pandas library.
    This method robustly handles multiple data series of different lengths.

    Args:
        plot_data_list (list): A list of dictionaries, where each dict represents a data series.
        csv_filepath (str): The full path for the output CSV file.

    Returns:
        bool: True on success, False on failure.
    """
    print(f"CLIENT: Attempting to save plot data to CSV: '{os.path.basename(csv_filepath)}'...")
    try:
        data_for_df = {}
        for series in plot_data_list:
            label = series.get('label', 'Unnamed Series')
            x_data = series.get('x')
            y_data = series.get('y')

            if x_data is not None and y_data is not None:
                # Create separate columns for each series' X and Y axes
                data_for_df[f'{label}_X (Frequency)'] = pd.Series(x_data)
                data_for_df[f'{label}_Y (Phase)'] = pd.Series(y_data)

        # pandas automatically handles columns of different lengths by padding with NaN
        df = pd.DataFrame(data_for_df)
        df.to_csv(csv_filepath, index=False, encoding='utf-8-sig')

        print(f"CLIENT: Successfully saved plot data to CSV.")
        return True
    except Exception as e:
        print(f"CLIENT ERROR: Failed to save plot data to CSV: {e}")
        return False


def main():
    """
    Main function to execute the IPC client workflow.
    """
    
    # --- 1. USER CONFIGURATION: Define your file paths here ---
    # IMPORTANT: Please replace these placeholder paths with the actual paths to your audio files.
    # The reference file is the baseline for comparison.
    # The target files are the ones that will be compared against the reference.
    # Ensure backslashes on Windows are escaped (e.g., "C:\\Users\\YourUser\\...") or use raw strings (r"C:\...").
    
    REFERENCE_WAVE_FILE = r"/path/to/your/reference_mic_capture.wav"
    TARGET_WAVE_FILE_1 = r"/path/to/your/target_mic_1_capture.wav"
    TARGET_WAVE_FILE_2 = r"/path/to/your/target_mic_2_capture.wav"

    # Define output file paths
    # These will be saved in the same directory where this script is run.
    output_directory = os.getcwd()
    PLOT_IMAGE_OUTPUT_PATH = os.path.join(output_directory, "ipc_inter_channel_phase_plot.png")
    PLOT_DATA_CSV_OUTPUT_PATH = os.path.join(output_directory, "ipc_inter_channel_phase_data.csv")
    PLOT_DATA_JSON_OUTPUT_PATH = os.path.join(output_directory, "ipc_inter_channel_phase_data.json")

    # --- End of User Configuration ---

    client_socket = None
    try:
        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"CLIENT: Connected to Audio Tool IPC server at {HOST}:{PORT}")
        
        # --- 2. Initial Setup Commands ---
        # It's good practice to check status and clear the tool's state before starting a test.
        send_ipc_command(client_socket, {"action": "get_status"})
        send_ipc_command(client_socket, {"action": "clear_all_loaded_files"})
        time.sleep(0.5)  # Give the GUI a moment to process

        # Load all necessary files into the AAT application
        files_to_load = [REFERENCE_WAVE_FILE, TARGET_WAVE_FILE_1, TARGET_WAVE_FILE_2]
        send_ipc_command(client_socket, {"action": "open_wave_file_gui",
                                         "parameters": {"path": files_to_load}})
        time.sleep(1) # Allow time for file loading and UI update

        # --- 3. Perform the Inter-Channel Phase Analysis ---
        print("\nCLIENT: --- Testing Mode 2: Inter-File Phase Analysis ---")
        
        # Define the command dictionary with all required parameters
        phase_command = {
            "action": "intel_channel_phase",
            "parameters": {
                # Specify which file is the reference for comparison
                "reference_file_path": REFERENCE_WAVE_FILE,
                # Provide a list of target files to compare against the reference
                "target_file_paths": [TARGET_WAVE_FILE_1, TARGET_WAVE_FILE_2],
                # Specify which channel (1-indexed) to use from each file
                "reference_channel_index": 1, 
                # Analysis parameters
                "fft_size": 8192,
                "noverlap": 4096,
                "freq_range": [50, 16000],
                "unwrap_phase": False,
                # Ask the server to save the resulting plot image to this path
                "save_plot_image": PLOT_IMAGE_OUTPUT_PATH
            }
        }
        
        # Send the command and wait for the analysis to complete
        phase_response = send_ipc_command(client_socket, phase_command)

        # --- 4. Handle the Server's Response ---
        if phase_response and phase_response.get("status") == "success":
            print(f"CLIENT: Inter-Channel Phase analysis successful. Server says: {phase_response.get('message')}")
            
            # Check if the server confirmed saving the plot image
            if phase_response.get("plot_image_saved_to"):
                print(f"CLIENT: Plot image was saved by the server to: {phase_response.get('plot_image_saved_to')}")

            # The response contains the data used to generate the plot
            plot_data_from_response = phase_response.get('last_plotted_lines_for_csv')
            
            # --- 5. Save Plot Data Locally on the Client ---
            if plot_data_from_response:
                print("CLIENT: Plot data received. Saving locally to CSV and JSON...")
                
                # a) Save the data to a CSV file
                save_plot_data_to_csv_client_side(plot_data_from_response, PLOT_DATA_CSV_OUTPUT_PATH)
                
                # b) Save the same data to a JSON file for more detailed inspection
                save_plot_data_to_json_file(plot_data_from_response, PLOT_DATA_JSON_OUTPUT_PATH)
                
            else:
                print("CLIENT: Analysis was successful, but no plot data was generated to save.")
        
        else:
            # Handle analysis failure
            print(f"CLIENT ERROR: Inter-Channel Phase analysis failed: {phase_response.get('message', 'Unknown error')}")
            if phase_response and phase_response.get("traceback"):
                print("SERVER TRACEBACK:\n", phase_response.get("traceback"))

    except Exception as e:
        print(f"CLIENT ERROR: An unexpected error occurred in main execution: {e}")
    
    finally:
        # --- 6. Cleanup ---
        print("CLIENT: Closing client socket.")
        if client_socket:
            client_socket.close()


if __name__ == "__main__":
    main()
