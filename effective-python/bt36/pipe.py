
import os
import subprocess

def run_openssl(data, i):
    env = os.environ.copy()
    env['password'] = b'\xe24U\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    proc.stdin.write(data)
    proc.stdin.flush()
    return proc


def run_md5(input_stdin, i):
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    ) 
    print('run_md5:', i)
    return proc


input_procs = []
hash_procs = []
for i in range(3):
    data = os.urandom(10)
    proc = run_openssl(data, i)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout, i)
    hash_procs.append(hash_proc)

for proc in input_procs:
    out, err = proc.communicate()

print('all input_procs communicate')

for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())


print('all hash_procs communicate')

