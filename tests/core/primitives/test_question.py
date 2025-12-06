import pytest

from twpm.core.base.models import ListData
from twpm.core.primitives import QuestionNode


class MockOutput:
    def __init__(self):
        self.messages = []

    async def send_text(self, text: str) -> None:
        self.messages.append(text)


@pytest.mark.asyncio
class TestQuestionNode:
    async def test_first_execution_awaits_input(self):
        node = QuestionNode(question="Your name?", key="name")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.is_awaiting_input

    async def test_first_execution_succeeds(self):
        node = QuestionNode(question="Your name?", key="name")
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success

    async def test_stores_user_input_on_second_execution(self):
        node = QuestionNode(question="Your name?", key="name")
        data = ListData(data={})
        output = MockOutput()
        await node.execute(data, output)
        data["_user_input"] = "John Doe"

        await node.execute(data, output)

        assert data["name"] == "John Doe"

    async def test_second_execution_does_not_await_input(self):
        node = QuestionNode(question="Your name?", key="name")
        data = ListData(data={})
        output = MockOutput()
        await node.execute(data, output)
        data["_user_input"] = "John Doe"

        result = await node.execute(data, output)

        assert not result.is_awaiting_input

    async def test_second_execution_succeeds(self):
        node = QuestionNode(question="Your name?", key="name")
        data = ListData(data={})
        output = MockOutput()
        await node.execute(data, output)
        data["_user_input"] = "John Doe"

        result = await node.execute(data, output)

        assert result.success
