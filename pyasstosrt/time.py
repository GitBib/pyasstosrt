class Time:
    hour: int
    minute: int
    second: int
    millisecond: int

    def __init__(self, text: str):
        """
        Time data structure.

        :param text: format time '0:00:00.00'
        """
        s = text.split(":")
        self.hour, self.minute = [int(sr) for sr in s[:-1]]
        self.second, self.millisecond = [int(sr) for sr in s[-1].split(".")]
        # fix for srt
        self.millisecond *= 10

    def __sub__(self, other: "Time") -> float:
        """
        We get the duration of the subtitles.

        :param other: Another time structure
        :return: The difference between the beginning and end of subtitles
        """
        return (
            (self.hour - other.hour) * 3600
            + (self.minute - other.minute) * 60
            + (self.second - other.second)
            + (self.millisecond - other.millisecond) / 1000
        )

    def __str__(self) -> str:
        """
        Format the time for str subtitles.

        :return: We get the format string '0:00:00,000'
        """
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d},{self.millisecond:03d}"
