from pathlib import Path
from typing import Annotated, List, Optional

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.traceback import install as install_rich_traceback
except ModuleNotFoundError as e:
    raise ImportError(
        "pyasstosrt was installed without the cli extra. Please reinstall it with: pip install 'pyasstosrt[cli]'"
    ) from e

from pyasstosrt import Subtitle, __version__

# Install rich traceback for better error display
install_rich_traceback(show_locals=True)

app = typer.Typer(
    name="pyasstosrt",
    help="🎬 Convert ASS/SSA subtitles to SRT format with style filtering",
    add_completion=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold green]PyAssToSrt[/bold green] version: {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version information and exit",
        ),
    ] = None,
):
    """
    [bold cyan]PyAssToSrt[/bold cyan] - Convert ASS/SSA subtitles to SRT format

    A powerful tool for converting Advanced SubStation Alpha (ASS/SSA) subtitle files
    to SubRip (SRT) format with advanced filtering capabilities.
    """
    pass


@app.command(name="export", help="Convert ASS/SSA subtitle file(s) to SRT format")
def export(
    filepath: Annotated[
        List[Path],
        typer.Argument(
            help="Path(s) to the ASS/SSA file(s) to convert",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            show_default=False,
        ),
    ],
    removing_effects: Annotated[
        bool,
        typer.Option(
            "--remove-effects",
            "-r",
            help="Remove ASS drawing/animation effects from subtitle text",
            show_default=True,
        ),
    ] = False,
    remove_duplicates: Annotated[
        bool,
        typer.Option(
            "--remove-duplicates",
            "-d",
            help="Merge consecutive duplicate subtitle lines",
            show_default=True,
        ),
    ] = False,
    only_default_style: Annotated[
        bool,
        typer.Option(
            "--only-default",
            "-D",
            help="Export only styles containing 'Default' in name (excludes Signs, Credits, etc.)",
            show_default=True,
        ),
    ] = False,
    include_styles: Annotated[
        Optional[str],
        typer.Option(
            "--include-styles",
            "-i",
            help="Comma-separated list of style names to include (e.g., 'Default,Signs')",
            show_default=False,
        ),
    ] = None,
    exclude_styles: Annotated[
        Optional[str],
        typer.Option(
            "--exclude-styles",
            "-x",
            help="Comma-separated list of style names to exclude (e.g., 'Signs,Credits_dvd')",
            show_default=False,
        ),
    ] = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--output-dir",
            "-o",
            help="Output directory for converted SRT file(s). Defaults to source file directory",
            file_okay=False,
            dir_okay=True,
            writable=True,
            show_default=False,
        ),
    ] = None,
    encoding: Annotated[
        str,
        typer.Option(
            "--encoding",
            "-e",
            help="Text encoding for output SRT file",
            show_default=True,
        ),
    ] = "utf8",
    output_dialogues: Annotated[
        bool,
        typer.Option(
            "--output-dialogues",
            "-p",
            help="Print converted dialogues to console instead of saving to file",
            show_default=True,
        ),
    ] = False,
):
    """
    Convert ASS/SSA subtitle file(s) to SRT format.

    [bold]Examples:[/bold]
        pyasstosrt export subtitle.ass
        pyasstosrt export subtitle.ass --remove-effects --remove-duplicates
        pyasstosrt export subtitle.ass --only-default -o output/
        pyasstosrt export *.ass --include-styles "Default,Alt"
    """
    # Validate mutually exclusive style options
    style_options_count = sum([only_default_style, bool(include_styles), bool(exclude_styles)])
    if style_options_count > 1:
        console.print(
            "[red]Error:[/red] Options [bold]--only-default[/bold], [bold]--include-styles[/bold], "
            "and [bold]--exclude-styles[/bold] are mutually exclusive. Please use only one.",
            style="bold red",
        )
        raise typer.Exit(1)

    # Parse style filters
    include_styles_list = [s.strip() for s in include_styles.split(",")] if include_styles else None
    exclude_styles_list = [s.strip() for s in exclude_styles.split(",")] if exclude_styles else None

    # Show conversion summary
    console.print(f"\n[bold cyan]🎬 Starting conversion of {len(filepath)} file(s)[/bold cyan]")
    if removing_effects:
        console.print("  • Removing ASS effects: [green]✓[/green]")
    if remove_duplicates:
        console.print("  • Removing duplicates: [green]✓[/green]")
    if only_default_style:
        console.print("  • Filter: [yellow]Only 'Default' styles[/yellow]")
    elif include_styles:
        console.print(f"  • Filter: [yellow]Include styles: {include_styles}[/yellow]")
    elif exclude_styles:
        console.print(f"  • Filter: [yellow]Exclude styles: {exclude_styles}[/yellow]")
    console.print()

    success_count = 0
    error_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Converting files...", total=len(filepath))

        for file in filepath:
            progress.console.print(f"[bold blue]📄 Processing:[/bold blue] {file.name}")

            try:
                sub = Subtitle(
                    file,
                    removing_effects,
                    remove_duplicates,
                    only_default_style,
                    include_styles_list,
                    exclude_styles_list,
                )
                result = sub.export(output_dir, encoding, output_dialogues)

                if output_dialogues and result:
                    progress.console.print(
                        Panel(
                            f"[bold]Dialogues for {file.name}:[/bold]\nTotal: {len(result)} dialogue(s)",
                            expand=False,
                            border_style="green",
                        )
                    )
                    for dialogue in result[:5]:  # Show first 5 as preview
                        progress.console.print(str(dialogue))
                    if len(result) > 5:
                        progress.console.print(f"... and {len(result) - 5} more dialogue(s)")

                output_file = Path(output_dir) / f"{file.stem}.srt" if output_dir else file.with_suffix(".srt")
                if not output_dialogues:
                    progress.console.print(f"[green]✓ Success:[/green] {file.name} → {output_file.name}")
                success_count += 1

            except FileNotFoundError:
                progress.console.print(f"[red]✗ Error:[/red] File not found: {file.name}", style="bold red")
                error_count += 1
            except PermissionError:
                progress.console.print(
                    f"[red]✗ Error:[/red] Permission denied when processing {file.name}", style="bold red"
                )
                error_count += 1
            except Exception as e:
                progress.console.print(f"[red]✗ Error:[/red] Failed to convert {file.name}: {str(e)}", style="bold red")
                error_count += 1

            progress.update(task, advance=1)

    # Show summary
    console.print()
    if error_count == 0:
        console.print(f"[bold green]✓ Conversion completed successfully![/bold green] ({success_count} file(s))")
    else:
        console.print(
            f"[bold yellow]⚠ Conversion completed with errors:[/bold yellow] "
            f"{success_count} successful, {error_count} failed"
        )
        if error_count > 0:
            raise typer.Exit(1)


