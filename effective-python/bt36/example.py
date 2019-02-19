import subprocess


proc = subprocess.Popen(
    ['sleep', '1'],
)

print('sleep start')
out, err = proc.communicate()
print('sleep end')
#print(out.decode('utf-8'))

proc = subprocess.Popen(['sleep', '0.01'])
'''
while proc.poll() is None:
    print('working...')

print('Exit status', proc.poll())
'''
