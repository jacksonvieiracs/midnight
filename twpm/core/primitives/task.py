from collections.abc import Awaitable
from typing import Callable, override

from twpm.core.base import ListData, Node, NodeResult
from twpm.core.decorators import safe_execute

AsyncTaskFunc = Callable[[ListData], Awaitable[bool]]


class TaskNode(Node):
    def __init__(self, task: AsyncTaskFunc, key: str):
        self.task: AsyncTaskFunc = task
        super().__init__(key)

    @override
    @safe_execute()
    async def execute(self, data: ListData) -> NodeResult:
        success = await self.task(data)
        result = NodeResult(success=success, data={}, message="")
        return result
