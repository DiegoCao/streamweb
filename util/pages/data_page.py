from cgitb import reset
import os
from tkinter.tix import Tree
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

# Use the non-interactive Agg backend, which is recommended as a
# thread-safe backend.
# See https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads.
mpl.use("agg")


_lock = RendererAgg.lock

datalength = 7
T = 52
format = "%m-%d %H:%M:%S"

# df = pd.read_csv("util/pages/RL_new.csv", parse_dates=['Date/Time'],infer_datetime_format=format)
# easydf = pd.read_csv("util/pages/easy_agent_data.csv", parse_dates=['Date/Time'], infer_datetime_format=format)
df = pd.read_csv("RL_final_v2.csv", parse_dates=['Date/Time'],infer_datetime_format=format)
cur_var = 1

if 'cur' not in st.session_state:
    st.session_state['cur'] = 1

def getGas(gas, df):
    if gas == "CO2":
        carbondf = df[["Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our",
        "Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy","Date/Time"]]
        carbondf.rename(columns={"Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our":
                        "CO2 Emission Mass (kg/h) of TRPO MPI",
                        "Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy":
                        "CO2 Emission Mass (kg/h) of Baseline"
                        }, inplace = True)
    elif gas == "CO":
        carbondf = df[["Site:Environmental Impact Electricity CO Emissions Mass [kg](Hourly)_our",
        "Site:Environmental Impact Electricity CO Emissions Mass [kg](Hourly)_easy","Date/Time"]]
        carbondf.rename(columns={"Site:Environmental Impact Electricity CO Emissions Mass [kg](Hourly)_our":
                        "CO Emission Mass (kg/h) of TRPO MPI",
                        "Site:Environmental Impact Electricity CO Emissions Mass [kg](Hourly)_easy":
                        "CO Emission Mass (kg/h) of Baseline"
                        }, inplace = True)
    elif gas == "CH4":
        # col1 = str(gas) + ":Facility [kg](Hourly)_our"
        # col2 = str(gas) + ":Facility [kg](Hourly)_our"
        carbondf = df[['CH4:Facility [kg](Hourly)_our', 'CH4:Facility [kg](Hourly)_easy', 'Date/Time']]
        carbondf.rename(columns = {"CH4:Facility [kg](Hourly)_our:col3":"CH4 Emission Mass (kg/h) of TRPO MPI"
                    , "CH4:Facility [kg](Hourly)_easy":"CH4 Emission Mass (kg/h) of Baseline"}, inplace = True)
    elif gas == "PM2.5":
        carbondf = df[['PM2.5:Facility [kg](Hourly)_our', 'PM2.5:Facility [kg](Hourly)_easy', 'Date/Time']]
        carbondf.rename(columns = {"PM2.5:Facility [kg](Hourly)_our:col3":"PM2.5 Emission Mass (kg/h) of TRPO MPI"
                    , "PM2.5:Facility [kg](Hourly)_easy":"PM2.5 Emission Mass (kg/h) of Baseline"}, inplace = True)
    elif gas == "SO2":
        carbondf = df[['SO2:Facility [kg](Hourly)_our', 'SO2:Facility [kg](Hourly)_easy', 'Date/Time']]
        carbondf.rename(columns = {"SO2:Facility [kg](Hourly)_our:col3":"SO2 Emission Mass (kg/h) of TRPO MPI"
                    , "SO2:Facility [kg](Hourly)_easy":"SO2 Emission Mass (kg/h) of Baseline"}, inplace = True)
    elif gas == "NOx":
        carbondf = df[['NOx:Facility [kg](Hourly)_our', 'NOx:Facility [kg](Hourly)_easy', 'Date/Time']]
        carbondf.rename(columns = {"NOx:Facility [kg](Hourly)_our:col3":"NOx Emission Mass (kg/h) of TRPO MPI"
                    , "NOx:Facility [kg](Hourly)_easy":"NOx Emission Mass (kg/h) of Baseline"}, inplace = True)
    return carbondf

