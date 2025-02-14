from pathlib import Path

from protostar.testing.test_results import PassedFuzzTestCaseResult
from protostar.testing.test_config import TestConfig
from tests.integration.conftest import (
    RunTestRunnerFixture,
    assert_cairo_test_cases,
)


async def test_basic(run_test_runner: RunTestRunnerFixture):
    seed = 10

    testing_summary = await run_test_runner(
        Path(__file__).parent / "basic_test.cairo", seed=seed
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=["test_fuzz_pass"],
        expected_failed_test_cases_names=["test_fuzz_fails"],
    )

    assert testing_summary.testing_seed == seed


async def test_non_felt_parameter(run_test_runner: RunTestRunnerFixture):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "non_felt_parameter_test.cairo"
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[],
        expected_failed_test_cases_names=[],
        expected_broken_test_cases_names=["test_fails_on_non_felt_parameter"],
    )


async def test_state_is_isolated(run_test_runner: RunTestRunnerFixture):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "state_isolation_test.cairo"
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[
            "test_storage_var",
        ],
        expected_failed_test_cases_names=[],
    )


async def test_hypothesis_multiple_errors(
    run_test_runner: RunTestRunnerFixture,
):
    """
    This test potentially raises ``hypothesis.errors.MultipleFailures``
    when ``report_multiple_bugs`` setting is set to ``True``.
    """

    testing_summary = await run_test_runner(
        Path(__file__).parent / "hypothesis_multiple_errors_test.cairo", seed=10
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[],
        expected_failed_test_cases_names=[
            "test_hypothesis_multiple_errors",
        ],
    )


async def test_max_examples_in_setup_hook(
    run_test_runner: RunTestRunnerFixture,
):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "max_examples_in_setup_hook_test.cairo", seed=3
    )

    [result] = testing_summary.passed
    assert isinstance(result, PassedFuzzTestCaseResult)
    assert result.fuzz_runs_count is not None
    assert result.fuzz_runs_count <= 5


async def test_max_examples_in_setup_case(
    run_test_runner: RunTestRunnerFixture,
):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "max_examples_in_setup_case_test.cairo", seed=3
    )

    [result] = testing_summary.passed
    assert isinstance(result, PassedFuzzTestCaseResult)
    assert result.fuzz_runs_count is not None
    assert result.fuzz_runs_count <= 5


async def test_max_examples_invalid_arguments(
    run_test_runner: RunTestRunnerFixture,
):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "max_examples_invalid_arguments_test.cairo"
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[],
        expected_broken_test_cases_names=["test_zero", "test_negative"],
    )


async def test_should_not_share_state(
    run_test_runner: RunTestRunnerFixture,
):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "shared_state_test.cairo"
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=["test_context"],
    )


async def test_parameterized_with_examples_tests(
    run_test_runner: RunTestRunnerFixture,
):
    testing_summary = await run_test_runner(
        Path(__file__).parent / "parameterized_test.cairo"
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[
            "test_check_exact_example",
            "test_given_and_examples",
            "test_only_examples",
            "test_only_given",
        ],
        expected_broken_test_cases_names=[
            "test_no_data_broken",
        ],
    )

    assert len(testing_summary.passed) == 4
    passed_list = [
        getattr(passed, "fuzz_runs_count")
        for passed in testing_summary.passed
        if hasattr(passed, "fuzz_runs_count")
    ]
    passed_list.sort()
    # TestConfig().fuzz_max_examples is a default value for max examples
    assert passed_list == [0, 0, 7, TestConfig().fuzz_max_examples]
