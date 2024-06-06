from collections import defaultdict
from contextlib import nullcontext

import pytest

from .interpreter import (
    get_key_with_zero_indegree,
    BooleanInterpreter,
)


@pytest.fixture(
    params=[
        (
            [{"key": "A", "operation": None, "data": ["a", "b", "c"]}],
            {"a", "b", "c"},
            {"data": ["a", "b", "c"]},
        ),
        (
            [
                {"key": "A", "operation": None, "data": ["a", "b", "c"]},
                {"key": "B", "operation": None, "data": ["c", "d", "e"]},
                {"key": "C", "operation": None, "data": ["d", "k"]},
                {
                    "key": "AB_AND",
                    "operation": {"type": "AND", "targets": ["A", "B"]},
                    "data": None,
                },
                {
                    "key": "ABC",
                    "operation": {"type": "OR", "targets": ["AB_AND", "C"]},
                    "data": None,
                },
            ],
            {"c", "d", "k"},
            {
                "op": "OR",
                "op_targets": [
                    {
                        "op": "AND",
                        "op_targets": [
                            {"data": ["a", "b", "c"]},
                            {"data": ["c", "d", "e"]},
                        ],
                    },
                    {"data": ["d", "k"]},
                ],
            },
        ),
        (
            [
                {"key": "A", "operation": None, "data": ["a", "b", "c"]},
                {"key": "B", "operation": None, "data": ["c", "d", "e"]},
                {"key": "C", "operation": None, "data": ["d", "k"]},
                {
                    "key": "AB_AND",
                    "operation": {"type": "AND", "targets": ["A", "B"]},
                    "data": None,
                },
                {
                    "key": "BC_AND",
                    "operation": {"type": "AND", "targets": ["B", "C"]},
                    "data": None,
                },
                {
                    "key": "ABC",
                    "operation": {"type": "OR", "targets": ["AB_AND", "BC_AND"]},
                    "data": None,
                },
            ],
            {"c", "d"},
            {
                "op": "OR",
                "op_targets": [
                    {
                        "op": "AND",
                        "op_targets": [
                            {"data": ["a", "b", "c"]},
                            {"data": ["c", "d", "e"]},
                        ],
                    },
                    {
                        "op": "AND",
                        "op_targets": [
                            {"data": ["c", "d", "e"]},
                            {"data": ["d", "k"]},
                        ],
                    },
                ],
            },
        ),
    ]
)
def data_for_boolean_interpreter(request):
    return request.param


class TestBooleanInterpreter:
    def test_build_operation_tree(self, data_for_boolean_interpreter):
        test_input_data, _, expected = data_for_boolean_interpreter
        interpreter = BooleanInterpreter(test_input_data)
        actual = interpreter.build_operation_tree()
        assert actual == expected

    def test_expr(self, data_for_boolean_interpreter):
        test_input_data, expected, _ = data_for_boolean_interpreter
        interpreter = BooleanInterpreter(test_input_data)
        actual = set(interpreter.expr())
        assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected,raises",
    [
        ({"A": 0, "B": 1, "C": 2}, "A", nullcontext()),
        ({"A": 1, "B": 1, "C": 2}, None, pytest.raises(ValueError)),
        ({"A": 0, "B": 0, "C": 2}, None, pytest.raises(ValueError)),
    ],
)
def test_get_key_with_zero_indegree(test_input, expected, raises):
    indegree = defaultdict(int, test_input)
    with raises:
        assert get_key_with_zero_indegree(indegree) == expected
