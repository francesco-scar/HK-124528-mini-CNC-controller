import sys

if len(sys.argv) != 3:
	print("Usage: pyhton3 Duplicate_line_gcode.py <FILE> <REPEAT_NUMBER>")
	exit()

file = open(sys.argv[1], 'r')
lines = file.read().split('\n')
file.close()

new_file = open(sys.argv[1]+'.edit', 'w')
for line in lines:
	new_file.write((line+'\n')*int(sys.argv[2]))
new_file.close()
