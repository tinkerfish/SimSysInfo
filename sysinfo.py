import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 -> '1.20MB'
        1253656678 -> '1.17GB'
    """

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def print_sys_info():
    uname = platform.uname()
    print("\n")
    print("="*40, "System Information", "="*40)
    print(f"System:\t\t{uname.system}")
    print(f"Node Name:\t{uname.node}")
    print(f"Release:\t{uname.release}")
    print(f"Version:\t{uname.version}")
    print(f"Machine:\t{uname.machine}")
    print(f"Processor:\t{uname.processor}")


def print_uptime():
    print("\n")
    print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = datetime.fromtimestamp(psutil.boot_time())
    bt = boot_time_timestamp.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"Boot Time: {bt}")


def print_cpu_info():
    print("\n")
    print("="*40, "CPU Info", "="*40)
    # number of cores
    print(f"Physical cores:\t\t{psutil.cpu_count(logical=False)}")
    print(f"Total cores:\t\t{psutil.cpu_count(logical=True)}")
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max frequency:\t\t{cpufreq.max:.2f}Mhz")
    print(f"Min frequency:\t\t{cpufreq.min:.2f}Mhz")
    print(f"Current frequency:\t{cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"  Core {i}: {percentage}%")
    print(f"Total CPU usage:\t{psutil.cpu_percent()}%")


def print_mem_info():
    # memory information
    print("\n")
    print("="*40, "Memory Information", "="*40)
    # memory details
    print("\n=== Physical memory ===")
    svmem = psutil.virtual_memory()
    print(f"Total:\t\t{get_size(svmem.total)}")
    print(f"Available:\t{get_size(svmem.available)}")
    print(f"Used:\t\t{get_size(svmem.used)}")
    print(f"Percentage:\t{svmem.percent}%")
    # swap memory details (if exists)
    print("\n=== Swap Memory ===")
    swap = psutil.swap_memory()
    print(f"Total:\t\t{get_size(swap.total)}")
    print(f"Free:\t\t{get_size(swap.free)}")
    print(f"Used:\t\t{get_size(swap.used)}")
    print(f"Percentage:\t{swap.percent}%")


def print_disk_info():
    # disk info
    print("\n")
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:\n")
    # get all partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint:\t\t{partition.mountpoint}")
        print(f"  File system type:\t{partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total size:\t\t{get_size(partition_usage.total)}")
            print(f"  Used:\t\t\t{get_size(partition_usage.used)}")
            print(f"  Free:\t\t\t{get_size(partition_usage.free)}")
            print(f"  Percentage:\t\t{partition_usage.percent}%")
        except PermissionError as e:
            # this can be safely caught if the disk isnt ready
            print("===[ERROR]: Unable to access disk===")
            print(f"===[ERROR]: {e}")
            continue
    # get io stats since boot
    disk_io = psutil.disk_io_counters()
    print(f"\nTotal read:\t{get_size(disk_io.read_bytes)}")
    print(f"Total write:\t{get_size(disk_io.write_bytes)}")


def print_network_info():
    # network info
    print("\n")
    print("="*40, "Network Information", "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_address, in if_addrs.items():
        for address in interface_address:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP address:\t{address.address}")
                print(f"  Netmask:\t{address.netmask}")
                print(f"  Broadcast IP:\t{address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address:\t\t{address.address}")
                print(f"  Netmask:\t\t{address.netmask}")
                print(f"  Broadcast MAC:\t{address.broadcast}")
    # IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"\nTotal bytes sent:\t{get_size(net_io.bytes_sent)}")
    print(f"Total bytes received:\t{get_size(net_io.bytes_recv)}")


def main():
    print_sys_info()
    print_uptime()
    print_cpu_info()
    print_mem_info()
    print_disk_info()
    print_network_info()


if __name__ == "__main__":
    main()
    print("\n\t===End Output===\n")

