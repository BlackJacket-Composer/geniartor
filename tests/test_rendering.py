"""
Test `geniartor.rendering` package.

Author: Nikolay Lysenko
"""


from typing import Dict, List

import pretty_midi
import pytest

from geniartor.piece import Piece, PieceElement, ScaleElement, Sonority
from geniartor.rendering import (
    create_events_from_piece,
    create_lilypond_file_from_piece,
    create_midi_from_piece,
    create_wav_from_events,
)


@pytest.mark.parametrize(
    "piece, measure_in_seconds, volume, row_number, expected",
    [
        (
            # `piece`
            Piece(
                n_measures=2,
                pitches=[
                    ScaleElement('C4', 39, 23, 1),
                    ScaleElement('D4', 41, 24, 2),
                    ScaleElement('E4', 43, 25, 3),
                    ScaleElement('F4', 44, 26, 4),
                    ScaleElement('G4', 46, 27, 5),
                    ScaleElement('A4', 48, 28, 6),
                    ScaleElement('B4', 50, 29, 7),
                    ScaleElement('C5', 51, 30, 1),
                ],
                melodic_lines=[
                    [
                        PieceElement('C4', 39, 23, 1, 0.0, 0.5),
                        PieceElement('D4', 41, 24, 2, 0.5, 0.5),
                        PieceElement('E4', 43, 25, 3, 1.0, 0.5),
                        PieceElement('F4', 44, 26, 4, 1.5, 0.5),
                    ],
                    [
                        PieceElement('G4', 46, 27, 5, 0.0, 1.0),
                        PieceElement('C5', 51, 30, 1, 1.0, 1.0),
                    ],
                ],
                sonorities=[
                    Sonority(0.0, 'beginning', [0, 0]),
                    Sonority(0.5, 'middle', [1, 0]),
                    Sonority(1.0, 'downbeat', [2, 1]),
                    Sonority(1.5, 'ending', [-1, -1]),
                ]
            ),
            # `measure_in_seconds`
            2,
            # `volume`
            0.2,
            # `row_number`
            5,
            # `expected`
            'default_timbre\t3.0\t2.0\tC5\t0.2\t0\t\n'
        ),
    ]
)
def test_create_events_from_piece(
        path_to_tmp_file: str, piece: Piece,
        measure_in_seconds: int, volume: float, row_number: int, expected: str
) -> None:
    """Test `create_events_from_piece` function."""
    create_events_from_piece(
        piece,
        path_to_tmp_file,
        measure_in_seconds=measure_in_seconds,
        timbre='default_timbre',
        volume=volume,
        opening_silence_in_seconds=1,
        trailing_silence_in_seconds=1
    )
    with open(path_to_tmp_file) as in_file:
        for i in range(row_number):
            in_file.readline()
        result = in_file.readline()
        assert result == expected


@pytest.mark.parametrize(
    "piece, row_number, expected",
    [
        (
            # `piece`
            Piece(
                n_measures=2,
                pitches=[
                    ScaleElement('C4', 39, 23, 1),
                    ScaleElement('D4', 41, 24, 2),
                    ScaleElement('E4', 43, 25, 3),
                    ScaleElement('F4', 44, 26, 4),
                    ScaleElement('G4', 46, 27, 5),
                    ScaleElement('A4', 48, 28, 6),
                    ScaleElement('B4', 50, 29, 7),
                    ScaleElement('C5', 51, 30, 1),
                ],
                melodic_lines=[
                    [
                        PieceElement('C4', 39, 23, 1, 0.0, 0.5),
                        PieceElement('D4', 41, 24, 2, 0.5, 0.5),
                        PieceElement('E4', 43, 25, 3, 1.0, 0.5),
                        PieceElement('F4', 44, 26, 4, 1.5, 0.5),
                    ],
                    [
                        PieceElement('G4', 46, 27, 5, 0.0, 1.0),
                        PieceElement('C5', 51, 30, 1, 1.0, 1.0),
                    ],
                ],
                sonorities=[
                    Sonority(0.0, 'beginning', [0, 0]),
                    Sonority(0.5, 'middle', [1, 0]),
                    Sonority(1.0, 'downbeat', [2, 1]),
                    Sonority(1.5, 'ending', [-1, -1]),
                ]
            ),
            # `row_number`
            9,
            # `expected`
            "            { \\voiceOne g'1 c''1}\n"
        ),
        (
            # `piece`
            Piece(
                n_measures=2,
                pitches=[
                    ScaleElement('C4', 39, 23, 1),
                    ScaleElement('D4', 41, 24, 2),
                    ScaleElement('E4', 43, 25, 3),
                    ScaleElement('F4', 44, 26, 4),
                    ScaleElement('G4', 46, 27, 5),
                    ScaleElement('A4', 48, 28, 6),
                    ScaleElement('B4', 50, 29, 7),
                    ScaleElement('C5', 51, 30, 1),
                ],
                melodic_lines=[
                    [
                        PieceElement('C4', 39, 23, 1, 0.0, 0.5),
                        PieceElement('D4', 41, 24, 2, 0.5, 1.0),
                        PieceElement('E4', 43, 25, 3, 1.5, 0.25),
                        PieceElement('F4', 44, 26, 4, 1.75, 0.25),
                    ],
                    [
                        PieceElement('G4', 46, 27, 5, 0.0, 1.0),
                        PieceElement('C5', 51, 30, 1, 1.0, 1.0),
                    ],
                ],
                sonorities=[
                    Sonority(0.0, 'beginning', [0, 0]),
                    Sonority(0.5, 'middle', [1, 0]),
                    Sonority(1.0, 'downbeat', [2, 1]),
                    Sonority(1.5, 'ending', [-1, -1]),
                ]
            ),
            # `row_number`
            15,
            # `expected`
            "            { \\voiceTwo c'2 d'2~ d'2 e'4 f'4}\n"
        ),
    ]
)
def test_create_lilypond_file_from_piece(
        path_to_tmp_file: str, piece: Piece, row_number: int, expected: str
) -> None:
    """Test `create_lilypond_file_from_piece` function."""
    create_lilypond_file_from_piece(piece, path_to_tmp_file)
    with open(path_to_tmp_file) as in_file:
        for i in range(row_number):
            in_file.readline()
        result = in_file.readline()
        assert result == expected


