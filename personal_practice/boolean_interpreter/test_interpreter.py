from collections import defaultdict
from unittest import TestCase

import pytest

from personal_practice.boolean_interpreter.interpreter import (
    get_key_with_zero_indegree,
    BooleanInterpreter,
)


class TestBooleanInterpreter:

    @pytest.mark.parametrize(
        "test_input_data, test_input_operations, expected",
        [
            ([{"key": "A", "data": ["a", "b", "c"]}], [], {"a", "b", "c"}),
            (
                [
                    {"key": "A", "data": ["a", "b", "c"]},
                    {"key": "B", "data": ["c", "d", "e"]},
                    {"key": "C", "data": ["d", "k"]},
                ],
                [
                    {"key": "AB_AND", "op": "AND", "op_targets": ["A", "B"]},
                    {"key": "ABC", "op": "OR", "op_targets": ["AB_AND", "C"]},
                ],
                {"c", "d", "k"},
            ),
            (
                [
                    {"key": "A", "data": ["a", "b", "c"]},
                    {"key": "B", "data": ["c", "d", "e"]},
                    {"key": "C", "data": ["d", "k"]},
                ],
                [
                    {"key": "AB_AND", "op": "AND", "op_targets": ["A", "B"]},
                    {"key": "BC_AND", "op": "AND", "op_targets": ["B", "C"]},
                    {"key": "ABC", "op": "OR", "op_targets": ["AB_AND", "BC_AND"]},
                ],
                {"c", "d"},
            ),
        ],
    )
    def test_expr(self, test_input_data, test_input_operations, expected):
        interpreter = BooleanInterpreter(test_input_data, test_input_operations)
        actual = set(interpreter.expr())
        assert actual == expected


def test_get_key_with_zero_indegree():
    indegree = defaultdict(int, {"A": 0, "B": 1, "C": 2})
    assert get_key_with_zero_indegree(indegree) == "A"


def test_get_key_with_zero_indegree__no_key():
    indegree = defaultdict(int, {"A": 1, "B": 1, "C": 2})
    with pytest.raises(ValueError):
        get_key_with_zero_indegree(indegree)


def test_get_key_with_zero_indegree__multiple_keys():
    indegree = defaultdict(int, {"A": 0, "B": 0, "C": 2})
    with pytest.raises(ValueError):
        get_key_with_zero_indegree(indegree)
