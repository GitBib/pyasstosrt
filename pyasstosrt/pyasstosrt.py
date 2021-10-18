import os
import re
from os.path import isfile
from pathlib import Path
from typing import AnyStr, List, Union, Optional

from .dialogue import Dialogue


class Subtitle:
    """
    Converting ass to art.

    :type filepath: Path to a file that contains text in Advanced SubStation Alpha format
    """
    dialog_mask = re.compile(r"Dialogue: \d+?,(\d:\d{2}:\d{2}.\d{2}),(\d:\d{2}:\d{2}.\d{2}),.*?,\d+,\d+,\d+,.*?,(.*)")

    def __init__(self, filepath: Union[str, os.PathLike]):
        if not isfile(filepath):
            raise FileNotFoundError('"{}" does not exist'.format(filepath))
        if isinstance(filepath, os.PathLike):
            self.filepath: AnyStr = str(filepath)
            self.file: AnyStr = filepath.stem
        elif isinstance(filepath, str):
            self.filepath: AnyStr = filepath
            self.file: AnyStr = Path(filepath).stem
        else:
            raise TypeError('"{}" is not of type str'.format(filepath))
        self.raw_text: AnyStr = self.get_text()
        self.dialogues: List = []

    def get_text(self) -> AnyStr:
        """
        Reads the file and returns the complete contents
        :return: File contents
        """
        return Path(self.filepath).read_text(encoding="utf8")

    def convert(self):
        """
        Convert the format ass subtitles to srt.

        :return:
        """
        cleaning_old_format = re.compile(r"{.*?}")
        dialogs = re.findall(self.dialog_mask, re.sub(cleaning_old_format, "", self.raw_text))
        dialogs = sorted(list(filter(lambda x: x[2], dialogs)))

        self.subtitle_formatting(dialogs)

    @staticmethod
    def text_clearing(raw_text: str) -> str:
        """
        We're clearing the text from unnecessary tags.

        :param raw_text: Dialog text with whitespace characters
        :return: Dialog text without whitespaces and with the right move to a new line
        """

        text = raw_text.replace(r'\h', '\xa0').strip()
        line_text = text.split(r'\N')
        return '\n'.join(item.strip() for item in line_text).strip()

    def subtitle_formatting(self, dialogues: List):
        """
        Formatting ass into srt.

        :param dialogues: Prepared dialogues
        :return: Prepared dialogue sheet
        """
        for index, values in enumerate(dialogues, start=1):
            start, end, text = values
            text = self.text_clearing(text.strip())
            dialogue = Dialogue(index, start, end, text)
            self.dialogues.append(dialogue)

    def export(
            self,
            output_dir: AnyStr = None,
            encoding: AnyStr = "utf8",
            output_dialogues: bool = False
    ) -> Optional[List]:
        """
        If ret_dialogues parameter is False exports the subtitles to a file.

        :param output_dir: Export path SubRip file
        :param encoding: In which encoding you should save the file
        :param output_dialogues: Whereas it should return a list of dialogues not creating a SubRip file
        :return: List of dialogues
        """

        self.convert()

        if output_dialogues:
            return self.dialogues

        path = Path(self.filepath)
        file = self.file + ".srt"
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            out_path = os.path.join(output_dir, file)
        else:
            out_path = os.path.join(path.parent, file)
        with open(out_path, encoding=encoding, mode="w") as writer:
            for dialogue in self.dialogues:
                writer.write(str(dialogue))
