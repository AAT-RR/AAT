# This is an example IPC client script you should run.
import socket
import json
import time
import struct  # <<-- NEW: Import the struct module

HOST = '127.0.0.1'
PORT = 12345

def send_ipc_command(action, parameters=None):
    """
    Sends an Inter-Process Communication (IPC) command to the server.

    Args:
        action (str): The action to be performed by the server (e.g., "restart_application").
        parameters (dict, optional): A dictionary of parameters for the action. Defaults to None.

    Returns:
        dict: The parsed JSON response from the server, or None if an error occurred.
    """
    if parameters is None:
        parameters = {}

    command = {
        "action": action,
        "parameters": parameters,
        "client_id": "my_ipc_client"  # A unique identifier for this client
    }

    try:
        # Create a socket using the AF_INET (IPv4) address family and SOCK_STREAM (TCP) socket type.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to the server at the specified host and port.
            sock.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            # ##############################****************************
            # NEW: Send the message in the format expected by the server (length prefix + JSON).
            # First, serialize the command dictionary to a JSON string and then encode it to bytes.
            json_message_bytes = json.dumps(command).encode('utf-8')
            # Get the length of the encoded JSON message.
            message_length = len(json_message_bytes)
            # Pack the message length into a 4-byte unsigned integer, using big-endian byte order ('>I').
            # This length prefix tells the server how many bytes to expect for the JSON message.
            length_prefix = struct.pack('>I', message_length) 
            
            # Concatenate the length prefix and the JSON message bytes to form the full message.
            full_message = length_prefix + json_message_bytes
            
            # Send the entire message (length prefix + JSON) to the server.
            sock.sendall(full_message)
            # ##############################****************************
            
            print(f"Sent command: '{action}' (length: {message_length} bytes)")

            response_data = b'' # Initialize an empty bytes object to store the incoming response.
            while True:
                # ##############################****************************
                # NEW: Receive the message in the format sent by the server (length prefix + JSON).
                # First, receive the 4-byte length prefix.
                header = sock.recv(4)
                if not header: # If no data is received, the server has closed the connection.
                    print("Server closed connection unexpectedly.")
                    break
                
                # Unpack the 4-byte header to get the expected response length.
                response_length = struct.unpack('>I', header)[0]
                
                # Now, receive the complete response body based on the `response_length`.
                while len(response_data) < response_length:
                    # Receive chunks of data until the full response is gathered.
                    # The argument to recv() is the maximum number of bytes to receive at once.
                    chunk = sock.recv(response_length - len(response_data))
                    if not chunk: # If no data is received during the body, the server closed the connection.
                        print("Server closed connection unexpectedly while receiving response body.")
                        break
                    response_data += chunk # Append the received chunk to the response data.
                
                # Once the complete response is received, break out of the loop.
                break 
                # ##############################****************************

            # Decode the received bytes into a UTF-8 string and parse it as JSON.
            # .strip() might not be needed if the server doesn't add trailing newlines,
            # but it's safe to keep for robustness.
            response = json.loads(response_data.decode('utf-8').strip()) 
            print(f"Received response: {json.dumps(response, indent=2)}")
            return response

    except ConnectionRefusedError:
        # Handle cases where the server is not running or not accessible.
        print(f"Connection refused. Is the server running on {HOST}:{PORT}?")
    except json.JSONDecodeError as e:
        # Handle cases where the received data is not valid JSON.
        print(f"Failed to decode JSON response: {e}. Raw response: {response_data.decode('utf-8')}")
    except Exception as e:
        # Catch any other unexpected errors during the process.
        print(f"An unexpected error occurred: {e}")
    return None # Return None if any error occurs.

if __name__ == "__main__":
    print("\n--- Sending restart command ---")
    # Example: Send a command to restart the application.
    response = send_ipc_command("restart_application")
    if response and response.get("status") == "success":
        print("Application should now be restarting...")
    else:
        print("Failed to initiate restart or received an error response.")

    # Give some time for the command to potentially take effect or for observation.
    time.sleep(5)
    print("Client script finished.")
