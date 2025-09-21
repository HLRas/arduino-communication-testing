import serial
import threading
import time
import bisect

arduino_lock = threading.Lock()
data = []
arduino_comm_thread = None
restarted = True

def thread():
    global restarted
    print("[Python] Thread started!")
    
    try:
        arduino_serial = serial.Serial('COM3', 115200, timeout=0)
        time.sleep(2) # Wait for the Arduino to reset after connection
        print("[Python] Connected to COM3")
    except Exception as e:
        print(f"[Python] Connection error: {e}")
        arduino_serial = None
   
    while True:
        if restarted:
            start_time = time.time()
            print(f"[Python] Thread started at: {start_time}")
            restarted = False

        try:
            if arduino_serial:
                try:
                    if arduino_serial.in_waiting > 0:
                        incoming_data = arduino_serial.readline().decode('utf-8').strip()
                        if incoming_data:
                            print(f"[Arduino] Received: {incoming_data}")
                except Exception as e:
                    print(f"[Python] Read error: {e}")
                
                new_t = time.time()
                dt = new_t - start_time
                
                if data:
                    left, right, timestamp = find_closest(data, dt)
                # Always remove data from queue (either send or discard)
                with arduino_lock:
                    if left:
                            try:
                                msg = f"{left},{right},{timestamp}\n"
                                arduino_serial.write(msg.encode('utf-8'))
                                arduino_serial.flush()
                                print(f"[Python] Sent: {msg}")
                            except Exception as e:
                                print(f"[Python] Write error: {e}")

            time.sleep(0.01)
            
        except Exception as e:
            #print(f"[Python] Failed: {e}")
            pass
            

def find_closest(data, timestamp, index=2):
    timestamps = [tp[index] for tp in data]
    return data[bisect.bisect_left(timestamps, timestamp)]


def main():
    global arduino_comm_thread, data, restarted

    start_time = time.time()
    data = []

    for i in range(0,1000,2):
        time.sleep(0.01)
        data.append((i, i+1, time.time()-start_time))

    if arduino_comm_thread is None:
        arduino_comm_thread = threading.Thread(target=thread, daemon=True)
        arduino_comm_thread.start()

    while True:
        if time.time() -start_time > 2:
            restarted = True
            main()
        pass

if __name__ == '__main__': main()
