"""Data preparation and summaries shared by the Streamlit dashboard."""
from pathlib import Path
import pandas as pd

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
LEAD_LABELS = ['0–7 days', '8–30 days', '31–90 days', '91–180 days',
               '181–365 days', 'Over 365 days']

def load_data(path):
    df = pd.read_csv(Path(path))
    df['arrival_date'] = pd.to_datetime(dict(
        year=df['arrival_date_year'],
        month=df['arrival_date_month'].map({m: i + 1 for i, m in enumerate(MONTHS)}),
        day=df['arrival_date_day_of_month']))
    df['lead_time_group'] = pd.cut(df['lead_time'],
        [-1, 7, 30, 90, 180, 365, float('inf')], labels=LEAD_LABELS)
    df['guest_group'] = df['is_family'].map({0: 'Non-family', 1: 'Family'})
    df['booking_status'] = df['is_canceled'].map({0: 'Not canceled', 1: 'Canceled'})
    return df

def select_records(df, hotels, segments, start, end):
    return df.loc[df['hotel'].isin(hotels) & df['market_segment'].isin(segments)
        & df['arrival_date'].between(pd.Timestamp(start), pd.Timestamp(end))].copy()

def rates(df, column):
    result = df.groupby(column, observed=True)['is_canceled'].agg(
        Bookings='size', Cancellations='sum').reset_index()
    result['Cancellation rate (%)'] = result['Cancellations'] / result['Bookings'] * 100
    return result

def headline(df):
    return dict(bookings=len(df), canceled=int(df['is_canceled'].sum()),
        cancellation_rate=df['is_canceled'].mean() * 100,
        median_rate=df['average_daily_rate'].median(),
        median_lead=df['lead_time'].median())
