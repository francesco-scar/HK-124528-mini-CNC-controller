import sys

if len(sys.argv) != 3:
	print("Usage: pyhton3 Duplicate_line_gcode.py <FILE> <REPEAT_NUMBER>")
	exit()

file = open(sys.argv[1], 'r')
lines = file.read().split('\n')
file.close()

if len(sys.argv[1].split('/')) == 1:
	output_filename = 'Edit_' + sys.argv[1]
else:
	output_filename = sys.argv[1].split(sys.argv[1].split('/')[-1])[0] + 'Edit_' + sys.argv[1].split('/')[-1]

new_file = open(output_filename, 'w')
for line in lines:
	new_file.write((line+'\n')*int(sys.argv[2]))
new_file.close()
