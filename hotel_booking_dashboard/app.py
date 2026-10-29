from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from analytics import load_data, select_records, rates, headline

st.set_page_config(page_title='Hotel Booking Insights | Group 4.2', page_icon='🏨', layout='wide')
st.markdown('''<style>
.stApp {background:#f3f5fa;color:#142e66}
.block-container {padding-top:4rem;padding-bottom:3rem;max-width:1600px}
[data-testid="stHeader"] {background:rgba(243,245,250,.95)}
h1,h2,h3 {color:#142e66;letter-spacing:-.025em}
h3 {font-size:1.18rem!important;line-height:1.4!important}
.hero {position:relative;overflow:hidden;background:linear-gradient(130deg,#142e66 0%,#142e66 79%,#f2ad00 79%,#f2ad00 100%);border-radius:20px;padding:32px 36px;margin-bottom:22px;box-shadow:0 10px 28px #142e6614}
.hero .eyebrow {color:#f2ad00;font-size:11px;font-weight:800;letter-spacing:.18em;margin-bottom:14px}
.hero h1 {color:white;font-size:2.45rem;line-height:1.15;max-width:76%;margin:0 0 14px;padding:0;letter-spacing:-.04em}
.hero p {color:#dae3f7;font-size:14px;line-height:1.6;max-width:72%;margin:0}
.section-label {font-size:11px;letter-spacing:.16em;font-weight:800;color:#697a9a;margin:10px 0 6px}
[data-testid="stMetric"] {background:white;border:1px solid #e0e5f0;border-top:4px solid #f2ad00;border-radius:14px;padding:18px 16px;box-shadow:0 4px 14px #142e6607}
[data-testid="stMetricLabel"] {color:#62718c;font-size:12px}
[data-testid="stMetricValue"] {color:#142e66;font-size:1.85rem;font-weight:750;letter-spacing:-.04em}
[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {margin-bottom:22px}
[data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {background:#fff;border-radius:16px;border-color:#dfe5f0!important;box-shadow:0 5px 18px #142e6605}
[data-testid="stAlert"] {background:#fff8df;border:0;border-left:3px solid #f2ad00;border-radius:0 10px 10px 0}
[data-testid="stAlert"] p {color:#344464;font-size:13px;line-height:1.6}
[data-testid="stAlert"] svg {color:#a36d00}
[data-testid="stCaptionContainer"] {color:#71809b}
[data-testid="stSidebar"] {background:#142e66;border-right:0}
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {color:white}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#e3eafa}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {color:#b9c8e7;font-size:12px;line-height:1.6}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#b9c8e7!important}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] span[title] {color:#142e66!important;font-weight:600}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {color:#e3eafa;font-size:12px;font-weight:600}
[data-testid="stSidebar"] hr {border-color:#ffffff23}
.sidebar-brand {display:flex;gap:12px;align-items:center;margin:8px 0 22px}
.brand-icon {background:#f2ad00;color:#142e66;border-radius:10px;font-weight:900;font-size:20px;padding:9px 13px}
.brand-name {font-size:21px;font-weight:800;line-height:1.15;color:white;letter-spacing:-.02em}
.brand-name span {display:block;font-size:10px;letter-spacing:.2em;color:#f2ad00;margin-top:7px}
[data-testid="stSidebar"] [data-testid="stButton"] button {background:#f2ad00;color:#142e66;border:0;font-weight:700;border-radius:9px}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {background:#ffd15c;color:#142e66}
[data-testid="stSidebar"] [data-testid="stButton"] button p {color:#142e66!important}
[data-testid="stExpander"] {background:white;border-radius:12px;border:1px solid #e0e5f0}
@media (max-width:900px) {
 [data-testid="stHorizontalBlock"] {flex-wrap:wrap}
 [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {flex:1 1 100%;min-width:0}
 [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"] {flex:1 1 160px;min-width:160px}
 .hero {padding:26px 24px;background:linear-gradient(130deg,#142e66 0%,#142e66 90%,#f2ad00 90%)}
 .hero h1 {font-size:2rem;max-width:90%}
 .hero p {max-width:88%;font-size:13px}
}
</style>''', unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data(Path(__file__).parent / 'hotel_bookings_cleaned.csv')

df = get_data()
with st.sidebar:
    st.markdown('<div class="sidebar-brand"><div class="brand-icon">H</div><div class="brand-name">Hotel Insights<span>BOOKING INTELLIGENCE</span></div></div>', unsafe_allow_html=True)
    st.caption('GROUP 4.2 · FOUNDATIONS OF BUSINESS ANALYTICS')
    st.divider()
    st.markdown('**Explore your bookings**')
    hotels = st.multiselect('Hotel', sorted(df.hotel.unique()), default=sorted(df.hotel.unique()), key='hotels')
    segments = st.multiselect('Market segment', sorted(df.market_segment.unique()),
                             default=sorted(df.market_segment.unique()), key='segments')
    period = st.date_input('Arrival date range',
        value=(df.arrival_date.min().date(), df.arrival_date.max().date()),
        min_value=df.arrival_date.min().date(), max_value=df.arrival_date.max().date(), key='period')
    if st.button('Reset filters', width='stretch'):
        for key in ['hotels', 'segments', 'period']:
            del st.session_state[key]
        st.rerun()
    st.divider()
    st.markdown('**Who this is for**')
    st.caption('Reservation and revenue managers reviewing booking volume and deciding which booking groups need closer cancellation monitoring.')

st.markdown('''<div class="hero"><div class="eyebrow">GROUP 4.2 / HOTEL BOOKING DEMAND</div><h1>A clearer view of<br>every booking.</h1><p>Understand demand, explore cancellation patterns, and focus your next reservation decision.</p></div>''', unsafe_allow_html=True)

if not isinstance(period, (tuple, list)) or len(period) != 2:
    st.info('Choose both a start and an end date to update the dashboard.')
    st.stop()
view = select_records(df, hotels, segments, *period)
st.caption(f'ARRIVAL PERIOD  {period[0]:%d %b %Y} – {period[1]:%d %b %Y}   ·   '
           f'{len(view):,} of {len(df):,} working records   ·   All visuals use the filters at left')
if view.empty:
    st.warning('No bookings match these filters. Select another hotel, segment, or date range, or reset the filters.')
    st.stop()

st.markdown('<div class="section-label">BOOKING PERFORMANCE</div>', unsafe_allow_html=True)
k = headline(view)
columns = st.columns(5)
for col, label, value, help_text in zip(columns,
    ['Total bookings', 'Canceled bookings', 'Cancellation rate', 'Median daily rate', 'Median lead time'],
    [f"{k['bookings']:,}", f"{k['canceled']:,}", f"{k['cancellation_rate']:.2f}%",
     f"{k['median_rate']:,.2f}", f"{k['median_lead']:,.0f} days"],
    ['Count of filtered records after the documented exact-match removal.',
     'Count where is_canceled = 1, using the source outcome label.',
     'Canceled bookings divided by all filtered bookings.',
     'Median recorded average_daily_rate; source rate units. This is not revenue.',
     'Median days between booking and arrival.']):
    col.metric(label, value, help=help_text)

COLORS = {'Not canceled': '#142e66', 'Canceled': '#f2ad00'}
def plot(fig):
    fig.update_layout(template='plotly_white', height=340,
        font=dict(family='Arial', color='#536482', size=12),
        margin=dict(l=10, r=15, t=25, b=15), paper_bgcolor='white', plot_bgcolor='white',
        legend_title_text='', legend=dict(orientation='h', y=1.15, x=0),
        hoverlabel=dict(bgcolor='#142e66', font_color='white', bordercolor='#142e66'),
        bargap=.28)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor='#eef1f7', zeroline=False)
    fig.update_traces(marker_line_width=0, selector=dict(type='bar'))
    st.plotly_chart(fig, width='stretch', config={'displaylogo': False})

