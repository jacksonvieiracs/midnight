from typing import override

from twpm.core.base import ListData, Node, NodeResult
from twpm.core.decorators import safe_execute
from twpm.core.depedencies import Output


class SummaryNode(Node):
    """
    Node that displays a summary of collected data with a nice formatted output.

    This node shows all the collected answers in a formatted way with checkmarks.
    """

    def __init__(
        self,
        title: str,
        fields: list[tuple[str, str]],
        key: str = "summary",
    ):
        """
        Initialize a SummaryNode.

        Args:
            title: The title message to display before the summary
            fields: List of tuples (label, data_key) to display in the summary
            key: Unique key for this node (default: "summary")
        """
        super().__init__(key)
        self.title = title
        self.fields = fields

    @override
    @safe_execute()
    async def execute(self, data: ListData, output: Output) -> NodeResult:
        """
        Display the summary of collected data.

        Args:
            data: Shared workflow data containing all collected answers

        Returns:
            NodeResult indicating success with the displayed summary
        """
        message = f"{self.title}\n"

        for _, data_key in self.fields:
            value = data.get(data_key, "-")
            message += f"✅ {value}\n"

        await output.send_text(message)

        return NodeResult(
            success=True, data={}, message="Summary displayed", is_awaiting_input=False
        )
