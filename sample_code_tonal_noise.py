import socket
import json, os
import struct
import time
from datetime import datetime


def send_command(sock, command):
    """
    Sends a JSON command to the server, prefixed with its length.
    This function first serializes the Python dictionary 'command' into a JSON string,
    encodes it to UTF-8 bytes, and then prepends a 4-byte big-endian length header
    before sending the entire message over the socket.
    """
    message = json.dumps(command).encode('utf-8')
    header = struct.pack('>I', len(message))  # Pack message length as a 4-byte unsigned int (big-endian)
    sock.sendall(header + message)


def receive_response(sock):
    """
    Receives a response from the server, reading the length prefix first.
    This function first reads a 4-byte header to determine the length of the incoming message.
    It then proceeds to read the full message body based on that length, handling potential
    fragmented packets. The received bytes are then decoded and parsed as JSON.
    """
    header = sock.recv(4)  # Receive the 4-byte length prefix
    if not header:
        print("Server disconnected or sent no header.")
        return None
    msg_len = struct.unpack('>I', header)[0]  # Unpack the message length

    full_response_bytes = b''
    bytes_received = 0
    # Loop to ensure all expected bytes of the response are received
    while bytes_received < msg_len:
        # Receive data in chunks, up to 4096 bytes or the remaining message length
        packet = sock.recv(min(4096, msg_len - bytes_received))
        if not packet:
            print("Server disconnected while receiving response body.")
            return None
        full_response_bytes += packet
        bytes_received += len(packet)
    
    try:
        # Decode the received bytes and parse the JSON response
        decoded_response = json.loads(full_response_bytes.decode('utf-8'))
        return decoded_response
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}. Raw data: {full_response_bytes}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during response reception: {e}")
        return None


