import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>
        /* ===== レイアウト全体 ===== */
        section[data-testid="stMain"] .block-container {
            max-width: 860px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .stButton > button {
            border-radius: 14px;
        }

        /* ===== サイドバー完全非表示 ===== */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        button[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        /* ===== 余白調整 ===== */
        section[data-testid="stMain"] {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
