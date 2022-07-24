from cgitb import reset
import os
from tkinter.tix import Tree
from turtle import width
import requests
import plotly.figure_factory as ff
import plotly.graph_objs as go
from matplotlib.backends.backend_agg import RendererAgg
import matplotlib as mpl
from streamlit import caching
import wavfile
from util.functions.gui import write_st_end
import io
import base64
from copy import deepcopy
from gwosc.api import fetch_event_json
from gwosc import datasets
from gwosc.locate import get_urls
from gwpy.timeseries import TimeSeries
import plotly.express as px
from sqlite3 import Time
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import plotly.offline as py                    
py.init_notebook_mode(connected=True)         
import plotly.graph_objs as go                
import plotly.figure_factory as ff   
import plotly.express as px
import requests, os
from gwpy.timeseries import TimeSeries
from gwosc.locate import get_urls
from gwosc import datasets
from gwosc.api import fetch_event_json

from copy import deepcopy
import base64
import io
from util.functions.gui import write_st_end
import wavfile
from streamlit import caching


def building_page():
    col, coli, col4 = st.columns([2,6,2])
    with col:
        st.write("")

    with coli:
        st.image('util/pages/building.png')


    with col4:
        st.write("")

    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    df = pd.read_csv("util/pages/table.csv",header=None, index_col=False)
    df1 = df[df.columns[0:2]]
    df2 = df[df.columns[2:4]]
    df1.columns = ['Property', 'Values']
    df2.columns = ['Property', 'Values']


    col1, col2 = st.columns(2)
    with col1:
        st.table(df1)
    with col2:
        st.table(df2)


    write_st_end()

