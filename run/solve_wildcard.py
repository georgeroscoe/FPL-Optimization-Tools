import os
import sys
import pathlib
import json
import datetime
import pandas as pd
from tqdm import tqdm
base_folder = pathlib.Path()
sys.path.append(str(base_folder / "../src"))
from multi_period_dev import solve_multi_period_fpl


def load_settings():
    base_folder = pathlib.Path()
    sys.path.append(str(base_folder / "../src"))
    from multi_period_dev import connect, get_my_data, prep_data

    with open('wildcard_settings.json') as f:
        options = json.load(f)

    session, team_id = connect()
    my_data = get_my_data(session, team_id)
    data = prep_data(my_data, options)

    return data, options

def run_solver(n):
    responses = []
    all_responses = []
    for i in tqdm(range(n)):
        print(f"ITERATION NUMBER {i+1}")
        data, options = load_settings()
        result = solve_multi_period_fpl(data, options)
        responses.append(result)
        print(result['summary'])
        current_gameweek = result['picks']['week'].iloc[0]
        team_and_bench = result['picks'][['name', 'lineup', 'bench', 'captain','vicecaptain','pos', 'week']]
        current_week_team_and_bench = team_and_bench.loc[team_and_bench['week'] == current_gameweek]
        captain = current_week_team_and_bench.loc[current_week_team_and_bench['captain'] == 1]['name'].values[0]
        vicecaptain = current_week_team_and_bench.loc[current_week_team_and_bench['vicecaptain'] == 1]['name'].values[0]
        lineup = current_week_team_and_bench.loc[current_week_team_and_bench['lineup'] == 1][['name', 'pos', 'lineup']]
        bench = current_week_team_and_bench.loc[current_week_team_and_bench['bench'] != -1][['name', 'pos', 'bench']]
        print("Expected Points:")
        print(result['total_xp'])
        print("Captain:")
        print(captain)
        print("Vice Captain:")
        print(vicecaptain)
        print("")
        print("Lineup")
        print(lineup)
        print("Bench")
        print(bench)
    for (k, response) in enumerate(responses):

        current_gameweek = response['picks']['week'].iloc[0]
        team_and_bench = response['picks'][['name', 'lineup', 'bench', 'captain','vicecaptain','pos', 'week']]
        current_week_team_and_bench = team_and_bench.loc[team_and_bench['week'] == current_gameweek]
        lineup = current_week_team_and_bench.loc[current_week_team_and_bench['lineup'] == 1][['name']].to_string(index=False)
        bench = current_week_team_and_bench.loc[current_week_team_and_bench['bench'] != -1][['name']].to_string(index=False)
        captain = current_week_team_and_bench.loc[current_week_team_and_bench['captain'] == 1]['name'].values[0]
        vicecaptain = current_week_team_and_bench.loc[current_week_team_and_bench['vicecaptain'] == 1]['name'].values[0]

        all_responses.append(
            pd.DataFrame(data=[
                (lineup, bench, captain, vicecaptain, response['total_xp'])
            ], columns=['Lineup', 'Bench', 'C', 'VC', 'xP'])
        )

    time_now = datetime.datetime.now()
    stamp = time_now.strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.concat(all_responses)
    df.sort_values('xP', inplace=True, ascending=False)
    df.to_csv(f"results/wildcard_solutions_{stamp}.csv")

if __name__=="__main__":
    # base_folder = pathlib.Path()
    # sys.path.append(str(base_folder / "../src"))
    # from multi_period_dev import connect, get_my_data, prep_data, solve_multi_period_fpl
    #
    # with open('wildcard_settings.json') as f:
    #     options = json.load(f)
    #
    # session, team_id = connect()
    # my_data = get_my_data(session, team_id)
    # data = prep_data(my_data, options)

    # result = solve_multi_period_fpl(data, options)
    # print(result['summary'])
    # current_gameweek = result['picks']['week'].iloc[0]
    # team_and_bench = result['picks'][['name', 'lineup', 'bench', 'captain','vicecaptain','pos', 'week']]
    # current_week_team_and_bench = team_and_bench.loc[team_and_bench['week'] == current_gameweek]
    # captain = current_week_team_and_bench.loc[current_week_team_and_bench['captain'] == 1]['name'].values[0]
    # vicecaptain = current_week_team_and_bench.loc[current_week_team_and_bench['vicecaptain'] == 1]['name'].values[0]
    # lineup = current_week_team_and_bench.loc[current_week_team_and_bench['lineup'] == 1][['name', 'pos', 'lineup']]
    # bench = current_week_team_and_bench.loc[current_week_team_and_bench['bench'] != -1][['name', 'pos', 'bench']]
    # print("Expected Points:")
    # print(result['total_xp'])
    # print("Captain:")
    # print(captain)
    # print("Vice Captain:")
    # print(vicecaptain)
    # print("")
    # print("Lineup")
    # print(lineup)
    # print("Bench")
    # print(bench)
    # time_now = datetime.datetime.now()
    # stamp = time_now.strftime("%Y-%m-%d_%H-%M-%S")
    # result['picks'].to_csv(f"results/wildcard_{stamp}.csv")
    run_solver(80)
