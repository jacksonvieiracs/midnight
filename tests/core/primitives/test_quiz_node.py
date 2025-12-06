import pytest

from twpm.core.base import ListData
from twpm.core.primitives.quiz import QuizNode


class MockOutput:
    def __init__(self):
        self.messages = []

    async def send_text(self, text: str) -> None:
        self.messages.append(text)


@pytest.mark.asyncio
class TestQuizNode:
    async def test_first_execution_awaits_input(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.is_awaiting_input
        assert result.success

    async def test_stores_correct_answer(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)
        data["_user_input"] = "2"
        result = await node.execute(data, output)

        assert not result.is_awaiting_input
        assert result.success
        assert data["math_answer"] == "4"
        assert data["math_answer_expected"] == "4"
        assert data["math_answer_correct"] == "true"

    async def test_stores_incorrect_answer(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)
        data["_user_input"] = "1"
        result = await node.execute(data, output)

        assert not result.is_awaiting_input
        assert result.success
        assert data["math_answer"] == "3"
        assert data["math_answer_expected"] == "4"
        assert data["math_answer_correct"] == "false"

    async def test_rejects_out_of_range_selection(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)
        data["_user_input"] = "5"
        result = await node.execute(data, output)

        assert result.is_awaiting_input
        assert result.success

    async def test_rejects_non_numeric_input(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)
        data["_user_input"] = "abc"
        result = await node.execute(data, output)

        assert result.is_awaiting_input
        assert result.success

    async def test_initialization_with_invalid_expected_answer_raises_error(self):
        with pytest.raises(
            ValueError, match="Resposta esperada.*deve ser uma das opções fornecidas"
        ):
            QuizNode(
                question="What is 2+2?",
                options=["3", "4", "5"],
                expected_answer="6",
                key="math_answer",
            )

    async def test_displays_question_and_options(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)

        assert len(output.messages) == 1
        message = output.messages[0]
        assert "What is 2+2?" in message
        assert "1. 3" in message
        assert "2. 4" in message
        assert "3. 5" in message

    async def test_message_contains_correctness_info(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)
        data["_user_input"] = "2"
        result = await node.execute(data, output)

        assert "Correto" in result.message

    async def test_message_contains_incorrectness_info(self):
        node = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="math_answer2",
        )
        data = ListData(data={})
        output = MockOutput()

        await node.execute(data, output)
        data["_user_input"] = "1"
        result = await node.execute(data, output)

        assert "Incorreto" in result.message

    async def test_multiple_quiz_nodes_independent(self):
        node1 = QuizNode(
            question="What is 2+2?",
            options=["3", "4", "5"],
            expected_answer="4",
            key="q1",
        )
        node2 = QuizNode(
            question="What is 3+3?",
            options=["5", "6", "7"],
            expected_answer="6",
            key="q2",
        )

        data = ListData(data={})
        output = MockOutput()

        await node1.execute(data, output)
        data["_user_input"] = "2"
        await node1.execute(data, output)

        await node2.execute(data, output)
        data["_user_input"] = "2"
        await node2.execute(data, output)

        assert data["q1"] == "4"
        assert data["q1_correct"] == "true"
        assert data["q2"] == "6"
        assert data["q2_correct"] == "true"
