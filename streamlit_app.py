import streamlit as st
import logging
from st_pages import add_page_title, get_nav_from_toml

##
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

# streamlit run streamlit_app.py --server.port 18890

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton>button {display: none;}
[data-testid="stToolbar"] {display: none;}
# a[href$="rag_chat"] { pointer-events: none; cursor: default;}
</style>
""", unsafe_allow_html=True)


logger.info("Streamlit application is starting up")

sections = st.sidebar.toggle("Admin Mode", value=False, key="use_sections")

nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if sections else ".streamlit/pages.toml"
)

pg = st.navigation(nav)

add_page_title(pg)

pg.run()