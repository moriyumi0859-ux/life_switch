# =========================
# 職業群 / スコア / 表示用
# =========================
JOB_GROUPS = {
    "analysis": "分析・数値・チェック系",
    "admin": "事務・正確性重視系",
    "it_support": "改善・ITサポート系",
    "support": "対人支援・相談系",
    "public": "公共・安定支援系",
    "management": "管理・運用・調整系",
    "creative": "企画・発信・変化系",
}

SCORE_MAP = {
    "Q1": {  # 仕事スタイル
        "A": {"analysis": 2, "creative": 1},
        "B": {"admin": 2, "analysis": 1},
        "C": {"support": 2},
        "D": {"it_support": 2, "management": 1},
    },
    "Q2": {  # 大切にしたいこと
        "A": {"analysis": 2},
        "B": {"admin": 2, "public": 1},
        "C": {"support": 2},
        "D": {"management": 2, "it_support": 1},
    },
    "Q3": {  # 人との距離
        "A": {"analysis": 2, "it_support": 1},
        "B": {"it_support": 2, "management": 1},
        "C": {"support": 2},
        "D": {"public": 2, "admin": 1},
    },
    "Q4": {  # 変化へのスタンス
        "A": {"creative": 2, "it_support": 1},
        "B": {"admin": 2, "public": 1},
        "C": {"support": 2},
        "D": {"it_support": 2, "management": 1},
    },
    "Q5": {  # やりがい
        "A": {"analysis": 2, "creative": 1},
        "B": {"admin": 2, "management": 1},
        "C": {"support": 2},
        "D": {"it_support": 2, "management": 1},
    },
}

# 5問（本番UIに合わせて dict 形式）
QUESTIONS_SCORE = [
    {
        "id": "Q1",
        "title": "仕事をしていて心地いいのは？",
        "hint": "",
        "options": [
            "A. データや情報を整理して、考える時間がある",
            "B. 決まった流れに沿って、正確に進める",
            "C. 人とやり取りしながら、状況に対応する",
            "D. 仕組みや環境を整えて、全体を支える",
        ],
    },
    {
        "id": "Q2",
        "title": "仕事で一番大切にしたいのは？",
        "hint": "",
        "options": [
            "A. 数字や事実の正しさ",
            "B. ルール・手順を守ること",
            "C. 相手の安心感・信頼感",
            "D. トラブルを未然に防ぐこと",
        ],
    },
    {
        "id": "Q3",
        "title": "人との距離感で近いのは？",
        "hint": "",
        "options": [
            "A. 基本は一人、必要な時だけ連携",
            "B. 少人数・決まった相手と関わる",
            "C. その場その場で、いろいろな人と関わる",
            "D. 表に出ず、裏から支える",
        ],
    },
    {
        "id": "Q4",
        "title": "仕事の変化についてどう感じますか？",
        "hint": "",
        "options": [
            "A. 新しいやり方を考えるのは楽しい",
            "B. 変化はある程度決まっている方が安心",
            "C. 相手や状況に応じて変わるのは自然",
            "D. 自分が変化を支える側でいたい",
        ],
    },
    {
        "id": "Q5",
        "title": "「この仕事やっててよかった」と思うのは？",
        "hint": "",
        "options": [
            "A. 数字や結果で貢献が見えたとき",
            "B. ミスなく終えられたとき",
            "C. 誰かに感謝されたとき",
            "D. 全体がスムーズに回ったとき",
        ],
    },
]

# 広がり型の保険（最後の1問）
FINAL_FOCUS = {
    "A": ("一人で落ち着いて、考える時間を大切にしたい", ["analysis", "admin", "creative"]),
    "B": ("人やチームと関わりながら、動いていきたい", ["support", "management", "it_support"]),
    "C": ("誰かの役に立っている実感を強く感じたい", ["support", "public", "admin"]),
    "D": ("新しいことを試しながら、変化を楽しみたい", ["creative", "it_support", "analysis"]),
}

# 職業群 → 職業名（本番はこの職業名で careers.json を引く）
JOB_EXAMPLES = {
    "analysis": [
        "data_analyst",
        "accounting",
        "audit_assistant",
        "compliance_assistant",
        "procurement_admin",
    ],
    "admin": [
        "office_admin",
        "medical_office",
        "school_admin",
        "insurance_clerk",
        "logistics_admin",
    ],
    "it_support": [
        "internal_se",
        "dx_support",
        "helpdesk_l1",
        "data_operator",
        "knowledge_management",
    ],
    "support": [
        "career_support",
        "welfare_staff",
        "childcare_worker",
        "municipal_service_counter",
        "customer_success_support",
    ],
    "public": [
        "library_staff",
        "public_admin",
        "school_admin",
        "industry_office_specialist",
    ],
    "management": [
        "building_facility_management",
        "property_management",
        "bpo_management",
        "management_role",
        "health_safety_admin",
    ],
    "creative": [
        "web_engineer",
        "digital_marketing",
        "internal_training_support",
        "process_manual_design",
    ],
}



def init_scores():
    return {k: 0 for k in JOB_GROUPS.keys()}


def calculate_scores(answers: dict):
    """
    answers: {"Q1": "A", ...}
    """
    scores = init_scores()
    for qid, choice in answers.items():
        for group, point in SCORE_MAP[qid][choice].items():
            scores[group] += point
    return scores


def judge_result(scores: dict):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top, second = sorted_scores[0], sorted_scores[1]

    if top[1] - second[1] >= 3:
        return {"type": "single", "sorted": sorted_scores}
    if top[1] - second[1] <= 2:
        return {"type": "dual", "sorted": sorted_scores}
    return {"type": "broad", "sorted": sorted_scores}


def top_career_ids_for_groups(groups: list[str], k_each: int = 2, limit: int = 3) -> list[str]:
    results = []
    for g in groups:
        results.extend(JOB_EXAMPLES.get(g, [])[:k_each])

    # 重複除去（順序維持）
    seen = set()
    uniq = []
    for x in results:
        if x not in seen:
            seen.add(x)
            uniq.append(x)

    return uniq[:limit]
