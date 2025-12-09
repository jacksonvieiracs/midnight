import pytest

from twpm.core.base import ListData
from twpm.core.primitives.quiz import QuizSummaryNode


class MockOutput:
    def __init__(self):
        self.messages = []

    async def send_text(self, text: str) -> None:
        self.messages.append(text)


@pytest.mark.asyncio
class TestQuizSummaryNode:
    async def test_displays_quiz_summary_with_correct_answers(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1", "q2"],
        )
        data = ListData(
            data={
                "q1": "4",
                "q1_expected": "4",
                "q1_correct": "true",
                "q2": "6",
                "q2_expected": "6",
                "q2_correct": "true",
            }
        )
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success
        assert not result.is_awaiting_input
        assert len(output.messages) == 1
        message = output.messages[0]
        assert "Quiz Results" in message
        assert "✅" in message
        assert "✅ 4" in message
        assert "✅ 6" in message
        assert "Você acertou 2 das 2 perguntas" in message
        assert data["quiz_summary_score"] == "2"
        assert data["quiz_summary_score_total"] == "2"

    async def test_displays_quiz_summary_with_incorrect_answers(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1", "q2"],
        )
        data = ListData(
            data={
                "q1": "3",
                "q1_expected": "4",
                "q1_correct": "false",
                "q2": "5",
                "q2_expected": "6",
                "q2_correct": "false",
            }
        )
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success
        message = output.messages[0]
        assert "❌" in message
        assert "❌ 4 - 3" in message
        assert "❌ 6 - 5" in message
        assert "Você acertou 0 das 2 perguntas" in message
        assert data["quiz_summary_score"] == "0"
        assert data["quiz_summary_score_total"] == "2"

    async def test_displays_mixed_results(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1", "q2", "q3"],
        )
        data = ListData(
            data={
                "q1": "4",
                "q1_expected": "4",
                "q1_correct": "true",
                "q2": "5",
                "q2_expected": "6",
                "q2_correct": "false",
                "q3": "7",
                "q3_expected": "7",
                "q3_correct": "true",
            }
        )
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success
        message = output.messages[0]
        assert "✅ 4" in message
        assert "❌ 6 - 5" in message
        assert "✅ 7" in message
        assert "Você acertou 2 das 3 perguntas" in message
        assert data["quiz_summary_score"] == "2"
        assert data["quiz_summary_score_total"] == "3"

    async def test_displays_user_and_expected_answers(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1"],
        )
        data = ListData(
            data={
                "q1": "3",
                "q1_expected": "4",
                "q1_correct": "false",
            }
        )
        output = MockOutput()

        await node.execute(data, output)

        message = output.messages[0]
        assert "❌ 4 - 3" in message
        assert "Você acertou 0 das 1 perguntas" in message

    async def test_handles_missing_data_gracefully(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1", "q2"],
        )
        data = ListData(
            data={
                "q1": "4",
                "q1_expected": "4",
                "q1_correct": "true",
                # q2 data is missing
            }
        )
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success
        message = output.messages[0]
        assert "✅ 4" in message
        assert "❌ - -" in message or "-" in message
        assert data["quiz_summary_score"] == "1"
        assert data["quiz_summary_score_total"] == "2"

    async def test_empty_quiz_keys_shows_zero_score(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=[],
        )
        data = ListData(data={})
        output = MockOutput()

        result = await node.execute(data, output)

        assert result.success
        message = output.messages[0]
        assert "Você acertou 0 das 0 perguntas" in message
        assert data["quiz_summary_score"] == "0"
        assert data["quiz_summary_score_total"] == "0"

    async def test_custom_key_set(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1"],
            key="custom_key",
        )

        assert node.key == "custom_key"

    async def test_custom_key_persists_score_with_prefix(self):
        node = QuizSummaryNode(
            title="Quiz Results",
            quiz_keys=["q1", "q2"],
            key="my_quiz",
        )
        data = ListData(
            data={
                "q1": "4",
                "q1_expected": "4",
                "q1_correct": "true",
                "q2": "5",
                "q2_expected": "6",
                "q2_correct": "false",
            }
        )
        output = MockOutput()

        await node.execute(data, output)

        assert data["my_quiz_score"] == "1"
        assert data["my_quiz_score_total"] == "2"
        assert data["my_quiz_score_percentage"] == "50.0"

    async def test_multiple_quiz_summaries_independent(self):
        node1 = QuizSummaryNode(
            title="Math Quiz",
            quiz_keys=["q1"],
        )
        node2 = QuizSummaryNode(
            title="Science Quiz",
            quiz_keys=["q2"],
        )

        data = ListData(
            data={
                "q1": "4",
                "q1_expected": "4",
                "q1_correct": "true",
                "q2": "6",
                "q2_expected": "6",
                "q2_correct": "true",
            }
        )
        output = MockOutput()

        await node1.execute(data, output)
        await node2.execute(data, output)

        assert len(output.messages) == 2
        assert "Math Quiz" in output.messages[0]
        assert "Science Quiz" in output.messages[1]
        assert "Você acertou 1 das 1 perguntas" in output.messages[0]
        assert "Você acertou 1 das 1 perguntas" in output.messages[1]
