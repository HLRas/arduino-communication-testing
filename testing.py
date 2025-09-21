import serial
import threading
import time
import bisect
import csv
import os

arduino_lock = threading.Lock()
data = []
runThread = True

def get_next_filename(base_name="output", extension=".csv"):
    """Find the next available filename (output.csv, output1.csv, output2.csv, etc.)"""
    filename = f"{base_name}{extension}"
    
    if not os.path.exists(filename):
        return filename
    
    counter = 1
    while True:
        filename = f"{base_name}{counter}{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

def thread():
    print("[Python] Thread started!")
    
    try:
        arduino_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
        time.sleep(2) # Wait for the Arduino to reset after connection
        print("[Python] Connected to /dev/ttyACM0")
    except Exception as e:
        print(f"[Python] Connection error: {e}")
        arduino_serial = None
    
    start_time = time.time()
    print(f"[Python] Thread started at: {start_time}")
    while runThread:
        try:
            if arduino_serial:
                try:
                    if arduino_serial.in_waiting > 0:
                        incoming_data = arduino_serial.readline().decode('utf-8').strip()
                        if incoming_data:
                            print(f"[Arduino] Received: {incoming_data}")
                            with arduino_lock:
                                data.append(incoming_data)
                except Exception as e:
                    print(f"[Python] Read error: {e}")

            time.sleep(0.001)
            
        except Exception as e:
            print(f"[Python] Failed: {e}")
            pass

def main():
    global runThread

    arduino_comm_thread = threading.Thread(target=thread, daemon=True)
    arduino_comm_thread.start()

    start_time = time.time()
    now = time.time()
    test_period = 10

    while now - start_time < test_period: # Save file after test_period elapsed
        now = time.time()

    runThread = False # Stop the thread
    time.sleep(0.1)

    # Save file
    filename = get_next_filename("output", ".csv")
    print("[Python] Saving to csv...")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow([row])

    print(f"[Python] CSV saved as {filename}!")

if __name__ == '__main__': main()
