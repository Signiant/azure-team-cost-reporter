import argparse
import yaml
import output
import azure_cost_collector


def read_config_file(path):
    config_map = []
    try:
        config_file_handle = open(path)
        config_map = yaml.load(config_file_handle, Loader=yaml.FullLoader)
        config_file_handle.close()
    except Exception as e:
        print('Error opening config file %s' % path)
        print(e)
    return config_map


def main():
    parser = argparse.ArgumentParser(description='Azure cost reporter')
    parser.add_argument('-d', '--debug', help='Enable debug output', action='store_true')
    parser.add_argument('-c', '--config', help='Full path to a config file', required=True)
    args = parser.parse_args()

    debug = args.debug
    config_map = read_config_file(args.config)
    costs_by_team = azure_cost_collector.get_all_costs(config_map, debug)
    if debug:
        print("All costs by team: %s" % costs_by_team)
    for team in config_map['teams']:
        output.outputResults(team['name'], config_map, costs_by_team[team['subscription']], debug)


if __name__ == "__main__":
    main()
