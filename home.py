# home.py（ルート直下）
import base64
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="人生のスイッチ", layout="centered")

# --- 修正1: データの読み込み前に「見た目」だけ先に決める ---
st.markdown(
    """
    <style>
    /* アプリが立ち上がった瞬間、背景を白ではなく黒めにする */
    .stApp { background-color: #0e1117; }
    /* サイドバーを即座に隠す */
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="stSidebarCollapsedControl"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ home.py の場所を起点に assets/video/background.mp4 を探す
BASE_DIR = Path(__file__).resolve().parent
VIDEO_PATH = BASE_DIR / "assets" / "video" / "background.mp4"

st.markdown(
    """
    <style>
    /* スマホで横揺れ（横スクロール）が発生するのを防ぐ */
    html, body {
        overflow-x: hidden;
    }
    /* 画像やカードが画面幅を突き抜けないようにする */
    img, div[data-testid="stVerticalBlockBorderWrapper"] {
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ ファイルが無い場合に分かりやすく表示（落とさない）
if not VIDEO_PATH.exists():
    st.error("動画ファイルが見つかりませんでした。")
    st.write("探している場所:", str(VIDEO_PATH))
    st.write("フォルダの中身:", [p.name for p in (BASE_DIR / "assets" / "video").glob("*")] if (BASE_DIR / "assets" / "video").exists() else "assets/video フォルダ自体がありません")
    st.stop()

video_bytes = VIDEO_PATH.read_bytes()
video_b64 = base64.b64encode(video_bytes).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background: transparent;
    }}
    .bg-video {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        object-fit: cover;
        filter: brightness(0.55);
    }}
    </style>

    <video autoplay muted loop playsinline class="bg-video">
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .glow-title {
        color: white !important;   /* ← ここが重要 */
        font-size: 64px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.05em;
        text-shadow:
            0 0 8px rgba(255,255,255,0.7),
            0 0 18px rgba(255,255,255,0.6),
            0 0 36px rgba(255,215,150,0.5);
    }
    </style>

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

# ---- ここから：ボタン見た目CSS（1回だけ）----
st.markdown(
    """
    <style>
    /* Streamlitのボタン全体を、homeページだけそれっぽくする */
    div.stButton > button {
        width: 100%;
        padding: 16px 0 !important;
        margin-top: 30px !important;

        font-size: 18px !important;
        font-weight: 700 !important;

        color: #3a2a00 !important;
        background: linear-gradient(
            135deg,
            rgba(255, 243, 214, 0.88),
            rgba(255, 210, 127, 0.88)
        ) !important;

        border-radius: 999px !important;
        border: none !important;

        box-shadow:
            0 4px 12px rgba(255, 230, 180, 0.6),
            0 0 24px rgba(255, 245, 220, 0.6) !important;

        cursor: pointer !important;
        transition: all 0.25s ease !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(
            135deg,
            rgba(255, 248, 230, 0.95),
            rgba(255, 220, 160, 0.95)
        ) !important;
        box-shadow:
            0 6px 16px rgba(255, 235, 200, 0.9),
            0 0 32px rgba(255, 250, 230, 0.9) !important;
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---- ここまで：ボタン見た目CSS ----
st.markdown(
    """
    <style>
    /* サイドバーそのものを非表示 */
    section[data-testid="stSidebar"] {display: none !important;}

    /* サイドバーを開く「>」ボタンも消す */
    button[data-testid="stSidebarCollapsedControl"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ 遷移は必ず st.switch_page で
if st.button("▶ はじめる", use_container_width=True):
    st.switch_page("pages/app.py")
