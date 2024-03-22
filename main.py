import streamlit as st


st.set_page_config(
    page_title="Draup Research Tools",
    page_icon="favicon-96.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
     'About': "# This is a header. This is an *extremely* cool app!"
    }
)

#Title Logo
st.image('draup-logo.svg',width = 100)

#Title
st.header('Draup Research Tools',divider='rainbow')


with st.container(border=True,):
     st.subheader('Keyword Match Tools')
     st.write("Description about the tool")
     #st.page_link('pages\Keyword Match Tool.py')

with st.container(border=True):
     st.subheader('MSFT Tool')
     st.write("Description about the tool")

   
   







# Footer bar
footer="""<style>
.footer {position: fixed; left: 0; bottom: -17px; width: 100%; background-color: #65cff6; color: black; text-align: center; }</style>
<div class="footer"><p>Copyright © 2024 Draup. All Rights Reserved.</p></div>
"""
st.markdown(footer,unsafe_allow_html=True)
