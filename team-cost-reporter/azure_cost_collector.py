import requests
from output import getEndDate, getStartDate


def _get_data(api_key, enrollment_number, start_date, end_date, next_link, debug):
    # URL to get costs for a specific timeframe is:
    # https://consumption.azure.com/v3/enrollments/{enrollmentNumber}/usagedetailsbycustomdate?startTime=yyyy-MM-dd&endTime=yyyy-MM-dd
    headers = {'Accept': 'application/json',
               'Authorization': 'bearer ' + api_key}
    if next_link == True:
        next_link = None

    if next_link:
        url = next_link
    elif (enrollment_number, start_date, end_date) is not None:
        url = 'https://consumption.azure.com:443/v3/enrollments/' + enrollment_number + \
              '/usagedetailsbycustomdate?startTime=' + start_date + '&endTime=' + end_date
    else:
        print("Unable to get data from Azure. This should not be able to fail this way")
        data, next_link = None
        return data, next_link
    response = requests.get(url, headers=headers)
    data = response.json()["data"]
    next_link = response.json()["nextLink"]
    return data, next_link


def _add_cost(current_cost, new_data, debug):
    for cost_line in new_data:
        if cost_line['subscriptionName'] not in current_cost.keys():
            if debug:
                print('Adding team %s to cost list' % cost_line['subscriptionName'])
            current_cost[cost_line['subscriptionName']] = 0
        if debug:
            print('Adding cost %s to team %s' % (cost_line['cost'], cost_line['subscriptionName']))
        current_cost[cost_line['subscriptionName']] += float(cost_line['cost'])
    return current_cost


def get_all_costs(config_map, debug):
    enrollment_number = config_map['global']['enrollment_number']
    api_key = config_map['global']['api_key']
    start_date = getStartDate(config_map)
    end_date = getEndDate(config_map)
    team_cost = {}
    next_link = True
    while next_link:
        if debug:
            print("Retrieving data from Azure for next link %s" % next_link)
        data, next_link = _get_data(api_key, enrollment_number, start_date, end_date, next_link, debug)
        team_cost = _add_cost(team_cost, data, debug)
    return team_cost
