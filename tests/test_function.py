"""Run integration tests with a speckle server."""

from speckle_automate import (
    AutomationContext,
    AutomationRunData,
    AutomationStatus,
    run_function
)

from main import FunctionInputs, automate_function

from speckle_automate.fixtures import *


def test_function_run(test_automation_run_data: AutomationRunData, test_automation_token: str):
    """Run an integration test for the automate function."""
    automation_context = AutomationContext.initialize(
        test_automation_run_data, test_automation_token
    )
    automate_sdk = run_function(
        automation_context,
        automate_function,
        FunctionInputs(
            url="https://gist.githubusercontent.com/andrsbtrg/1c6ebcfca23492b2dd899b43817ea88a/raw/4183c73c61816a36f0cfe0fc51ef0e2459aaf253"
        ),
    )

    assert automate_sdk.run_status == AutomationStatus.SUCCEEDED
