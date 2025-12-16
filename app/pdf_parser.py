from abc import abstractmethod, ABC
import re

class PDFParser(ABC):
    @abstractmethod
    def parse(self) -> str:
        """Extracts text from a PDF and returns a raw string."""
        pass

class SectionNode:
    def __init__(self, title: str, depth: int):
        self.title = title
        self.depth = depth
        self.content: list[str] = []
        self.children: list[SectionNode] = []

    def __repr__(self):
        return f"SectionNode(depth={self.depth}, title={self.title!r})"


class CustomPDFParser(PDFParser):
    HEADING_PATTERN = re.compile(r"^(?P<num>(\d+(?:\.\d+)*))\.\s*(?P<title>.+)$")

    def __init__(self, raw_text: str):
        # Normalize whitespace to preserve line structure
        self.lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    def parse(self) -> list[SectionNode]:
        root: list[SectionNode] = []
        stack: list[SectionNode] = []

        for line in self.lines:
            heading_match = self.HEADING_PATTERN.match(line)

            if heading_match:
                # Extract numbering: "1", "1.1", "1.1.1", etc.
                numbering = heading_match.group("num")
                title = heading_match.group("title")

                # Determine depth = how many dots in numbering
                depth = numbering.count(".")

                # Create new section node
                node = SectionNode(title=f"{numbering}. {title}", depth=depth)

                # Attach to tree
                if depth == 0:
                    root.append(node)
                    stack = [node]
                else:
                    # Parent should be the last node at depth-1
                    parent = stack[depth - 1]
                    parent.children.append(node)

                    # Fix stack: keep only parents up to this depth
                    stack = stack[:depth]
                    stack.append(node)
            else:
                # This is content, attach to the last active node
                if stack:
                    stack[-1].content.append(line)

        return root
