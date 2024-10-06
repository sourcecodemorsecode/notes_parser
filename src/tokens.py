"""This file contains the classes of different tokens."""

from __future__ import annotations
import abc


class GenericText(abc.ABC):
    """A generic class for text values"""

    def __init__(self, txt: str):
        """General instance set up."""

        self.text = txt

    def __len__(self):
        """Return the length of the text."""

        return len(self.text)


class HeaderText(GenericText):
    """A class for headers/titles."""

    def __init__(self, title: str, speaker: str) -> None:
        """
        Instance set up.

        Args:
            title: the title of the sermon
            speaker: who the sermon is by

        Returns:
            None
        """

        super().__init__(title)
        self.speaker = speaker

    def __str__(self) -> str:
        """String display of object, to help with debugging."""

        return f"Text={self.text}\nSpeaker={self.speaker}"


class ContentText(GenericText):
    """A class for text content."""

    def __init__(self, txt: str) -> None:
        """
        Instance set up.

        Args:
            txt: general text to display

        Returns:
            None
        """

        super().__init__(txt)

    def __str__(self) -> str:
        """String display of object, to help with debugging."""

        return self.text


class BulletList(GenericText):
    """A class for bulleted lists."""

    def __init__(self, txt: str, parent: BulletList | None = None) -> None:
        """
        Instance set up.

        Args:
            txt: the text in the bullet list item
            parent: the parent list item

        Returns:
            None
        """

        super().__init__(txt)
        self.parent = parent
        self.children = []


class NumberList(GenericText):
    """A class for numbered lists."""

    def __init__(self, txt: str, parent: BulletList | None = None):
        """
        Instance set up.

        Args:
            txt: the text in the bullet list item
            parent: the parent list item

        Returns:
            None
        """

        super().__init__(txt)
        self.parent = parent
        self.children = []


class QuotedText(GenericText):
    """A class for quotes."""

    def __init__(self, quote: str, author: str) -> None:
        """
        Instance set up.

        Args:
            quote: the quoted text
            author: a string of who who said the quote

        Returns:
            None
        """

        super().__init__(quote)
        self.author = author


class BibleQuote:
    """A class for Bible quotes."""

    def __init__(self, verse: str, version: str|None = None):
        """
        Instance set up.

        Args:
            verse: the book, chapter and verse of the quote
            version: the translation quoted from

        Returns:
            None
        """

        self.verse = verse
        self.version = version


class SideBySideComparison:
    """A class for a side by side comparison of two ideas."""

    def __init__(self, left_heading: str, right_heading: str) -> None:
        """
        Instance set up.

        Args:
            left_heading: the heading of the left column
            right_heading: the heading of the right column

        Returns:
            None
        """

        self.left_head = ContentText(left_heading)
        self.right_head = ContentText(right_heading)

        self.left_content = []
        self.right_content = []

    def __str__(self) -> str:
        """String display of object, to help with debugging."""

        output = f"*{self.left_head}* vs. *{self.right_head}*"

        assert len(self.left_content) == len(self.right_content)

        for i, left_item in enumerate(self.left_content):
            output += f"\n{left_item} vs. {self.right_content[i]}"

        return output

    def add_comp_pair(self, left_side: str, right_side: str):
        """
        Adds an item to each side of the comparison.

        Args:
            left_side: the text going on the left side of the comparison
            right_side: the text going on the right side of the comparison

        Returns:
            None
        """

        self.left_content.append(left_side)
        self.right_content.append(right_side)
