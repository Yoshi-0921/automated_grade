import csv
import glob
import subprocess

def compile_c(root):
    c_files = glob.glob(f'{root}/*/*.c')

    for c_file in c_files:
        assert ".c" in c_file

        c_file = c_file[:-2] # remove ".c" from the path
        cmd = ["gcc", fr"{c_file}.c", "-o", fr"{c_file}"]

        subprocess.run(cmd)
