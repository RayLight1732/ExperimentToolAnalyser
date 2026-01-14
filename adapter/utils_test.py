from domain.value.condition import Condition, CoolingMode, Position
from application.dto.value_type import ValueType
from adapter.utils import (
    # tokenize_conditions,
    # parse_conditions_list,
    # parse_condition_str,
    # parse_line,
    parse_value_type_str,
)
import pytest


def test_parse_value_type_normal():
    line = "peak_fms"
    result = parse_value_type_str(line)
    assert result == ValueType.PEAK_FMS


# def test_parse_line_normal():
#     line = "peak_fms (PERIODIC, CAROTID) (ALWAYS,NECK) (NONE)"
#     result = parse_line(line)

#     assert result == (
#         ValueType.PEAK_FMS,
#         [
#             Condition(CoolingMode.PERIODIC, Position.CAROTID),
#             Condition(CoolingMode.ALWAYS, Position.NECK),
#             Condition(CoolingMode.NONE),
#         ],
#     )


# def test_tokenize_conditions_normal():
#     line = "peak_fms (PERIODIC, CAROTID) (ALWAYS,CAROTID) (NONE)"
#     result = tokenize_conditions(line)

#     assert result == [
#         "peak_fms",
#         "(PERIODIC, CAROTID)",
#         "(ALWAYS,CAROTID)",
#         "(NONE)",
#     ]


# def test_tokenize_conditions_extra_spaces():
#     line = "  peak_fms   (PERIODIC, CAROTID)   (ALWAYS, CAROTID)   "
#     result = tokenize_conditions(line)

#     assert result == [
#         "peak_fms",
#         "(PERIODIC, CAROTID)",
#         "(ALWAYS, CAROTID)",
#     ]


# def test_tokenize_conditions_only_value_type():
#     line = "peak_fms"
#     result = tokenize_conditions(line)

#     assert result == ["peak_fms"]


# def test_tokenize_conditions_empty():
#     assert tokenize_conditions("") == []
#     assert tokenize_conditions("   ") == []


# # ----------------------------
# # parse_condition_str
# # ----------------------------


# def test_parse_condition_periodic_with_position():
#     cond = parse_condition_str("(PERIODIC, CAROTID)")

#     assert isinstance(cond, Condition)
#     assert cond.mode == CoolingMode.PERIODIC
#     assert cond.position == Position.CAROTID


# def test_parse_condition_without_position():
#     cond = parse_condition_str("(NONE)")

#     assert cond.mode == CoolingMode.NONE
#     assert cond.position is None


# def test_parse_condition_lowercase_and_spaces():
#     cond = parse_condition_str("(  periodic ,  carotid )")

#     assert cond.mode == CoolingMode.PERIODIC
#     assert cond.position == Position.CAROTID


# def test_parse_condition_missing_parentheses():
#     with pytest.raises(ValueError, match="Condition must be enclosed"):
#         parse_condition_str("PERIODIC, CAROTID")


# def test_parse_condition_empty_parentheses():
#     with pytest.raises(ValueError, match="Empty condition"):
#         parse_condition_str("()")


# def test_parse_condition_unknown_mode():
#     with pytest.raises(ValueError, match="Unknown CoolingMode"):
#         parse_condition_str("(FOO)")


# def test_parse_condition_requires_position_but_missing():
#     with pytest.raises(ValueError, match="Position is required"):
#         parse_condition_str("(PERIODIC)")


# def test_parse_condition_unknown_position():
#     with pytest.raises(ValueError, match="Unknown Position"):
#         parse_condition_str("(PERIODIC, ARM)")


# # ----------------------------
# # parse_conditions_list
# # ----------------------------


# def test_parse_conditions_list_normal():
#     tokens = ["(PERIODIC, CAROTID)", "(ALWAYS,NECK)", "(NONE)"]

#     result = parse_conditions_list(tokens)

#     assert len(result) == 3

#     assert result[0].mode == CoolingMode.PERIODIC
#     assert result[0].position == Position.CAROTID

#     assert result[1].mode == CoolingMode.ALWAYS
#     assert result[1].position == Position.NECK

#     assert result[2].mode == CoolingMode.NONE
#     assert result[2].position is None


# def test_parse_conditions_list_empty():
#     assert parse_conditions_list([]) == []


# def test_parse_conditions_list_propagates_error():
#     tokens = ["(PERIODIC, CAROTID)", "(FOO)"]

#     with pytest.raises(ValueError):
#         parse_conditions_list(tokens)
