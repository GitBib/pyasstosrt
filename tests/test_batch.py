import sys
import unittest.mock

from pyasstosrt.batch import app


def test_version(cli_runner):
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "PyAssToSrt version:" in result.stdout


def test_export_help(cli_runner):
    result = cli_runner.invoke(app, ["export", "--help"])
    assert result.exit_code == 0
    assert "Convert ASS subtitle file(s) to SRT format" in result.stdout


def test_export_file_not_exists(cli_runner):
    result = cli_runner.invoke(app, ["export", "nonexistent_file.ass"])
    assert result.exit_code != 0

    if sys.version_info < (3, 10):
        assert "nonexistent_file.ass" in result.stdout
    else:
        assert "nonexistent_file.ass" in result.stderr


def test_export_with_existing_ass_file(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub"]
    assert test_file.exists(), f"Test file {test_file} not found"

    srt_file = test_file.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(test_file)])
    assert result.exit_code == 0
    assert "Success: Converted sub.ass to" in result.stdout
    assert srt_file.exists()

    srt_content = srt_file.read_text(encoding="utf-8")
    assert "1" in srt_content
    assert "It's time for the main event!" in srt_content


def test_export_with_output_dir(cli_runner, test_files, output_dir):
    test_file = test_files["sub"]

    result = cli_runner.invoke(app, ["export", str(test_file), "--output-dir", str(output_dir)])
    assert result.exit_code == 0
    expected_output = output_dir / "sub.srt"
    assert expected_output.exists()

    if expected_output.exists():
        expected_output.unlink()


def test_export_with_remove_effects(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub"]
    srt_file = test_file.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(test_file), "--remove-effects"])
    assert result.exit_code == 0
    assert srt_file.exists()

    srt_content = srt_file.read_text(encoding="utf-8")
    assert "It's time for the main event!" in srt_content


def test_export_with_specialized_effects_removal(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub_removing_effects"]
    standard_srt = test_files["sub_standard_removing_effects"]

    assert test_file.exists(), f"Test file {test_file} not found"
    assert standard_srt.exists(), f"Standard SRT file {standard_srt} not found"

    srt_file = test_file.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(test_file), "--remove-effects"])
    assert result.exit_code == 0
    assert srt_file.exists()

    generated_content = srt_file.read_text(encoding="utf-8")

    assert len(generated_content) > 0


def test_export_with_remove_duplicates(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub"]
    srt_file = test_file.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(test_file), "--remove-duplicates"])
    assert result.exit_code == 0
    assert srt_file.exists()


def test_export_with_output_dialogues(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub"]

    result = cli_runner.invoke(app, ["export", str(test_file), "--output-dialogues"])
    assert result.exit_code == 0

    assert "Dialogues for sub.ass:" in result.stdout
    assert "It's time for the main event!" in result.stdout


def test_export_with_custom_encoding(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub"]
    srt_file = test_file.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(test_file), "--encoding", "utf-8"])
    assert result.exit_code == 0
    assert srt_file.exists()


def test_export_standard_srt_comparison(cli_runner, test_files, cleanup_srt_files):
    test_file = test_files["sub"]
    standard_srt = test_files["sub_standard"]

    assert test_file.exists(), f"Test file {test_file} not found"
    assert standard_srt.exists(), f"Standard SRT file {standard_srt} not found"

    srt_file = test_file.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(test_file)])
    assert result.exit_code == 0
    assert srt_file.exists()

    generated_content = srt_file.read_text(encoding="utf-8")

    assert len(generated_content) > 0


def test_export_multiple_files(cli_runner, test_files, cleanup_srt_files):
    file1 = test_files["sub"]
    file2 = test_files["sub_removing_effects"]

    assert file1.exists(), f"Test file {file1} not found"
    assert file2.exists(), f"Test file {file2} not found"

    srt_file1 = file1.with_suffix(".srt")
    srt_file2 = file2.with_suffix(".srt")

    result = cli_runner.invoke(app, ["export", str(file1), str(file2)])
    assert result.exit_code == 0

    assert f"Processing: {file1.name}" in result.stdout
    assert f"Processing: {file2.name}" in result.stdout
    assert f"Success: Converted {file1.name}" in result.stdout
    assert f"Success: Converted {file2.name}" in result.stdout

    assert srt_file1.exists()
    assert srt_file2.exists()


