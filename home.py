# home.py（ルート直下）
import base64
from pathlib import Path
import streamlit as st

# 1. ページ設定
st.set_page_config(page_title="人生のスイッチ", layout="centered")

# 2. 動画ファイルの読み込み（先にデータを準備します）
BASE_DIR = Path(__file__).resolve().parent
VIDEO_PATH = BASE_DIR / "assets" / "video" / "background.mp4"

if not VIDEO_PATH.exists():
    st.error("動画ファイルが見つかりませんでした。")
    st.stop()

video_bytes = VIDEO_PATH.read_bytes()
video_b64 = base64.b64encode(video_bytes).decode()

# 3. CSSと動画を一度に流し込む（ここがポイントです）
st.markdown(
    f"""
    <style>
    /* アプリ全体の設定：最初は黒、動画が読み込まれたら透明に */
    .stApp {{
        background-color: #0e1117;
    }}
    
    /* 動画の配置設定 */
    .bg-video {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1; /* タイトルより後ろ */
        object-fit: cover;
        filter: brightness(0.55);
    }}

    /* 読み込み中の余計な要素を隠す */
    div[data-testid="stSkeleton"] {{ display: none !important; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}
    button[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

    /* タイトルの光るエフェクト */
    .glow-title {{
        color: white !important;
        font-size: 64px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.05em;
        text-shadow:
            0 0 8px rgba(255,255,255,0.7),
            0 0 18px rgba(255,255,255,0.6),
            0 0 36px rgba(255,215,150,0.5);
    }}

    /* ボタンのカスタマイズ */
    div.stButton > button {{
        width: 100%;
        padding: 16px 0 !important;
        margin-top: 30px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #3a2a00 !important;
        background: linear-gradient(135deg, rgba(255, 243, 214, 0.88), rgba(255, 210, 127, 0.88)) !important;
        border-radius: 999px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 230, 180, 0.6), 0 0 24px rgba(255, 245, 220, 0.6) !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
    }}
    </style>

    <video autoplay muted loop playsinline class="bg-video">
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# 4. コンテンツ表示
st.markdown(
    """
    <div style="text-align:center; margin-top:120px;">
        <h1 class="glow-title">人生のスイッチ</h1>
        <p style="font-size:18px; margin-top:20px; color:white;">
            迷いの中にいるあなたへ。人生のヒントを一緒に見つけます。<br>
            人生のスイッチはすぐそこに…さあ、道を開いてスタートしましょう！
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# 5. 開始ボタン
if st.button("▶ はじめる", use_container_width=True):
    st.switch_page("pages/app.py")