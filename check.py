from pathlib import Path
import csv
import pattern_util as putil
import re

class Data:
    ssq_before:Path
    ssq_after:Path
    balance_board:Path
    vection:Path

def get_data(working_dir:Path):
    saved:dict[str,dict[int,Data]] = {}
    ssq_before_pattern = re.compile(r'^SSQ_\d{8}_\d{6}_before\.csv$')
    ssq_after_pattern = re.compile(r'^SSQ_\d{8}_\d{6}\_after.csv$')
    balance_board_pattern = re.compile(r'^\d{12}\.csv$')
    vection_pattern = re.compile(r'^vection_\d{8}_\d{6}\.csv$')
    for condition in putil.list_condition():
        parent_dir = putil.get_save_dir(working_dir,condition,"")
        subdirs = [p for p in parent_dir.iterdir() if p.is_dir()]
        for subdir in subdirs:
            data_dict = saved.get(subdir.name,{})
            data:Data = data_dict.get(condition,Data())
            ssq_befores = [p for p in subdir.iterdir() if p.is_file() and ssq_before_pattern.match(p.name)]
            ssq_afters = [p for p in subdir.iterdir() if p.is_file() and ssq_after_pattern.match(p.name)]
            balance_boards = [p for p in subdir.iterdir() if p.is_file() and balance_board_pattern.match(p.name)]
            vections =  [p for p in subdir.iterdir() if p.is_file() and vection_pattern.match(p.name)]
            data.ssq_before = ssq_befores[0] if len(ssq_befores) > 0 else None
            data.ssq_after = ssq_afters[0] if len(ssq_afters) > 0 else None
            data.balance_board = balance_boards[0] if len(balance_boards) > 0 else None
            data.vection = vections[0] if len(vections) > 0 else None
            flag = len(ssq_befores) > 1 or len(ssq_afters) > 1 or len(balance_boards) > 1 or len(vections) > 1
            if flag:
                print(subdir.name,putil.get_mode(condition),putil.get_position(condition))
            data_dict[condition] = data
            saved[subdir.name] = data_dict
    return saved

def filter_data(data_dict:dict[str,dict[int,Data]]):
    filtered = {}
    for name,condition_dict in data_dict.items():
        flag = True
        for condition,data in condition_dict.items():
            balance_board = data.balance_board is not None
            ssq_before = data.ssq_before is not None
            ssq_after = data.ssq_after is not None
            vection = data.vection is not None
            flag = flag and balance_board and ssq_before and ssq_after and vection
        if flag:
            filtered[name] = data_dict
    return filtered


if __name__ == "__main__":
    working_dir = Path("C:\\Users\\arusu\\OneDrive\\ドキュメント\\ExperimentOfCooling")
    filtered = filter_data(get_data(working_dir))
    print(len(filtered))