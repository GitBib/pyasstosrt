import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union

from .dialogue import Dialogue


class Subtitle:
    """
    Converting ASS (Advanced SubStation Alpha) subtitles to SRT format.

    This class provides functionality to read an ASS subtitle file, convert its contents
    to SRT format, and export the result either as a file or as a list of dialogues.

    :param filepath: Path to a file that contains text in Advanced SubStation Alpha format
    :type filepath: Union[str, os.PathLike]
    :param removing_effects: Whether to remove effects from the text
    :type removing_effects: bool
    :param remove_duplicates: Whether to remove and merge consecutive duplicate dialogues
    :type remove_duplicates: bool

    :raises FileNotFoundError: If the specified file does not exist

    :ivar filepath: The path to the input ASS file
    :type filepath: Path
    :ivar file: The stem (filename without extension) of the input file
    :type file: str
    :ivar raw_text: The raw content of the input file
    :type raw_text: str
    :ivar dialogues: List of :class:`~pyasstosrt.dialogue.Dialogue` objects representing the subtitles
    :type dialogues: List[Dialogue]
    :ivar removing_effects: Flag indicating whether to remove effects from the text
    :type removing_effects: bool
    :ivar is_remove_duplicates: Flag indicating whether to remove and merge consecutive duplicate dialogues
    :type is_remove_duplicates: bool

    :Example:

    >>> from pyasstosrt import Subtitle
    >>> sub = Subtitle("path/to/subtitle.ass", removing_effects=True, remove_duplicates=True)
    >>> sub.convert()
    >>> sub.export("output/directory", encoding="utf-8")
    """

    dialog_mask = re.compile(
        r"Dialogue: \d+?,(\d:\d{2}:\d{2}.\d{2}),(\d:\d{2}:\d{2}.\d{2}),.*?,\d+,\d+,\d+,.*?,(.*)"
    )
    effects = re.compile(r"(\s?[ml].+?(-?\d+(\.\d+)?).+?(-?\d+(\.\d+)?).+)")

    def __init__(
        self,
        filepath: Union[str, os.PathLike],
        removing_effects: bool = False,
        remove_duplicates: bool = False,
    ):
        self.filepath = Path(filepath)
        if not self.filepath.is_file():
            raise FileNotFoundError(f'"{self.filepath}" does not exist')
        self.file: str = self.filepath.stem
        self.raw_text: str = self.get_text()
        self.dialogues: List[Dialogue] = []
        self.removing_effects: bool = removing_effects
        self.is_remove_duplicates: bool = remove_duplicates

    def get_text(self) -> str:
        """
        Reads the file and returns the complete contents.

        :return: File contents as a string
        :rtype: str
        """
        return self.filepath.read_text(encoding="utf8")

    def convert(self):
        """
        Convert the ASS subtitles to SRT format.

        This method processes the raw text, applies any necessary filters (like removing effects),
        and prepares the dialogues for formatting.
        """
        cleaning_old_format = re.compile(r"{.*?}")
        dialogs = re.findall(
            self.dialog_mask, re.sub(cleaning_old_format, "", self.raw_text)
        )
        if self.removing_effects:
            dialogs = filter(lambda x: re.sub(self.effects, "", x[2]), dialogs)
        dialogs = sorted(list(filter(lambda x: x[2], dialogs)))

        self.subtitle_formatting(dialogs)

    @staticmethod
    def text_clearing(raw_text: str) -> str:
        """
        Clear the text from unnecessary tags and format line breaks.

        :param raw_text: Dialog text with whitespace characters and ASS format tags
        :type raw_text: str
        :return: Cleaned dialog text without whitespaces and with proper line breaks
        :rtype: str
        """
        text = raw_text.replace(r"\h", "\xa0").strip()
        line_text = text.split(r"\N")
        return "\n".join(item.strip() for item in line_text).strip()

    @staticmethod
    def merged_dialogues(
        dialogues: List[Tuple[str, str, str]],
    ) -> List[Tuple[str, str, str]]:
        """
        Group consecutive dialogues with the same text into a single dialogue with a merged time range.

        :param dialogues: List of dialogue tuples (start_time, end_time, text)
        :type dialogues: List[Tuple[str, str, str]]
        :return: Generator yielding merged dialogues
        :rtype: List[Tuple[str, str, str]]
        """
        curr_dialogue = None
        for start, end, text in dialogues:
            if curr_dialogue is None:
                curr_dialogue = (start, end, text)
            elif text == curr_dialogue[2]:
                curr_dialogue = (curr_dialogue[0], end, text)
            else:
                yield curr_dialogue
                curr_dialogue = (start, end, text)
        if curr_dialogue is not None:
            yield curr_dialogue

    def remove_duplicates(
        self, dialogues: List[Tuple[str, str, str]]
    ) -> List[Tuple[str, str, str]]:
        """
        Remove consecutive duplicate dialogues in the given list and merge their time ranges.

        :param dialogues: A list of dialogues, where each dialogue is a tuple (start, end, text)
        :type dialogues: List[Tuple[str, str, str]]
        :return: A list of dialogues with consecutive duplicates removed and time ranges merged
        :rtype: List[Tuple[str, str, str]]
        """
        return list(self.merged_dialogues(dialogues))

    def subtitle_formatting(self, dialogues: List[Tuple[str, str, str]]):
        """
        Format ASS dialogues into SRT format.

        This method processes the dialogues, removes duplicates if necessary, and creates
        :class:`~pyasstosrt.dialogue.Dialogue` objects for each subtitle entry.

        :param dialogues: Prepared dialogues as tuples (start_time, end_time, text)
        :type dialogues: List[Tuple[str, str, str]]
        """
        cleaned_dialogues = (
            self.remove_duplicates(dialogues)
            if self.is_remove_duplicates
            else dialogues
        )

        for index, values in enumerate(cleaned_dialogues, start=1):
            start, end, text = values
            text = self.text_clearing(text.strip())
            dialogue = Dialogue(index, start, end, text)
            self.dialogues.append(dialogue)

    def export(
        self,
        output_dir: Optional[Union[str, os.PathLike]] = None,
        encoding: str = "utf8",
        output_dialogues: bool = False,
    ) -> Optional[List[Dialogue]]:
        """
        Export the subtitles either to a file or as a list of dialogues.

        If `output_dialogues` is False, this method exports the subtitles to an SRT file.
        Otherwise, it returns a list of :class:`~pyasstosrt.dialogue.Dialogue` objects.

        :param output_dir: Export path for the SRT file (optional)
        :type output_dir: Optional[Union[str, os.PathLike]]
        :param encoding: Encoding to use when saving the file (default is UTF-8)
        :type encoding: str
        :param output_dialogues: Whether to return a list of dialogues instead of creating an SRT file
        :type output_dialogues: bool
        :return: List of :class:`~pyasstosrt.dialogue.Dialogue` objects if `output_dialogues` is True, otherwise None
        :rtype: Optional[List[Dialogue]]
        """
        self.convert()

        if output_dialogues:
            return self.dialogues

        file = f"{self.file}.srt"
        if output_dir:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            out_path = out_path / file
        else:
            out_path = self.filepath.parent / file
        with open(out_path, encoding=encoding, mode="w") as writer:
            for dialogue in self.dialogues:
                writer.write(str(dialogue))
