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

    # Copy the python files to the working dir
    copyfile("test_current_line.py", working_dir + "test_current_line.py")
    copyfile("build_maps.py", working_dir + "build_maps.py")
    copyfile("update_test_map.py", working_dir + "update_test_map.py")

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

    # Copy bootstrap_update_test_map.sh to working dir
    copyfile("bootstrap_update_test_map.sh", working_dir + "bootstrap_update_test_map.sh")
    st = os.stat(working_dir + "bootstrap_update_test_map.sh")
    os.chmod(working_dir + "bootstrap_update_test_map.sh",  st.st_mode | stat.S_IEXEC)

    # Copy bootstrap_run_test.sh to working dir
    copyfile("bootstrap_run_test.sh", working_dir + "bootstrap_run_test.sh")
    st = os.stat(working_dir + "bootstrap_run_test.sh")
    os.chmod(working_dir + "bootstrap_run_test.sh",  st.st_mode | stat.S_IEXEC)

    # Copy gen_tests.sh to working dir
    copyfile("gen_tests.sh", working_dir + "gen_tests.sh")
    st = os.stat(working_dir + "gen_tests.sh")
    os.chmod(working_dir + "gen_tests.sh",  st.st_mode | stat.S_IEXEC)

    # Create configuration file if it doesn't exist
    if not os.path.exists(working_dir + "conf.json"):
        print "Configuration file does not exist."
        print "Please update " + working_dir + "conf.json"
        config = {
            # Members of this list should be of the form:
            # {
            #  "dir": <absolute path to dir>, 
            #  "venv": <absolute path to corresponding virtualenv>
            # }
            "dirs_to_track": [  # Absolute paths to repos it's active in

            ]
        }
        with open(working_dir + "conf.json", 'w') as outfile:
            json.dump(config, outfile)
    
    # Create test map file if it doesn't exist
    if not os.path.exists(working_dir + "test_map.json"):
        with open(working_dir + "test_map.json", 'w') as outfile:
            json.dump({}, outfile)

      # TODO: Add cron job


if __name__ == "__main__":
    main() 
