"""Unit tests for weather_station."""

import contextlib
import datetime
import io
import os
import sys
import tempfile
import unittest
from unittest import mock

import weather_station


class WeatherStationTest(unittest.TestCase):
    """Tests weather observation reading, analysis, and output."""

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def _write_input(self, contents):
        filename = os.path.join(
            self.temporary_directory.name, "observations.csv")
        with open(filename, "w", encoding="utf-8") as input_file:
            input_file.write(contents)
        return filename

    def test_reads_several_stations_and_sorts_by_date(self):
        filename = self._write_input(
            "Miami,09:30:00 AM 04/21/2026,82.0\n"
            "Orlando,08:00:00 AM 04/20/2026,75.0\n"
            "Miami,09:30:00 AM 04/20/2026,80.0\n")

        observations, errors = weather_station.read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {"Miami", "Orlando"})
        self.assertEqual(
            observations["Miami"],
            [
                (datetime.datetime(2026, 4, 20, 9, 30), 80.0),
                (datetime.datetime(2026, 4, 21, 9, 30), 82.0),
            ],
        )

    def test_accepts_negative_and_boundary_temperatures(self):
        filename = self._write_input(
            "North,01:00:00 AM 01/01/2026,-100.0\n"
            "South,01:00:00 AM 01/01/2026,150.0\n")

        observations, errors = weather_station.read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(observations["North"][0][1], -100.0)
        self.assertEqual(observations["South"][0][1], 150.0)

    def test_rejects_duplicate_observations(self):
        filename = self._write_input(
            "Miami,09:28:09 AM 04/20/2026,81.0\n"
            "Miami,09:28:09 AM 04/20/2026,82.0\n")

        observations, errors = weather_station.read_observations(filename)

        self.assertEqual(len(observations["Miami"]), 1)
        self.assertEqual(errors, [(2, "Duplicate station/date observation.")])

    def test_rejects_invalid_ranges_and_malformed_lines(self):
        filename = self._write_input(
            "Cold,12:00:00 PM 01/01/2026,-100.1\n"
            "Hot,12:00:00 PM 01/01/2026,150.1\n"
            "Missing fields\n"
            "BadDate,today,70.0\n"
            "NotNumber,12:00:00 PM 01/01/2026,warm\n")

        observations, errors = weather_station.read_observations(filename)

        self.assertEqual(observations, {})
        self.assertEqual(
            [line_number for line_number, _ in errors], [1, 2, 3, 4, 5])

    def test_calculates_station_statistics(self):
        date = datetime.datetime(2026, 4, 20)
        observations = {
            "Miami": [(date, 70.0), (date + datetime.timedelta(days=1), 80.0)],
            "Orlando": [(date, -5.0), (date + datetime.timedelta(days=1), 5.0)],
        }

        statistics = weather_station.station_statistics(observations)

        self.assertEqual(statistics["Miami"], (70.0, 80.0, 75.0))
        self.assertEqual(statistics["Orlando"], (-5.0, 5.0, 0.0))

    def test_finds_only_latest_temperature_outliers(self):
        first = datetime.datetime(2026, 4, 20)
        latest = datetime.datetime(2026, 4, 21)
        observations = {
            "Rising": [(first, 60.0), (latest, 80.0)],
            "Falling": [(first, 80.0), (latest, 60.0)],
        }

        outliers = weather_station.station_outliers(observations)

        self.assertEqual(outliers, {"Rising": (latest, 80.0, 70.0)})

    def test_writes_sorted_output_with_one_decimal_place(self):
        filename = os.path.join(self.temporary_directory.name, "statistics.csv")
        statistics = {
            "Zulu": (-2.0, 4.0, 2.0 / 3.0),
            "Alpha": (70.0, 80.0, 75.25),
        }

        weather_station.write_statistics(filename, statistics)

        with open(filename, encoding="utf-8") as output_file:
            self.assertEqual(
                output_file.read(),
                "Alpha,70.0,80.0,75.2\nZulu,-2.0,4.0,0.7\n",
            )

    def test_missing_input_file_raises_file_not_found(self):
        missing_filename = os.path.join(
            self.temporary_directory.name, "missing.csv")

        with self.assertRaises(FileNotFoundError):
            weather_station.read_observations(missing_filename)

    def test_main_handles_missing_file_gracefully(self):
        missing_filename = os.path.join(
            self.temporary_directory.name, "missing.csv")
        output_filename = os.path.join(
            self.temporary_directory.name, "output.csv")
        error_output = io.StringIO()

        with mock.patch.object(
            sys,
            "argv",
            ["weather_station.py", missing_filename, output_filename],
        ), contextlib.redirect_stderr(error_output):
            exit_code = weather_station.main()

        self.assertEqual(exit_code, 1)
        self.assertIn("File error:", error_output.getvalue())
        self.assertFalse(os.path.exists(output_filename))


if __name__ == "__main__":
    unittest.main()
