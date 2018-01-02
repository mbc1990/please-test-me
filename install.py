import os
import stat
import json
import subprocess
from shutil import copyfile


def main():
    """
    Sets up all the PTM stuff. This setup script is meant to be
    idempotent, and to automatically copy source file updates
    without changing configuration settings
    """

    # If the working dir doesn't exist, create it
    working_dir = os.path.expanduser("~") + "/.please-test-me/"
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    # Copy requirements.txt
    copyfile("requirements.txt", working_dir+"requirements.txt")

    # Initialize the virtualenv and install requirements.txt
    if not os.path.exists(working_dir+"venv"):
        print "virtualenv does not exist - creating..."
        subprocess.call(["./init_venv.sh"])

    # Copy test_current_line.py and build_map.py to working dir
    copyfile("test_current_line.py", working_dir + "test_current_line.py")
    copyfile("build_map.py", working_dir + "build_map.py")

    # Copy run_tcl.sh to working dir
    copyfile("run_tcl.sh", working_dir + "run_tcl.sh")
    st = os.stat(working_dir + "run_tcl.sh")
    os.chmod(working_dir + "run_tcl.sh",  st.st_mode | stat.S_IEXEC)
    
    # Copy bootstrap_tcl.sh to working dir
    copyfile("bootstrap_tcl.sh", working_dir + "bootstrap_tcl.sh")
    st = os.stat(working_dir + "bootstrap_tcl.sh")
    os.chmod(working_dir + "bootstrap_tcl.sh",  st.st_mode | stat.S_IEXEC)
  
    # Copy bootstrap_bm.sh to working dir
    copyfile("bootstrap_bm.sh", working_dir + "bootstrap_bm.sh")
    st = os.stat(working_dir + "bootstrap_bm.sh")
    os.chmod(working_dir + "bootstrap_bm.sh",  st.st_mode | stat.S_IEXEC)

    # Create configuration file if it doesn't exist
    if not os.path.exists(working_dir + "conf.json"):
        print "Configuration file does not exist."
        print "Please update " + working_dir + "conf.json"
        config = {
            "update_every": 60 * 5,  # How often to regenerate maps in seconds
            "dirs_to_track": [  # Absolute paths to repos it's active in

            ]
        }
        with open(working_dir + "conf.json", 'w') as outfile:
            json.dump(config, outfile)


if __name__ == "__main__":
    main() 
