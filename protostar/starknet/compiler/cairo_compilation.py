from pathlib import Path
from typing import List

from starkware.cairo.lang.compiler.assembler import assemble
from starkware.cairo.lang.compiler.preprocessor.preprocessor import PreprocessedProgram
from starkware.cairo.lang.compiler.preprocessor.preprocess_codes import preprocess_codes
from starkware.cairo.lang.compiler.program import Program

from .common import CompilerConfig
from .pass_managers import CairoPassManagerFactory


class CairoCompiler:
    def __init__(self, config: CompilerConfig):
        self.compiler_config = config

    def preprocess(self, file: Path) -> PreprocessedProgram:  # TODO: Cache result
        pass_manager = CairoPassManagerFactory.build(self.compiler_config)
        return preprocess_codes(
            codes=[(file.read_text("utf-8"), str(file))],
            pass_manager=pass_manager,
        )

    @staticmethod
    def compile_preprocessed(
        preprocessed: PreprocessedProgram,
    ) -> Program:  # TODO: Cache result
        return assemble(preprocessed)

    def get_function_names(self, file_path: Path) -> List[str]:
        preprocessed = self.preprocess(file_path)
        return [
            name
            for name, identifier in preprocessed.identifiers.root.identifiers.items()
            if identifier.TYPE == "function"  # pyright: ignore
        ]