@pytest.mark.parametrize(
    "piece, note_number, expected",
    [
        (
            # `piece`
            Piece(
                n_measures=2,
                pitches=[
                    ScaleElement('C4', 39, 23, 1),
                    ScaleElement('D4', 41, 24, 2),
                    ScaleElement('E4', 43, 25, 3),
                    ScaleElement('F4', 44, 26, 4),
                    ScaleElement('G4', 46, 27, 5),
                    ScaleElement('A4', 48, 28, 6),
                    ScaleElement('B4', 50, 29, 7),
                    ScaleElement('C5', 51, 30, 1),
                ],
                melodic_lines=[
                    [
                        PieceElement('C4', 39, 23, 1, 0.0, 0.5),
                        PieceElement('D4', 41, 24, 2, 0.5, 0.5),
                        PieceElement('E4', 43, 25, 3, 1.0, 0.5),
                        PieceElement('F4', 44, 26, 4, 1.5, 0.5),
                    ],
                    [
                        PieceElement('G4', 46, 27, 5, 0.0, 1.0),
                        PieceElement('C5', 51, 30, 1, 1.0, 1.0),
                    ],
                ],
                sonorities=[
                    Sonority(0.0, 'beginning', [0, 0]),
                    Sonority(0.5, 'middle', [1, 0]),
                    Sonority(1.0, 'downbeat', [2, 1]),
                    Sonority(1.5, 'ending', [-1, -1]),
                ]
            ),
            # `note_number`
            3,
            # `expected`
            {'pitch': 64, 'start': 2.0, 'end': 2.5}
        ),
    ]
)
def test_create_midi_from_piece(
        path_to_tmp_file: str, piece: Piece, note_number: int,
        expected: Dict[str, float]
) -> None:
    """Test `create_midi_from_piece` function."""
    create_midi_from_piece(
        piece,
        path_to_tmp_file,
        measure_in_seconds=1,
        instrument=0,
        velocity=100,
        opening_silence_in_seconds=1,
        trailing_silence_in_seconds=1
    )
    midi_data = pretty_midi.PrettyMIDI(path_to_tmp_file)
    instrument = midi_data.instruments[0]
    midi_note = instrument.notes[note_number]
    result = {
        'pitch': midi_note.pitch,
        'start': midi_note.start,
        'end': midi_note.end
    }
    assert result == expected


@pytest.mark.parametrize(
    "tsv_content",
    [
        (
            [
                "timbre\tstart_time\tduration\tfrequency\tvolume\tlocation\teffects",
                "default_timbre\t1\t1\tA0\t1\t0\t",
                'default_timbre\t2\t1\t1\t1\t0\t[{"name": "tremolo", "frequency": 1}]'
            ]
        )
    ]
)
def test_create_wav_from_events(
        path_to_tmp_file: str, path_to_another_tmp_file: str,
        tsv_content: List[str]
) -> None:
    """Test `create_wav_from_events` function."""
    with open(path_to_tmp_file, 'w') as tmp_tsv_file:
        for line in tsv_content:
            tmp_tsv_file.write(line + '\n')
    create_wav_from_events(path_to_tmp_file, path_to_another_tmp_file)