left, right = st.columns(2, gap='large')
with left, st.container(border=True):
    st.subheader('01 · How does booking volume change?')
    trend = view.assign(month=view.arrival_date.dt.to_period('M').dt.to_timestamp()).groupby(
        ['month', 'booking_status'], observed=True).size().reset_index(name='Bookings')
    plot(px.bar(trend, x='month', y='Bookings', color='booking_status',
        color_discrete_map=COLORS, labels={'month': 'Arrival month'}, barmode='stack'))
    monthly = trend.groupby('month').Bookings.sum()
    peak = monthly.idxmax()
    st.info(f'{peak:%B %Y} has the most selected arrival records ({monthly.max():,}). '
            'Review confirmation and staffing needs around high-volume periods; counts include canceled bookings.')
    st.caption('Monthly totals reflect selected days. Boundary years and selected boundary months may be incomplete.')
with right, st.container(border=True):
    st.subheader('02 · Which hotel has a higher cancellation share?')
    hotel = rates(view, 'hotel')
    plot(px.bar(hotel, x='hotel', y='Cancellation rate (%)', color='hotel',
        color_discrete_sequence=['#38599a', '#142e66'], text=hotel['Cancellation rate (%)'].map('{:.1f}%'.format),
        custom_data=['Bookings', 'Cancellations'], labels={'hotel': 'Hotel'}).update_traces(
        hovertemplate='%{x}<br>Rate: %{y:.2f}%<br>Bookings: %{customdata[0]:,}<br>Canceled: %{customdata[1]:,}<extra></extra>',
        showlegend=False).update_yaxes(range=[0, 100]))
    top = hotel.loc[hotel['Cancellation rate (%)'].idxmax()]
    st.info(f"{top.hotel}: {top['Cancellation rate (%)']:.2f}% canceled across {int(top.Bookings):,} selected records. "
        + ('Use this comparison to focus hotel-specific monitoring.' if len(hotel) > 1 else 'Select both hotels to compare their cancellation rates.'))

