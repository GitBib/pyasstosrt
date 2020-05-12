import os
from pathlib import Path
import re
from typing import AnyStr, List
from .dialogue import Dialogue


class Subtitle(object):
    """

    Converting ass to art

    :type filepath: Path to a file that contains text in Advanced SubStation Alpha format
    """

    def __init__(self, filepath: AnyStr):
        self.filepath: AnyStr = filepath
        self.file: AnyStr = Path(filepath).stem
        self.raw_text: AnyStr = self.get_text()
        self.dialogues: List = list()

    def get_text(self) -> AnyStr:
        return Path(self.filepath).read_text(encoding="utf8")

    def convert(self):
        """

        Convert the format ass subtitles to srt.

        :return:
        """
        cleaning_old_format = re.compile(r"{.*?}")
        dialog_mask = re.compile(r"Dialogue: \d+?,(\d:\d{2}:\d{2}.\d{2}),(\d:\d{2}:\d{2}.\d{2}),.*?,\d+,\d+,\d+,.*?,(.*)")
        dialogs = re.findall(dialog_mask, re.sub(cleaning_old_format, "", self.raw_text))
        dialogs = sorted(list(filter(lambda x: x[2], dialogs)))

        self.subtitle_formatting(dialogs)

    @staticmethod
    def text_clearing(raw_text: str) -> str:
        """

        We're clearing the text from unnecessary tags.

        :param raw_text: Dialog text with whitespace characters
        :return: Dialog text without whitespaces and with the right move to a new line
        """

        text = raw_text.replace('\h', '\xa0').strip()
        line_text = text.split(r'\N')
        return '\n'.join([item.strip() for item in line_text]).strip()

    def subtitle_formatting(self, dialogues: List):
        """

        Formatting ass into srt

        :param dialogues: Prepared dialogues
        :return: Prepared dialogue sheet
        """
        for index, values in enumerate(dialogues, start=1):
            start, end, text = values
            text = self.text_clearing(text.strip())
            dialogue = Dialogue(index, start, end, text)
            self.dialogues.append(dialogue)

    def export(self, output_dir: AnyStr = None):
        """

        Export the subtitles to a file.

        :param output_dir: Export path SubRip file
        :return: SubRip file
        """

        self.convert()
        path = Path(self.filepath)
        file = self.file + ".srt"
        if output_dir:
            out_path = os.path.join(output_dir, file)
        else:
            out_path = os.path.join(path.parent, file)
        with open(out_path, encoding="utf8", mode="w") as writer:
            for dialogue in self.dialogues:
                writer.write(str(dialogue))
