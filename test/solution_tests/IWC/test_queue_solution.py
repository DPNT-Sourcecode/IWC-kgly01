from __future__ import annotations

from .utils import call_dequeue, call_enqueue, call_size, iso_ts, run_queue
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


# def test_enqueue_size_dequeue_flow() -> None:

#     entry_1 = {"user_id": 1, "provider":"companies_house", "timestamp":iso_ts(delta_minutes=0)}
#     entry_2 = {"user_id": 2, "provider":"bank_statements", "timestamp":iso_ts(delta_minutes=0)}
#     entry_3 = {"user_id": 1, "provider":"id_verification", "timestamp":iso_ts(delta_minutes=0)}
#     entry_4 = {"user_id": 1, "provider":"bank_statements", "timestamp":iso_ts(delta_minutes=0)}

#     run_queue(
#         [
#             call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
#             call_size().expect(1),
#             call_dequeue().expect("companies_house", 1),
#         ]
#     )
