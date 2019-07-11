import subprocess
import directory_management as dm
from file_management import write_to_file as wf
import shutil
import re


def wmi_lookup(search_title, cmd, arguments):
    try:
        process = subprocess.Popen(cmd + arguments,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

        outs, errs = process.communicate()
        success = {search_title, outs}

    except SystemError:
        print(errs)
        raise SystemError

    return success


def clean_list(a_list):
    delimiters = "\n", ":"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    a_string = re.split(regex_pattern, str(a_list))
    return list(a_string)


def make_dict(a_list):

    a_dict = {}
    i = 0
    a_dict.setdefault(f'inventory_category{i}',
                      [
                          {'item', 'value'},
                          {'item', 'value'},
                          {'item', 'value'},
                          {'item', 'value'}
                      ]
                      )

    for i in range(0, len(a_list), 2):
        a_dict.setdefault(a_list[i], a_list[i+1])

    return a_dict


def windows_inventory_list():

    inventory_list = []
    cmd = 'powershell.exe Get-WmiObject -class '

    inventory_list.append(wmi_lookup('Open Ports', 'powershell.exe get-nettcpconnection',
                                     ' | select local*,remote*,state '
                                     '| ConvertTo-json'))

    inventory_list.append(wmi_lookup('General System Info', 'powershell.exe systeminfo', ' | ConvertTo-json'))

    inventory_list.append(wmi_lookup('Processor Details', cmd, 'Win32_processor | '
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
                                                               'convertTo-Json'))

    inventory_list.append(wmi_lookup('Physical Memory', cmd, ' Win32_PhysicalMemory | select-object '
                                                             'Name, '
                                                             'ConfiguredClockSpeed,'
                                                             ' Capacity, '
                                                             'TotalWidth, '
                                                             'SerialNumber |'
                                                             'convertTo-Json'))

    inventory_list.append(wmi_lookup('HDD Details', cmd, 'Win32_LogicalDisk | '
                                                         'select-object '
                                                         'Name,'
                                                         'Description, '
                                                         'Size,'
                                                         'FreeSpace,'
                                                         'DriveType | '
                                                         'convertTo-Json'))

    inventory_list.append(wmi_lookup('Sound Card Details', cmd, 'win32_SoundDevice | '
                                                                'select-object '
                                                                'ProductName, '
                                                                'Name,'
                                                                'Status | '
                                                                'convertTo-Json'))

    inventory_list.append(wmi_lookup('Network Adapter Details', cmd, 'Win32_NetworkAdapter | select-object '
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
                                                                     ' | convertTo-Json'))

    inventory_list.append(wmi_lookup('Installed Software', cmd, 'Win32_Product | Select-Object '
                                                                'Name, '
                                                                'PackageCode,'
                                                                'IdentifyingNumber, '
                                                                'PackageCache,  '
                                                                'Vendor, '
                                                                'Version, '
                                                                'InstallSource,'
                                                                'InstallDate,'
                                                                'InstallDate2 '
                                                                ' | convertTo-Json'))

    inventory_list.append(wmi_lookup('OS Version', cmd, 'win32_operatingsystem | Select-Object '
                                                        'Name, '
                                                        'OSArchitecture, '
                                                        'BuildNumber,'
                                                        'Version, '
                                                        'ServicePackMajorVersion, '
                                                        'ServicePackMinorVersion |'
                                                        ' convertTo-Json'))

    inventory_list.append(wmi_lookup('Driver Details', cmd, 'Win32_PnPSignedDriver | select-object '
                                                            'devicename, '
                                                            'driverversion | '
                                                            'convertTo-Json'))

    inventory_list.append(wmi_lookup('Running Processes', cmd, 'win32_process | Select-Object '
                                                               'ProcessName, '
                                                               'ProcessId, '
                                                               'PageFaults '
                                                               ' | convertTo-json'))



    inventory_list.append(wmi_lookup('Start Up Programs', cmd, 'Win32_StartupCommand |'
                                                               'select-object  '
                                                               'Description, '
                                                               'Location, '
                                                               'User | '
                                                               'convertTo-Json'))

    inventory_list.append(wmi_lookup('Environment Variables', cmd, 'Win32_Environment | '
                                                                   'select-object '
                                                                   'Name, '
                                                                   'VariableValue | '
                                                                   'convertTo-Json'))

    return inventory_list


def store_inventory(inventory_list):

    dir_name = 'Windows_System_Inventory'
    file_name = 'Windows_Inventory_Sweep'
    main_dir_name = 'Inventory_store'

    # Create unique directory name and create directory.
    directory = dm.unique_directory(dir_name)
    dm.create_directory(directory)
    dm.create_directory(main_dir_name)

    wf(file_name, inventory_list)

    shutil.move(file_name, directory)
    shutil.move(directory, main_dir_name)


def main():
    store_inventory(windows_inventory_list())


if __name__ == '__main__':
    main()

