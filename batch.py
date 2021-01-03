import fire
from pyfiglet import Figlet

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
