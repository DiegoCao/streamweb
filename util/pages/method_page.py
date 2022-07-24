import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64

from ..functions.table import mask_equal
from ..functions.col import pdb_code_col
from ..functions.path import pages_str, data_str, get_file_path
from ..functions.gui import load_st_table, write_st_end, create_st_button, show_st_structure, get_neighbor_path

def method_page():
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.table()
    with col2:
        st.table()

    write_st_end()