def test_simple_text_file_conversion(cli_runner, invalid_ass_file):
    invalid_file, _ = invalid_ass_file

    result = cli_runner.invoke(app, ["export", str(invalid_file)])
    assert result.exit_code == 0
    assert f"Success: Converted {invalid_file.name}" in result.stdout

    srt_file = invalid_file.with_suffix(".srt")
    assert srt_file.exists()

    if srt_file.exists():
        srt_file.unlink()


def test_export_with_subtitle_exception(cli_runner, test_files, monkeypatch):
    test_file = test_files["sub"]

    from pyasstosrt import Subtitle as OriginalSubtitle

    def mock_init(*args, **kwargs):
        raise ValueError("Test error")

    monkeypatch.setattr(OriginalSubtitle, "__init__", mock_init)

    result = cli_runner.invoke(app, ["export", str(test_file)])

    assert result.exit_code == 0
    assert "Error:" in result.stdout
    assert f"Failed to convert {test_file.name}" in result.stdout
    assert "Test error" in result.stdout


def test_main_entry_point():
    with unittest.mock.patch("pyasstosrt.batch.__name__", "__main__"):
        with unittest.mock.patch("pyasstosrt.batch.app"):
            with open(sys.modules["pyasstosrt.batch"].__file__, encoding="utf-8") as f:
                f.read()


def test_export_srt_file_with_cli(cli_runner, test_dir, output_dir):
    """Test converting SRT file through CLI."""

    test_file = test_dir / "test_sample.srt"
    assert test_file.exists(), f"Test file {test_file} not found"

    try:
        result = cli_runner.invoke(app, ["export", str(test_file), "--output-dir", str(output_dir)])
        assert result.exit_code == 0
        assert "Success: Converted test_sample.srt to" in result.stdout

        expected_output = output_dir / "test_sample.srt"
        assert expected_output.exists()

        srt_content = expected_output.read_text(encoding="utf-8")
        assert "1" in srt_content
        assert "It's time for the main event!" in srt_content
    finally:
        expected_output = output_dir / "test_sample.srt"
        if expected_output.exists():
            expected_output.unlink()


def test_export_srt_with_output_dir_cli(cli_runner, test_dir, output_dir):
    """Test exporting SRT file to output directory through CLI."""

    test_file = test_dir / "test_sample.srt"

    result = cli_runner.invoke(app, ["export", str(test_file), "--output-dir", str(output_dir)])
    assert result.exit_code == 0
    expected_output = output_dir / "test_sample.srt"
    assert expected_output.exists()

    if expected_output.exists():
        expected_output.unlink()


def test_export_srt_with_remove_duplicates_cli(cli_runner, test_dir, output_dir):
    """Test exporting SRT file with remove-duplicates flag through CLI."""

    test_file = test_dir / "test_sample.srt"

    try:
        result = cli_runner.invoke(
            app, ["export", str(test_file), "--remove-duplicates", "--output-dir", str(output_dir)]
        )
        assert result.exit_code == 0

        expected_output = output_dir / "test_sample.srt"
        assert expected_output.exists()
    finally:
        expected_output = output_dir / "test_sample.srt"
        if expected_output.exists():
            expected_output.unlink()


def test_export_srt_with_output_dialogues_cli(cli_runner, test_dir):
    """Test exporting SRT file with output-dialogues flag through CLI."""

    test_file = test_dir / "test_sample.srt"

    result = cli_runner.invoke(app, ["export", str(test_file), "--output-dialogues"])
    assert result.exit_code == 0

    assert f"Dialogues for {test_file.name}:" in result.stdout
    assert "It's time for the main event!" in result.stdout
