import sys
import os
import subprocess
import shlex

def get_executable_files():
    path = os.environ['PATH']
    directories = path.split(os.pathsep)
    executable_files = {}
    for directory in directories:
        if os.path.isdir(directory):
            for entry in os.scandir(directory):
                try:
                    if entry.is_file() and os.access(entry.path, os.X_OK):
                        executable_files[entry.name] = entry.path
                except:
                    pass
    return executable_files

def main():
    executable_files = get_executable_files()

    while True:
        sys.stdout.write("$ ")
        try:
            command, *args = shlex.split(input().strip())
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            continue

        if not command:
            continue

        if command == "exit":
            if len(args) > 0:
                try:
                    code = int(args[0])
                except ValueError:
                    sys.stdout.write(f"exit: {args[0]}: numeric argument required\n")
                sys.exit(code)
            else:
                sys.stdout.write("Invalid number of arguments\n")

        elif command == "echo":
            sys.stdout.write(f"{' '.join(args)}\n")

        elif command == "type":
            if len(args) != 1:
                sys.stdout.write("Invalid number of arguments\n")
                continue
            
            if args[0] in ["echo", "type", "exit", "pwd", "cd"]:
                sys.stdout.write(f"{args[0]} is a shell builtin\n")
            elif args[0] in executable_files:
                sys.stdout.write(f"{args[0]} is {executable_files[args[0]]}\n")
            else:
                sys.stdout.write(f"{args[0]}: not found\n")

        elif command == "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        
        elif command == "cd":
            if len(args) != 1:
                sys.stdout.write("Invalid number of arguments\n")
                continue
            destination = args[0]
            if args[0] == "~":
                homedir = os.path.expanduser("~")
                destination = homedir
            elif not os.path.isdir(destination):
                sys.stdout.write(f"cd: {args[0]}: No such file or directory\n")
                continue

            try:
                os.chdir(destination)
            except Exception as e:
                sys.stdout.write(f"cd: {e}\n")
        else:
            if command in executable_files:
                try:
                    subprocess.run([executable_files[command], *args])
                except Exception as e:
                    sys.stdout.write(f"Error: {e}\n")
            else:
                sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