def staticPlot(weeks):
    st.title("Static HVAC Dashboard")
    st.markdown("""
        Use Checkbox and Select menu to select the data you want to display.
    """)
    Parameters = ['HVAC West Temperature', 'HVAC East Temperature']
    Fanmeters = ['West Zone Supply Fan Rate', 'East Zone Supply Fan Rate']
    Outmeters = ['West Temperature', 'East Temperature']
    check1 = st.checkbox("Baseline")
    check2 = st.checkbox("TRPO MPI")

    # selectzone = st.multiselect('Evaluation Parameters', eval, default=['CO2'])
    gas = st.selectbox('Evaluation Gas', ('CO2', 'CO', 'CH4', 'PM2.5', 'SO2', 'NOx'))
    selectzone = st.multiselect('Action Temperature Parameters  ', Parameters, default=['HVAC West Temperature'])
    fanmass = st.multiselect('HVAC Supply Fan Rate', Fanmeters, default = ['West Zone Supply Fan Rate'])


    outtemperatre = st.multiselect('Select Output Temperatures ', Outmeters, default=['West Temperature'])

    length = len(df)
    X = np.linspace(0, 1, len(df))
    start = weeks[0]
    end = weeks[1]


    carbondf = getGas(gas, df)
    carbondf = carbondf[int(start*length/T):int(end*length/T)]

    zonedf= df[[
                'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our',
                'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy',
                'EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our',
                'EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy',
                'Date/Time'
            ]]
    zonedf.rename(columns={
        "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
        "West Out Temperature (C) of TRPO MPI",
        "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
        "West Out Temperature (C) of Baseline",
        "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
        "East Out Temperature (C) of TRPO MPI",
        "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
        "East Out Temperature (C) of Baseline"
    }, inplace=True)
    outdf = df[[
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_our",
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_easy",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_our",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_easy",
                "Date/Time"
            ]]
    outdf.rename(columns={
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_our":
                "West Zone real temperature of TRPO MPI",
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_easy":
                "West Zone real temperature of Baseline",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_our":
                "East Zone real temperature of TRPO MPI",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_easy":
                "East Zone real temperature of Baseline"
            }, inplace=True)
    fandf = df[[
        "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our",
        "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy",
        "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our",
        "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy",
        "Date/Time"
    ]]
    fandf.rename(columns={
        "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our":
        "West Zone Supply Fan Rate of TRPO MPI",
        "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy":
        "West Zone Supply Fan Rate of Baseline",
        "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our":
        "East Zone Supply Fan Rate of TRPO MPI",
        "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy":
        "East Zone Supply Fan Rate of Easy Baseline",
    }, inplace=True)

    zonedf = zonedf[int(start*length/T):int(end*length/T)]
    outdf = outdf[int(start*length/T):int(end*length/T)]
    fandf = fandf[int(start*length/T):int(end*length/T)]

    # print(plotdf.columns[3:5])
    if check1 and check2:
        y = carbondf.columns[0:2]
    elif not check1 and not check2:
        y = None
    elif not check1:
        y = carbondf.columns[0:1]
    elif not check2:
        y = carbondf.columns[1:2]
    placeholder = st.empty()
    

    with placeholder.container():
        if y is not None:
            fig = px.line(carbondf, x='Date/Time', y=y)
            # labels = ['Outer Temprature', ]
            fig.update_xaxes(
                tickangle=45,
                tickformat=format,
                title = "Carbon Emisson with Time Monitor"
                )

            st.plotly_chart(fig, use_container_width=True)

        y2 = gety2index(check1, check2, selectzone, zonedf)
        if y2 is not None:
            fig2 = px.line(zonedf, x='Date/Time', y=y2)
            fig2.update_xaxes(
                tickangle=45,
                tickformat=format,
                title = "West/East Zone Temperature (Action of HVAC) Monitor"
                )
            st.plotly_chart(fig2, use_container_width=True)
        y4 = gety4index(check1, check2,fanmass , fandf)
        if y4 is not None:
            fig4 = px.line(fandf, x='Date/Time', y=y4)
            fig4.update_xaxes(
                tickangle=45,
                tickformat=format,
                title = "Real-time West/East Supply Fan Air Mass Flow Rate[kg/s] Hourly"
                )

            fig4.update_xaxes(
                range=[0,8]
            )
            st.plotly_chart(fig4, use_container_width=True)
            

        y3 = gety3index(check1, check2, outtemperatre, outdf)
        if y3 is not None:
            fig3 = px.line(outdf, x='Date/Time', y=y3)
            fig3.update_xaxes(
                tickangle=45,
                tickformat=format,
                title = "Real-time West/East Zone Real Temperature Monitor"
                )

            st.plotly_chart(fig3, use_container_width=True)
        

            
            
        
    if 'cur' not in st.session_state:
        st.session_state['cur'] = 1
    st.session_state['cur'] = 1
    

    
    # st.caption("Date/Time vs Controled Air ")
    # fig2 = px.line(plotdf, x='Date/Time', y=plotdf.columns[4:6])
    # st.plotly_chart(fig2, use_container_width=True)

    # # st.caption("Date/Time vs Evaluation Data")
    # fig3 = px.line(plotdf, x='Date/Time', y=plotdf.columns[7:10])
    # st.plotly_chart(fig3, use_container_width=True)


