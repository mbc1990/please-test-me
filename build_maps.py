import json
import os
import subprocess


def main():
    """
    Called from bootstrap_bm.sh, this updates the test maps for every repo
    """
    working_dir = os.path.expanduser("~") + "/.please-test-me/"
    conf = json.load(open(working_dir + "conf.json"))
    for subjects in conf["dirs_to_track"]:
        dir = subjects["dir"]
        venv = subjects["venv"]

        # Generate the nose output
        subprocess.call(["./gen_tests.sh", dir, venv])

        # For each test, run coverage and save output
        # This has to be bootstrapped like the other python programs that
        # depend on the host virtualenv
        subprocess.call(["./bootstrap_update_test_map.sh", dir, venv])

        # Cleanup .nose_output.txt
        os.remove(dir + ".nose_output.txt")

if __name__ == "__main__":
    main()
