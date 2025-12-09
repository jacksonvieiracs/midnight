from typing import override

from twpm.core.base import ListData, Node, NodeResult
from twpm.core.decorators import safe_execute
from twpm.core.depedencies import Output

_SELECT_PROMPT = "Selecione uma opção (1-{}):"


class QuizNode(Node):
    """
    Node that presents a quiz question with multiple choice options.

    This node displays a question with options, validates the user's answer
    against an expected answer, and stores both the user's answer and whether
    it was correct in the workflow data.
    """

    def __init__(
        self, question: str, options: list[str], expected_answer: str, key: str
    ):
        """
        Initialize a QuizNode.

        Args:
            question: The quiz question to ask the user
            options: List of options to present to the user
            expected_answer: The correct answer (must be one of the options)
            key: The key to store the quiz result in the workflow data
        """
        super().__init__(key)
        self.question = question
        self.options = options
        self.expected_answer = expected_answer
        self._waiting_for_input = True

        if expected_answer not in options:
            raise ValueError(
                f"Resposta esperada '{expected_answer}' deve ser uma das opções fornecidas"
            )

    @override
    @safe_execute()
    async def execute(self, data: ListData, output: Output) -> NodeResult:
        """
        Display quiz question with options and process user selection.

        First execution: displays options, waits for input.
        Second execution: validates and stores the answer with correctness.

        Args:
            data: Shared workflow data
            output: Output interface for sending messages

        Returns:
            NodeResult indicating awaiting input or completed
        """
        if self._waiting_for_input:
            message = ""
            message += f"\n? {self.question}:\n"
            for i, option in enumerate(self.options, 1):
                message += f"  {i}. {option}\n"

            message += _SELECT_PROMPT.format(len(self.options))
            await output.send_text(message)

            self._waiting_for_input = False

            return NodeResult(
                success=True,
                data={},
                message=f"Aguardando resposta para: {self.question}",
                is_awaiting_input=True,
            )

        user_input = data.get("_user_input", "")

        try:
            index = int(user_input.strip()) - 1
            if 0 <= index < len(self.options):
                selected_answer = self.options[index]
                is_correct = selected_answer == self.expected_answer

                data[self.key] = selected_answer
                data[f"{self.key}_expected"] = self.expected_answer
                data[f"{self.key}_correct"] = "true" if is_correct else "false"

                return NodeResult(
                    success=True,
                    data={},
                    message=f"Resposta registrada: {selected_answer} ({'Correto' if is_correct else 'Incorreto'})",
                    is_awaiting_input=False,
                )

            max_opt = len(self.options)
            await output.send_text(_SELECT_PROMPT.format(max_opt))

            return NodeResult(
                success=True,
                data={},
                message="Seleção inválida, aguardando entrada válida",
                is_awaiting_input=True,
            )
        except ValueError:
            await output.send_text("Entrada inválida. Por favor, digite um número.")

            return NodeResult(
                success=True,
                data={},
                message="Formato de entrada inválido, aguardando entrada válida",
                is_awaiting_input=True,
            )
