import os
import re
from pathlib import Path
from typing import Any, Generator, List, Optional, Tuple, Union

from .dialogue import Dialogue


class Subtitle:
    """
    Converting ASS (Advanced SubStation Alpha) and SRT subtitles.

    This class provides functionality to read ASS or SRT subtitle files, convert their contents
    to SRT format, and export the result either as a file or as a list of dialogues.

    :param filepath: Path to a file that contains text in ASS or SRT format
    :type filepath: Union[str, os.PathLike]
    :param removing_effects: Whether to remove effects from the text (applies to ASS files)
    :type removing_effects: bool
    :param remove_duplicates: Whether to remove and merge consecutive duplicate dialogues
    :type remove_duplicates: bool
    :param only_default_style: If True, exports only styles with "Default" in the name (e.g., Default, Default_dvd)
    :type only_default_style: bool
    :param include_styles: List of styles to include (if specified, only these styles will be exported)
    :type include_styles: Optional[List[str]]
    :param exclude_styles: List of styles to exclude (if specified, these styles will be filtered out)
    :type exclude_styles: Optional[List[str]]

    :raises FileNotFoundError: If the specified file does not exist

    :ivar filepath: The path to the input subtitle file
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
    :ivar only_default_style: Flag indicating whether to export only styles with "Default" in name
    :type only_default_style: bool
    :ivar include_styles: List of styles to include (if specified, only these styles will be exported)
    :type include_styles: Optional[List[str]]
    :ivar exclude_styles: List of styles to exclude (if specified, these styles will be filtered out)
    :type exclude_styles: Optional[List[str]]

    :Example:

    >>> from pyasstosrt import Subtitle
    >>> sub = Subtitle("path/to/subtitle.ass", removing_effects=True, remove_duplicates=True)
    >>> sub.convert()
    >>> sub.export("output/directory", encoding="utf-8")
    """

    dialog_mask = re.compile(
        r"Dialogue: \d+?,(\d:\d{2}:\d{2}.\d{2}),(\d:\d{2}:\d{2}.\d{2}),(.*?),.*?,\d+,\d+,\d+,.*?,(.*)"
    )
    effects = re.compile(r"(\s?[ml].+?(-?\d+(\.\d+)?).+?(-?\d+(\.\d+)?).+)")
    srt_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")

    def __init__(
        self,
        filepath: Union[str, os.PathLike],
        removing_effects: bool = False,
        remove_duplicates: bool = False,
        only_default_style: bool = False,
        include_styles: Optional[List[str]] = None,
        exclude_styles: Optional[List[str]] = None,
    ):
        self.filepath = Path(filepath)
        if not self.filepath.is_file():
            raise FileNotFoundError(f'"{self.filepath}" does not exist')
        self.file: str = self.filepath.stem
        self.raw_text: str = self.get_text()
        self.dialogues: List[Dialogue] = []
        self.styles: List[str] = []
        self.removing_effects: bool = removing_effects
        self.is_remove_duplicates: bool = remove_duplicates
        self.only_default_style: bool = only_default_style
        self.include_styles: Optional[List[str]] = include_styles
        self.exclude_styles: Optional[List[str]] = exclude_styles

    def get_text(self) -> str:
        """
        Reads the file and returns the complete contents.

        :return: File contents as a string
        :rtype: str
        """
        return self.filepath.read_text(encoding="utf8")

    def get_styles(self) -> List[str]:
        """
        Return all unique style names from the ASS file.

        Styles are collected during conversion. If convert() hasn't been called yet,
        this method will call it automatically.

        :return: List of unique style names found in the file
        :rtype: List[str]
        """
        if not self.styles:
            self.convert()

        return self.styles

    def is_srt_format(self) -> bool:
        """
        Determines if the file is in SRT format.

        :return: True if the file is in SRT format, False otherwise
        :rtype: bool
        """
        return self.filepath.suffix.lower() == ".srt" or bool(self.srt_pattern.search(self.raw_text))

    def convert(self):
        """
        Convert the subtitles to SRT format.

        This method processes the raw text, applies any necessary filters (like removing effects),
        and prepares the dialogues for formatting. Automatically detects ASS or SRT format.
        """
        if self.is_srt_format():
            self._convert_srt()
        else:
            self._convert_ass()

    def _convert_ass(self):
        """
        Convert ASS subtitles to SRT format.

        This method processes ASS format, applies any necessary filters (like removing effects),
        and prepares the dialogues for formatting.
        """
        cleaning_old_format = re.compile(r"{.*?}")
        dialogs = re.findall(self.dialog_mask, re.sub(cleaning_old_format, "", self.raw_text))

        # Collect unique styles
        self.styles = sorted(set(d[2] for d in dialogs))

        # Filter by styles if specified
        if self.only_default_style and not self.include_styles and not self.exclude_styles:
            # Keep only styles containing "Default" (e.g., Default, Default_dvd, etc.)
            dialogs = list(filter(lambda d: "Default" in d[2], dialogs))
        elif self.include_styles:
            # Build inclusion set for efficient lookup
            include_set = set(self.include_styles)
            dialogs = list(filter(lambda d: d[2] in include_set, dialogs))
        elif self.exclude_styles:
            # Build exclusion set for efficient lookup
            exclude_set = set(self.exclude_styles)
            dialogs = list(filter(lambda d: d[2] not in exclude_set, dialogs))

        if self.removing_effects:
            dialogs = filter(lambda x: re.sub(self.effects, "", x[3]), dialogs)
        dialogs = list(filter(lambda x: x[3], dialogs))

        # Convert from (start, end, style, text) to (start, end, text) for subtitle_formatting
        dialogs = [(d[0], d[1], d[3]) for d in dialogs]

        # Sort by (start, end, text) for chronological and stable order
        dialogs = sorted(dialogs)

        self.subtitle_formatting(dialogs)

    def _convert_srt(self):
        """
        Parse SRT subtitles into internal tuple format.

        Converts SRT format to the same (start, end, text) tuple format used by _convert_ass(),
        then uses the shared subtitle_formatting() pipeline for creating Dialogue objects.

        Note: SRT subtitle numbers are ignored - new sequential indices are generated
        by subtitle_formatting() using enumerate(start=1).
        """
        # Parse all SRT entries using regex (similar to _convert_ass approach)
        srt_entry_pattern = re.compile(
            r"^\d+\s*$\s+"  # Subtitle number (ignored)
            r"^(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*$\s+"  # Timecodes
            r"((?:^(?!\d+\s*$).+$\s*)*)",  # Text (lines that are NOT just a number)
            re.MULTILINE,
        )

        dialogs = []
        for match in srt_entry_pattern.finditer(self.raw_text):
            start_srt, end_srt, text = match.groups()

            # Convert to ASS format for Time class: "00:00:10,580" → "0:00:10.58"
            start_ass = self._srt_time_to_ass(start_srt)
            end_ass = self._srt_time_to_ass(end_srt)

            # Clean and join multiline text, filtering empty lines
            text = " ".join(line.strip() for line in text.strip().split("\n") if line.strip())

            if text:
                dialogs.append((start_ass, end_ass, text))

        # Sort by time, then use shared formatting pipeline
        dialogs = sorted(dialogs)
        self.subtitle_formatting(dialogs)

    @staticmethod
    def _srt_time_to_ass(srt_time: str) -> str:
        """
        Convert SRT time format to ASS time format.

        :param srt_time: Time in SRT format (HH:MM:SS,mmm)
        :type srt_time: str
        :return: Time in ASS format (H:MM:SS.mm)
        :rtype: str
        """
        # SRT: 00:00:10,580 -> ASS: 0:00:10.58
        time_part, ms_part = srt_time.split(",")
        h, m, s = time_part.split(":")
        # Remove leading zero from hours and truncate milliseconds to 2 digits
        return f"{int(h)}:{m}:{s}.{ms_part[:2]}"

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
    ) -> Generator[Union[Tuple[str, str, str], Tuple[Any, str, str]], Any, None]:
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

    def remove_duplicates(self, dialogues: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
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
        cleaned_dialogues = self.remove_duplicates(dialogues) if self.is_remove_duplicates else dialogues

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
            return None
