"""Analyze daily temperature observations grouped by weather station."""

import datetime
import math
import sys


_DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
_MINIMUM_TEMPERATURE = -100.0
_MAXIMUM_TEMPERATURE = 150.0


def read_observations(filename):
    """Reads and validates weather observations from filename.

    Args:
        filename: The name of a comma-separated observations file. Each line
            must contain a station, date, and temperature.

    Returns:
        A tuple containing an observations dictionary and an error list. Each
        station maps to a chronologically sorted list of (date, temperature)
        tuples. Dates are datetime.datetime objects. Each error is a
        (line_number, error_message) tuple.

    Raises:
        OSError: If filename cannot be opened or read.
    """
    observations = {}
    errors = []
    station_dates = set()

    with open(filename, encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            fields = [field.strip() for field in line.strip().split(",")]
            if len(fields) != 3:
                errors.append(
                    (line_number, "Expected station,date,temperature."))
                continue

            station, date_text, temperature_text = fields
            if not station:
                errors.append((line_number, "Station name is missing."))
                continue

            try:
                date = datetime.datetime.strptime(date_text, _DATE_FORMAT)
            except ValueError:
                errors.append((line_number, "Invalid date."))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "Invalid temperature."))
                continue

            if not math.isfinite(temperature) or not (
                _MINIMUM_TEMPERATURE
                <= temperature
                <= _MAXIMUM_TEMPERATURE
            ):
                errors.append(
                    (
                        line_number,
                        "Temperature must be between -100.0 and 150.0.",
                    )
                )
                continue

            station_date = (station, date)
            if station_date in station_dates:
                errors.append(
                    (line_number, "Duplicate station/date observation."))
                continue

            station_dates.add(station_date)
            observations.setdefault(station, []).append((date, temperature))

    for station_observations in observations.values():
        station_observations.sort(key=lambda observation: observation[0])

    return observations, errors


def station_statistics(observations):
    """Calculates minimum, maximum, and mean temperatures by station."""
    statistics = {}
    for station, station_observations in observations.items():
        if not station_observations:
            continue
        temperatures = [temperature for _, temperature in station_observations]
        statistics[station] = (
            min(temperatures),
            max(temperatures),
            sum(temperatures) / len(temperatures),
        )
    return statistics


def station_outliers(observations):
    """Returns stations whose latest temperature exceeds their mean."""
    statistics = station_statistics(observations)
    return {
        station: (
            station_observations[-1][0],
            station_observations[-1][1],
            statistics[station][2],
        )
        for station, station_observations in observations.items()
        if station_observations
        and station_observations[-1][1] > statistics[station][2]
    }


def write_statistics(filename, statistics):
    """Writes station statistics in lexicographic station order."""
    with open(filename, "w", encoding="utf-8", newline="") as output_file:
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            output_file.write(
                f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n")


def _print_statistics(statistics):
    """Prints station statistics in a consistent, readable format."""
    print("Statistics:")
    for station in sorted(statistics):
        minimum, maximum, mean = statistics[station]
        print(
            f"{station}: minimum={minimum:.1f}, maximum={maximum:.1f}, "
            f"mean={mean:.1f}")


def _print_outliers(outliers):
    """Prints station outliers in a consistent, readable format."""
    print("Outliers:")
    for station in sorted(outliers):
        date, temperature, mean = outliers[station]
        print(
            f"{station}: date={date.strftime(_DATE_FORMAT)}, "
            f"temperature={temperature:.1f}, mean={mean:.1f}")


def main():
    """Reads command-line filenames, reports results, and writes statistics."""
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} OBSERVATIONS_FILE STATISTICS_FILE",
            file=sys.stderr,
        )
        return 2

    input_filename, output_filename = sys.argv[1:]
    try:
        observations, errors = read_observations(input_filename)
        statistics = station_statistics(observations)
        outliers = station_outliers(observations)
        _print_statistics(statistics)
        _print_outliers(outliers)
        if errors:
            print("Errors:", file=sys.stderr)
            for line_number, message in errors:
                print(f"Line {line_number}: {message}", file=sys.stderr)
        write_statistics(output_filename, statistics)
    except OSError as error:
        print(f"File error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
