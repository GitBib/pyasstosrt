import os
from pathlib import Path
import re
from typing import AnyStr, Dict, List


class Substation(object):
    """
    :type filepath: Path to a file that contains text in Advanced SubStation Alpha format
    """

    def __init__(self, filepath: AnyStr):
        self.filepath: AnyStr = filepath
        self.file: AnyStr = Path(filepath).stem
        self.raw_text: AnyStr = self.get_text()
        self.dialogues: Dict = dict()

    def get_text(self) -> AnyStr:
        return Path(self.filepath).read_text(encoding="utf8")

    def convert(self):
        cleaning_old_format = re.compile(r"{.*?}")
        dialog_mask = re.compile(r"Dialogue: \d,(\d:\d{2}:\d{2}.\d{2}),(\d:\d{2}:\d{2}.\d{2}),.*,.*.*,.*,.*,.*,(.*)")
        dialogs = re.findall(dialog_mask, re.sub(cleaning_old_format, "", self.raw_text))
        dialogs = sorted(list(filter(lambda x: x[2], dialogs)))

        self.subtitle_formatting(dialogs)

    @staticmethod
    def text_clearing(raw_text: AnyStr) -> AnyStr:
        """
        :param raw_text: Dialog text with whitespace characters
        :return: Dialog text without whitespaces and with the right move to a new line
        """

        text = raw_text.strip()
        line_text = text.split(r'\N')
        return '\n'.join([item.strip() for item in line_text]).strip()

    def subtitle_formatting(self, dialogs: List):
        """
        :param dialogs: Prepared dialogues
        :return: Prepared dialogue sheet
        """

        self.dialogues = {start.replace(".", ",") + " --> " +
                          end.replace(".", ","): self.text_clearing(text.strip()) for start, end, text in dialogs}

    def translate(self, output_dir: AnyStr = None):
        """
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
            entry = 1
            for timestamp, text in self.dialogues.items():
                sub = f"{entry}\n{timestamp}\n{text}\n\n"
                writer.write(sub)
                entry += 1
