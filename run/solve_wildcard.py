import os
import sys
import pathlib
import json
import datetime

if __name__=="__main__":
    base_folder = pathlib.Path()
    sys.path.append(str(base_folder / "../src"))
    from multi_period_dev import connect, get_my_data, prep_data, solve_multi_period_fpl

    with open('wildcard_settings.json') as f:
        options = json.load(f)

    session, team_id = connect()
    my_data = get_my_data(session, team_id)
    data = prep_data(my_data, options)

    result = solve_multi_period_fpl(data, options)
    print(result['summary'])
    current_gameweek = result['picks']['week'].iloc[0]
    team_and_bench = result['picks'][['name', 'lineup', 'bench', 'captain','vicecaptain','week']]
    current_week_team_and_bench = team_and_bench.loc[team_and_bench['week'] == current_gameweek]
    captain = current_week_team_and_bench.loc[current_week_team_and_bench['captain'] == 1]['name'].values[0]
    vicecaptain = current_week_team_and_bench.loc[current_week_team_and_bench['vicecaptain'] == 1]['name'].values[0]
    lineup = current_week_team_and_bench.loc[current_week_team_and_bench['lineup'] == 1][['name', 'lineup']]
    bench = current_week_team_and_bench.loc[current_week_team_and_bench['bench'] != -1][['name', 'bench']]
    print("Captain:")
    print(captain)
    print("Vice Captain:")
    print(vicecaptain)
    print("")
    print("Lineup")
    print(lineup)
    print("Bench")
    print(bench)
    time_now = datetime.datetime.now()
    stamp = time_now.strftime("%Y-%m-%d_%H-%M-%S")
    result['picks'].to_csv(f"results/wildcard_{stamp}.csv")
    