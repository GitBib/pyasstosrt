from pathlib import Path
from typing import Optional, List

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress
except ModuleNotFoundError as e:
    raise ImportError(
        "pyasstosrt was installed without the cli extra. Please reinstall it with: pip install 'pyasstosrt[cli]'"
    ) from e

from pyasstosrt import Subtitle, __version__

app = typer.Typer(help="Convert ASS subtitles to SRT format")
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold green]PyAssToSrt[/bold green] version: {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, help="Show version and exit"
    ),
):
    """
    PyAssToSrt - Convert ASS subtitles to SRT format
    """
    pass


@app.command()
def export(
    filepath: List[Path] = typer.Argument(
        ...,
        help="Path to the ASS file(s)",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    removing_effects: bool = typer.Option(
        False, "--remove-effects", "-r", help="Remove effects from subtitles"
    ),
    remove_duplicates: bool = typer.Option(
        False, "--remove-duplicates", "-d", help="Remove duplicate subtitles"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Output directory for the SRT file(s)",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
    encoding: str = typer.Option(
        "utf8", "--encoding", "-e", help="Encoding for the output file"
    ),
    output_dialogues: bool = typer.Option(
        False, "--output-dialogues", "-p", help="Print dialogues to console"
    ),
):
    """Convert ASS subtitle file(s) to SRT format"""
    with Progress() as progress:
        task = progress.add_task("[green]Converting...", total=len(filepath))

        for file in filepath:
            progress.console.print(f"\n[bold blue]Processing: {file.name}[/bold blue]")

            try:
                sub = Subtitle(file, removing_effects, remove_duplicates)
                result = sub.export(output_dir, encoding, output_dialogues)

                if output_dialogues:
                    progress.console.print(
                        Panel(f"Dialogues for {file.name}:", expand=False)
                    )
                    for dialogue in result:
                        progress.console.print(str(dialogue))

                output_file = (
                    Path(output_dir) / f"{file.stem}.srt"
                    if output_dir
                    else file.with_suffix(".srt")
                )
                progress.console.print(
                    f"[green]Success:[/green] Converted {file.name} to {output_file}"
                )
            except Exception as e:
                progress.console.print(
                    f"[red]Error:[/red] Failed to convert {file.name}. {str(e)}",
                    style="bold red",
                )

            progress.update(task, advance=1)

    console.print("\n[bold green]Conversion completed![/bold green]")


if __name__ == "__main__":
    app()
