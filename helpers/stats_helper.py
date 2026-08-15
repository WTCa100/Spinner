from time import strftime
import csv

def dump_statistics(turns_info: dict[int, tuple], detailed = True):
    time_triggered = strftime("%Y%m%d_%H%M%S")
    file_path = f"Statistics_Dump_{'Detailed_' if detailed else ''}{time_triggered}.csv"
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