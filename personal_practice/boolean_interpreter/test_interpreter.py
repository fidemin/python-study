from collections import defaultdict
from contextlib import nullcontext
from typing import List

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
        "operation": {
            "type": "OR",
            "targets": [
                {
                    "operation": {
                        "type": "AND",
                        "targets": [
                            {"data": ["a", "b", "c"]},
                            {"data": ["c", "d", "e"]},
                        ],
                    }
                },
                {"data": ["d", "k"]},
            ],
        },
    },
    {
        "operation": {
            "type": "OR",
            "targets": [
                {
                    "operation": {
                        "type": "AND",
                        "targets": [
                            {"data": ["a", "b", "c"]},
                            {"data": ["c", "d", "e"]},
                        ],
                    }
                },
                {
                    "operation": {
                        "type": "AND",
                        "targets": [
                            {"data": ["c", "d", "e"]},
                            {"data": ["d", "k"]},
                        ],
                    }
                },
            ],
        },
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


def assert_topological_sort(data: dict, sorted_keys: List[str]):
    for d in data:
        if d["operation"] is None:
            continue
        for target in d["operation"]["targets"]:
            assert sorted_keys.index(target) < sorted_keys.index(d["key"])


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

    def test_build_sorted_keys(self, data_for_expr):
        test_input_data, _ = data_for_expr
        interpreter = BooleanInterpreter(test_input_data)
        actual = interpreter.build_sorted_keys()
        assert len(actual) == len(test_input_data)
        assert_topological_sort(test_input_data, actual)


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
