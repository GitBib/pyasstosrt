from .time import Time


class Dialogue:
    """
    Represents a dialogue entry in a subtitle file.

    This class encapsulates a single dialogue entry, including its index,
    start and end times, and text content.

    :param index: The position of the dialogue in the subtitle file
    :type index: int
    :param start: The start time of the dialogue
    :type start: str
    :param end: The end time of the dialogue
    :type end: str
    :param text: The text content of the dialogue
    :type text: str

    :ivar start: The start time of the dialogue
    :type start: :class:`~pyasstosrt.time.Time`
    :ivar end: The end time of the dialogue
    :type end: :class:`~pyasstosrt.time.Time`
    :ivar text: The text content of the dialogue
    :type text: str
    :ivar index: The position of the dialogue in the subtitle file
    :type index: int
    """

    def __init__(self, index: int, start: str, end: str, text: str):
        """
        Initialize a Dialogue instance.

        :param index: The position of the dialogue in the subtitle file
        :type index: int
        :param start: The start time of the dialogue
        :type start: str
        :param end: The end time of the dialogue
        :type end: str
        :param text: The text content of the dialogue
        :type text: str
        """
        self.index = index
        self.start = Time(start)
        self.end = Time(end)
        self.text = text

    def get_timestamp(self) -> str:
        """
        Format the timestamp for SRT format.

        Generates a formatted string representation of the dialogue's start and end times
        in the SRT timestamp format.

        :return: A formatted string representing the start and end times of the dialogue
        :rtype: str
        """
        return f"{self.start} --> {self.end}"

    def __str__(self) -> str:
        """
        Format the dialogue as a string in SRT format.

        :return: A formatted string representation of the dialogue, including index, timestamp, and text
        :rtype: str
        """
        return f"{self.index}\n{self.get_timestamp()}\n{self.text}\n\n"
