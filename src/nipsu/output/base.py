from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType

from nipsu.sniffer import FrameInfo


class Output(ABC):
    def __enter__(self) -> Output:
        self.display_start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.display_end()

    @abstractmethod
    def display_start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def display_frame(self, frame: FrameInfo) -> None:
        raise NotImplementedError()

    @abstractmethod
    def display_end(self) -> None:
        raise NotImplementedError()
