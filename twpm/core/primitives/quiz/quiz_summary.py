from typing import override

from twpm.core.base import ListData, Node, NodeResult
from twpm.core.decorators import safe_execute
from twpm.core.depedencies import Output


class QuizSummaryNode(Node):
    """
    Node that displays a summary of quiz results with correct/incorrect indicators.

    This node shows all quiz questions with the user's answers, expected answers,
    and whether each answer was correct or incorrect, along with a final score.
    """

    def __init__(
        self,
        title: str,
        quiz_keys: list[str],
        key: str = "quiz_summary",
    ):
        """
        Initialize a QuizSummaryNode.

        Args:
            title: The title message to display before the quiz summary
            quiz_keys: List of keys used to store quiz results (from QuizNode)
            key: Unique key for this node (default: "quiz_summary")
        """
        super().__init__(key)
        self.title = title
        self.quiz_keys = quiz_keys

    @override
    @safe_execute()
    async def execute(self, data: ListData, output: Output) -> NodeResult:
        """
        Display the quiz summary with results.

        Args:
            data: Shared workflow data containing all quiz results
            output: Output interface for sending messages

        Returns:
            NodeResult indicating success with the displayed summary
        """
        message = f"{self.title}\n\n"

        correct_count = 0
        total_count = len(self.quiz_keys)

        for quiz_key in self.quiz_keys:
            user_answer = data.get(quiz_key, "-")
            expected_answer = data.get(f"{quiz_key}_expected", "-")
            is_correct_str = data.get(f"{quiz_key}_correct", "false")

            is_correct = is_correct_str == "true"
            if is_correct:
                correct_count += 1

            if is_correct:
                message += f"✅ {expected_answer}\n"
            else:
                message += f"❌ {expected_answer} - {user_answer}\n"

        score_key = (
            f"{self.key}_score" if hasattr(self, "key") and self.key else "quiz_score"
        )
        data[score_key] = str(correct_count)
        data[f"{score_key}_total"] = str(total_count)
        data[f"{score_key}_percentage"] = str(
            round((correct_count / total_count * 100) if total_count > 0 else 0, 1)
        )

        message += f"\nVocê acertou {correct_count} das {total_count} perguntas.\n"

        await output.send_text(message)

        return NodeResult(
            success=True,
            data={},
            message="Resumo do quiz exibido",
            is_awaiting_input=False,
        )
