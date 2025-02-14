from pathlib import Path

from tests.integration.conftest import (
    RunTestRunnerFixture,
    assert_cairo_test_cases,
)


async def test_reflect_cheatcode(run_test_runner: RunTestRunnerFixture):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "reflect_test.cairo"
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[
            "test_reflect_passed_simple",
            "test_reflect_passed_pointer",
            "test_reflect_passed_pointer_loop",
            "test_reflect_passed_type_pointer",
            "test_reflect_passed_repr",
            "test_reflect_passed_full",
            "test_reflect_passed_two_hints",
        ],
        expected_broken_test_cases_names=[
            "test_reflect_failed_illegal_arg",
            "test_reflect_failed_getattr_felt",
            "test_reflect_failed_getattr_pointer",
            "test_reflect_failed_invalid_member",
            "test_reflect_failed_get_on_none",
            "test_reflect_failed_corruption",
        ],
        expected_failed_test_cases_names=[
            "test_reflect_failed_simple",
        ],
    )
