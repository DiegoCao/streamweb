import streamlit as st
from PIL import Image

from ..functions.table import mask_equal
from ..functions.col import pdb_code_col
from ..functions.path import pages_str, data_str, get_file_path
from ..functions.gui import load_st_table, write_st_end, create_st_button, show_st_structure, get_neighbor_path


def member_page():
    img = Image.open(
        get_file_path(
            "bio.png",
            dir_path=get_neighbor_path(__file__, pages_str, data_str),
        )
    )
    st.image(img, output_format="PNG")
    st.write("---")
    st.write("""
             ## Jiafeng Chen
             <p style="font-size: 22px;">Jiafeng Chen is an undergraduate student majoring in Electrical and Computer Engineering at Shanghai Jiao Tong University and Computer Science at the University of
             Michigan. He’s planning to take a gap year and is going to apply for graduate program
             in Fall 2022. His research interest lies in the intersection of music and machine learning, specifically music information retrieval, music recommendation system, and physical
             modelling synthesis. His role in this project is the team leader, who’s responsible for
             managing the overall development process, as well as the simulation and data generation
             pipeline.</p>
             """, unsafe_allow_html=True
             )
    st.write("---")
    st.write("""
             ## Xingjian Zhang
             <p style="font-size: 22px;">Xingjian Zhang is an undergraduate student majoring in Computer Science at the University of Michigan. Besides, he has a dual degree in Electrical and Computer Engineering
             at the Shanghai Jiao Tong University, where he served as a teaching assistant of Prof.
             Horst Hohberger for multiple honors-level math courses. He is going to pursue his Ph.D.
             at the School of Information at the University of Michigan, advised by Prof. Qiaozhu
             Mei. His research interests lie in building fair, explainable, and generalizable machine
             learning systems using causal inference. He has a broad research experience in Learning-
             to-Rank, Graph Neural Network, and Natural Language Processing. He is responsible for
             implementing the data pipeline and machine learning module in this project. (Moreover,
             he designed the team logo.) His powerlifting personal records is 330Lb (Squat), 352Lb
             (Deadlift), 224Lb (Bench Press). His goal for this year is to read a 1000Lb in total.
             Welcome to visit Xingjian Zhang's homepage : <a href="https://xingjian-zhang.notion.site">https://xingjian-zhang.notion.site</a>.</p>
             """, unsafe_allow_html=True
             )
    st.write("---")
    st.write("""
             ## Yijie Shi
             <p style="font-size: 22px;">Yijie Shi is an undergraduate student majoring in Computer Science at the University
            of Michigan and get a dual degree in Electrical and Computer Engineering at Shanghai
            Jiaotong University. He is going to pursue the Master’s degree of Computer Science of
            Engineering at Rackham Graduate School at the University of Michigan. His interest lies
            in machine learning, computer vision and natural language processing. He is responsible
            for simulation and website design.</p>
             """, unsafe_allow_html=True
             )
    st.write("---")
    st.write("""
             ## Wenbin Ouyang
             <p style="font-size: 22px;">Wenbin Ouyang is an undergraduate majoriing in Computer Science at the University of
             Michigan and dual degree in Electrical and Computer Engineering at Shanghai Jiao Tong
             University. He is going to continue his Ph.D. of Civil and Environmental Engineering
             degree at Massachusetts Institute of Technology. His research interest lies in the areas
             of Reinforcement Learning, Combinatorial Optimization and Transportation. He has not
             decided his life-long career, and his goal for this year is to complete one clearance in a
             row in 8 pool.</p>
             """, unsafe_allow_html=True
             )
    st.write("---")
    st.write("""
             ## Hangrui Cao
             <p style="font-size: 22px;">Hangrui Cao is an undergraduate majoring in Computer Science at University of Michigan
             and dual degree in Electrical and Computer Engineering at Shanghai Jiao Tong Univer-
             sity. He is going to pursue a Master of Computational Data Science degree at School of
             Computer Science Department, Carnegie Mellon University. His interest lie in federated
             learning, machine learning optimization, data science and mobile computing, and hopes to
             devote distributed machine learning in future career. He is responsible for the simulation
             and data generation pipeline in this project.
             Here is Hangrui Cao personal website <a href="https://diegocao.github.io/">https://diegocao.github.io/</a>.</p>
             """, unsafe_allow_html=True
             )
    write_st_end()