Medudict = {'West': ['WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy.',
                    'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our'
                    ],
            'East': [
                    'EAST ZONE:Zone Air Temperature [C](TimeStep)_easy',
                    'EAST ZONE:Zone Air Temperature [C](TimeStep)_our'
                    ]
            }

def gety2index(check1, check2, selectzone, zonedf):
    west = False
    east = False
    if "HVAC West Temperature" in selectzone:
        west = True
    if "HVAC East Temperature" in selectzone:
        east = True
    if not check1 and not check2:
        return None
    if check1 and check2:
        if west and east:
            return zonedf.columns[0:4]
        elif west and not east:
            return zonedf.columns[0:2]
        elif east and not west:
            return zonedf.columns[2:4]
        else:
            return None

    if not check2:
        if west and east:
            newdf = zonedf[["East Out Temperature (C) of Baseline","West Out Temperature (C) of Baseline"]]
            return newdf.columns[0:2]
        elif west:
            return zonedf.columns[1:2]
        elif east:
            return zonedf.columns[3:4]
    if not check1:
        if west and east:
            newdf = zonedf[["East Out Temperature (C) of Our","West Out Temperature (C) of Our"]]
            return newdf.columns[0:2]
        elif west:
            return zonedf.columns[0:1]
        elif east:
            return zonedf.columns[2:3]


def gety3index(check1, check2, selectzone, zonedf):
    west = False
    east = False
    if "West Temperature" in selectzone:
        west = True
    if "East Temperature" in selectzone:
        east = True
    if not check1 and not check2:
        return None
    if check1 and check2:
        if west and east:
            return zonedf.columns[0:4]
        elif west and not east:
            return zonedf.columns[0:2]
        elif east and not west:
            return zonedf.columns[2:4]
        else:
            return None
    if not check2:
        if west and east:
            newdf = zonedf[["East Zone Real Temperature(C) of Baseline","West Zone Real Temperature(C) of Baseline"]]
            return newdf.columns[0:2]
        elif west:
            return zonedf.columns[1:2]
        elif east:
            return zonedf.columns[3:4]
    if not check1:
        if west and east:
            newdf = zonedf[["East Zone Real Temperature(C) of Our","West Zone Real Temperature(C) of Our"]]
            return newdf.columns[0:2]
        elif west:
            return zonedf.columns[0:1]
        elif east:
            return zonedf.columns[2:3]

