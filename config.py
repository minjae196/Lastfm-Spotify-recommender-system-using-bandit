import streamlit as st
import os
from dotenv import load_dotenv

# 로컬에서는 .env 로딩
load_dotenv()

# st.secrets 먼저 시도하고, 없으면 os.getenv() 사용
LASTFM_API_KEY = st.secrets.get("LASTFM_API_KEY", os.getenv("LASTFM_API_KEY"))
SPOTIFY_CLIENT_ID = st.secrets.get("SPOTIFY_CLIENT_ID", os.getenv("SPOTIFY_CLIENT_ID"))
SPOTIFY_CLIENT_SECRET = st.secrets.get("SPOTIFY_CLIENT_SECRET", os.getenv("SPOTIFY_CLIENT_SECRET"))
SPOTIFY_REDIRECT_URI = st.secrets.get("SPOTIFY_REDIRECT_URI", os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8501"))
SPOTIFY_ACCESS_TOKEN = st.secrets.get("SPOTIFY_ACCESS_TOKEN", os.getenv("SPOTIFY_ACCESS_TOKEN", ""))