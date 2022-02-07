from compiler import compile_c
from executer import execute
from select_files import select_files


def main(root):
    select_files(root)
    compile_c(root)
    execute(root)

if __name__ == '__main__':
    root = "./part1"

    main(root)