with left, st.container(border=True):
    st.subheader('03 · Which channels need closer review?')
    segment = rates(view, 'market_segment').sort_values('Cancellation rate (%)')
    plot(px.bar(segment, y='market_segment', x='Cancellation rate (%)', orientation='h',
        text=segment['Cancellation rate (%)'].map('{:.1f}%'.format), color_discrete_sequence=['#38599a'],
        custom_data=['Bookings', 'Cancellations'], labels={'market_segment': 'Market segment'}).update_traces(
        hovertemplate='%{y}<br>Rate: %{x:.2f}%<br>Bookings: %{customdata[0]:,}<br>Canceled: %{customdata[1]:,}<extra></extra>')
        .update_xaxes(range=[0,100]))
    named = segment[segment.market_segment != 'Undefined']
    if not named.empty:
        top = named.iloc[-1]
        st.info(f"{top.market_segment} has the highest selected named-segment rate: {top['Cancellation rate (%)']:.2f}% "
                f"across {int(top.Bookings):,} records. Use its booking count to judge the scale before prioritizing follow-ups.")
    else:
        st.info('Only Undefined is selected. Its small source group cannot support a reliable channel comparison.')
    st.caption('Undefined is shown for completeness and excluded from the named-segment ranking. Small groups can produce unstable rates.')
with right, st.container(border=True):
    st.subheader('04 · Does booking notice relate to cancellations?')
    lead = rates(view, 'lead_time_group')
    plot(px.bar(lead, x='lead_time_group', y='Cancellation rate (%)',
        color_discrete_sequence=['#142e66'], custom_data=['Bookings', 'Cancellations'],
        labels={'lead_time_group': 'Lead time'}).update_traces(
        hovertemplate='%{x}<br>Rate: %{y:.2f}%<br>Bookings: %{customdata[0]:,}<br>Canceled: %{customdata[1]:,}<extra></extra>')
        .update_yaxes(range=[0,100]))
    top = lead.loc[lead['Cancellation rate (%)'].idxmax()]
    st.info(f"{top.lead_time_group} has the highest observed rate in this selection: {top['Cancellation rate (%)']:.2f}% "
            f"({int(top.Bookings):,} bookings). Consider booking notice when prioritizing confirmations; this is an association.")

