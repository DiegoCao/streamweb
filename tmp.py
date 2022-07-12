import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.offline as py 
import numpy as np  

import plotly.express as px 
import pandas as pd 
import numpy as np 

# data
df = pd.read_csv('util/pages/newmtr.csv')
print(len(df))
print(df)
fig = px.line(df, x='Date/Time', y=df.columns[1:3])

# Show plot 
fig.show()