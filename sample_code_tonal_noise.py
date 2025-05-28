import socket
import json, os
import struct
import time
from datetime import datetime


def send_command(sock, command):
    """
    Sends a JSON command to the server, prefixed with its length.
    """
    message = json.dumps(command).encode('utf-8')
    header = struct.pack('>I', len(message))
    sock.sendall(header + message)


def receive_response(sock):
    """
    Receives a response from the server, reading the length prefix first.
    """
    header = sock.recv(4)
    if not header:
        return None
    msg_len = struct.unpack('>I', header)[0]

    full_response_bytes = b''
    bytes_received = 0
    while bytes_received < msg_len:
        packet = sock.recv(min(4096, msg_len - bytes_received))
        if not packet:
            return None
        full_response_bytes += packet
        bytes_received += len(packet)
    try:
        decoded_response = json.loads(full_response_bytes.decode('utf-8'))
        return decoded_response
    except json.JSONDecodeError:
        return None
    except Exception:
        return None


def save_json_to_file(data, directory, filename):
    """Saves a Python dictionary as a JSON file in the specified directory."""
    try:
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    # --- DEFINE YOUR LIST OF WAV FILES HERE ---
    # Replace these paths with the actual paths to your WAV files.
    test_wav_paths = [
        r" path to test.wav",
        r" path to  test2.wav",
    ]

    # Path to your custom INI file for the AUT application
    custom_ini_file_path = r" path to aat.ini"

    # Define output paths for results and plots
    output_base_dir = "d:\\Production_Logs"
    output_result_filename = "Batch_XYZ_Results.json"
    output_plot_filename = "Batch_XYZ_Plot.png"

    output_log_dir = os.path.join(output_base_dir, "test_analysis_logs")
    os.makedirs(output_log_dir, exist_ok=True)

    analysis_log_data = {
        "test_name": "IPC Client Tonal Noise Batch Test",
        "input_files": [],
        "timestamp": datetime.now().isoformat(),
        "overall_status": "PENDING",
        "overall_abnormal_noise_detected": True,
        "parameters_used": {},
        "file_specific_results": [],
        "error_message": None,
        "plot_all_loaded_files": True,
        "messages": []
    }

    test_failed_early = False
    final_overall_status = "FAIL"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            # 1. Send Get Status Command (Optional, for initial check)
            print("\n--- Sending Get Status Command ---")
            send_command(sock, {"action": "get_status"})
            response_status = receive_response(sock)
            print("Get Status Response:", response_status)
            time.sleep(0.5)

            # 2. Trigger the GUI's open_wave_file method to load multiple files
            print("\n--- Sending Open Wave File GUI Command to Load Multiple Files ---")
            command_open_gui_files = {
                "action": "open_wave_file_gui",
                "parameters": {"path": test_wav_paths}
            }
            send_command(sock, command_open_gui_files)
            response_open_gui = receive_response(sock)
            print("Open Wave File GUI Response:", response_open_gui)

            if response_open_gui and response_open_gui.get('status') == 'success':
                analysis_log_data["input_files"].extend([os.path.basename(p) for p in test_wav_paths])
                print(f"Successfully sent command to load {len(test_wav_paths)} files into GUI.")
            else:
                test_failed_early = True
                final_overall_status = "GUI_LOAD_FAIL"
                analysis_log_data["error_message"] = f"Failed to load multiple files via GUI command. Server response: {response_open_gui}"
                print(f"Error: {analysis_log_data['error_message']}")
            time.sleep(1)

            # 3. Run Scan Tonal Noise Analysis on ALL LOADED FILES
            if not test_failed_early:
                print("\n--- Sending Run Scan Tonal Noise Command (to process all loaded files) ---")

                output_plot_full_path = os.path.join(output_base_dir, output_plot_filename)
                os.makedirs(os.path.dirname(output_plot_full_path), exist_ok=True)

                command_run_scan_batch = {
                    "action": "run_scan_tonal_noise",
                    "parameters": {
                        "save_plot_image": output_plot_full_path,
                        "ini_file": custom_ini_file_path,
                        "plot_all_loaded_files": True,
                        "override_params": {
                            "noise_freq_range": [7000.0, 15000.0],
                            "noise_db_threshold": 12.0,
                            "enable_cumulative_analysis": True,
                            "max_allowed_cumulative_duration": 5.0
                        }
                    }
                }
                send_command(sock, command_run_scan_batch)
                response_scan_batch = receive_response(sock)
                print("Run Scan Tonal Noise Batch Response:", response_scan_batch)

                if response_scan_batch and response_scan_batch.get('status') == 'success':
                    final_overall_status = response_scan_batch.get('result', {}).get('overall_status', 'PASS')
                    server_results = response_scan_batch.get('result', {})

                    analysis_log_data["parameters_used"].update(server_results.get('parameters_used', {}))
                    if "noise_freq_range" in analysis_log_data["parameters_used"] and isinstance(analysis_log_data["parameters_used"]["noise_freq_range"], tuple):
                        analysis_log_data["parameters_used"]["noise_freq_range"] = list(analysis_log_data["parameters_used"]["noise_freq_range"])

                    analysis_log_data["file_specific_results"] = server_results.get('file_specific_results', [])
                    analysis_log_data["overall_abnormal_noise_detected"] = server_results.get('overall_abnormal_noise_detected', False)

                    if 'plot_image_saved_to' in response_scan_batch:
                        print(f"Plot saved by server to: {response_scan_batch['plot_image_saved_to']}")
                    print(f"Successfully ran batch scan. Overall status: {final_overall_status}")

                    # NEW: Send command to clear loaded WAVs after analysis
                    print("\n--- Sending Clear All Loaded Files Command ---")
                    command_clear_files = {"action": "clear_all_loaded_files"}
                    send_command(sock, command_clear_files)
                    response_clear_files = receive_response(sock)
                    print("Clear All Loaded Files Response:", response_clear_files)
                    time.sleep(0.5)

                else:
                    final_overall_status = "BATCH_ANALYSIS_FAIL"
                    analysis_log_data["error_message"] = response_scan_batch.get('message', 'Batch scan command failed without specific error message from server.')
                    print(f"Batch Scan Tonal Noise failed: {analysis_log_data['error_message']}")
            else:
                print("Skipping Batch Scan Tonal Noise: Files not loaded or previous error occurred.")
                if not test_failed_early:
                    final_overall_status = "SKIPPED_BATCH_ANALYSIS"

            time.sleep(1)

        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running on {HOST}:{PORT}?")
            final_overall_status = "CONNECTION_FAIL"
            analysis_log_data["error_message"] = f"Connection refused. Is the server running on {HOST}:{PORT}?"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            final_overall_status = "CLIENT_ERROR"
            analysis_log_data["error_message"] = str(e)
        finally:
            print("\n--- Test Execution Finished ---")
            sock.close()

            analysis_log_data["overall_status"] = final_overall_status

            log_filename = f"analysis_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_successful = save_json_to_file(analysis_log_data, output_log_dir, log_filename)

            # --- PRINT THE FINAL RESULT SUMMARY TO CONSOLE ---
            print("\n" + "=" * 50)
            print("                TEST SUMMARY REPORT               ")
            print("=" * 50)
            print(f"Test Name: {analysis_log_data.get('test_name')}")
            print(f"Timestamp: {analysis_log_data.get('timestamp')}")
            print(f"Log File Path: {os.path.join(output_log_dir, log_filename) if save_successful else 'Failed to save log file.'}")
            print(f"\nOverall Test Status: {analysis_log_data.get('overall_status')}")
            print(f"Overall Abnormal Noise Detected: {analysis_log_data.get('overall_abnormal_noise_detected')}")

            if analysis_log_data.get('error_message'):
                print(f"Error Message: {analysis_log_data.get('error_message')}")

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
                            print(f"    Most Cum Freq (Hz): {cum_an.get('freq_hz')}")
                            print(f"    Most Cum Dur (s): {cum_an.get('duration_s')}")
                    if res.get('error_message'):
                        print(f"    File Error: {res.get('error_message')}")
            else:
                print("\nNo file-specific analysis results available (analysis might have been skipped or failed early).")

            print("=" * 50)
            print("                 END OF REPORT                   ")
            print("=" * 50 + "\n")