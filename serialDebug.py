import serial
import time
import serial.tools.list_ports


# List available COM ports
def list_com_ports():
    ports = serial.tools.list_ports.comports()
    print("\nAvailable COM ports:")
    for port in ports:
        print(f"  {port.device}")


# Try to connect to a COM port
def test_com_port(port, baudrate=9600, timeout=1):
    try:
        print(f"\nTrying to open {port} at {baudrate} baud...")
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for initialization

        if ser.is_open:
            print(f"Successfully opened {port}")

            # Send a test message
            test_message = b"I\n"
            ser.write(test_message)
            print(f"Sent: {test_message.decode().strip()}")

            # Read response (if any)
            response = ser.readline().decode().strip()
            if response:
                print(f"Received: {response}")
            else:
                print("No response received.")

            # Close the port
            ser.close()
            print(f"Closed {port} successfully.")
        else:
            print(f"Failed to open {port}")

    except serial.SerialException as e:
        print(f"SerialException: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Main script execution
if __name__ == "__main__":
    list_com_ports()
    port = input("\nEnter the COM port to test (e.g., COM3): ").strip()
    test_com_port(port)
