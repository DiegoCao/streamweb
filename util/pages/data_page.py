import os
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
df = pd.read_csv("util/pages/RL_final.csv", parse_dates=['Date/Time'],infer_datetime_format=format)
cur_var = 1

if 'cur' not in st.session_state:
    st.session_state['cur'] = 1


def staticPlot(weeks):
    st.title("Static HVAC Dashboard")
    st.markdown("""
        Use Checkbox and Select menu to select the data you want to display.
    """)

    Parameters = ['West Temperature', 'East Temperature']
    check1 = st.checkbox("Easy Agent")
    check2 = st.checkbox("Our RL Agent")
    selectzone = st.multiselect('Select Temperature Parameters  ', Parameters, default=['West Temperature'])
    length = len(df)
    X = np.linspace(0, 1, len(df))
    start = weeks[0]
    end = weeks[1]
    # X = X[int(start*length/T):int(end*length/T)]
    # y = pd.melt(df, id_vars=['Date/Time'], value_vars=['outer_T', 'left_T'])
    carbondf = df[["Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our",
        "Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy","Date/Time"]]

    carbondf = carbondf[int(start*length/T):int(end*length/T)]
    carbondf.rename(columns={"Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our":
                    "CO2 Emission Mass (kg/h) of Our Method",
                    "Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy":
                    "CO2 Emission Mass (kg/h) of Easy Agent"
                    }, inplace = True)

    zonedf= df[[
                'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our',
                'WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy',
                'EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our',
                'EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy',
                'Date/Time'
            ]]
    zonedf.rename(columns={
        "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
        "West Out Temperature (C) of Our",
        "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
        "West Out Temperature (C) of Easy Agent",
        "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
        "East Out Temperature (C) of Our",
        "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
        "East Out Temperature (C) of Easy Agent"
    }, inplace=True)
    zonedf = zonedf[int(start*length/T):int(end*length/T)]

    # print(plotdf.columns[3:5])
    if check1 and check2:
        y = carbondf.columns[0:2]
    elif not check1 and not check2:
        y = None
    elif not check1:
        y = carbondf.columns[1:2]
    elif not check2:
        y = carbondf.columns[0:1]

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
            newdf = zonedf[["East Out Temperature (C) of Easy Agent","West Out Temperature (C) of Easy Agent"]]
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


