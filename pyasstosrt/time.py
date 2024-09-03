class Time:
    """
    Represents a time structure for subtitle timestamps.

    Attributes:
        hour (int): The hour component of the time.
        minute (int): The minute component of the time.
        second (int): The second component of the time.
        millisecond (int): The millisecond component of the time.
    """

    hour: int
    minute: int
    second: int
    millisecond: int

    def __init__(self, text: str):
        """
        Initialize a Time object from a string representation.

        Args:
            text (str): A string representing time in the format '0:00:00.00'.

        Example:
            >>> time = Time("1:23:45.67")
            >>> print(time)
            01:23:45,670
        """
        s = text.split(":")
        self.hour, self.minute = [int(sr) for sr in s[:-1]]
        self.second, self.millisecond = [int(sr) for sr in s[-1].split(".")]
        # fix for srt
        self.millisecond *= 10

    def __sub__(self, other: "Time") -> float:
        """
        Calculate the duration between two :class:`Time` objects.

        Args:
            other (:class:`Time`): Another Time object to subtract from this one.

        Returns:
            float: The difference in seconds between the two :class:`Time` objects.

        Example:
            >>> t1 = Time("0:00:10.00")
            >>> t2 = Time("0:00:05.00")
            >>> print(t1 - t2)
            5.0
        """
        return (
            (self.hour - other.hour) * 3600
            + (self.minute - other.minute) * 60
            + (self.second - other.second)
            + (self.millisecond - other.millisecond) / 1000
        )

    def __str__(self) -> str:
        """
        Format the :class:`Time` object as a string for SRT subtitles.

        Returns:
            str: A string representation of the time in the format '00:00:00,000'.

        Example:
            >>> time = Time("1:23:45.67")
            >>> str(time)
            '01:23:45,670'
        """
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d},{self.millisecond:03d}"
