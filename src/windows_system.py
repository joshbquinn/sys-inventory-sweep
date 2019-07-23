#!/usr/bin/env python

import subprocess
import directory_management as dm
from file_management import *
import shutil
import json
from dict_factory import *
from time_stamper import *


def windows_cli(cmd, arguments):
    try:
        process = subprocess.Popen(cmd + " " + arguments,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

        outs, errs = process.communicate()
        success = outs

    except SystemError:
        print(errs)
        raise SystemError

    return success


def serialize_json(list_object):
    return json.loads(list_object)


def do_json(inventory_string, inventory_cat):
    return make_dict(serialize_json(inventory_string), inventory_cat)


def ports():
    ports = windows_cli('powershell.exe get-nettcpconnection',
                                     ' | select local*,remote*,state '
                                     '| ConvertTo-json')
    return do_json(ports, 'Open Port ')


def general_sysinfo():
    general_sysinfo = windows_cli('powershell.exe systeminfo', ' | ConvertTo-JSON')
    return multiple_column_dict('System Info', clean_string(general_sysinfo))


def processor_details(cmd):
    processor_details = windows_cli(cmd, 'Win32_processor | '
                                                               'select-object '
                                                               'Name, '
                                                               'DeviceID, '
                                                               'NumberOfCores,'
                                                               'NumberOfEnabledCore, '
                                                               'NumberOfLogicalProcessors, '
                                                               'L2CacheSize,'
                                                               'L3CacheSize,'
                                                               'MaxClockSpeed,'
                                                               'CurrentClockSpeed,'
                                                               'Addresswidth |'
                                                               'convertTo-Json')
    return do_json(processor_details, 'Processor ')


def physical_memory(cmd):
    physical_memory = windows_cli(cmd, ' Win32_PhysicalMemory | select-object '
                                                             'Name, '
                                                             'ConfiguredClockSpeed,'
                                                             'Capacity, '
                                                             'TotalWidth, '
                                                             'SerialNumber |'
                                                             'convertTo-Json')
    return do_json(physical_memory, 'Physical Memory Details ')


def hdd_details(cmd):
    hdd_details = windows_cli(cmd, 'Win32_LogicalDisk | '
                                                         'select-object '
                                                         'Name,'
                                                         'Description, '
                                                         'Size,'
                                                         'FreeSpace,'
                                                         'DriveType | '
                                                         'convertTo-Json')
    return do_json(hdd_details, 'HDD ')


def sound_card_details(cmd):
    sound_card_details = windows_cli(cmd, 'win32_SoundDevice | '
                                                                'select-object '
                                                                'ProductName, '
                                                                'Name,'
                                                                'Status | '
                                                                'convertTo-Json')
    return do_json(sound_card_details, 'Sound Card ' )


def network_adapter_details(cmd):
    network_adapter_details = windows_cli( cmd, 'Win32_NetworkAdapter | select-object '
                                                                     'MACAddress,'
                                                                     'ProductName,'
                                                                     'ServiceName,'
                                                                     'TimeOfLastReset,  '
                                                                     'AdapterType,'
                                                                     'AdapterTypeId,'
                                                                     'AutoSense,'
                                                                     'Caption,'
                                                                     'ConfigManagerErrorCode,'
                                                                     'ConfigManagerUserConfig,'
                                                                     'CreationClassName,'
                                                                     'Description,'
                                                                     'ErrorCleared,'
                                                                     'ErrorDescription,'
                                                                     'GUID,'
                                                                     'Index,'
                                                                     'InstallDate,'
                                                                     'Installed,'
                                                                     'InterfaceIndex,'
                                                                     'LastErrorCode,'
                                                                     'Manufacturer,'
                                                                     'MaxNumberControlled,'
                                                                     'MaxSpeed,'
                                                                     'Manufacturer,'
                                                                     'MaxNumberControlled,'
                                                                     'MaxSpeed,'
                                                                     'NetConnectionID,'
                                                                     'NetConnectionStatus,'
                                                                     'NetEnabled,'
                                                                     'NetworkAddresses,'
                                                                     'PermanentAddress,'
                                                                     'PhysicalAdapter,'
                                                                     'PowerManagementCapabilities'
                                                                     ' | convertTo-Json')
    return do_json(network_adapter_details, 'Network Adapter ')


def installed_software(cmd):
    installed_software = windows_cli(cmd, 'Win32_Product | Select-Object '
                                                                'Name, '
                                                                'PackageCode,'
                                                                'IdentifyingNumber, '
                                                                'PackageCache,  '
                                                                'Vendor, '
                                                                'Version, '
                                                                'InstallSource,'
                                                                'InstallDate,'
                                                                'InstallDate2 '
                                                                ' | convertTo-Json')
    return do_json(installed_software, 'Software Package ')


def os_version(cmd):
    os = windows_cli(cmd, 'win32_operatingsystem | Select-Object '
                                                        'Name, '
                                                        'OSArchitecture, '
                                                        'BuildNumber,'
                                                        'Version, '
                                                        'ServicePackMajorVersion, '
                                                        'ServicePackMinorVersion |'
                                                        ' convertTo-Json')
    return do_json(os, 'OS Version')


def driver_details(cmd):
    driver_details = windows_cli(cmd, 'Win32_PnPSignedDriver | select-object '
                                                            'devicename, '
                                                            'driverversion | '
                                                            'convertTo-Json')
    return do_json(driver_details, 'Driver ')


def running_processes(cmd):
    running_processes = windows_cli(cmd, 'win32_process | Select-Object '
                                                               'ProcessName, '
                                                               'ProcessId, '
                                                               'PageFaults '
                                                               ' | convertTo-json')
    return do_json(running_processes, 'Running Process ')


def startup_programs(cmd):
    startup_programs= windows_cli(cmd, 'Win32_StartupCommand |'
                                                               'select-object  '
                                                               'Description, '
                                                               'Location, '
                                                               'User | '
                                                               'convertTo-Json')
    return do_json(startup_programs, 'Start Up Program ')


def env_vars(cmd):
    env_vars = windows_cli(cmd, 'Win32_Environment | '
                                                                   'select-object '
                                                                   'Name, '
                                                                   'VariableValue | '
                                                                   'convertTo-Json')
    return do_json(env_vars, 'Environmental Variable ')


def windows_inventory_list():
    psgwmi = 'powershell.exe Get-WmiObject -class '
    inventory_dict = {}

    inventory_dict.update({"Date Time": time_stamp()})
    inventory_dict.update(dict({'Ports': ports()}))
    # inventory_dict.update(dict({'Sys': general_sysinfo()}))
    inventory_dict.update(dict({'Processor Details': processor_details(psgwmi)}))
    inventory_dict.update(dict({'Physical Mem': physical_memory(psgwmi)}))
    inventory_dict.update(dict({'HDD': hdd_details(psgwmi)}))
    inventory_dict.update(dict({'Sound Card': sound_card_details(psgwmi)}))
    inventory_dict.update(dict({'Network Adapters': network_adapter_details(psgwmi)}))
    inventory_dict.update(dict({'Installed Software': installed_software(psgwmi)}))
    inventory_dict.update(dict({'OS': os_version(psgwmi)}))
    inventory_dict.update(dict({'Drivers': driver_details(psgwmi)}))
    inventory_dict.update(dict({'Running Processes': running_processes(psgwmi)}))
    inventory_dict.update(dict({'Startup Programs': startup_programs(psgwmi)}))
    inventory_dict.update(dict({'Environmental Variables': env_vars(psgwmi)}))

    write_file(inventory_dict)


def write_file(json_dict):

    file_name = 'Windows_Inventory_Sweep.json'
    main_dir_name = 'Inventory_store'

    # Create unique directory name and create directory.
    file_name = dm.unique_name(file_name)
    dm.create_directory(main_dir_name)

    write_json_file(file_name, json_dict)
    shutil.move(file_name, main_dir_name)


def main():
    windows_inventory_list()


if __name__ == '__main__':
    main()