def gety4index(check1, check2, selectzone, zonedf):
    west = False
    east = False
    if "West Zone Supply Fan Rate" in selectzone:
        west = True
    if "East Zone Supply Fan Rate" in selectzone:
        east = True
    if not check1 and not check2:
        return None
    if check1 and check2:
        if west and east:
            return zonedf.columns[0:4]
        elif west and not east:
            return zonedf.columns[0:2]
        elif east and not west:
            return zonedf.columns[2:4]
        else:
            return None
    if not check2:
        if west and east:
            newdf = zonedf[["East Zone Supply Fan Rate of Baseline","West Zone Supply Fan Rate of Baseline"]]
            return newdf.columns[0:2]
        elif west:
            return zonedf.columns[1:2]
        elif east:
            return zonedf.columns[3:4]
    if not check1:
        if west and east:
            newdf = zonedf[["East Zone Supply Fan Rate of Our","West Zone Supply Fan Rate of Our"]]
            return newdf.columns[0:2]
        elif west:
            return zonedf.columns[0:1]
        elif east:
            return zonedf.columns[2:3]



def dynamicPlot(weeks):
    st.title("Real-Time HVAC Dashboard")
    st.markdown("""
        Use Checkbox and Select menu to select the data you want to display.
    """)
    move_length = 160
    st.experimental_memo.clear()
    Parameters = ['HVAC West Temperature', 'HVAC East Temperature']
    Fanmeters = ['West Zone Supply Fan Rate', 'East Zone Supply Fan Rate']

    Outmeters = ['West Temperature', 'East Temperature']
    check1 = st.checkbox("Baseline")
    check2 = st.checkbox("TRPO MPI")

    gas = st.selectbox('Evaluation Gas', ('CO2', 'CO', 'CH4', 'PM2.5', 'SO2', 'NOx'))   
    selectzone = st.multiselect('Select HVAC Temperature Parameters ', Parameters, default=['HVAC West Temperature'])
    fanmass = st.multiselect('Select Zone Fan Parameters',Fanmeters, default=['West Zone Supply Fan Rate'])

    outtemperatre = st.multiselect('Select Output Temperatures ', Outmeters, default=['West Temperature'])

    placeholder = st.empty()
    Timestep = len(df)
    # start = cur_var
    start = st.session_state['cur']

    if not check1 and not check2:
        return 
    

    for i in range(start, Timestep):
        with placeholder.container():

            length = len(df)
            kpi1, kpi2 = st.columns(2)

            if i < move_length:
                plotdf = df[0:int(i*length/Timestep)]
                # basedf = easydf[0:int(i*length/Timestep)]
            else:
                plotdf = df[int((i-move_length)*length/Timestep):int(i*length/Timestep)]

            kpi1.metric(
                label = "Our Carbon CO2 Emission Rate Running Average (kg/h)",
                value = round(np.average(plotdf['Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our']),2)
            )
            kpi2.metric(
                label = "Baseline CO2 Emisson Data Running Average (kg/h)",
                value = round(np.average(plotdf['Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy'
                ]),2)
            )

                # basedf = easydf[int((i-5)*length/Timestep):int(i*length/Timestep)]
            zonedf = plotdf[[
                'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our',
                'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy',
                'EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our',
                'EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy',
                'Date/Time'
            ]]

            zonedf.rename(columns={
                "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
                "West HVAC Temperature (C) of TRPO MPI",
                "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
                "West HVAC Temperature (C) of Baseline",
                "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
                "East HVAC Temperature (C) of TRPO MPI",
                "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
                "East HVAC Temperature (C) of Baseline"
            }, inplace=True)

            outdf = plotdf[[
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_our",
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_easy",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_our",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_easy",
                'Date/Time'
            ]]
            outdf.rename(columns={
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_our":
                "West Zone Real Temperature(C) of TRPO MPI",
                "WEST ZONE:Zone Air Temperature [C](TimeStep)_easy":
                "West Zone Real Temperature(C)  of Baseline",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_our":
                "East Zone Real Temperature(C) of TRPO MPI",
                "EAST ZONE:Zone Air Temperature [C](TimeStep)_easy":
                "East Zone Real Temperature(C) of Baseline"
            }, inplace=True)


            fandf = plotdf[[
                "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our",
                "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy",
                "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our",
                "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy",
                "Date/Time"
            ]]
            fandf.rename(columns={
                "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our":
                "West Zone Supply Fan Rate of TRPO MPI",
                "WEST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy":
                "West Zone Supply Fan Rate of Baseline",
                "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_our":
                "East Zone Supply Fan Rate of TRPO MPI",
                "EAST ZONE SUPPLY FAN:Fan Air Mass Flow Rate [kg/s](Hourly)_easy":
                "East Zone Supply Fan Rate of Easy Baseline",
            }, inplace=True)

            subdf = getGas(gas, plotdf)

            y_ = subdf.columns[0:2]
            if check1 and not check2:
                y_ = subdf.columns[1:2]
            if check2 and not check1:
                y_ = subdf.columns[0:1]
            
            fig = px.line(subdf, x='Date/Time', y=y_)
            fig.update_xaxes(
                            tickangle=45,
                            dtick=12,
                            tickformat=format,
                            range=[0,move_length],
                            title = "Real-time CO2 Emission Equivalent Mass Monitor"
                            )
            fig.update_yaxes(range=[0,32])
            # fig.addtrace(bbasedf, x = 'Date/Time', y=basedf.columms[5:6])
            st.plotly_chart(fig, use_container_width=True)

        
            y2 = gety2index(check1, check2, selectzone, zonedf)
            fig2 = px.line(zonedf, x='Date/Time', y=y2)
            fig2.update_xaxes(
                tickangle=45,
                dtick=12,
                tickformat=format,
                range=[0,move_length],
                title = "Real-time West/East Zone Temperature (Action of HVAC) Monitor"
                )


            st.plotly_chart(fig2, use_container_width=True)

            y4 = gety4index(check1, check2,fanmass , fandf)
            fig4 = px.line(fandf, x='Date/Time', y=y4)
            fig4.update_xaxes(
                tickangle=45,
                dtick=12,
                tickformat=format,
                range=[0,move_length],
                title = "Real-time West/East Zone Real Temperature Monitor"
                )
            fig4.update_yaxes(
                range=[0,8]
            )
            st.plotly_chart(fig4, use_container_width=True)
            
            y3 = gety3index(check1, check2,outtemperatre, outdf)
            fig3 = px.line(outdf, x='Date/Time', y=y3)
            fig3.update_xaxes(
                tickangle=45,
                dtick=12,
                tickformat=format,
                range=[0,move_length],
                title = "Real-time West/East Zone Real Temperature Monitor"
                )
            st.plotly_chart(fig3, use_container_width=True)
            


            
            

            time.sleep(0.1)
            st.session_state['cur'] += 1

    st.session_state['cur'] = 1


