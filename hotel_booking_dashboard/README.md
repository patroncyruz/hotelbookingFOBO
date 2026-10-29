# B. Descriptive Analytics Dashboard

Hotel Booking Insights — Group 4.2

## Run

Use Python 3.12 or newer. Open a terminal inside this extracted folder:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).
Keep the terminal running while using the dashboard. This is a local application;
it does not need a paid account, database, or API key. The CSV must stay beside app.py.

To reproduce the packaged cleaned CSV from the original input, optionally run:

```powershell
python prepare_data.py "C:\path\to\hotel_bookings.csv"
```

## Audience and purpose

The intended users are hotel reservation and revenue managers. The dashboard supports
reviewing booking volume and prioritizing booking groups for cancellation monitoring
and confirmation follow-ups. It reports descriptive associations, not predictions.

## Required components

Five headline KPIs:
1. Total bookings: number of selected working records.
2. Canceled bookings: selected records where is_canceled equals 1.
3. Cancellation rate: canceled bookings / selected bookings × 100.
4. Median daily rate: median average_daily_rate, in source rate units.
5. Median lead time: median days between booking and arrival.

Six visuals, each with an updating conclusion and business implication:
1. Monthly bookings by cancellation outcome — when are recorded arrival volumes highest?
2. Cancellation rate by hotel — which property has the higher cancellation share?
3. Cancellation rate by market segment — which channels deserve closer review?
4. Cancellation rate by lead-time group — how does advance notice relate to cancellations?
5. Cancellation rate by family status — how do guest groups differ?
6. Daily-rate box plots by hotel and outcome — how do typical prices and spreads differ?

Interactive filters: hotel, market segment, and arrival date range. All KPIs, visuals,
insight notes, group tables, and downloadable records respect these filters. The reset
button restores the complete working dataset. Plotly also supports hover details,
legend toggles, zoom, and chart-image export.

## Design rationale

The overview KPIs appear first, followed by six numbered visual questions in a
two-column layout. Navy (#142E66) denotes non-canceled bookings and gold (#F2AD00) denotes canceled
bookings consistently. The navy sidebar, diagonal gold header accent, and white chart cards use the supplied palette. Bar charts show categorical comparisons and monthly volume;
box plots show price distributions. Rates use 0–100% axes, and hover details include
booking counts to show denominators. The sidebar keeps global filters separate from
the analytical content. Narrow screens use Streamlit's responsive layout.

## Data and interpretation

Input: the supplied hotel_bookings.csv. The packaged hotel_bookings_cleaned.csv
reproduces the existing notebook's cleaning and derived features: 119,390 source
rows → removal of 31,994 exact matches → 87,396 rows. Rename adr, convert the status
date, fill children with 0, country with Unknown, agent with 0, and drop company.
Add total_nights, total_guests, is_family, and four standardized columns (population
standard deviation, equivalent to StandardScaler). The resulting CSV has 38 columns.
The application derives arrival dates, lead-time bins, and readable labels in memory.
Calendar order is encoded in arrival dates and lead-time bin order; CSV cannot retain
pandas categorical metadata.

There is no unique reservation identifier; exact matching rows may represent distinct
reservations. Seven later identical rows remain, as in the notebook. Unknown values
are placeholders, not recovered facts. Zero-night, zero-guest, and negative-rate records
remain in the analysis. The rate box plot alone omits negative prices and values above
the selected 99th percentile for readability; KPIs retain all selected rows.

Coverage is July 2015–August 2017, with incomplete boundary years. Selected months
may also be partial. Counts do not represent occupancy or revenue. Undefined is
displayed but excluded from the named-channel risk ranking because its original group
has just two records. All small filtered groups require caution. Associations do not
establish causes or prove that a follow-up policy will reduce cancellations.

## Default expected results

87,396 bookings; 24,025 canceled; 27.49% cancellation rate; median daily rate 98.10;
median lead time 49 days. City Hotel: 30.04%; Resort Hotel: 23.48%.

## Demo sequence

Start with the five KPIs. Explain the monthly volume chart and hotel comparison.
Select City Hotel, then select Online TA to show all views updating. Change the date
range and hover over a bar to show its denominator. Reset the filters and explain
the lead-time, guest-group, and price comparisons. Use the definitions panel to
explain scope and limitations. The filtered CSV download supports follow-up review.

Prepared by Job Russel Enriquez and John Cyruz Patron, BSIT–401I, ITC C307.
