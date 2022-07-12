# -*- coding: utf-8 -*-

import streamlit as st
from PIL import Image

from ..functions.table import mask_equal
from ..functions.col import pdb_code_col
from ..functions.path import pages_str, data_str, get_file_path
from ..functions.gui import load_st_table, write_st_end, create_st_button, show_st_structure, get_neighbor_path


def home_page():

    left_col, right_col = st.columns([1, 2])

    df = load_st_table(__file__)

    img = Image.open(
        get_file_path(
            "Logo 450 I.png",
            dir_path=get_neighbor_path(__file__, pages_str, data_str),
        )
    )
    left_col.image(img, width=300, output_format="PNG")

    right_col.markdown(
        "# Real-time Carbon Emission Evaluation for Future Low-Carbon Buildings")
    right_col.markdown(
        "### An intelligent tool for smart carbon building Control based on Reinforcement Learning and EnergyPlus")
    right_col.markdown("#### Created by VE 450 Group 12")
    # right_col.markdown("**F**")

    paper_link_dict = {
        "IBM Paper": "https://github.com/IBM/rl-testbed-for-energyplus",
    }

    st.sidebar.markdown("## Database-Related Links")
    for link_text, link_url in paper_link_dict.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)

    community_link_dict = {
        "NCI RAS Initiative": "https://www.cancer.gov/research/key-initiatives/ras",
        "KRAS Kickers": "https://www.kraskickers.org",
        "RASopathies Network": "https://rasopathiesnet.org",
    }

    st.sidebar.markdown("## Community-Related Links")
    for link_text, link_url in community_link_dict.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)

    software_link_dict = {
        "EnergyPlus": "https://energyplus.net/",
        "DesignBuilder": "https://designbuilder.co.uk/",
        "Pandas": "https://pandas.pydata.org",
        "NumPy": "https://numpy.org",
        "SciPy": "https://scipy.org",
        "Sklearn": "https://scikit-learn.org/stable/",
        "Matplotlib": "https://matplotlib.org",
        "Seaborn": "https://seaborn.pydata.org",
        "Streamlit": "https://streamlit.io",
    }

    st.sidebar.markdown("## Software-Related Links")
    link_1_col, link_2_col, link_3_col = st.sidebar.columns(3)

    i = 0
    link_col_dict = {0: link_1_col, 1: link_2_col, 2: link_3_col}
    for link_text, link_url in software_link_dict.items():

        st_col = link_col_dict[i]
        i += 1
        if i == len(link_col_dict.keys()):
            i = 0

        create_st_button(link_text, link_url, st_col=st_col)

    st.markdown("---")

    st.markdown(
        """
        ## Summary
        <p style="font-size: 22px;">Nowadays, the energy consumed from residential or office buildings contributes a very large share of carbon emissions.
        Knowledge of the real-time status of carbon emissions in buildings enables building operatorsto optimize energy usage 
        and control carbon emissions. In addition, it is of great importance to make a real-time carbon emission monitoring 
        system, as the basis for evaluating the renewable energy solutions for future low-carbon buildings. 
        As a long-term direction, the project aims to design and engineer future low-carbon buildings for rural vitalization.
        Students are expected to work closely with the mentors to deliver the project deliverables.</p>

        <p style="font-size: 30px;">TODO</p>
        Details of our work are 
        provided in the [*Cancer Research*](https://aacrjournals.org/cancerres/article/doi/10.1158/0008-5472.CAN-22-0804/696349/Delineating-The-RAS-Conformational-LandscapeThe)
        paper, **Delineating The RAS Conformational Landscape**.
        We hope that researchers will use 
        *Rascore* to gain novel insights into RAS biology and 
        drug discovery. 
        """, unsafe_allow_html=True
    )

    st.markdown("---")
    left_col, right_col = st.columns([1, 2])

    img = Image.open(
        get_file_path(
            "diagram.png",
            dir_path=get_neighbor_path(__file__, pages_str, data_str),
        )
    )

    right_col.image(img, width=680, output_format="PNG")

    left_col.markdown(
        """
        ## Usage

        <p style="font-size: 22px;">To the left, is a dropdown main menu for navigating to 
        each page of our product:</p>
        <p style="font-size: 20px;">-&nbsp <b>Home Page:</b> We are here!</p>
        <p style="font-size: 20px;">-&nbsp <b>Group Members:</b> Profile of group members</p>
        <p style="font-size: 20px;">-&nbsp <b>System Overview:</b> Overview of the System</p>
        <p style="font-size: 20px;">-&nbsp <b>Result Visualization</b></p>
        
        """, unsafe_allow_html=True
    )
    st.markdown("---")

    left_info_col, right_info_col = st.columns(2)

    left_info_col.markdown(
        f"""
        ## Authors
        <p style="font-size: 20px;">Please feel free to contact us with any issues, comments, or questions.</p>

        <p style="font-size: 20px;"><b>Hangrui Cao</b>&nbsp(<a href="mailto:caohangrui@sjtu.edu.cn">caohangrui@sjtu.edu.cn</a>)</p>
        <p style="font-size: 20px;"><b>Jiafeng Chen</b>&nbsp(<a href="mailto:wynnwy@sjtu.edu.cn">wynnwy@sjtu.edu.cn</a>)</p>
        <p style="font-size: 20px;"><b>Wenbin Ouyang</b>&nbsp(<a href="mailto:ouyangwenbin@sjtu.edu.cn">ouyangwenbin@sjtu.edu.cn</a>)</p>
        <p style="font-size: 20px;"><b>Yijie Shi</b>&nbsp(<a href="mailto:StevenShi2018@sjtu.edu.cn">StevenShi2018@sjtu.edu.cn</a>)</p>
        <p style="font-size: 20px;"><b>Xingjian Zhang</b>&nbsp(<a href="mailto:xingjian_zhang@sjtu.edu.cn">xingjian_zhang@sjtu.edu.cn</a>)</p>
        

        """,
        unsafe_allow_html=True,
    )

    right_info_col.markdown(
        """
        ## Sponsor

        <p style="font-size: 20px;"><b>Dezhi Zhou</b>&nbsp(<a href="mailto:dezhi.zhou@sjtu.edu.cn">dezhi.zhou@sjtu.edu.cn</a>)</p>
         """, unsafe_allow_html=True
    )

    right_info_col.markdown(
        """
        ## Instructor

        <p style="font-size: 20px;"><b>Yulian He</b>&nbsp(<a href="mailto:yulian.he@sjtu.edu.cn">yulian.he@sjtu.edu.cn</a>)</p>
         """, unsafe_allow_html=True
    )

    right_info_col.markdown(
        """
        ## License
        Apache License 2.0
        """
    )

    write_st_end()
