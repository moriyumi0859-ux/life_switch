import streamlit as st
from ui.styles import inject_css
from core.data import ENDING_DEFAULT_ON
import base64
from pathlib import Path

from core.score_engine import (
    QUESTIONS_SCORE,
    FINAL_FOCUS,
    JOB_GROUPS,
    calculate_scores,
    judge_result,
    top_career_ids_for_groups,   # ← これ
)

from core.logic import (
    load_careers,
    resolve_qual_details,
    get_careers_by_qualification,
)

st.set_page_config(page_title="人生のスイッチ", layout="centered")
inject_css()

FEASIBILITY_LABEL = {
    "easy": "🟢 easy（最短で現実を変えやすい）",
    "medium": "🟡 medium（安定＋専門性を作りやすい）",
    "learn_required": "🔵 learn_required（学習投資は必要だが、道は明確）",
}

FEAS_DOT = {"easy": "🟢", "medium": "🟡", "learn_required": "🔵"}


# =============================
# 背景画像とレイアウトの設定（修正版）
# =============================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def inject_custom_css():
    # 画像パスの指定
    img_path = "assets/images/result_hint.png"
    
    # 画像が存在する場合の背景設定
    if Path(img_path).exists():
        bin_str = get_base64_of_bin_file(img_path)
        bg_style = f'background-image: url("data:image/png;base64,{bin_str}");'
    else:
        bg_style = ""

    st.markdown(
        f"""
        <style>
        /* 背景全体の設定 */
        [data-testid="stAppViewContainer"] {{
            {bg_style}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* メインコンテンツの幅と余白の設定 */
        section[data-testid="stMain"] .block-container {{
            max-width: 860px;
            padding-top: 7rem;
            padding-bottom: 3rem;
        }}
        
        /* コンテンツの背景を透過 */
        [data-testid="stVerticalBlock"] {{
            background-color: rgba(255, 255, 255, 0.0);
        }}
        
        /* カード（border=True）の可読性アップ */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: rgba(255, 255, 255, 0.85); 
            border-radius: 10px;
            padding: 10px;
        }}

        /* サイドバー非表示 */
        section[data-testid="stSidebar"] {{
            display: none !important;
        }}
        button[data-testid="stSidebarCollapsedControl"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 実行
inject_custom_css()

# =============================
# state
# =============================
def init_state():
    st.session_state.setdefault("stage", "q")        # q -> result -> final -> guide -> end
    st.session_state.setdefault("answers", {})       # {"Q1":"A", ...}
    st.session_state.setdefault("q_index", 0)
    st.session_state.setdefault("ending_on", ENDING_DEFAULT_ON)
    st.session_state.setdefault("picked_career", None)
    st.session_state.setdefault("final_focus", None)  # "A"/"B"/"C"/"D" or None
    st.session_state.setdefault("show_debug", False)

def reset_all():
    for k in ["stage", "answers", "q_index", "picked_career", "final_focus"]:
        if k in st.session_state:
            del st.session_state[k]
    init_state()

init_state()

# =============================
# header
# =============================
st.markdown(
    "## 🌱 人生のスイッチ <span style='font-size: 0.7em; color: gray; margin-left: 20px;'>-The Turning Point-</span>", 
    unsafe_allow_html=True
)
st.caption("悩んでいる貴方へ。ここでは『正解』ではなく『最初の一歩』をまずは見つけていきましょう。")

st.divider()

# =============================
# Q stage
# =============================
if st.session_state.stage == "q":
    i = st.session_state.q_index
    q = QUESTIONS_SCORE[i]

    st.markdown(f"### Q{i+1}. {q['title']}")
    st.caption(q.get("hint", ""))

    key = f"ans_{q['id']}"
    if key not in st.session_state and q["id"] in st.session_state.answers:
        # "A" を復元したいので、見た目用に options から再構成
        saved = st.session_state.answers[q["id"]]
        for opt in q["options"]:
            if opt.startswith(saved + "."):
                st.session_state[key] = opt
                break

    ans = st.radio("選んでください", q["options"], index=None, key=key)
    if ans:
        st.session_state.answers[q["id"]] = ans.split(".")[0].strip()

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 最初からやり直す", use_container_width=True):
            reset_all()
            st.rerun()

    with col2:
        label = "次へ ▶" if i < len(QUESTIONS_SCORE) - 1 else "結果を見る ▶"
        if st.button(label, type="primary", use_container_width=True):
            if not st.session_state.answers.get(q["id"]):
                st.warning("回答を1つ選んでください。")
                st.stop()

            if i < len(QUESTIONS_SCORE) - 1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.session_state.stage = "result"
                st.rerun()

# =============================
# result stage
# =============================
if st.session_state.stage == "result":
    # 1. 基礎スコアの計算（常に計算はするが、使い道を分ける）
    scores = calculate_scores(st.session_state.answers)
    verdict = judge_result(scores)

    # 2. 表示するグループの決定
    # final_focus (どれもしっくりこない後の選択) がある場合は、それを最優先する
    if st.session_state.get("final_focus"):
        # FINAL_FOCUS[key][1] に定義されたグループリストを強制使用
        top3_groups = FINAL_FOCUS[st.session_state.final_focus][1]
    else:
        # 通常時
        top3_groups = [g for g, _ in verdict["sorted"][:3]]
        
        # 診断結果が「広すぎる(broad)」かつ、まだ final_focus を選んでいないなら分岐へ
        if verdict["type"] == "broad":
            st.session_state.stage = "final"
            st.rerun()

    # 3. 職業の抽出
    # ★ポイント：k_each を増やしたり、シャッフルを検討するとより変化が出ます
    career_ids = top_career_ids_for_groups(top3_groups, k_each=2, limit=3)

    careers_all = load_careers()
    by_id = {c.get("id", ""): c for c in careers_all}
    careers = [by_id.get(cid) for cid in career_ids]
    careers = [c for c in careers if c]


    if not careers:
        st.error("候補は出ましたが、data/careers.json に同じ id の職業が見つかりませんでした。")
        st.write("候補（career id）:", career_ids)
        st.stop()

    st.markdown("### 【結果】職業候補（3つ）")
    st.caption("断定ではなく候補です。『試してみたい』を1つ選びます。")
    st.info("🟢 easy：最短で現実を変えやすい / 🟡 medium：安定＋専門性 / 🔵 learn_required：要学習だが道は明確")

    if st.session_state.show_debug:
        st.write("上位の方向（最大3）:", [JOB_GROUPS[g] for g in top3_groups])
        st.write("候補（career id）:", career_ids)

    # ✅ ここが「resultの中」に入っているのが重要
    for idx, c in enumerate(careers, 1):
        with st.container(border=True):
            f = c.get("feasibility", "medium")
            dot = FEAS_DOT.get(f, "🟡")

            st.markdown(f"**{idx}. {dot} {c.get('name','')}**")

            desc = c.get("description", [])
            if desc:
                for line in desc:
                    st.write("・" + line)
            else:
                st.caption("（仕事内容の詳しい説明は準備中です）")

            if st.button("この候補で進む ▶", key=f"pick_{c.get('id','')}_{idx}", use_container_width=True):
                st.session_state.picked_career = c
                st.session_state.stage = "guide"
                st.session_state.final_focus = None
                st.rerun()

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 最初からやり直す", use_container_width=True):
            reset_all()
            st.rerun()
    with col2:
        if st.button("🤔 どれもしっくり来ない ▶", use_container_width=True):
            st.session_state.stage = "final"
            st.rerun()

# =============================
# final stage
# =============================
if st.session_state.stage == "final":
    st.markdown("### 【結果】")
    st.caption("最後に一つだけ。今の気分に一番近いものを選んでください。")

    keys = list(FINAL_FOCUS.keys())
    label_list = [f"{k}. {FINAL_FOCUS[k][0]}" for k in keys]
    selected = st.radio("最後の1問", label_list, index=0, key="final_focus_radio")
    focus_key = selected.split(".")[0]
    st.session_state.final_focus = focus_key

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↩︎ 結果一覧へ戻る", use_container_width=True):
            st.session_state.stage = "result"
            st.rerun()
    with col2:
        if st.button("この方向で候補を見る ▶", type="primary", use_container_width=True):
            st.session_state.stage = "result"
            st.rerun()

# =============================
# guide stage（あなたの元のまま）
# =============================
if st.session_state.stage == "guide":
    c = st.session_state.picked_career
    if not c:
        reset_all()
        st.rerun()

    st.markdown("## ✅【初めの一歩／指南】")
    st.markdown(f"### 選んだ候補：{c.get('name','')}")

    f = c.get("feasibility", "medium")
    st.caption(FEASIBILITY_LABEL.get(f, FEASIBILITY_LABEL["medium"]))
    if c.get("why"):
        st.caption(c["why"])

    st.divider()

    st.markdown("### 🔑 必ず必要になる“入口資格”")
    qual_details = resolve_qual_details(c.get("quals", []))

    if not qual_details:
        st.caption("この職業に必須の入口資格は、現在登録されていません。")
    else:
        for q in qual_details:
            with st.container(border=True):
                st.markdown(f"**{q.get('name','')}**")
                st.caption(q.get("why", ""))

                if q.get("trend_note"):
                    st.caption(f"メモ：{q['trend_note']}")
                if q.get("entry_task"):
                    st.markdown(f"✅ **入口タスク**：{q['entry_task']}")

                with st.expander("🔁 この資格で行ける職業（逆引き）", expanded=False):
                    # profile が無いので、profile=None でOK
                    related = get_careers_by_qualification(q["id"], profile=None, limit=8)
                    related = [rc for rc in related if rc.get("id") != c.get("id")]

                    if not related:
                        st.caption("この資格を含む他の職業は、まだ登録されていません。")
                    else:
                        for rc in related:
                            f2 = rc.get("feasibility", "medium")
                            st.markdown(f"**・{rc.get('name','')}**")
                            st.caption(FEASIBILITY_LABEL.get(f2, FEASIBILITY_LABEL["medium"]))
                            if rc.get("why"):
                                st.caption(rc["why"])

    st.divider()

    st.markdown("### 🧭 決定する前に、必ずやった方がいいこと（3つ）")
    pre = c.get("pre_decision", []) or [
        "求人票を3件だけ見て共通点をメモする（10分）",
        "自分が苦痛に感じる点を1行で書く（1分）",
        "今日10分だけ触れてみる（10分）",
    ]
    for t in pre[:3]:
        st.checkbox(t)

    st.divider()

if st.session_state.stage == "guide":
    # ... (既存の career 取得処理などはそのまま) ...

    st.divider()

    st.markdown("### 🌱 今日の最初の一歩（Day1）")
    study = c.get("study", [])
    
    # データの取り出しと具体化
    if study:
        # 配列の1番目をDay1とする
        raw_step = study[0]
        # テキストが短い場合に備えて、具体的な行動を補足する
        display_step = raw_step.replace("Day1:", "").strip()
    else:
        display_step = "ネットで実際の求人情報を1件だけ詳しく見る（条件や年収の確認）"

    # コンテナを使って視覚的に強調
    with st.status("🚀 あなたが今日、10分で完了できること", expanded=True):
        st.write(f"**行動内容：** {display_step}")
        st.write("**目標：** 「自分にもできそうか」の直感を得る")
        st.markdown("""
        **おすすめのやり方：**
        1. スマホで職業名を検索
        2. 体験談ブログやYouTube動画を1つだけ見る
        3. 最後に「自分ならどう思うか」を一言メモする
        """)

    st.success("✨ これを完了したら、今日のあなたのミッションは成功です！")
    st.caption("※ 迷いが残ってもOK。『10分やった事実』で貴方は一歩前進しています")


    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 最初からやり直す", use_container_width=True):
            reset_all()
            st.rerun()
    with col2:
        if st.button("🌙 終了", type="primary", use_container_width=True):
            st.session_state.stage = "end"
            st.rerun()

# =============================
# サイドバー非表示
# =============================

def inject_css():
    st.markdown(
        """
        <style>
        /* サイドバー本体を消す */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* 折りたたみボタン（>）も消す */
        button[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# =============================
# end stage
# =============================
if st.session_state.stage == "end":
    st.markdown("## 🌙 終了")
    if st.session_state.ending_on:
        st.success("今日、あなたは迷いの中でも一歩を選びました。その一歩が、これからを動かしていきます☺️")
    else:
        st.info("今日はここまで。次に開いたとき、今とは少し違う答えが見つかるかもしれません🤓")

    st.divider()
    if st.button("🔁 最初からやり直す", use_container_width=True):
        reset_all()
        st.rerun()
