# Land Plot Survey Tool

A Python tool for plotting land surveys with bearing and distance measurements.

## Features

- Processes survey data with bearings and distances
- Handles internal and external angles
- Applies magnetic declination corrections
- Calculates closure errors
- Generates detailed survey plots with matplotlib

## Usage

```bash
python land_plot.py
```

## Requirements

- Python 3.x
- matplotlib
- numpy

## Survey Data Format

The tool processes survey data with:
- Side lengths (in feet and inches)
- Bearings (in degrees and minutes)
- Internal/external angles
- Magnetic declination corrections

## Output

- Detailed step-by-step survey calculations
- Visual plot of the survey with labeled sides, angles, and bearings
- Closure error calculations
- Corrected bearings for true north

## Example

The current implementation processes Plot 7 with:
- 6 sides with various lengths
- Magnetic bearing corrections for Adelaide 1961
- Closure error analysis 