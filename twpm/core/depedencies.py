from typing import Protocol


class Output(Protocol):
    async def send_text(self, message: str) -> None: ...