@app.command(name="styles", help="List all unique styles found in an ASS subtitle file")
def styles(
    filepath: Annotated[
        Path,
        typer.Argument(
            help="Path to the ASS/SSA file to analyze",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            show_default=False,
        ),
    ],
    table_format: Annotated[
        bool,
        typer.Option(
            "--table",
            "-t",
            help="Display styles in a formatted table",
            show_default=True,
        ),
    ] = False,
):
    """
    List all unique styles found in an ASS/SSA subtitle file.

    This command helps you identify available styles before using
    --include-styles or --exclude-styles options in the export command.

    [bold]Examples:[/bold]
        pyasstosrt styles subtitle.ass
        pyasstosrt styles subtitle.ass --table
    """
    try:
        console.print(f"\n[bold cyan]🔍 Analyzing styles in:[/bold cyan] {filepath.name}\n")

        sub = Subtitle(filepath)
        style_list = sub.get_styles()

        if not style_list:
            console.print("[yellow]⚠ No styles found or file is in SRT format[/yellow]")
            console.print("[dim]Note: SRT files don't have style information[/dim]")
            return

        if table_format:
            # Display as a rich table
            table = Table(title=f"Styles in {filepath.name}", show_header=True, header_style="bold cyan")
            table.add_column("#", style="dim", width=6, justify="right")
            table.add_column("Style Name", style="green")

            for idx, style in enumerate(style_list, start=1):
                table.add_row(str(idx), style)

            console.print(table)
        else:
            # Display as a simple list
            console.print(f"[bold blue]Styles found in {filepath.name}:[/bold blue]\n")
            for idx, style in enumerate(style_list, start=1):
                # Highlight "Default" styles
                if "Default" in style:
                    console.print(f"  {idx}. [bold green]{style}[/bold green] [dim](default)[/dim]")
                else:
                    console.print(f"  {idx}. [green]{style}[/green]")

        console.print(f"\n[bold]Total:[/bold] [cyan]{len(style_list)}[/cyan] unique style(s)")

        # Show helpful tips
        console.print("\n[dim]💡 Tips:[/dim]")
        console.print("  [dim]• Use --include-styles to export specific styles[/dim]")
        console.print("  [dim]• Use --exclude-styles to skip unwanted styles[/dim]")
        console.print("  [dim]• Use --only-default to export only 'Default' styles[/dim]")

    except FileNotFoundError:
        console.print(f"[red]✗ Error:[/red] File not found: {filepath}", style="bold red")
        raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}", style="bold red")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
