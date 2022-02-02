file_data = open('lib/ctms/reference.ctm').read()
lines = file_data.split('\n')
print(len(lines))
print(lines[-1])