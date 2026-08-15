from time import strftime
from pathlib import Path
import csv

STATS_FOLDER = Path("Game_stats")

def dump_statistics(turns_info: dict[int, tuple], detailed = True):
    if not STATS_FOLDER.is_dir():
        STATS_FOLDER.mkdir()

    time_triggered = strftime("%Y%m%d_%H%M%S")
    file_path = STATS_FOLDER / f"Statistics_Dump_{'Detailed_' if detailed else ''}{time_triggered}.csv"
    keys = ["Turn", "Wager_numeric", "Turn_win"]
    if detailed:
        keys += ["Total_player_win", "Total_player_loose", "Total_player_diff", "Current_player_balance"]
    with open(str(file_path), mode="w") as fp:
        writer = csv.writer(fp)
        writer.writerow(keys)
        for turn_id, info in turns_info.items():
            wager, current_win, total_won, total_lost, total_diff, current_balance = info
            row = [turn_id] + [wager, current_win]
            if detailed:
                row += [total_won, total_lost, total_diff, current_balance]
            writer.writerow(row)
    return file_path