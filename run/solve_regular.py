import datetime
import json
import pathlib
import sys
from collections import Counter
from tqdm import tqdm
import pandas as pd
base_folder = pathlib.Path()
sys.path.append(str(base_folder / "../src"))
from multi_period_dev import solve_multi_period_fpl


def run_solver(n):
  responses = []
  all_responses = []
  next_gw_list = []

  for i in tqdm(range(n)):
    print(f"ITERATION NUMBER {i+1}")
    data, options = load_settings()
    result = solve_multi_period_fpl(data, options)
    responses.append(result)
    print(result['summary'].split('GW')[1])
    current_gameweek = result['picks']['week'].iloc[0]
    team_and_bench = result['picks'][['name', 'bench', 'captain','vicecaptain','week']]
    current_week_team_and_bench = team_and_bench.loc[team_and_bench['week'] == current_gameweek]
    captain = current_week_team_and_bench.loc[current_week_team_and_bench['captain'] == 1]['name'].values[0]
    vicecaptain = current_week_team_and_bench.loc[current_week_team_and_bench['vicecaptain'] == 1]['name'].values[0]
    bench = current_week_team_and_bench.loc[current_week_team_and_bench['bench'] != -1][['name', 'bench']]
    print("Captain:")
    print(captain)
    print("Vice Captain:")
    print(vicecaptain)
    print("")
    print("Bench")
    print(bench)


  for (k, response) in enumerate(responses):
    next_gw = response['summary'].split('GW')[1]
    next_gw_list.append(next_gw)

    all_responses.append(
        pd.DataFrame([
          (k,
           response['summary'],
           response['total_xp'])
        ])
    )
  time_now = datetime.datetime.now()
  stamp = time_now.strftime("%Y-%m-%d_%H-%M-%S")
  counter = Counter(next_gw_list)
  counter_results = open(f"results/counter_results_{stamp}.txt", "w")
  cs = sorted(counter.items(), key=lambda n: n[1], reverse=True)
  counter_results.write(", ".join(f"{el[1]} times: \n {el[0]}" for el in cs))

  df = pd.concat(all_responses)
  df.to_csv(f"results/multiobj_ws_solution_group_{stamp}.csv")


def load_settings():
  base_folder = pathlib.Path()
  sys.path.append(str(base_folder / "../src"))
  from multi_period_dev import connect, get_my_data, prep_data

  with open('regular_settings.json') as f:
    options = json.load(f)

  session, team_id = connect()
  my_data = get_my_data(session, team_id)
  data = prep_data(my_data, options)

  return data, options


if __name__ == "__main__":
  # base_folder = pathlib.Path()
  # sys.path.append(str(base_folder / "../src"))
  # from multi_period_dev import connect, get_my_data, prep_data, \
  #   solve_multi_period_fpl
  #
  # with open('regular_settings.json') as f:
  #   options = json.load(f)
  #
  # session, team_id = connect()
  # my_data = get_my_data(session, team_id)
  # data = prep_data(my_data, options)

  run_solver(1)

  # all_responses.to_csv(
  #         f"results/multiobj_ws_solution_group_{stamp}.csv")

  # result = solve_multi_period_fpl(data, options)
  # print(result['summary'])
  # time_now = datetime.datetime.now()
  # stamp = time_now.strftime("%Y-%m-%d_%H-%M-%S")
  # result['picks'].to_csv(f"results/regular_{stamp}.csv")
