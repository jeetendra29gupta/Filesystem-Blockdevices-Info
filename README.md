# Filesystem and Block Device Information

This script gathers and displays information about the filesystems and block devices on a Unix-like system. 
It provides details on the block devices associated with specific filesystems and checks if a given device is part of the boot volume.

## Requirements

- Python 3.x
- Unix-like operating system (e.g., Linux)

## Dependencies

- `json` (standard library)
- `subprocess` (standard library)

## Installation

No additional installation is required for dependencies as the script uses Python's standard libraries.



## Usage

1. **Clone the repository or download the script**:

   ```bash
   git clone https://github.com/jeetendra29gupta/Filesystem-Blockdevices-Info
   cd Filesystem-Blockdevices-Info
   ```

2. **Run the script:**
   ```bash
   python filesystem_blockdevices_info.py
   ```

## Script Details
- **run_native_command(cmd)**
  - Runs a shell command and returns its output.
  - Handles errors and prints error messages if the command fails.
    
- **read_file_system()**
  - Reads the filesystem information using the df command.
  - Returns a list of filesystems with their source and target paths.
    
- **read_block_devices()**
  - Reads block device information in JSON format using the lsblk command.
  - Returns a list of block devices with their details.
    
- **get_children_info(children, fs)**
  - Recursively searches for filesystem information in block device children.
    
- **get_block_device_info(block_devices, fs)**
  - Finds block device information for a given filesystem.
  - Handles block device children if present.
    
- **is_boot_volume(device_name, device_serial, block_devices)**
  - Checks if a given device is part of the boot volume by comparing its name and serial.
    
- **search_file_system_info(blockdevices, filesystem)**
  - Searches and prints block device information for a specified filesystem.
  - Indicates if the device is part of the boot volume.
    
- **main()**
  - The main function that executes the script.
  - Reads filesystem and block device information, then prints details for each filesystem.

## Example Output
```
Name: sda
Path: /dev/sda
Serial: 1234567890
Mount Point: /
Disk Path: /dev/sda
UUID: abcdefgh-1234-5678-9101-112233445566
Is Boot Volume: Yes
```

## Troubleshooting
- Ensure you have the necessary permissions to run df and lsblk commands.
- Check if the commands are available in your system's PATH.
