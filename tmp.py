from datetime import datetime
import pandas as pd

import pandas as pd
import datetime as dt

# def my_to_datetime(date_str):
#     if date_str[8:10] != '24':
#         return pd.to_datetime(date_str, format=' %m/%d  %H:%M:%S')

#     date_str = date_str[0:8] + '00' + date_str[10:]

#     return pd.to_datetime(date_str, format=' %m/%d  %H:%M:%S') + dt.timedelta(days=1)

# format = "%m-%d  %H:%M:%S"
df = pd.read_csv("util/pages/RL_agent_data.csv", parse_dates=['Date/Time'],infer_datetime_format=format)
easydf = pd.read_csv("util/pages/easy_agent_data.csv", parse_dates=['Date/Time'],infer_datetime_format=format)

finaldf = pd.merge(df, easydf, left_on="Date/Time", right_on = "Date/Time",suffixes=['_our', '_easy'])
# print(finaldf.columns[5:8])

finaldf.to_csv("RL_final_v2.csv")
# df = pd.read_csv("util/pages/RL_agent_data.csv")
# df['Date/Time'] = df['Date/Time'].apply(my_to_datetime)
# df.to_csv("util/pages/RL_new.csv")

# df = pd.read_csv("util/pages/RL_new.csv")
# df['Date/Time'] = df['Date/Time'].str.replace('1900-', '')
# df.to_csv("util/pages/RL_new.csv")

# df['Date/Time'].str.replace('24:00', '0:00')
# # obj = pd.to_datetime(dstr, format,unit='s')
# df = pd.read_csv("util/pages/newmtr.csv", parse_dates=['Date/Time'],date_parser=lambda x: datetime.strptime(x, format))

# print(obj)
# print(obj.date())