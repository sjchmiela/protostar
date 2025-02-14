import dataclasses
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from starkware.starknet.services.api.contract_class import ContractClass
from typing_extensions import Self

from protostar.compiler import ProjectCompiler
from protostar.starknet.execution_state import ExecutionState
from protostar.starknet.forkable_starknet import ForkableStarknet
from protostar.testing.stopwatch import Stopwatch
from protostar.testing.test_config import TestConfig
from protostar.testing.test_context import TestContext
from protostar.testing.test_output_recorder import OutputRecorder
from protostar.testing.test_suite import TestCase
from protostar.starknet import Address


@dataclass
class TestExecutionState(ExecutionState):
    config: TestConfig
    context: TestContext
    output_recorder: OutputRecorder
    stopwatch: Stopwatch
    project_compiler: ProjectCompiler

    @classmethod
    async def from_test_suite_definition(
        cls,
        test_suite_definition: ContractClass,
        test_config: TestConfig,
        contract_path: Path,
        project_compiler: ProjectCompiler,
    ) -> Self:
        starknet = await ForkableStarknet.empty()
        contract = await starknet.deploy(contract_class=test_suite_definition)
        assert test_suite_definition.abi is not None
        starknet.cheatable_state.cheatable_state.class_hash_to_contract_abi_map[
            0
        ] = test_suite_definition.abi
        starknet.cheatable_state.cheatable_state.class_hash_to_contract_path_map[
            0
        ] = contract_path
        starknet.cheatable_state.cheatable_state.contract_address_to_class_hash_map[
            Address(contract.contract_address)
        ] = 0
        return cls(
            config=test_config,
            context=TestContext(),
            contract=contract,
            output_recorder=OutputRecorder(),
            stopwatch=Stopwatch(),
            starknet=starknet,
            project_compiler=project_compiler,
        )

    def fork(self) -> Self:
        return dataclasses.replace(
            super().fork(),
            config=deepcopy(self.config),
            context=deepcopy(self.context),
            output_recorder=self.output_recorder.fork(),
            stopwatch=self.stopwatch.fork(),
        )

    def determine_test_mode(self, test_case: TestCase):
        self.config.determine_mode(test_case=test_case, contract=self.contract)
