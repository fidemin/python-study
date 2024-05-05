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
            [{"key": "A", "data": ["a", "b", "c"]}],
            [],
            {"a", "b", "c"},
            {"data": ["a", "b", "c"]},
        ),
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

    def test_expr(self, data_for_boolean_interpreter):
        test_input_data, test_input_operations, expected, _ = (
            data_for_boolean_interpreter
        )
        interpreter = BooleanInterpreter(test_input_data, test_input_operations)
        actual = set(interpreter.expr())
        assert actual == expected

    def test_integrate_dict(self, data_for_boolean_interpreter):
        test_input_data, test_input_operations, _, expected = (
            data_for_boolean_interpreter
        )
        interpreter = BooleanInterpreter(test_input_data, test_input_operations)
        actual = interpreter.build_operation_tree()
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
