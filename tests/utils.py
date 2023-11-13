from typing import Type, TypedDict
import unittest


def assert_dict_structure(
    testcase: unittest.TestCase, dict_obj: dict, expected_type: Type[TypedDict]
):
    """assert_dict_structure.
    Recursively asserts that the dictionary object matches the structure of the expected TypedDict type.

    Args:
        testcase (unittest.TestCase): The test case to use for assertions
        dict_obj (dict): The dictionary object to check
        expected_type (Type[TypedDict]): The expected type of the dictionary object
    """
    for key, expected_value_type in expected_type.__annotations__.items():
        testcase.assertIn(key, dict_obj)
        actual_value = dict_obj[key]
        # Check for simple types
        if expected_value_type in [int, str, bool]:
            testcase.assertIsInstance(actual_value, expected_value_type)
        # Check for nested TypedDict
        elif isinstance(actual_value, dict):
            testcase.assertTrue(isinstance(actual_value, dict))
            assert_dict_structure(testcase, actual_value, expected_value_type)
        # Add checks for other types or structures as necessary
