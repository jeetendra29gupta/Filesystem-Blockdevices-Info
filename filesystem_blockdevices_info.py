import json
import subprocess


def run_native_command(cmd):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr.strip()}")
        return None


def read_file_system():
    """Read the file system information."""
    try:
        output = run_native_command(["df", "--output=source,target"])
        if output is None:
            print("Failed to get file system information.")
            return []

        lines = output.splitlines()[1:]  # Skip header line
        filesystems = [[line.split()[0].strip(), line.split()[1].strip()] for line in lines]
        return filesystems

    except Exception as ex:
        print(f"Error reading file system: {ex}")
        return []


def read_block_devices():
    """Read the block devices information in JSON format."""
    try:
        output = run_native_command(["lsblk", "--output=NAME,PATH,MOUNTPOINT,UUID,SERIAL", "--json"])
        if output is None:
            print("Failed to get block devices information.")
            return []

        blockdevices = json.loads(output)
        return blockdevices.get("blockdevices", [])

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except Exception as ex:
        print(f"Error reading block devices: {ex}")
        return []


def get_children_info(children, fs):
    """Recursively search for the filesystem in children."""
    if not children:
        return None, None, None

    for child in children:
        if child.get("mountpoint") == fs:
            return child.get("mountpoint"), child.get("path"), child.get("uuid")

        # Recur into children
        result = get_children_info(child.get("children"), fs)
        if result[0] is not None:
            return result

    return None, None, None


def get_block_device_info(block_devices, fs):
    """Find the block device information for the given filesystem."""
    for block_device in block_devices:
        if block_device.get("mountpoint") == fs:
            return (
                block_device.get("name"),
                block_device.get("path"),
                block_device.get("serial"),
                block_device.get("mountpoint"),
                block_device.get("path"),
                block_device.get("uuid")
            )

        # Check children if present
        result = get_children_info(block_device.get("children"), fs)
        if result[0] is not None:
            return (
                block_device.get("name"),
                block_device.get("path"),
                block_device.get("serial"),
                result[0],  # Mount point from children
                result[1],  # Disk path from children
                result[2]  # UUID from children
            )

    return None


def is_boot_volume(device_name, device_serial, block_devices):
    """Check if the given device is part of the boot volume."""
    try:
        root_device_info = get_block_device_info(block_devices, "/")
        if root_device_info:
            root_name, _, root_serial, _, _, _ = root_device_info
            return root_name == device_name and root_serial == device_serial
        return False
    except Exception as e:
        print(f"Error checking boot volume: {e}")
        return False


def search_file_system_info(blockdevices, filesystem):
    """Search and print block device information for the given filesystem."""
    try:
        device_info = get_block_device_info(blockdevices, filesystem)
        if device_info:
            name, path, serial, mount_point, disk, uuid = device_info
            print(f"Name: {name}")
            print(f"Path: {path}")
            print(f"Serial: {serial}")
            print(f"Mount Point: {mount_point}")
            print(f"Disk Path: {disk}")
            print(f"UUID: {uuid}")
            boot_volume = is_boot_volume(name, serial, blockdevices)
            print(f"Is Boot Volume: {'Yes' if boot_volume else 'No'}")
        else:
            print(f"No block device found for mount point: {filesystem}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Main function to execute the script."""
    filesystems = read_file_system()
    blockdevices = read_block_devices()

    for filesystem in filesystems:
        search_file_system_info(blockdevices, filesystem[1])
        print()


if __name__ == '__main__':
    main()
