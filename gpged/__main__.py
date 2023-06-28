from gpged.run_gpged import run_app
import subprocess
import argparse
import os
import sys


def main():
    # print(sys.argv)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-d", action="store_true")
    # args = parser.parse_args()

    # if not args.d:
    #     script_dir = os.path.dirname(os.path.realpath(__file__))
    #     script_path = os.path.join(script_dir, "run_gpged.py")
    #     subprocess.Popen([sys.executable, script_path])
    #     sys.exit(0)

    # If -d flag was supplied, run the application in the current process
    run_app()


if __name__ == "__main__":
    main()
