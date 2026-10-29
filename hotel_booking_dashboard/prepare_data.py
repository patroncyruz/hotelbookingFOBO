from pathlib import Path
import pandas as pd
import argparse
parser=argparse.ArgumentParser(description='Reproduce the notebook cleaning from the original CSV.')
parser.add_argument('source', type=Path)
args=parser.parse_args()
source=args.source
df=pd.read_csv(source).rename(columns={'adr':'average_daily_rate'})
df['reservation_status_date']=pd.to_datetime(df['reservation_status_date'])
df=df.drop_duplicates().reset_index(drop=True)
df['children']=df.children.fillna(0).astype(int)
df['country']=df.country.fillna('Unknown')
df['agent']=df.agent.fillna(0)
df=df.drop(columns='company')
df['total_nights']=df.stays_in_weekend_nights+df.stays_in_week_nights
df['total_guests']=df.adults+df.children+df.babies
df['is_family']=(((df.children>0)|(df.babies>0))&(df.adults>0)).astype(int)
for col in ['lead_time','average_daily_rate','total_nights','total_guests']:
 df[col+'_scaled']=(df[col]-df[col].mean())/df[col].std(ddof=0)
assert df.shape==(87396,38)
assert df.duplicated().sum()==7
assert df.isna().sum().sum()==0
df.to_csv(Path(__file__).parent / 'hotel_bookings_cleaned.csv',index=False)
print('Saved cleaned dataset:',df.shape)

