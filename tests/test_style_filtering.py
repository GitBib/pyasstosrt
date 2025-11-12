import pytest

from pyasstosrt import Subtitle


def test_include_single_style(sub_with_styles):
    dialogues = sub_with_styles.export(output_dialogues=True)
    total_dialogues = len(dialogues)

    # Test with include_styles - should only get Default style lines
    sub_filtered = Subtitle("tests/sub_with_styles.ass", include_styles=["Default"])
    filtered_dialogues = sub_filtered.export(output_dialogues=True)

    assert isinstance(filtered_dialogues, list)
    assert len(filtered_dialogues) < total_dialogues
    assert len(filtered_dialogues) == 12  # 12 Default style lines in test file


def test_include_multiple_styles():
    sub_filtered = Subtitle("tests/sub_with_styles.ass", include_styles=["Default", "Alt"])
    filtered_dialogues = sub_filtered.export(output_dialogues=True)

    assert isinstance(filtered_dialogues, list)
    assert len(filtered_dialogues) == 15  # 12 Default + 3 Alt lines


def test_exclude_single_style(sub_with_styles):
    dialogues = sub_with_styles.export(output_dialogues=True)
    total_dialogues = len(dialogues)

    # Exclude Signs style - should get all except 3 Signs lines
    sub_filtered = Subtitle("tests/sub_with_styles.ass", exclude_styles=["Signs"])
    filtered_dialogues = sub_filtered.export(output_dialogues=True)

    assert isinstance(filtered_dialogues, list)
    assert len(filtered_dialogues) == total_dialogues - 3  # 25 total - 3 Signs = 22


def test_exclude_multiple_styles():
    # Exclude Signs and Credits - should get 25 - 3 Signs - 1 Credits = 21
    sub_filtered = Subtitle("tests/sub_with_styles.ass", exclude_styles=["Signs", "Credits"])
    filtered_dialogues = sub_filtered.export(output_dialogues=True)

    assert isinstance(filtered_dialogues, list)
    assert len(filtered_dialogues) == 21


def test_style_filtering_with_export_file(output_dir):
    try:
        sub = Subtitle("tests/sub_with_styles.ass", include_styles=["Default"])
        sub.export(output_dir)
        output_file = output_dir / "sub_with_styles.srt"
        assert output_file.is_file()
    finally:
        if output_file.exists():
            output_file.unlink()


def test_style_filtering_with_removing_effects():
    sub = Subtitle("tests/sub_with_styles.ass", removing_effects=True, include_styles=["Default"])
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    assert len(dialogues) == 12


def test_style_filtering_with_remove_duplicates():
    sub = Subtitle("tests/sub_with_styles.ass", remove_duplicates=True, exclude_styles=["Signs"])
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    assert len(dialogues) == 22


def test_style_filtering_empty_include_list(sub_with_styles):
    dialogues_normal = sub_with_styles.export(output_dialogues=True)

    sub = Subtitle("tests/sub_with_styles.ass", include_styles=[])
    dialogues = sub.export(output_dialogues=True)

    # Empty include list is treated as None (no filtering)
    assert len(dialogues) == len(dialogues_normal)
    assert len(dialogues_normal) == 25


def test_style_filtering_empty_exclude_list(sub_with_styles):
    dialogues_normal = sub_with_styles.export(output_dialogues=True)

    sub_filtered = Subtitle("tests/sub_with_styles.ass", exclude_styles=[])
    dialogues_filtered = sub_filtered.export(output_dialogues=True)

    # Empty exclude list should not filter anything
    assert len(dialogues_filtered) == len(dialogues_normal)
    assert len(dialogues_filtered) == 25


@pytest.mark.parametrize(
    "include_styles, exclude_styles, expected_count",
    [
        (["Default"], None, 12),
        (None, ["Signs"], 22),
        (["Default", "Alt"], None, 15),
        (None, ["Signs", "Credits"], 21),
    ],
)
def test_style_filtering_combinations(include_styles, exclude_styles, expected_count):
    sub = Subtitle("tests/sub_with_styles.ass", include_styles=include_styles, exclude_styles=exclude_styles)
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    assert len(dialogues) == expected_count


def test_only_default_style_flag():
    # Test only_default_style flag keeps only styles with "Default" in name
    sub = Subtitle("tests/sub_with_styles.ass", only_default_style=True)
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    # Should keep only "Default" style (12 dialogues)
    assert len(dialogues) == 12


def test_only_default_style_with_explicit_include():
    # If include_styles is explicitly set, only_default_style should not override it
    sub = Subtitle("tests/sub_with_styles.ass", only_default_style=True, include_styles=["Default"])
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    assert len(dialogues) == 12


def test_only_default_style_with_removing_effects():
    sub = Subtitle("tests/sub_with_styles.ass", only_default_style=True, removing_effects=True)
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    assert len(dialogues) == 12


def test_only_default_style_with_remove_duplicates():
    sub = Subtitle("tests/sub_with_styles.ass", only_default_style=True, remove_duplicates=True)
    dialogues = sub.export(output_dialogues=True)

    assert isinstance(dialogues, list)
    assert len(dialogues) == 12


def test_get_styles(sub_with_styles):
    styles = sub_with_styles.get_styles()

    assert isinstance(styles, list)
    assert len(styles) == 6
    assert "Default" in styles
    assert "Alt" in styles
    assert "Thoughts" in styles
    assert "Top" in styles
    assert "Signs" in styles
    assert "Credits" in styles


def test_get_styles_sorted(sub_with_styles):
    styles = sub_with_styles.get_styles()

    # Styles should be returned in alphabetical order
    assert styles == sorted(styles)


def test_get_styles_srt_format(sub_srt):
    styles = sub_srt.get_styles()

    # SRT files don't have styles
    assert styles == []
