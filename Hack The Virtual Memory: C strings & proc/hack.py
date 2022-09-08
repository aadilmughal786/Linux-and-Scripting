#!/usr/bin/python

'''             
Locates and replaces the first occurrence of a string in the heap
of a process    

Usage: ./1.py PID search_string replace_by_string
Where:           
- PID is the pid of the target process
- search_string is the ASCII string you are looking to overwrite
- replace_by_string is the ASCII string you want to replace
  search_string with
'''

import sys

def print_usage_and_exit():
	print(f"Usage :{sys.argv[0]} pid search write.")
	sys.exit()

#check usage
if len(sys.argv) !=4:
	print_usage_and_exit()

#get the pid from args
pid = int(sys.argv[1])

if(pid<=0):
	print_usage_and_exit()

search_string = str(sys.argv[2])

if search_string == "":
	print_usage_and_exit()

replace_by_string = str(sys.argv[3])

if replace_by_string == "":
	print_usage_and_exit()


#open the maps and mem files of the process
maps_filenamepath = f"/proc/{pid}/maps"
print(f"[*] maps: {maps_filenamepath}")
mem_filenamepath = f"/proc/{pid}/mem"
print(f"[*] mem: {mem_filenamepath}")

#try opening map file
try:
	maps_file = open(maps_filenamepath,"r")
except IOError as e:
	print(f"[ERROR] Can not open file {maps_filenamepath}")
	print(f"{' '*7} I/O error({e.errno}) : {e.strerror}")
	sys.exit(1)


for line in maps_file:
    sline = line.split(' ')
    # check if we found the heap
    if sline[-1][:-1] != "[heap]":
        continue
    print("[*] Found [heap]:")

    # parse line
    addr = sline[0]
    perm = sline[1]
    offset = sline[2]
    device = sline[3]
    inode = sline[4]
    pathname = sline[-1][:-1]
    print("\tpathname = {}".format(pathname))
    print("\taddresses = {}".format(addr))
    print("\tpermisions = {}".format(perm))
    print("\toffset = {}".format(offset))
    print("\tinode = {}".format(inode))

    # check if there is read and write permission
    if perm[0] != 'r' or perm[1] != 'w':
        print("[*] {} does not have read/write permission".format(pathname))
        maps_file.close()
        exit(0)

    # get start and end of the heap in the virtual memory
    addr = addr.split("-")
    if len(addr) != 2: # never trust anyone, not even your OS :)
        print("[*] Wrong addr format")
        maps_file.close()
        exit(1)
    addr_start = int(addr[0], 16)
    addr_end = int(addr[1], 16)
    print("\tAddr start [{:x}] | end [{:x}]".format(addr_start, addr_end))

    # open and read mem
    try:
        mem_file = open(mem_filenamepath, 'rb+')
    except IOError as e:
        print("[ERROR] Can not open file {}:".format(mem_filenamepath))
        print("        I/O error({}): {}".format(e.errno, e.strerror))
        maps_file.close()
        exit(1)

    # read heap  
    mem_file.seek(addr_start)
    heap = mem_file.read(addr_end - addr_start)

    # find string
    try:
        i = heap.index(bytes(search_string, "ASCII"))
    except Exception:
        print("Can't find '{}'".format(search_string))
        maps_file.close()
        mem_file.close()
        exit(0)
    print("[*] Found '{}' at {:x}".format(search_string, i))

    # write the new string
    print("[*] Writing '{}' at {:x}".format(replace_by_string, addr_start + i))
    mem_file.seek(addr_start + i)
    mem_file.write(bytes(replace_by_string, "ASCII"))

    # close files
    maps_file.close()
    mem_file.close()

    # there is only one heap in our example
    break