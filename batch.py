try:
    import fire
    from pyfiglet import Figlet
except ModuleNotFoundError:
    raise ImportError(
        "pyasstosrt was installed without the cli extra." 'Please reinstall it with: pip install "pyasstosrt[cli]"'
    )

from pyasstosrt import Subtitle, __version__


def main():
    text = Figlet(font="slant")
    print(  # noqa: T201
        text.renderText("PyAssToSrt"),
        text.renderText(__version__),
        end="\n",
    )
    fire.Fire(Subtitle)


if __name__ == "__main__":
    main()
