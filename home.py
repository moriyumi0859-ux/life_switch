# home.py（ルート直下）
import base64
from pathlib import Path
import streamlit as st

# 1. ページ設定を一番最初に
st.set_page_config(page_title="人生のスイッチ", layout="centered")

# 2. 【改善】動画ロード前の白飛びを防ぎ、サイドバーを即座に消すCSS
st.markdown(
    """
    <style>
    /* アプリ全体を最初から暗くしておく */
    .stApp {
        background-color: #0e1117; 
    }
    /* 読み込み中のスケルトン（グレーの枠）を非表示にする */
    div[data-testid="stSkeleton"] {
        display: none !important;
    }
    /* サイドバーを完全に非表示 */
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="stSidebarCollapsedControl"] { display: none !important; }

    /* 背景動画のスタイル */
    .bg-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        object-fit: cover;
        filter: brightness(0.55);
    }
    
    /* タイトルの光るエフェクト */
    .glow-title {
        color: white !important;
        font-size: 64px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.05em;
        text-shadow:
            0 0 8px rgba(255,255,255,0.7),
            0 0 18px rgba(255,255,255,0.6),
            0 0 36px rgba(255,215,150,0.5);
    }

    /* ボタンのカスタマイズ */
    div.stButton > button {
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
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 248, 230, 0.95), rgba(255, 220, 160, 0.95)) !important;
        box-shadow: 0 6px 16px rgba(255, 235, 200, 0.9), 0 0 32px rgba(255, 250, 230, 0.9) !important;
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. 動画ファイルの読み込み
BASE_DIR = Path(__file__).resolve().parent
VIDEO_PATH = BASE_DIR / "assets" / "video" / "background.mp4"

if not VIDEO_PATH.exists():
    st.error("動画ファイルが見つかりませんでした。")
    st.stop()

video_bytes = VIDEO_PATH.read_bytes()
video_b64 = base64.b64encode(video_bytes).decode()

# 4. 背景動画の配置
st.markdown(
    f"""
    <video autoplay muted loop playsinline class="bg-video">
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# 5. コンテンツ表示
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

# 6. 開始ボタン
if st.button("▶ はじめる", use_container_width=True):
    st.switch_page("pages/app.py")