with left, st.container(border=True):
    st.subheader('05 · How do family bookings compare?')
    family = rates(view, 'guest_group')
    plot(px.bar(family, x='guest_group', y='Cancellation rate (%)',
        color_discrete_sequence=['#38599a'], text=family['Cancellation rate (%)'].map('{:.1f}%'.format),
        custom_data=['Bookings', 'Cancellations'], labels={'guest_group': 'Guest group'}).update_traces(
        hovertemplate='%{x}<br>Rate: %{y:.2f}%<br>Bookings: %{customdata[0]:,}<br>Canceled: %{customdata[1]:,}<extra></extra>')
        .update_yaxes(range=[0,100]))
    top = family.loc[family['Cancellation rate (%)'].idxmax()]
    st.info(f"{top.guest_group} bookings have the highest selected group rate ({top['Cancellation rate (%)']:.2f}%, "
            f"{int(top.Bookings):,} records). Review guest-group differences alongside channel and hotel before tailoring communications.")
    st.caption('Family = at least one adult and at least one child or baby. The groups may differ in season, hotel, and channel.')
with right, st.container(border=True):
    st.subheader('06 · How do typical room rates differ?')
    cap = view.average_daily_rate.quantile(.99)
    price = view[view.average_daily_rate.between(0, cap)]
    if not price.empty:
        plot(px.box(price, x='hotel', y='average_daily_rate', color='booking_status',
            color_discrete_map=COLORS, points=False,
            labels={'hotel': 'Hotel', 'average_daily_rate': 'Recorded average daily rate'}))
        medians = view.groupby('hotel').average_daily_rate.median()
        st.info('Selected full-data median rates: ' + '; '.join(f'{h}: {r:,.2f}' for h,r in medians.items())
                + '. Compare typical price levels when reviewing booking patterns; these values do not measure revenue loss.')
    else:
        st.info('No nonnegative rates fall inside the selected plot range.')
    st.caption(f'Chart only: 0 through the selected 99th percentile ({cap:,.2f}); '
               f'{len(view)-len(price):,} records are outside this display range. KPIs retain every selected record. Box: Q1–Q3; line: median; whiskers: 1.5×IQR.')

st.divider()
with st.expander('Definitions, data quality, and interpretation'):
    st.markdown('''**Source and preparation.** Group 4.2 Hotel Booking Demand dataset, originally 119,390 rows and 32 columns.
31,994 exact matching rows were removed, leaving 87,396 working records. No unique reservation ID is provided,
so exact matches are not proof of duplicate real-world reservations. `adr` was renamed to `average_daily_rate`;
missing children were filled with 0, country with Unknown, and agent with 0; company was dropped.
Three derived features and four standardized features reproduce the existing notebook (38 columns).
Seven rows became identical after cleaning; no second duplicate removal was applied.

**Interpretation.** These are historical booking records, not current occupancy, unique customers, or revenue.
Cancellation follows the source `is_canceled` label. The coverage is July 2015–August 2017 and boundary years are partial.
Charts describe associations rather than causes or validated predictions. Negative rates, zero-night stays,
and zero-guest records remain in the dataset and should be investigated before policy decisions.
All displayed rates are within the active filters, and chart hover labels show their denominators.''')
    st.caption('Prepared by Job Russel Enriquez & John Cyruz Patron · BSIT–401I · ITC C307')
with st.expander('View group counts and export selected data'):
    st.dataframe(segment.rename(columns={'market_segment':'Market segment'}), hide_index=True, width='stretch')
    st.download_button('Download selected records (CSV)',
        view.drop(columns=['lead_time_group']).to_csv(index=False).encode('utf-8'),
        file_name='hotel_bookings_filtered.csv', mime='text/csv')


