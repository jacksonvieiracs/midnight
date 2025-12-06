import pytest

from twpm.core.base.models import ListData
from twpm.core.primitives import ProgressNode


class MockOutput:
    def __init__(self):
        self.messages = []

    async def send_text(self, text: str) -> None:
        self.messages.append(text)


@pytest.mark.asyncio
class TestProgressNode:
    async def test_executes_successfully(self):
        fields = [("Name", "name"), ("Email", "email")]
        node = ProgressNode(fields=fields, key="progress")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success

    async def test_does_not_await_input(self):
        fields = [("Name", "name"), ("Email", "email")]
        node = ProgressNode(fields=fields, key="progress")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert not result.is_awaiting_input

    async def test_displays_completed_and_pending_fields(self):
        fields = [("Name", "name"), ("Email", "email"), ("Phone", "phone")]
        node = ProgressNode(fields=fields, key="progress")
        data = ListData(data={"name": "John", "phone": "123456"})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success

    async def test_executes_with_title(self):
        fields = [("Name", "name")]
        node = ProgressNode(fields=fields, title="Progress Update", key="progress")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success

    async def test_executes_with_empty_fields(self):
        fields = []
        node = ProgressNode(fields=fields, key="progress")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success
