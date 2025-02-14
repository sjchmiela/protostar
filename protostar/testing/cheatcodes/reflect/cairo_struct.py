from typing import Any, List, OrderedDict, Tuple, Type, Union

from starkware.cairo.lang.vm.relocatable import RelocatableValue

from protostar.starknet import HintLocal, SimpleBreakingReportedException


class CairoStructException(SimpleBreakingReportedException):
    pass


class CairoStruct:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if len(args) > 0:  # / syntax not available in py3.7
            raise CairoStructException(
                "CairoStruct constructor takes only keyword arguments."
            )

        self._ordered_dict: OrderedDict[str, CairoValueType] = OrderedDict()

        for key, value in kwargs.items():
            if not isinstance(value, VALID_CAIRO_TYPES):
                raise CairoStructException(
                    f'"{type(value).__name__}" is not a valid CairoType.'
                )
            self._ordered_dict[key] = value

    def __getattr__(self, name: str) -> "CairoValueType":
        if name in self._ordered_dict:
            return self._ordered_dict[name]
        raise CairoStructException(f'"{name}" is not a member of this CairoStruct.')

    def __setattr__(self, name: str, value: Any) -> None:
        if name != "_ordered_dict":
            raise CairoStructException("CairoStruct is immutable.")
        super().__setattr__(name, value)

    def _set(self, name: str, value: "CairoValueType") -> None:
        if not isinstance(value, VALID_CAIRO_TYPES):  # type: ignore
            raise CairoStructException(
                f'"{type(value).__name__}" is not a valid CairoType.'
            )
        self._ordered_dict[name] = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CairoStruct):
            return False
        return self._ordered_dict == other._ordered_dict

    def __str__(self) -> str:
        stack: List[Tuple[Union[CairoStruct, RelocatableValue, str, int], int]] = [
            (self, 0)
        ]
        result: List[str] = []
        depth = 0

        while len(stack) > 0:
            curr, depth = stack.pop()

            if not isinstance(curr, CairoStruct):
                result.append(str(curr) + ("" if isinstance(curr, str) else "\n"))
            else:
                result.append(f"{type(curr).__name__}(\n")
                stack.append(("    " * depth + ")\n", 0))

                for name, child in reversed(list(curr._ordered_dict.items())):  # type: ignore
                    stack.append((child, depth + 1))
                    stack.append(("    " * (depth + 1) + f"{name}=", 0))

        return "".join(result)


VALID_CAIRO_TYPES = (CairoStruct, RelocatableValue, int)
CairoValueType = Union[CairoStruct, RelocatableValue, int]


class CairoStructHintLocal(HintLocal):
    @property
    def name(self) -> str:
        return "CairoStruct"

    def build(self) -> Type[CairoStruct]:
        return CairoStruct
