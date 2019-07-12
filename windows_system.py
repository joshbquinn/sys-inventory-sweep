import subprocess
import directory_management as dm
from file_management import write_to_file as wf
import shutil
import re
import json
import pprint


def windows_cli(cmd, arguments):
    try:
        process = subprocess.Popen(cmd + arguments,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

        outs, errs = process.communicate()
        success = outs

    except SystemError:
        print(errs)
        raise SystemError

    return success


def clean_list(a_string):
    delimiters = ":"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    a_string = re.split(regex_pattern, str(a_string))
    print(str(a_string))
    return str(a_string)


def make_dict(a_list, category_name):

    a_dict = {}
    i = 1

    if isinstance(a_list, dict):
        a_dict[category_name] = a_list
        return a_dict
    else:
        for item in a_list:
            a_dict[(category_name + str(i))] = item
            i += 1
        return a_dict


def serialize_json(list_object):
    return json.loads(list_object)


def deserialize_json(dictionary_object):
    return json.dumps(dictionary_object, indent=4)


def do_json(inventory_string, inventory_cat):
    return make_dict(serialize_json(inventory_string), inventory_cat)


def ports():
    ports = windows_cli('powershell.exe get-nettcpconnection',
                                     ' | select local*,remote*,state '
                                     '| ConvertTo-json')
    return do_json(ports, 'Open Port ')


def general_sysinfo():
    general_sysinfo = windows_cli('powershell.exe systeminfo', ' | ConvertTo-JSON')

    print(general_sysinfo)

    return do_json(general_sysinfo, 'Sys')


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
                                                             ' Capacity, '
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
    json_list = []

    json_list.append(dict({'Ports': ports()}))
    # json_list.append(general_sysinfo())
    json_list.append(dict({'Processor Details': processor_details(psgwmi)}))
    json_list.append(dict({'Physical Mem': physical_memory(psgwmi)}))
    json_list.append(dict({'HDD': hdd_details(psgwmi)}))
    json_list.append(dict({'Sound Card': sound_card_details(psgwmi)}))
    json_list.append(dict({'Network Adapters': network_adapter_details(psgwmi)}))
    json_list.append(dict({'Installed Software': installed_software(psgwmi)}))
    json_list.append(dict({'OS': os_version(psgwmi)}))
    json_list.append(dict({'Drivers': driver_details(psgwmi)}))
    json_list.append(dict({'Running Processes': running_processes(psgwmi)}))
    json_list.append(dict({'Startup Programs': startup_programs(psgwmi)}))
    json_list.append(dict({'Environmental Variables': env_vars(psgwmi)}))

    for item in json_list:
        print(deserialize_json(item))

    write_json_file("windows_scrape.json", json_dict)
    write_file(json_list)


def write_file(json_list):

    dir_name = 'Windows_System_Inventory'
    file_name = 'Windows_Inventory_Sweep'
    main_dir_name = 'Inventory_store'

    # Create unique directory name and create directory.
    directory = dm.unique_directory(dir_name)
    dm.create_directory(directory)
    dm.create_directory(main_dir_name)

    wf(file_name, json_list)

    shutil.move(file_name, directory)
    shutil.move(directory, main_dir_name)


def write_json_file(filename, json_dict):

    with open(filename, 'w') as f:
        json.dump(json_dict, f)


def main():
    windows_inventory_list()


if __name__ == '__main__':
    main()

