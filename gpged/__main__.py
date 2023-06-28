from gpged.run_gpged import run_app
import os, sys, traceback, atexit


def main():
    home_dir = os.path.expanduser("~")
    log_dir = os.path.join(home_dir, "Library/Logs/gpged")

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    log_file_path = os.path.join(home_dir, "Library/Logs/gpged/output.log")
    log_file = open(log_file_path, "w")
    atexit.register(log_file.close)
    sys.stdout = sys.stderr = log_file

    try:
        run_app()
    except Exception:
        traceback.print_exc()
        print("\nEnvironment:")
        print(os.environ)
        sys.exit(1)


if __name__ == "__main__":
    main()