def data_page():

    # -- Set page config
    # apptitle = 'GW Quickview'

    # st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    width: 300px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
    width: 300px;
    margin-left: -300px;
    }
    </style>
    """,
        unsafe_allow_html=True
    )

    # -- Default detector list
    detectorlist = ['H1', 'L1', 'V1']

    # Title the app

    if 'cur' not in st.session_state:
        st.session_state['cur'] = 1

    @st.cache(ttl=3600, max_entries=10)  # -- Magic command to cache data
    def load_gw(t0, detector, fs=4096):
        strain = TimeSeries.fetch_open_data(
            detector, t0-14, t0+14, sample_rate=fs, cache=False)
        return strain

        
    st.sidebar.markdown("## Display Mode")
    mode = st.sidebar.selectbox('How do you want to display data', [ 'Static', 'Dynamic' ])   

    st.sidebar.markdown('## Weeks')
    weeks = st.sidebar.slider('Weeks', min_value=1,
                              max_value=52, value=(1,2), step=1)
    df = pd.read_csv('util/pages/newmtr.csv')
    X = df['Date/Time']



    if mode == 'Static':
        with _lock:
            staticPlot(weeks)
            write_st_end()

    elif mode == 'Dynamic':
        with _lock:
            dynamicPlot(weeks)
            write_st_end()

        pass


 