from collections import namedtuple
from directory_management import *
from file_management import *
import shutil
import subprocess
from dict_factory import *


def bash(cmd):
    try:
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True,
                                   universal_newlines=True)

        outs, errs = process.communicate()

    except SystemError:
        print(errs)
        raise SystemError

    return outs


def hardware_inventory():
    hardware_dict = {}

    # Shows information like number of CPUs, cores, threads and more - -J for json output
    hardware_dict.update(two_column_dict('CPU', clean_list(bash('lscpu'))))

    hardware_dict.update(two_column_dict('Memory', clean_list(bash('cat /proc/meminfo'))))

    # Produces information about all block devices, such as hard disks, DVD readers and more
    hardware_dict.update(dict({'Block Devices': multiple_column_dict('Block Device {}', bash('lsblk'))}))

    # Provides information on all SCSI devices or hosts attached to your box, such as hard
    # disk drives or optical drives.
    hardware_dict.update(dict({'SCSI Devices': multiple_column_dict('SCSI Device {}', (bash('lsblk --scsi')))}))

    # Displays information about PCI buses in your box and devices connected to them,
    # such as graphics cards, network adapters and more.
    hardware_dict.update(dict({'PCI Buses': multiple_column_dict('PCI Bus {}', (bash('lspci')))}))

    # USB busses and current connections information
    # Display only real disk partitions
    hardware_dict.update(dict({'Real Disk Partitions': multiple_column_dict('Real Disk Partition {}',
                               bash('df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs'))}))

    # TODO
    #inv.append(bash('lshw'))
    # TODO
    #inv.append(bash('Show hardware interrupts: \n', 'cat /proc/interrupts'))

    return hardware_dict


# TODO
def network_info():

    # Network devices with statistics
    inv.append(
        bash('cat /proc/net/dev'))

    # Interface index, label, number of references, number of bound addresses
    inv.append(
        bash(' cat /proc/net/dev_mcast'))

    netdevs = netdev()
    for dev in netdevs.keys():
        inv.append('RX and TX bytes for each of the network devices: \n'
            '{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx) + '\n \n')


# TODO
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
    software_dict = {}

    # Modules
    software_dict.update(dict({'Modules': multiple_column_dict('Module {}', bash('lsmod'))}))

    # List of installed packages
    software_dict.update(dict({'Packages': multiple_column_dict('Installed Package {}', (bash('dpkg --get-selections')))}))

    return software_dict


def os_version():
    return dict({'OS Version': bash('cat /proc/version')})


def process_list():

    # Number of running services
    return dict({'Processes': multiple_column_dict('Process {}', bash('ps -A'))})


def hostname():

    return dict({'Hostname': bash('uname -n')})


def mounted_drives():
    # Mounted drives and filesystems
    return dict({'Mounted drives and filesystems':
                         multiple_column_dict('Filesytem {}',
                                              bash('df -h --output=source,target'))})


def environment_vars():
    # List Environment Variables
    return dict({'Environment Variables': multiple_column_dict('Environment Variable {}', bash('env'))})


def collect_inventory():
    inventory_dict = {}

    inventory_dict.update(time_stamp())
    inventory_dict.update(hostname())
    inventory_dict.update(hardware_inventory())
    # inventory_dict.update(network_info())
    inventory_dict.update(software_inventory())
    inventory_dict.update(os_version())
    inventory_dict.update(process_list())
    inventory_dict.update(mounted_drives())
    inventory_dict.update(environment_vars())

    return inventory_dict


def main():
    dir_name = 'Linux System Inventory'
    main_dir_name = 'Inventory_store'
    file_name = 'Linux_Inventory_Sweep.json'

    # Create unique directory name and create directory.
    directory = unique_directory(dir_name)
    create_directory(directory)
    create_directory(main_dir_name)

    # return the system dictionary and write json file
    write_json_file(file_name, collect_inventory())
    # write_to_file(file_name, inv)

     # Move file to directory
    shutil.move(file_name, directory)
    # Move directory to directory
    shutil.move(directory, main_dir_name)

    # test()

if __name__ == '__main__':
    main()
