"""This file processes a string to check for and process tokens."""

import pathlib
import tokens

# priority:
# 1 - Header
# 2 - Comp
# 3 - Number
# 4 - Bullet
# 5 - Bible Quote
# 6 - Quote
# 7 - General


class SermonAnalyser:
    """A class for lexical analysis of sermon notes."""


    def __init__(self, file_dir: str) -> None:
        """
        Set up the class and reads the specified file.
        
        Args:
            file_dir: a path to the file to be read/adapted
            
        Returns:
            None

        Raises:
            FileNotFoundError: when the given file directory is not valid

        """
        
        self.file = pathlib.Path(file_dir)

        if not self.file.is_file():
            raise FileNotFoundError(f"Could not find {str(self.file)}")
        elif self.file.suffix != ".txt":
            raise TypeError(f"Expected a .txt file but got "
                            f"a {self.file.suffix} file.")
        
        with open(self.file, mode='r', encoding='utf-8') as f:
            # read lines into a list and remove new line characters
            self.lines = [ln.replace('\n', '') for ln in f.readlines()]

    def find_header(self) -> tokens.HeaderText:
        """
        Finds the header/title of the text.
        
        title - the first non-blank line of text
        speaker - key start: "by", first subsequent non-black line of text

        Returns:
            tokens.HeaderText: an object containing the title and speaker

        Raises:
            Exception: when a title and speaker cannot both be found
        """

        title = ""
        speaker = ""

        # find title
        while len(self.lines) > 0:
            if self.lines[0] != "":
                title = self.lines[0]
                self.lines.pop(0)
                break
            
            self.lines.pop(0)

        # find speaker
        while len(self.lines) > 0:
            if self.lines[0] != "":
                if self.lines[0][:2].lower() == "by":
                    speaker = self.lines[0]
                    self.lines.pop(0)
                    break
                else:
                    speaker = "(no speaker)"
                    break
            
            self.lines.pop(0)

        # confirm both have been found
        if title == "" or speaker == "":
            raise Exception(f"Could not find header in {len(self.lines)} lines.")

        return tokens.HeaderText(title, speaker)

    def find_comparison(self) -> list[tokens.SideBySideComparison]:
        """
        Finds all instances of side-by-side comparison.

        Conditions:
            Key start: "::" for headings, ":" for items
            Left and right sides separated by a "/"
            Each comparison must begin with a header
            Each comparison items must be continuous (blank lines allowed)
            Can only compare two things side-by-side

        Returns:
            list[tokens.SideBySideComparison]:
                a list of objects containing each comparison group
        """

        comps = []
        # search through all lines for heading matches
        for i, ln in enumerate(self.lines):
            if ln[:2] == "::":
                # once a heading is found, gather all related items
                items = self.get_comp_items(i + 1)
                comps.append([i] + items)

        # create comparison objects
        comp_objs = []
        for group in comps:
            comp_objs.append(self.make_comp_obj(group))

        return comp_objs

    def get_comp_items(self, start: int) -> list[int]:
        """
        A method to collect the lines related to comparison.
        
        Args:
            start: the line number to begin searching at

        Returns:
            a list representing lines numbers of related comparison items
        """

        items = []

        i = start
        while i < len(self.lines):
            if self.lines[i] == "":  # remove blank lines
                self.lines.pop(i)
                i -= 1
            elif self.lines[i][0] == ":" and self.lines[i][1] != ":":
                # check for key start and not new group start
                items.append(i)
            else:
                break
            i += 1
        
        return items
    
    def make_comp_obj(self, comp_lines: list[int]
                      ) -> tokens.SideBySideComparison:
        """
        Creates a single comparison object.

        Args:
            comp_lines: the list of lines in a particular comparison group

        Returns:
            tokens.SideBySideComparison: the comparison object
        """

        # get the line and remove the leading "::"
        header_line = self.lines[comp_lines[0]][2:]
        # split the line by the '//' divider
        heads = header_line.split("//", 1)
        comparison = tokens.SideBySideComparison(*heads)

        for ln_ind in comp_lines[1:]:
            # get and split the line after removing the leading ":"
            items = self.lines[ln_ind][1:].split("//", 1)
            comparison.add_comp_pair(*items)

        return comparison


if __name__ == "__main__":

    path = pathlib.Path('test_sermon.txt')

    analyser = SermonAnalyser(path)
    print(analyser.find_header())
    analyser = SermonAnalyser(path) 
    comps = analyser.find_comparison()
    for c in comps:
        print(c)