from argparse import ArgumentParser
from pathlib import Path
import subprocess

project_dir = Path.cwd()

pars = ArgumentParser()
pars.add_argument("--init", "-i", action="store_true")
pars.add_argument("--add", "-a", type=str)
pars.add_argument("--commit", "-c", action="store_true")
pars.add_argument("--message", "-m", type=str)
pars.add_argument("--push", "-p", type=str)
pars.add_argument("--file1", "-a1", type=str)
pars.add_argument("--file2", "-a2", type=str)
arg = vars(pars.parse_args())
print(arg)


def execute_init():
    return subprocess.run(["git", "init"])


def execute_add(filename):
    return subprocess.run(["git", "add", filename])


def execute_commit(message=str | None):
    if message is not None:
        return subprocess.run(["git", "commit", "-m", message])
    else:
        return subprocess.run(["git", "commit",])


def hash_object_create(filename):
    result = subprocess.run(["git", "hash-object", "-w", filename], stdout=subprocess.PIPE)
    return result


def execute_push(remote_branch):
    return subprocess.run(["git", "push", remote_branch])


if __name__ == "__main__":
    if arg["init"]:
        execute_init()

    if arg["add"] is not None:
        execute_add(arg["add"])

    if arg["commit"]:
        execute_commit(message=arg["message"])

    if (arg["file1"] is not None) and (arg["file2"] is None):
        file_1 = hash_object_create(arg["file1"]).stdout.decode("utf-8").strip()
        print(file_1)
    elif (arg["file1"] is not None) and (arg["file2"] is not None):
        file_1 = hash_object_create(arg["file1"]).stdout.decode("utf-8").strip()
        print("1:", file_1)
        file_2 = hash_object_create(arg["file2"]).stdout.decode("utf-8").strip()
        print("2:", file_2)
        command = ["git", "cat-file", "-p", file_2]
        res = subprocess.run(command, stdout=subprocess.PIPE)
        if res.returncode == 0:
            with open(arg["file1"], "wb") as file:
                file.write(res.stdout)
        else:
            print("Error: Failed to execute the command.")

    if arg["push"]:
        execute_push(arg["push"])
