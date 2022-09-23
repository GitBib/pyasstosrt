import sys

try:
    import fire
    from pyfiglet import Figlet
except ModuleNotFoundError:
    print(
        'ERROR: pyasstosrt was installed without the cli extra. '
        'Please reinstall it with: pip install "pyasstosrt[cli]"',
        file=sys.stderr
    )
    sys.exit(1)

from pyasstosrt import Subtitle, __version__


def main():
    text = Figlet(font='slant')
    print(
        text.renderText('PyAssToSrt'),
        text.renderText(__version__),
        end='\n',
    )
    fire.Fire(Subtitle)


if __name__ == '__main__':
    main()