def dynamicPlot(weeks):
    st.title("Real-Time HVAC Dashboard")
    st.markdown("""
        Use Checkbox and Select menu to select the data you want to display.
    """)
    move_length = 160
    st.experimental_memo.clear()
    Parameters = ['West Temperature', 'East Temperature']
    check1 = st.checkbox("Easy Agent")
    check2 = st.checkbox("Our RL Agent")
    selectzone = st.multiselect('Select Temperature Parameters  ', Parameters, default=['West Temperature'])
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
                label = "Easy Agent CO2 Emisson Data Running Average (kg/h)",
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
                "West Out Temperature (C) of Our",
                "WEST ZONE DEC OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
                "West Out Temperature (C) of Easy Agent",
                "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_our":
                "East Out Temperature (C) of Our",
                "EAST AIR LOOP OUTLET NODE:System Node Setpoint Temperature [C](TimeStep)_easy":
                "East Out Temperature (C) of Easy Agent"
            }, inplace=True)

            subdf = plotdf[['Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our',
                    'Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy',
                    'Date/Time']]
            subdf.rename(columns={"Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_our":
                    "CO2 Emission Mass (kg/h) of Our Method",
                    "Site:Environmental Impact Total CO2 Emissions Carbon Equivalent Mass [kg](Hourly)_easy":
                    "CO2 Emission Mass (kg/h) of Easy Agent"
                    }, inplace = True)



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
            fig.update_yaxes(range=[0,30])
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


    # if mode == 'Static':

    # # -- Get list of events
    # # eventlist = get_eventlist()
    # event_list = ['adsf', 'adf']
    # #-- Set time by GPS or event
    # select_event = st.sidebar.selectbox('How do you want to find data?',
    #                                     ['By event name', 'By GPS'])

    # if select_event == 'By GPS':
    #     # -- Set a GPS time:
    #     str_t0 = st.sidebar.text_input('GPS Time', '1126259462.4')    # -- GW150914
    #     t0 = float(str_t0)

    #     st.sidebar.markdown("""
    #     Example times in the H1 detector:
    #     * 1126259462.4    (GW150914)
    #     * 1187008882.4    (GW170817)
    #     * 1128667463.0    (hardware injection)
    #     * 1132401286.33   (Koi Fish Glitch)
    #     """)
    # else:
    #     chosen_event = st.sidebar.selectbox('Select Event', event_list)
    #     # t0 = datasets.event_gps(chosen_event)
    #     detectorlist = list(datasets.event_detectors(chosen_event))
    #     detectorlist.sort()
    #     st.subheader(chosen_event)
    #     # st.write('GPS:', t0)

    #     # -- Experiment to display masses

    # #-- Choose detector as H1, L1, or V1
    # detector = st.sidebar.selectbox('Detector', detectorlist)

    # # -- Select for high sample rate data
    # fs = 4096
    # maxband = 2000
    # high_fs = st.sidebar.checkbox('Full sample rate data')
    # if high_fs:
    #     fs = 16384
    #     maxband = 8000

    # # -- Create sidebar for plot controls
    # st.sidebar.markdown('## Set Plot Parameters')
    # dtboth = st.sidebar.slider('Time Range (seconds)', 0.1, 8.0, 1.0)  # min, max, default
    # dt = dtboth / 2.0

    # st.sidebar.markdown('#### Whitened and band-passed data')
    # whiten = st.sidebar.checkbox('Whiten?', value=True)
    # freqrange = st.sidebar.slider('Band-pass frequency range (Hz)', min_value=10, max_value=maxband, value=(30,400))

    # # -- Create sidebar for Q-transform controls
    # st.sidebar.markdown('#### Q-tranform plot')
    # vmax = st.sidebar.slider('Colorbar Max Energy', 10, 500, 25)  # min, max, default
    # qcenter = st.sidebar.slider('Q-value', 5, 120, 5)  # min, max, default
    # qrange = (int(qcenter*0.8), int(qcenter*1.2))

    # #-- Create a text element and let the reader know the data is loading.
    # strain_load_state = st.text('Loading data...this may take a minute')
    # try:
    #     strain_data = load_gw(t0, detector, fs)
    # except:
    #     st.warning('{0} data are not available for time {1}.  Please try a different time and detector pair.'.format(detector, t0))
    #     st.stop()

    # strain_load_state.text('Loading data...done!')

    # #-- Make a time series plot

    # cropstart = t0-0.2
    # cropend   = t0+0.1

    # cropstart = t0 - dt
    # cropend   = t0 + dt

    # st.subheader('Raw data')
    # center = int(t0)
    # strain = deepcopy(strain_data)

    # with _lock:
    #     fig1 = strain.crop(cropstart, cropend).plot()
    #     #fig1 = cropped.plot()
    #     st.pyplot(fig1, clear_figure=True)

    # # -- Try whitened and band-passed plot
    # # -- Whiten and bandpass data
    # st.subheader('Whitened and Band-passed Data')

    # if whiten:
    #     white_data = strain.whiten()
    #     bp_data = white_data.bandpass(freqrange[0], freqrange[1])
    # else:
    #     bp_data = strain.bandpass(freqrange[0], freqrange[1])

    # bp_cropped = bp_data.crop(cropstart, cropend)

    # with _lock:
    #     fig3 = bp_cropped.plot()
    #     st.pyplot(fig3, clear_figure=True)

    # # # -- Allow data download
    # # download = {'Time':bp_cropped.times, 'Strain':bp_cropped.value}
    # # df = pd.DataFrame(download)
    # # csv = df.to_csv(index=False)
    # # b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # # fn =  detector + '-STRAIN' + '-' + str(int(cropstart)) + '-' + str(int(cropend-cropstart)) + '.csv'
    # # href = f'<a href="data:file/csv;base64,{b64}" download="{fn}">Download Data as CSV File</a>'
    # # st.markdown(href, unsafe_allow_html=True)

    # # # -- Make audio file
    # # st.audio(make_audio_file(bp_cropped), format='audio/wav')

    # # -- Notes on whitening
    # with st.expander("See notes"):
    #     st.markdown("""
    # * Whitening is a process that re-weights a signal, so that all frequency bins have a nearly equal amount of noise.
    # * A band-pass filter uses both a low frequency cutoff and a high frequency cutoff, and only passes signals in the frequency band between these values.
    # See also:
    # * [Signal Processing Tutorial](https://share.streamlit.io/jkanner/streamlit-audio/main/app.py)
    # """)

    # st.subheader('Q-transform')

    # hq = strain.q_transform(outseg=(t0-dt, t0+dt), qrange=qrange)

    # with _lock:
    #     fig4 = hq.plot()
    #     ax = fig4.gca()
    #     fig4.colorbar(label="Normalised energy", vmax=vmax, vmin=0)
    #     ax.grid(False)
    #     ax.set_yscale('log')
    #     ax.set_ylim(bottom=15)
    #     st.pyplot(fig4, clear_figure=True)

    # with st.expander("See notes"):

    #     st.markdown("""
    # A Q-transform plot shows how a signal’s frequency changes with time.
    # * The x-axis shows time
    # * The y-axis shows frequency
    # The color scale shows the amount of “energy” or “signal power” in each time-frequency pixel.
    # A parameter called “Q” refers to the quality factor.  A higher quality factor corresponds to a larger number of cycles in each time-frequency pixel.
    # For gravitational-wave signals, binary black holes are most clear with lower Q values (Q = 5-20), where binary neutron star mergers work better with higher Q values (Q = 80 - 120).
    # See also:
    # * [GWpy q-transform](https://gwpy.github.io/docs/stable/examples/timeseries/qscan.html)
    # * [Reading Time-frequency plots](https://labcit.ligo.caltech.edu/~jkanner/aapt/web/math.html#tfplot)
    # * [Shourov Chatterji PhD Thesis](https://dspace.mit.edu/handle/1721.1/34388)
    # """)

    # st.subheader("About this app")
    # st.markdown("""
    # This app displays data from LIGO, Virgo, and GEO downloaded from
    # the Gravitational Wave Open Science Center at https://gw-openscience.org .
    # You can see how this works in the [Quickview Jupyter Notebook](https://github.com/losc-tutorial/quickview) or
    # [see the code](https://github.com/jkanner/streamlit-dataview).
    # """)
