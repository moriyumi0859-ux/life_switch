# core/data.py
ENDING_DEFAULT_ON = True

# 5つの質問（全部 "single"）
QUESTIONS = [
    {
        "id": "Q1",
        "title": "時間を忘れやすいのはどれですか？",
        "hint": "迷ったら「近いもの」でOK",
        "type": "single",
        "options": [
            "調べて整理する",
            "手を動かして作る",
            "人の話を聴いて支える",
            "アイデアを考えて企画する",
            "数値やルールで整える",
        ],
    },
    {
        "id": "Q2",
        "title": "どんな環境だと力が出やすいですか？",
        "hint": "理想というより「出やすい」を選ぶ",
        "type": "single",
        "options": [
            "一人で集中",
            "人と会話しながら",
            "締切があると燃える",
            "自由度が高いと伸びる",
            "ルールがあると安心",
        ],
    },
    {
        "id": "Q3",
        "title": "周りから頼まれがちなことは？",
        "hint": "過去の事実ベースで",
        "type": "single",
        "options": [
            "調べてまとめる",
            "作業を確実に進める",
            "相談に乗る",
            "調整して場を整える",
            "判断して決める",
        ],
    },
    {
        "id": "Q4",
        "title": "仕事で一番避けたいのは？",
        "hint": "嫌なものが分かると選びやすい",
        "type": "single",
        "options": [
            "人と話し続けること",
            "一人で黙々が多いこと",
            "数字や規則が多いこと",
            "曖昧で正解がないこと",
            "学び続ける必要があること",
        ],
    },
    {
        "id": "Q5",
        "title": "いま一番ほしいのは？",
        "hint": "今の気持ちでOK",
        "type": "single",
        "options": [
            "安定",
            "成長",
            "自由な働き方",
            "人の役に立つ実感",
            "評価・達成感",
        ],
    },
]

# 選択肢 → タグ（スコア用）
OPTION_TAGS = {
    # Q1
    "調べて整理する": ["research", "logic"],
    "手を動かして作る": ["build", "execution"],
    "人の話を聴いて支える": ["care", "communication"],
    "アイデアを考えて企画する": ["planning", "overview"],
    "数値やルールで整える": ["structure", "execution", "logic"],

    # Q2
    "一人で集中": ["solo"],
    "人と会話しながら": ["communication"],
    "締切があると燃える": ["deadline", "execution"],
    "自由度が高いと伸びる": ["autonomy", "planning"],
    "ルールがあると安心": ["structure"],

    # Q3
    "調べてまとめる": ["research", "writing", "logic"],
    "作業を確実に進める": ["execution", "reliable"],
    "相談に乗る": ["care", "communication"],
    "調整して場を整える": ["coordination", "overview", "communication"],
    "判断して決める": ["decision", "overview"],

    # Q4（避けたい＝ペナルティにする）
    "人と話し続けること": ["avoid_communication"],
    "一人で黙々が多いこと": ["avoid_solo"],
    "数字や規則が多いこと": ["avoid_structure"],
    "曖昧で正解がないこと": ["avoid_ambiguity"],
    "学び続ける必要があること": ["avoid_learning"],

    # Q5
    "安定": ["stable"],
    "成長": ["growth"],
    "自由な働き方": ["flexible"],
    "人の役に立つ実感": ["service"],
    "評価・達成感": ["achievement"],
}
