from collections import namedtuple
from directory_management import *
from file_management import write_to_file as wf
import shutil
import subprocess
import re

full_inventory_list = []


def linux_command(search_title, cmd):
    try:
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True,
                                   universal_newlines=True)

        outs, errs = process.communicate()
        success = search_title + '\n', outs, '\n\n'

    except SystemError:
        print(errs)
        raise SystemError

    return list(success)


def clean_list(a_list):
    delimiters = "\n", ":"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    a_string = re.split(regex_pattern, str(a_list))
    return list(a_string)


def make_dict(a_list, inventory_category):

    a_dict = {}
    a_dict.setdefault('inventory_category',
                        [
                          {'item', 'value'},
                          {'item', 'value'},
                          {'item', 'value'},
                          {'item', 'value'}
                        ]
                      )

    for i in range(0, len(a_list), 2):
        a_dict.setdefault(inventory_category, [{a_list[i], a_list[i+1]}])

    return a_dict


def hardware_inventory():
    # Shows information like number of CPUs, cores, threads and more - -J for json output
    full_inventory_list.append(
        linux_command('Number of CPUs, cores, threads and more: \n', 'lscpu'))

    # List a general hardward data -json option for json output
    full_inventory_list.append(
        linux_command('General hardware data: \n', 'lshw'))

    # Buffer size
    full_inventory_list.append(
        linux_command('Buffer Size: \n', 'cat /proc/meminfo | grep Buffers'))

    # All mem info
    full_inventory_list.append(
        linux_command('Memory Information: \n', 'cat /proc/meminfo'))

    # Produces information about all block devices, such as hard disks, DVD readers and more
    full_inventory_list.append(
        linux_command('Block Devices: \n', 'lsblk'))

    # Provides information on all SCSI devices or hosts attached to your box, such as hard
    # disk drives or optical drives.
    full_inventory_list.append(
        linux_command('SCSI devices/ hosts attached to machine: \n ',
                      'lsblk --scsi'))

    # Displays information about PCI buses in your box and devices connected to them,
    # such as graphics cards, network adapters and more.
    full_inventory_list.append(
        linux_command('PCI buses:'
                          'such as graphics cards, network adapters etc: \n', 'lspci'))

    # USB busses and current connections information
    full_inventory_list.append(
        linux_command('USB buses: \n', 'lsusb'))

    # Display only real disk partitions
    full_inventory_list.append(
        linux_command('Real disk partitions: \n',
                      'df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs'))

    # Show hardware interrupts
    full_inventory_list.append(
        linux_command('Show hardware interrupts: \n', 'cat /proc/interrupts'))


def network_info():

    full_inventory_list.append(
        linux_command('Network devices with statistics: \n', 'cat /proc/net/dev'))

    full_inventory_list.append(
        linux_command('The Layer2 multicast groups which a device is listening '
                      'to (interface index, label, number of references, '
                      'number of bound addresses). \n', ' cat /proc/net/dev_mcast'))

    netdevs = netdev()
    for dev in netdevs.keys():
        full_inventory_list.append('RX and TX bytes for each of the network devices: \n'
            '{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx) + '\n \n')


def netdev():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    device_data = {}

    data = namedtuple('data', ['rx', 'tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                float(line[1].split()[8])/(1024.0*1024.0))

    return device_data


def software_inventory():
    # Modules
    full_inventory_list.append(
        linux_command('List of modules: \n', 'lsmod'))

    # List of installed packages
    full_inventory_list.append(
        linux_command('List of installed packages: \n', 'dpkg --get-selections'))


def os_version():
    full_inventory_list.append(
        linux_command('OS Version: \n', 'cat /proc/version'))


def process_list():

    # Number of running services
    pids = []

    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)

    full_inventory_list.append(
        'Total number of running processes: {0}'.format(len(pids)) + '\n \n')

    full_inventory_list.append(
        linux_command('All Processes', 'ps -A'))


def hostname():
    full_inventory_list.append(
        linux_command('Hostname: \n', 'uname -n'))


def mounted_drives():
    # Mounted drives and filesystems
    full_inventory_list.append(
        linux_command('Mounted drives and filesystems: \n', 'df -h --output=source,target'))


def environment_vars():
    # List environment varuables
    full_inventory_list.append(
        linux_command('List environment varuables: \n', 'env'))


def collect_inventory():
    hostname()
    hardware_inventory()
    network_info()
    software_inventory()
    os_version()
    process_list()
    mounted_drives()
    environment_vars()


def write_inventory_to_file(inventory_list):
    file_name = 'Linux Inventory Sweep'
    wf(file_name, inventory_list)


def main():
    dir_name = 'Linux System Inventory'
    main_dir_name = 'Inventory_store'
    file_name = 'Linux Inventory Sweep'

    # Create unique directory name and create directory.
    directory = unique_directory(dir_name)
    create_directory(directory)
    create_directory(main_dir_name)

    # Add all inventories to a list
    collect_inventory()
    wf(file_name, full_inventory_list)

    # Move file to directory
    shutil.move(file_name, directory)
    # Move directory to directory
    shutil.move(directory, main_dir_name)


if __name__ == '__main__':
    main()
