import subprocess

a = subprocess.run('executables/test_size', capture_output=True)

print(a.stdout.decode("utf-8"))
