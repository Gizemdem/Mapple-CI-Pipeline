"""This module contains the business logic of the function.

Use the automation_context module to wrap your function in an Autamate context helper
"""

from pydantic import Field, SecretStr
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from flatten import flatten_base
import maple as mp


class FunctionInputs(AutomateBase):
    """These are function author defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    read_only: str = Field(
        default="Placeholder",
        title="Automated Test Cases",
        description=( "checks window height is greater than 2600 mm"
                    "validates SIP 202mm wall type area is greater than 43 m2"
                    "checks pipes OmniClass value" 
                    "validates basic roof`s thermal mass"
                    "validates columns assembly type."
                    "validates ceiling thickness is 50"
                    "checks there are exactly 55 walls" ) 
    ) 


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """This is an example Speckle Automate function.

    Args:
        automate_context: A context helper object, that carries relevant information
            about the runtime context of this function.
            It gives access to the Speckle project data, that triggered this run.
            It also has conveniece methods attach result data to the Speckle model.
        function_inputs: An instance object matching the defined schema.
    """
    # the context provides a conveniet way, to receive the triggering version
    version_root_object = automate_context.receive_version()
    mp.init(version_root_object)

    from maple_test import spec_a, spec_b, spec_c, spec_d, spec_e, spec_f, spec_g

    mp.run(spec_a, spec_b, spec_c, spec_d, spec_e, spec_f, spec_g)

    failed_count = 0
    for case in mp.test_cases:
        assertions = case.assertions
        for assertion in assertions:
            if len(assertion.failed) > 0:
                failed_count += 1
                # this is how a run is marked with a failure cause
                automate_context.attach_error_to_objects(
                    category=case.spec_name,
                    object_ids=assertion.failed,
                    message=f"{case.spec_name}.\n"
                    f"On {len(assertion.failed)} objects, assertion {assertion.assertion_type} failed.",
                )

    if failed_count > 0:
        automate_context.mark_run_failed(
                "Some tests failed: "
                f"{failed_count} out of {len(mp.test_cases)} specs failed"
                "See the Results for more information."
        )
        # set the automation context view, to the original model / version view
        # to show the offending objects
        automate_context.set_context_view()
    else:
        automate_context.mark_run_success("All tests passed :)")

    # if the function generates file results, this is how it can be
    # attached to the Speckle project / model
    # automate_context.store_file_result("./report.pdf")


def automate_function_without_inputs(automate_context: AutomationContext) -> None:
    """A function example without inputs.

    If your function does not need any input variables,
     besides what the automation context provides,
     the inputs argument can be omitted.
    """
    pass


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference, do not invoke it!

    # pass in the function reference with the inputs schema to the executor
    execute_automate_function(automate_function, FunctionInputs)

    # if the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
