Problem 2
- 
 
Write a python script to capture Hardware, software, firmware inventory on any machine. It should work on both Windows and Linux. All the details should be captured in a file.

**How to solve:** 
- Where is this information stored on each the system types? 
- What commands do I need to access files containing the information?

**Script Steps**
- Determine OS
- Run CLI commands with sub-processes to return inventory strings.
- Remove certain characters from strings with reg ex if required.
- Create dictionaries from those strings. 
- Add to one single dictionary
- Write the dictionary as json file 
- Store file in directory in CWD 

 