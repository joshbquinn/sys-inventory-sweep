Problem 2
- 
 
The skills and knowledge developed from problem 1 will be reused in in building DevSecOps pipeline for problem 2.
Write a python script to capture Hardware, software, firmware inventory on any machine. It should work on both Windows and Linux. All the details should be captured in a file.

**How to solve:** 
- Where is this information stored on each the system types? 
- What functions do I need to access those files containing the information?

 **Creating Pipeline** 


**a.	Hardware inventory items:** 

- https://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/proc.html 
- https://www.tecmint.com/exploring-proc-file-system-in-linux/
- https://www.linuxjournal.com/content/interrogating-linux-machine
- https://www.networkworld.com/article/2825679/unix--automating-your-server-inventory.html
- https://unix.stackexchange.com/questions/24182/how-to-get-the-complete-and-exact-list-of-mounted-filesystems-in-linux 

1 .	CPU size
    
    $ cat /proc/cpuinfo
    
2 .	Buffer size

    $ cat /proc/meminfo | grep Buffers
    
3 .	Memory

    $ cat /proc/meminfo

4 .	HDD details

- Information (including device numbers) for each of the logical disk devices

     $ /proc/diskstats

- df file systems that are not real disk partitions 
    dev file systems are actual devices or partitions 
   
   ` $ df -h`
- To display only real disk partitions along with partition type, use df like this
  
    `$ df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs`

5 .	Audio/sound card details 
	
	$ lspci
	$ aplay -l (works)
	$ arecord -l
	$ cat /proc/asound/cards
	
6.	Network details etc

**b.	Software inventory items:** 
1.	List of software installed in a machine

	$ cat /proc/modules 
	$ dpkg --get-selections
	$ ls /usr/share/applications | awk -F '.desktop' ' { print $1}' -
	
2.	OS version & patch details
    
    $ cat /proc/version

**c.	Driver/Firmware details:**
1.	Soundcard
2.	Motherboard
3.	Network

- information about any devices connected via a SCSI or RAID controller 

    `cat /proc/scsi/device_info`

**d.	Running services**


**e.	Hostname**

    $ /proc/sys/kernel/hostname

**f.	List of startup programs**

**g.	List of mounted drives/mapped network locations**
    
        df -h --output=source,target
        
**h.	List of environment settings/variables**
    
    $ /proc/PID/environ 
    $ env
 
There is no single way to get these details. 

_You can use Python internally_

_You can call other scripts/binaries to get the details._ 

