import zipfile
import re
from pathlib import Path
from io import BytesIO
import pandas as pd
from datetime import date, time, datetime

data_dir = Path('option_data')

def clean_data():

    month_to_num = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    header_csv9 = ['Name', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']
    header_csv8 = ['Name', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']    # Some of the data has Open Interest missing.
    top_dir = data_dir      # Folder where the data is kept. It has three folders by the year (like 2019, 2020 etc). Output is kept in this folder.
    all_years_dir = [x for x in top_dir.iterdir() if x.is_dir()]        # Path to all all year folders.
    all_df = pd.DataFrame(columns=header_csv9)      # Final df that has all the data.
    for year_dir in all_years_dir:
        year = year_dir.name
        try:
            int(year)
        except ValueError:
            continue
        all_weeks_zip = [x for x in year_dir.iterdir()]
        for week_zip in all_weeks_zip:
            week = week_zip.name                        # The format is assumed to be 'Expiry DDth Month.zip'
            expiry_date_list = week.split(' ')
            day = expiry_date_list[1][0:2]              # Extract the day.
            month_name = expiry_date_list[2][:-4]       # Month Name
            month = month_to_num[month_name]            # Month Number
            expiry_stamp = day+'-'+month+'-'+year
            expiry_df = pd.DataFrame(columns=header_csv9)       # All data for a given expiry.
            print("---------------------------------------------------------")
            print(expiry_stamp + ":")
            with zipfile.ZipFile(week_zip, "r") as zfile:
                for name in zfile.namelist():
                    if 'CSV' not in name:               # Process only the zip inside zip that has CSV in name. Skip otherwise.
                        continue
                    else:
                        # We have a zip within a zip
                        zfiledata = BytesIO(zfile.read(name))
                        with zipfile.ZipFile(zfiledata) as zfile2:
                            for strike_name in zfile2.namelist():
                                strike_type = 'PE' if 'PE' in strike_name else 'CE'
                                strike = re.findall(r"\d+", strike_name)        # Find all the numbers in string.
                                strike = strike[-1]         # Get the last number.
                                if len(strike)>5:           # The strike can only be 4 or  digits long. (As long as Nifty doesn't hit 1000 or 1 lac.)
                                    strike = strike[2:]
                                print('\t' + strike + ' ' + strike_type)
                                df = pd.read_csv(zfile2.open(strike_name), header=None)
                                df.columns = header_csv9 if len(df.columns) == 9 else header_csv8
                                strike_type_col = [strike_type] * len(df)
                                strike_col = [strike] * len(df)
                                expiry_date = date(year=int(year), month=int(month), day=int(day))
                                expiry_date_col = [expiry_date]*len(df)
                                df['Strike'] = strike_col
                                df['Type'] = strike_type_col
                                df['Expiry Date'] = expiry_date_col
                                expiry_df = pd.concat([expiry_df, df], sort=False)
            print("---------------------------------------------------------")
            expiry_file_path = top_dir/Path('concat/'+expiry_stamp+'.csv')
            expiry_df.to_csv(expiry_file_path)
            all_df = pd.concat([all_df, expiry_df], sort=False)
    all_file_path = top_dir/Path('concat/all_in_1.csv')
    all_df.to_csv(all_file_path)
    pass

if __name__ == '__main__':
    all_data_filename = data_dir/Path('concat/all_in_1.csv')
    if not all_data_filename.is_file():
        clean_data()
    master_data = pd.read_csv(all_data_filename)
    master_date = master_data['Date']
    uniq_dates = master_date.unique()
    date_sort_index = [i[0] for i in sorted(enumerate(uniq_dates), key=lambda x: x[1])]
    uniq_dates_sorted = list(uniq_dates[date_sort_index])
    day_hash = {dat: index for index, dat in enumerate(uniq_dates_sorted)}
    day_id = pd.Series([day_hash[day] for day in master_date])
    master_data['Day'] = day_id
    master_data.to_csv(all_data_filename)
    pass