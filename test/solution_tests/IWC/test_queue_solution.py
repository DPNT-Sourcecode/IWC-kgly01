from __future__ import annotations

from .utils import call_dequeue, call_enqueue, call_size, iso_ts, run_queue
from typing import Any
import pytest


# @pytest.mark.parametrize(
#     "user_id",
#     "provider",
#     "timestamp",
#     [(1, "companies_house", iso_ts(delta_minutes=0))],
# )
def test_enqueue_size_dequeue_flow() -> None:
    run_queue(
        [
            call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
            call_size().expect(1),
            call_dequeue().expect("companies_house", 1),
        ]
    )


def get_test_data() -> dict[str, dict[str, Any]]:
    entry_1 = {
        "user_id": 1,
        "provider": "companies_house",
        "timestamp": iso_ts(delta_minutes=0),
    }
    entry_2 = {
        "user_id": 2,
        "provider": "bank_statements",
        "timestamp": iso_ts(delta_minutes=0),
    }
    entry_3 = {
        "user_id": 1,
        "provider": "id_verification",
        "timestamp": iso_ts(delta_minutes=0),
    }
    entry_4 = {
        "user_id": 1,
        "provider": "bank_statements",
        "timestamp": iso_ts(delta_minutes=0),
    }

    test_data = {
        "entry_1": entry_1,
        "entry_2": entry_2,
        "entry_3": entry_3,
        "entry_4": entry_4,
    }

    return test_data


def test_prioritisations_rule_of_3() -> None:
    test_data = get_test_data()

    run_queue(
        [
            call_enqueue(
                test_data["entry_1"]["provider"],
                test_data["entry_1"]["user_id"],
                test_data["entry_1"]["timestamp"],
            ).expect(1),
            call_enqueue(
                test_data["entry_2"]["provider"],
                test_data["entry_2"]["user_id"],
                test_data["entry_2"]["timestamp"],
            ).expect(2),
            call_enqueue(
                test_data["entry_3"]["provider"],
                test_data["entry_3"]["user_id"],
                test_data["entry_3"]["timestamp"],
            ).expect(3),
            call_enqueue(
                test_data["entry_4"]["provider"],
                test_data["entry_4"]["user_id"],
                test_data["entry_4"]["timestamp"],
            ).expect(4),
            call_size().expect(4),
            call_dequeue().expect("companies_house", 1),
            call_dequeue().expect("id_verification", 1),
            call_dequeue().expect("bank_statements", 1),
            call_dequeue().expect("bank_statements", 2),
            call_size().expect(0),
        ]
    )




