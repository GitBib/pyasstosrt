from .time import Time


class Dialogue:
    start: Time
    end: Time
    text: str
    index: int

    def __init__(self, index: int, start: str, end: str, text: str):
        """
        Dialogue structure.

        :param index: Must contain a position of dialogue
        :param start: Start time of the dialogue
        :param end: End of dialog time
        :param text: Contains the text of the dialogue
        """
        self.index = index
        self.start = Time(start)
        self.end = Time(end)
        self.text = text

    def get_timestamp(self) -> str:
        """
        Format a time line for srt.

        :return: Let's finish the line of the beginning and end of the dialogue...
        """
        return f"{self.start} --> {self.end}"

    def __str__(self) -> str:
        """
        Formatting the dialogue in string.

        :return: We get a dialogue in string
        """
        return f"{self.index}\n{self.get_timestamp()}\n{self.text}\n\n"
