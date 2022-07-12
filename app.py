# -*- coding: utf-8 -*-
"""
  Copyright 2022 Mitchell Isaac Parker
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from util.pages.member_page import member_page
from util.pages.data_page import data_page
from util.pages.overview_page import overview_page
from util.pages.home_page import home_page
from util.functions.path import get_file_path, get_dir_name, util_str, data_str
from PIL import Image
import streamlit as st
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


# from util.pages.pdb_page import pdb_page
# from util.pages.conformation_page import conformation_page
# from util.pages.mutation_page import mutation_page
# from util.pages.inhibitor_page import inhibitor_page
# from util.pages.query_page import query_page
# from util.pages.classify_page import classify_page


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        img = Image.open(
            get_file_path(
                "rascore_logo.png",
                dir_path=f"{get_dir_name(__file__)}/{util_str}/{data_str}",
            ),
        )

        st.set_page_config(page_title="Energy Plus Demo",
                           page_icon=img, layout="wide")

        st.sidebar.markdown("## Main Menu")
        app = st.sidebar.selectbox(
            "Select Page", self.apps, format_func=lambda app: app["title"]
        )
        st.sidebar.markdown("---")
        app["function"]()


app = MultiApp()

app.add_app("Home Page", home_page)
app.add_app("Group Members", member_page)
app.add_app("System Overview", overview_page)
app.add_app("Result Visualization", data_page)
# app.add_app("Search PDB", pdb_page)
# app.add_app("Explore Conformations", conformation_page)
# app.add_app("Analyze Mutations", mutation_page)
# app.add_app("Compare Inhibitors", inhibitor_page)
# app.add_app("Query Database", query_page)
# app.add_app("Classify Structures", classify_page)

app.run()
