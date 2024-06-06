from collections import defaultdict
from contextlib import nullcontext

import pytest

from .interpreter import (
    get_key_with_zero_indegree,
    BooleanInterpreter,
)

common_test_dataset = [
    [{"key": "A", "operation": None, "data": ["a", "b", "c"]}],
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
]

expected_for_expr = [
    {"a", "b", "c"},
    {"c", "d", "k"},
    {"c", "d"},
]

expected_for_build_operation_tree = [
    {
        "data": ["a", "b", "c"],
    },
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
]


@pytest.fixture(params=[(x, y) for x, y in zip(common_test_dataset, expected_for_expr)])
def data_for_expr(request):
    return request.param


@pytest.fixture(
    params=[
        (x, y) for x, y in zip(common_test_dataset, expected_for_build_operation_tree)
    ]
)
def data_for_build_operation_tree(request):
    return request.param


class TestBooleanInterpreter:
    def test_build_operation_tree(self, data_for_build_operation_tree):
        test_input_data, expected = data_for_build_operation_tree
        interpreter = BooleanInterpreter(test_input_data)
        actual = interpreter.build_operation_tree()
        assert actual == expected

    def test_expr(self, data_for_expr):
        test_input_data, expected = data_for_expr
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
