import pytest

from main import process_nl_request


def test_even_filter():
    response = process_nl_request({
        "natural_language": "Given a list of integers, return only the even ones.",
        "input_data": [1, 2, 3, 4, 5, 6],
    })

    assert response["execution"]["status"] == "success"
    assert response["execution"]["output"] == [2, 4, 6]
    assert response["refactor_suggestions"]


def test_vowel_counter():
    response = process_nl_request({
        "natural_language": "Given a string, return the number of vowels.",
        "input_data": "OpenAI makes models",
    })

    assert response["execution"]["status"] == "success"
    assert response["execution"]["output"] == 8
    assert response["refactor_suggestions"]


def test_sort_tuples():
    response = process_nl_request({
        "natural_language": "Sort a list of (name, age) tuples by age descending.",
        "input_data": [("Alice", 30), ("Bob", 25), ("Charlie", 35)],
    })

    assert response["execution"]["status"] == "success"
    assert response["execution"]["output"] == [("Charlie", 35), ("Alice", 30), ("Bob", 25)]
    assert response["refactor_suggestions"]


def test_ambiguous_description():
    response = process_nl_request({
        "natural_language": "Do stuff",
        "input_data": None,
    })

    assert response["execution"]["status"] == "error"
    assert "ambiguous" in response["execution"]["error_message"].lower()
