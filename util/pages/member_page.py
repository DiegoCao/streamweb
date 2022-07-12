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
    write_st_end()
