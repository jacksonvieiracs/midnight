import pytest

from twpm.core.base.models import ListData
from twpm.core.primitives import DisplayMessageNode


class MockOutput:
    def __init__(self):
        self.messages = []

    async def send_text(self, text: str) -> None:
        self.messages.append(text)


@pytest.mark.asyncio
class TestDisplayMessageNode:
    async def test_executes_successfully(self):
        node = DisplayMessageNode(message="Test message", key="test_msg")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success

    async def test_does_not_await_input(self):
        node = DisplayMessageNode(message="Test message", key="test_msg")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert not result.is_awaiting_input

    async def test_preserves_message_in_result(self):
        message = "Important message"
        node = DisplayMessageNode(message=message, key="test_msg")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.message == message
