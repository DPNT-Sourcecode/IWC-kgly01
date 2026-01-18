from __future__ import annotations

from .utils import (
    call_dequeue,
    call_enqueue,
    call_size,
    call_age,
    iso_ts,
    run_queue,
)
from typing import Any


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

    entry_5 = {
        "user_id": 1,
        "provider": "credit_check",
        "timestamp": iso_ts(delta_minutes=0),
    }
    entry_6 = {
        "user_id": 2,
        "provider": "companies_house",
        "timestamp": iso_ts(delta_minutes=0),
    }

    test_data = {
        "entry_1": entry_1,
        "entry_2": entry_2,
        "entry_3": entry_3,
        "entry_4": entry_4,
        "entry_5": entry_5,
        "entry_6": entry_6,
    }

    return test_data


def test_enqueue_size_dequeue_flow() -> None:
    run_queue(
        [
            call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
            call_size().expect(1),
            call_dequeue().expect("companies_house", 1),
        ]
    )


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


def test_prioritisations_timestamp_ordering() -> None:
    test_data = get_test_data()

    run_queue(
        [
            call_enqueue(
                test_data["entry_4"]["provider"],
                test_data["entry_4"]["user_id"],
                iso_ts(delta_minutes=5),
            ).expect(1),
            call_enqueue(
                test_data["entry_2"]["provider"],
                test_data["entry_2"]["user_id"],
                test_data["entry_2"]["timestamp"],
            ).expect(2),
            call_size().expect(2),
            call_dequeue().expect("bank_statements", 2),
            call_dequeue().expect("bank_statements", 1),
            call_size().expect(0),
        ]
    )


def test_prioritisations_dependency_resolution() -> None:
    test_data = get_test_data()

    run_queue(
        [
            call_enqueue(
                test_data["entry_5"]["provider"],
                test_data["entry_5"]["user_id"],
                test_data["entry_5"]["timestamp"],
            ).expect(2),
            call_size().expect(2),
            call_dequeue().expect("companies_house", 1),
            call_dequeue().expect("credit_check", 1),
            call_size().expect(0),
        ]
    )


def test_duplication_removal() -> None:
    test_data = get_test_data()
    run_queue(
        [
            call_enqueue(
                test_data["entry_4"]["provider"],
                test_data["entry_4"]["user_id"],
                test_data["entry_4"]["timestamp"],
            ).expect(1),
            call_enqueue(
                test_data["entry_4"]["provider"],
                test_data["entry_4"]["user_id"],
                iso_ts(delta_minutes=5),
            ).expect(1),
            call_enqueue(
                test_data["entry_3"]["provider"],
                test_data["entry_3"]["user_id"],
                iso_ts(delta_minutes=5),
            ).expect(2),
            call_size().expect(2),
            call_dequeue().expect("bank_statements", 1),
            call_dequeue().expect("id_verification", 1),
            call_size().expect(0),
        ]
    )


def test_deprioritize_bank_statements() -> None:
    test_data = get_test_data()
    run_queue(
        [
            call_enqueue(
                test_data["entry_4"]["provider"],
                test_data["entry_4"]["user_id"],
                test_data["entry_4"]["timestamp"],
            ).expect(1),
            call_enqueue(
                test_data["entry_3"]["provider"],
                test_data["entry_3"]["user_id"],
                iso_ts(delta_minutes=1),
            ).expect(2),
            call_enqueue(
                test_data["entry_6"]["provider"],
                test_data["entry_6"]["user_id"],
                iso_ts(delta_minutes=2),
            ).expect(3),
            call_size().expect(3),
            call_dequeue().expect("id_verification", 1),
            call_dequeue().expect("companies_house", 2),
            call_dequeue().expect("bank_statements", 1),
            call_size().expect(0),
        ]
    )


def test_deprioritize_bank_statements_rule_of_three() -> None:
    test_data = get_test_data()
    run_queue(
        [
            call_enqueue(
                test_data["entry_2"]["provider"],
                test_data["entry_2"]["user_id"],
                test_data["entry_2"]["timestamp"],
            ).expect(1),
            call_enqueue(
                test_data["entry_4"]["provider"],
                test_data["entry_4"]["user_id"],
                iso_ts(delta_minutes=1),
            ).expect(2),
            call_enqueue(
                test_data["entry_3"]["provider"],
                test_data["entry_3"]["user_id"],
                iso_ts(delta_minutes=2),
            ).expect(3),
            call_enqueue(
                test_data["entry_1"]["provider"],
                test_data["entry_1"]["user_id"],
                iso_ts(delta_minutes=3),
            ).expect(4),
            call_size().expect(4),
            call_dequeue().expect("id_verification", 1),  # entry 3
            call_dequeue().expect("companies_house", 1),  # entry 1
            call_dequeue().expect("bank_statements", 1),  # entry 4
            call_dequeue().expect("bank_statements", 2),  # entry 6
            call_size().expect(0),
        ]
    )


def test_age() -> None:
    test_data = get_test_data()
    age_seconds = 7 * 60
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
                iso_ts(delta_minutes=5),
            ).expect(2),
            call_enqueue(
                test_data["entry_3"]["provider"],
                test_data["entry_3"]["user_id"],
                iso_ts(delta_minutes=7),
            ).expect(3),
            call_size().expect(3),
            call_age().expect(age_seconds),
        ]
    )


def test_age_empty_queue() -> None:
    test_data = get_test_data()
    age_seconds = 0
    run_queue(
        [
            call_enqueue(
                test_data["entry_1"]["provider"],
                test_data["entry_1"]["user_id"],
                test_data["entry_1"]["timestamp"],
            ).expect(1),
            call_size().expect(1),
            call_dequeue().expect("companies_house", 1),
            call_size().expect(0),
            call_age().expect(age_seconds),
        ]
    )


def test_age_one_task_queue() -> None:
    test_data = get_test_data()
    age_seconds = 0
    run_queue(
        [
            call_enqueue(
                test_data["entry_1"]["provider"],
                test_data["entry_1"]["user_id"],
                test_data["entry_1"]["timestamp"],
            ).expect(1),
            call_size().expect(1),
            call_age().expect(age_seconds),
        ]
    )


def test_old_bank_statements() -> None:
    test_data = get_test_data()

    run_queue(
        [
            call_enqueue(
                test_data["entry_3"]["provider"],
                test_data["entry_3"]["user_id"],
                test_data["entry_3"]["timestamp"],
            ).expect(1),
            call_enqueue(
                test_data["entry_2"]["provider"],
                test_data["entry_2"]["user_id"],
                iso_ts(delta_minutes=1),
            ).expect(2),
            call_enqueue(
                test_data["entry_1"]["provider"],
                test_data["entry_1"]["user_id"],
                iso_ts(delta_minutes=7),
            ).expect(3),
            call_size().expect(3),
            call_dequeue().expect("id_verification", 1),
            call_dequeue().expect("bank_statements", 2),
            call_dequeue().expect("companies_house", 1),
        ]
    )