def save_json_to_file(data, directory, filename):
    """
    Saves a Python dictionary as a JSON file in the specified directory.
    Creates the directory if it doesn't exist.
    """
    try:
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)  # Save with indentation for readability
        print(f"Successfully saved data to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving JSON to file {os.path.join(directory, filename)}: {e}")
        return False


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 12345       # Port to listen on (non-privileged ports are > 1023)

    # --- DEFINE YOUR LIST OF WAV FILES HERE ---
    # IMPORTANT: Replace these paths with the actual, valid paths to your WAV files.
    # These paths should be accessible by the AUT application running the server.
    test_wav_paths = [
        # r"C:\path\to\your\audio_file_1.wav",
        # r"C:\path\to\your\audio_file_2.wav",
        # Example for demonstration (replace with your actual files):
        # "C:\\Users\\Public\\Music\\Sample Music\\Kalimba.wav", 
        # "C:\\Users\\Public\\Music\\Sample Music\\Maid with the Flaxen Hair.wav",
        
        # Placeholder for user to add actual paths:
        # For Linux/macOS:
        # "/path/to/your/audio_file_1.wav",
        # "/path/to/your/audio_file_2.wav",
        
        # For Windows (using raw string or double backslashes):
        "C:\\Temp\\AudioSamples\\sample_audio_1.wav", 
        "C:\\Temp\\AudioSamples\\sample_audio_2.wav",
    ]
    
    # Create dummy files for demonstration if they don't exist
    # In a production setup, these files would already exist.
    for path in test_wav_paths:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            try:
                # Create a dummy WAV file (minimal valid WAV header)
                # This is just a placeholder to prevent file not found errors for the client.
                # The actual audio content doesn't matter for the client script itself,
                # but the server will need valid audio files.
                with open(path, 'wb') as f:
                    f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
                print(f"Created dummy WAV file: {path}")
            except Exception as e:
                print(f"Could not create dummy WAV file {path}: {e}")


    # Path to your custom INI file for the AUT application (if required)
    # This file should contain configuration parameters for the audio analysis.
    custom_ini_file_path = r"C:\Users\Public\Documents\aat.ini" # Example path
    if not os.path.exists(custom_ini_file_path):
        # Create a dummy INI file if it doesn't exist for demonstration
        os.makedirs(os.path.dirname(custom_ini_file_path), exist_ok=True)
        with open(custom_ini_file_path, 'w') as f:
            f.write("[TonalNoise]\n")
            f.write("NoiseFreqRange=500,20000\n")
            f.write("NoiseDbThreshold=20.0\n")
            f.write("EnableCumulativeAnalysis=True\n")
            f.write("MaxAllowedCumulativeDuration=5.0\n")
        print(f"Created dummy INI file: {custom_ini_file_path}")


    # Define output paths for results and plots generated by the server
    # Ensure these directories are writable by the server application.
    output_base_dir = r"C:\Users\Public\Documents\IPC_Results"
    output_result_filename = "Batch_Tonal_Noise_Results.json"
    output_plot_filename = "Batch_Tonal_Noise_Plot.png"

    # Directory for client-side analysis logs
    output_log_dir = os.path.join(output_base_dir, "client_analysis_logs")
    os.makedirs(output_log_dir, exist_ok=True)

    # Initialize a dictionary to store the client-side log data
    analysis_log_data = {
        "test_name": "IPC Client Tonal Noise Batch Test",
        "input_files": [],  # List to store base names of processed input files
        "timestamp": datetime.now().isoformat(),  # ISO formatted timestamp of test execution
        "overall_status": "PENDING",  # Initial status, updated based on test outcome
        "overall_abnormal_noise_detected": None, # Will be True/False based on server response
        "parameters_used": {},  # Parameters actually used by the analysis, reported by server
        "file_specific_results": [],  # Detailed results for each file from the server
        "error_message": None,  # Any error message encountered during client execution
        "plot_all_loaded_files": True, # Indicates if a combined plot was requested
        "messages": [] # General messages/logs during client execution
    }

    test_failed_early = False # Flag to track if the test failed before analysis could run
    final_overall_status = "FAIL" # Default final status, updated upon successful completion

    # Establish socket connection within a 'with' statement for automatic closing
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            # --- IPC Command Sequence ---

            # 1. Send Get Status Command (Optional: good for initial server check)
            print("\n--- Sending Get Status Command ---")
            send_command(sock, {"action": "get_status"})
            response_status = receive_response(sock)
            print("Get Status Response:", response_status)
            time.sleep(0.5) # Short delay to allow server to process

            # 2. Trigger the GUI's open_wave_file method to load multiple files
            # This command instructs the server (AUT GUI) to load the specified WAV files.
            print("\n--- Sending Open Wave File GUI Command to Load Multiple Files ---")
            command_open_gui_files = {
                "action": "open_wave_file_gui",
                "parameters": {"path": test_wav_paths} # Pass a list of file paths
            }
            send_command(sock, command_open_gui_files)
            response_open_gui = receive_response(sock)
            print("Open Wave File GUI Response:", response_open_gui)

            if response_open_gui and response_open_gui.get('status') == 'success':
                # If files are successfully loaded, record their base names in the log.
                analysis_log_data["input_files"].extend([os.path.basename(p) for p in test_wav_paths])
                print(f"Successfully sent command to load {len(test_wav_paths)} files into GUI.")
            else:
                # If file loading fails, set early failure flag and update log.
                test_failed_early = True
                final_overall_status = "GUI_LOAD_FAIL"
                analysis_log_data["error_message"] = (
                    f"Failed to load multiple files via GUI command. Server response: {response_open_gui}"
                )
                print(f"Error: {analysis_log_data['error_message']}")
            time.sleep(1) # Wait for GUI to potentially update

            # 3. Run Scan Tonal Noise Analysis on ALL LOADED FILES
            # This command triggers the tonal noise analysis on all currently loaded files in the AUT.
            if not test_failed_early:
                print("\n--- Sending Run Scan Tonal Noise Command (to process all loaded files) ---")

                # Ensure the directory for the plot image exists.
                output_plot_full_path = os.path.join(output_base_dir, output_plot_filename)
                os.makedirs(os.path.dirname(output_plot_full_path), exist_ok=True)

                command_run_scan_batch = {
                    "action": "run_scan_tonal_noise",
                    "parameters": {
                        # Specify the path where the server should save the generated plot image.
                        "save_plot_image": output_plot_full_path,
                        # Provide the path to the custom INI file for analysis configuration.
                        "ini_file": custom_ini_file_path,
                        # Instruct the server to plot all currently loaded files on a single graph.
                        "plot_all_loaded_files": True,
                        # Override specific parameters directly via IPC, if desired.
                        # These will take precedence over settings in the INI file for this command.
                        "override_params": {
                            "noise_freq_range": [4000.0, 15000.0],  # Example: Analyze noise between 4kHz and 15kHz
                            "noise_db_threshold": 15.0,             # Example: Threshold for detecting abnormal noise
                            "enable_cumulative_analysis": True,     # Enable cumulative duration analysis
                            "max_allowed_cumulative_duration": 6.0  # Max allowed duration of cumulative noise
                        },
                        "apply_a_weighting": False,  # Control A-weighting application (True/False)
                        "selected_channel_index": -1 # -1 for all channels, 1 for Left, 2 for Right etc.
                    }
                }
                send_command(sock, command_run_scan_batch)
                response_scan_batch = receive_response(sock)
                print("Run Scan Tonal Noise Batch Response:", response_scan_batch)

                if response_scan_batch and response_scan_batch.get('status') == 'success':
                    # Extract overall status and results from the server's response.
                    final_overall_status = response_scan_batch.get('result', {}).get('overall_status', 'PASS')
                    server_results = response_scan_batch.get('result', {})

                    # Update client log with parameters used and file-specific results from server.
                    analysis_log_data["parameters_used"].update(server_results.get('parameters_used', {}))
                    # Convert tuple to list for JSON serialization if necessary
                    if "noise_freq_range" in analysis_log_data["parameters_used"] and \
                       isinstance(analysis_log_data["parameters_used"]["noise_freq_range"], tuple):
                        analysis_log_data["parameters_used"]["noise_freq_range"] = \
                            list(analysis_log_data["parameters_used"]["noise_freq_range"])

                    analysis_log_data["file_specific_results"] = server_results.get('file_specific_results', [])
                    analysis_log_data["overall_abnormal_noise_detected"] = server_results.get('overall_abnormal_noise_detected', False)

                    if 'plot_image_saved_to' in response_scan_batch:
                        print(f"Plot saved by server to: {response_scan_batch['plot_image_saved_to']}")
                    print(f"Successfully ran batch scan. Overall status: {final_overall_status}")

                    # NEW: Send command to clear loaded WAVs after analysis to free up resources
                    print("\n--- Sending Clear All Loaded Files Command ---")
                    command_clear_files = {"action": "clear_all_loaded_files"}
                    send_command(sock, command_clear_files)
                    response_clear_files = receive_response(sock)
                    print("Clear All Loaded Files Response:", response_clear_files)
                    time.sleep(0.5) # Short delay

                else:
                    # Handle cases where the batch analysis command itself failed.
                    final_overall_status = "BATCH_ANALYSIS_FAIL"
                    analysis_log_data["error_message"] = response_scan_batch.get('message', 'Batch scan command failed without specific error message from server.')
                    print(f"Batch Scan Tonal Noise failed: {analysis_log_data['error_message']}")
            else:
                # Log that analysis was skipped due to earlier failure.
                print("Skipping Batch Scan Tonal Noise: Files not loaded or previous error occurred.")
                if not test_failed_early: # If not already marked as failed early, mark as skipped
                    final_overall_status = "SKIPPED_BATCH_ANALYSIS"

            time.sleep(1) # Final short delay before closing socket

        except ConnectionRefusedError:
            # Handle cases where the server is not running or not accessible.
            print(f"Connection refused. Is the server running on {HOST}:{PORT}?")
            final_overall_status = "CONNECTION_FAIL"
            analysis_log_data["error_message"] = f"Connection refused. Is the server running on {HOST}:{PORT}?"
        except Exception as e:
            # Catch any other unexpected errors during the client script execution.
            print(f"An unexpected error occurred: {e}")
            final_overall_status = "CLIENT_ERROR"
            analysis_log_data["error_message"] = str(e)
        finally:
            print("\n--- Test Execution Finished ---")
            # The 'with' statement handles sock.close() automatically, but explicit close is fine too.
            # sock.close() 

            # Update the overall status in the log data before saving.
            analysis_log_data["overall_status"] = final_overall_status

            # Save the comprehensive analysis log to a JSON file.
            log_filename = f"analysis_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_successful = save_json_to_file(analysis_log_data, output_log_dir, log_filename)

            # --- PRINT THE FINAL RESULT SUMMARY TO CONSOLE ---
            print("\n" + "=" * 50)
            print("                TEST SUMMARY REPORT               ")
            print("=" * 50)
            print(f"Test Name: {analysis_log_data.get('test_name')}")
            print(f"Timestamp: {analysis_log_data.get('timestamp')}")
            # Indicate the path to the saved log file or if saving failed.
            print(f"Log File Path: {os.path.join(output_log_dir, log_filename) if save_successful else 'Failed to save log file.'}")
            print(f"\nOverall Test Status: {analysis_log_data.get('overall_status')}")
            print(f"Overall Abnormal Noise Detected: {analysis_log_data.get('overall_abnormal_noise_detected')}")

            if analysis_log_data.get('error_message'):
                print(f"Error Message: {analysis_log_data.get('error_message')}")

            # Print detailed results for each file if available.
            if analysis_log_data.get('file_specific_results'):
                print("\nFile Specific Results:")
                for res in analysis_log_data['file_specific_results']:
                    print(f"  File: {res.get('file_name')}")
                    print(f"    Status: {res.get('status')}")
                    print(f"    Abnormal Noise Detected: {res.get('abnormal_noise_detected')}")
                    if res.get('cumulative_analysis'):
                        cum_an = res['cumulative_analysis']
                        print(f"    Cumulative Analysis Performed: {cum_an.get('performed')}")
                        if cum_an.get('performed'):
                            print(f"    Most Cum Freq (Hz): {cum_an.get('freq_hz'):.2f}")
                            print(f"    Most Cum Dur (s): {cum_an.get('duration_s'):.2f}")
                    if res.get('error_message'):
                        print(f"    File Error: {res.get('error_message')}")
            else:
                print("\nNo file-specific analysis results available (analysis might have been skipped or failed early).")

            print("=" * 50)
            print("                 END OF REPORT                   ")
            print("=" * 50 + "\n")
