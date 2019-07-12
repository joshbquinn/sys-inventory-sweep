from collections import namedtuple
from directory_management import *
from file_management import *
import shutil
import subprocess
import re
import os
from dict_factory import *
from json_management import *
from datetime import datetime


inv = []



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


def test():
    lscpu = bash('lscpu')
    clean = clean_list(lscpu)
    print(deserialize_json(two_column_dict(clean, 'CPU')))

    lsblk = bash('lsblk')
    d = multiple_column_dict(lsblk, 'Block Devices {}')
    print(deserialize_json(d))


def hardware_inventory():
    # Shows information like number of CPUs, cores, threads and more - -J for json output
    inv.append(two_column_dict('CPU', clean_list(bash('lscpu'))))

    inv.append(two_column_dict('Memory', clean_list(bash('cat /proc/meminfo'))))

    # Produces information about all block devices, such as hard disks, DVD readers and more
    inv.append(dict({'Block Devices': multiple_column_dict('Block Device {}', bash('lsblk'))}))

    # Provides information on all SCSI devices or hosts attached to your box, such as hard
    # disk drives or optical drives.
    inv.append(dict({'SCSI Devices': multiple_column_dict('SCSI Device {}', (bash('lsblk --scsi')))}))

    # Displays information about PCI buses in your box and devices connected to them,
    # such as graphics cards, network adapters and more.
    inv.append(dict({'PCI Buses': multiple_column_dict('PCI Bus {}', (bash('lspci')))}))


    # USB busses and current connections information
    # Display only real disk partitions
    inv.append(dict({'Real Disk Partitions': multiple_column_dict('Real Disk Partition {}',
                               bash('df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs'))}))

    # TODO
    #inv.append(bash('lshw'))
    # TODO
    #inv.append(bash('Show hardware interrupts: \n', 'cat /proc/interrupts'))


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
    inv.append(dict({'Modules': multiple_column_dict('Module {}', bash('lsmod'))}))

    # List of installed packages
    inv.append(dict({'Packages': multiple_column_dict('Installed Package {}', (bash('dpkg --get-selections')))}))


def os_version():
    inv.append(dict({'OS Version': bash('cat /proc/version')}))



def process_list():

    # Number of running services
    inv.append(dict({'Processes': multiple_column_dict('Process {}', bash('ps -A'))}))


def hostname():

    inv.append(dict({'Hostname': bash('uname -n')}))


def mounted_drives():
    # Mounted drives and filesystems
    inv.append(dict({'Mounted drives and filesystems':
                         multiple_column_dict('Filesytem {}',
                                              bash('df -h --output=source,target'))}))


def environment_vars():
    # List Environment Variables
    inv.append(dict({'Environment Variables': multiple_column_dict('Environment Variable {}', bash('env'))}))

def collect_inventory():
    hostname()
    hardware_inventory()
    #network_info()
    software_inventory()
    os_version()
    process_list()
    mounted_drives()
    environment_vars()


def main():
    dir_name = 'Linux System Inventory'
    main_dir_name = 'Inventory_store'
    file_name = 'Linux_Inventory_Sweep.json'

    now = datetime.now()
    date = now.strftime("%d.%m.%Y %Hhr.%Mm.%Ss")
    date_dict = dict({'Date': date})



    # Create unique directory name and create directory.
    directory = unique_directory(dir_name)
    create_directory(directory)
    create_directory(main_dir_name)

    # Add all inventories to a global list
    collect_inventory()
    write_json_file(file_name, date_dict)
    write_json_file(file_name, inv)
    # write_to_file(file_name, inv)

     # Move file to directory
    shutil.move(file_name, directory)
    # Move directory to directory
    shutil.move(directory, main_dir_name)

    # test()

if __name__ == '__main__':
    main()
