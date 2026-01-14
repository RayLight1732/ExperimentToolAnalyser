from domain.value.condition import Condition, CoolingMode, Position
from application.model.value_type import ValueType
import re
from typing import List, Tuple


def parse_value_type_str(input_line: str) -> ValueType:
    return ValueType[input_line.strip().upper()]


# def parse_line(input_line: str) -> Tuple[ValueType, List[Condition]]:
#     tokens = tokenize_conditions(input_line)
#     if len(tokens) < 1:
#         raise ValueError("Usage: <value_type> <conditions...>")

#     value_type = parse_value_type_str(tokens[0])
#     condition_tokens = tokens[1:]
#     conditions = parse_conditions_list(condition_tokens)
#     return value_type, conditions


# def tokenize_conditions(input_line: str) -> List[str]:
#     """
#     入力例:
#         "peak_fms (PERIODIC, CAROTID) (ALWAYS,CAROTID) (NONE)"
#     戻り値:
#         ["peak_fms", "(PERIODIC, CAROTID)", "(ALWAYS,CAROTID)", "(NONE)"]
#     """
#     input_line = input_line.strip()
#     if not input_line:
#         return []

#     # 最初の単語（value_type）を取得
#     match = re.match(r"^\S+", input_line)
#     if not match:
#         raise ValueError("No value_type found")
#     value_type = match.group(0)

#     # 残りの文字列から括弧付きの条件を抽出
#     rest = input_line[match.end() :].strip()
#     # 括弧単位で抽出
#     condition_tokens = re.findall(r"\([^\)]*\)", rest)

#     return [value_type] + condition_tokens


# def parse_condition_str(cond_str: str) -> Condition:
#     """
#     "(PERIODIC, CAROTID)" -> Condition(CoolingMode.PERIODIC, Position.CAROTID)
#     "(ALWAYS)" -> error
#     "(NONE)" -> Condition(CoolingMode.NONE)
#     """
#     cond_str = cond_str.strip()
#     if not cond_str.startswith("(") or not cond_str.endswith(")"):
#         raise ValueError(f"Condition must be enclosed in (): {cond_str}")

#     # 括弧内の文字列を取り出して前後スペースを除去
#     inner = cond_str[1:-1].strip()
#     if not inner:
#         raise ValueError(f"Empty condition: {cond_str}")

#     # カンマで分割、各要素の前後スペースを除去
#     parts = [p.strip().upper() for p in inner.split(",")]

#     try:
#         mode = CoolingMode[parts[0]]
#     except KeyError:
#         raise ValueError(f"Unknown CoolingMode: {parts[0]}")

#     if mode.requires_position:
#         if len(parts) < 2:
#             raise ValueError(f"Position is required for mode {mode.name}")
#         try:
#             position = Position[parts[1]]
#         except KeyError:
#             raise ValueError(f"Unknown Position: {parts[1]}")
#         return Condition(mode, position)
#     else:
#         return Condition(mode)


# def parse_conditions_list(tokens: list[str]) -> list[Condition]:
#     """
#     ["(PERIODIC, CAROTID)", "(ALWAYS,CAROTID)", "(NONE)"]
#     -> List[Condition]
#     """
#     return [parse_condition_str(t) for t in tokens]
