# Arduino Communication Testing

This project contains Python scripts for testing serial communication with Arduino devices.

## Files

- `my_serial.py` - Main serial communication script with data timestamping and closest-match finding
- `testing.py` - Simple serial communication test script with CSV output
- `output*.csv` - Generated CSV files containing communication logs

## Requirements

```bash
pip install pyserial
```

## Usage

### Basic Testing
```bash
python testing.py
```

### Advanced Communication with Timestamping
```bash
python my_serial.py
```

## Configuration

- Default serial port: `COM3` (Windows) or `/dev/ttyACM0` (Linux/Mac)
- Baud rate: 115200
- Test duration: 10 seconds (configurable in `testing.py`)

## Features

- Thread-safe serial communication
- Automatic CSV file generation with incremental naming
- Real-time data logging
- Arduino echo response handling
- Timestamp-based data matching

## Hardware Setup

Connect your Arduino to the specified COM port and ensure it's running compatible firmware that can handle the communication protocol used in these scripts.