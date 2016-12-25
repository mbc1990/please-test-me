import json
import sys
import map_maker

def main():
    # TODO: Argument parsing/error message
    config_path = sys.argv[1]

    with open(config_path) as config_file:    
        config = json.load(config_file)
        mm = map_maker.MapMaker(config['watch_paths'], config['delta_threshold'])

if __name__ == "__main__":
    main()
