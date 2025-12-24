# core/logic.py
import json
from pathlib import Path
from collections import Counter
from core.data import OPTION_TAGS, QUESTIONS

CAREERS_PATH = "data/careers.json"
QUALS_PATH = "data/qualifications.json"



def _load_json(path: str):
    p = Path(path)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[JSONDecodeError] {path}: {e}")
        return []
    
def load_careers():
    careers = _load_json(CAREERS_PATH)
    for c in careers:
        c.setdefault("quals", [])
        c.setdefault("study", [])
        c.setdefault("pre_decision", [])
        c.setdefault("tags", [])
        c.setdefault("why", "")
        c.setdefault("description", [])
        c.setdefault("name", "")
        c.setdefault("id", "")
        c.setdefault("feasibility", "medium")  # ← 追加：入れ忘れたら medium 扱い
    return careers



def load_quals():
    quals = _load_json(QUALS_PATH)
    by_id = {q["id"]: q for q in quals}
    return by_id


def build_profile(answers: dict, extra_tags: list[str] | None = None) -> dict:
    """answers: {Qid: option_str | list[str]}"""
    tags = []

    for q in QUESTIONS:
        qid = q["id"]
        opt = answers.get(qid)

        if not opt:
            continue

        if isinstance(opt, list):
            for o in opt:
                tags.extend(OPTION_TAGS.get(o, []))
        else:
            tags.extend(OPTION_TAGS.get(opt, []))

    # ✅ 追加：最後の1問などで方向性タグを注入
    if extra_tags:
        tags.extend(extra_tags)

    counts = Counter(tags)

    avoid = [t for t in tags if t.startswith("avoid_")]
    pos = [t for t in tags if not t.startswith("avoid_")]

    top = [t for t, _ in Counter(pos).most_common(4)]
    return {"tags": pos, "avoid": avoid, "top_tags": top, "counts": counts}


FEASIBILITY_BONUS = {
    "easy": 3,
    "medium": 1,
    "learn_required": 0,
}

def score_career(profile: dict, career: dict) -> int:
    counts = profile["counts"]
    score = 0

    for t in career.get("tags", []):
        score += counts.get(t, 0) * 2

    # 避けたいもののペナルティ（既存）
    avoid = profile.get("avoid", [])
    if "avoid_communication" in avoid and "communication" in career.get("tags", []):
        score -= 2
    if "avoid_solo" in avoid and "solo" in career.get("tags", []):
        score -= 1
    if "avoid_structure" in avoid and "structure" in career.get("tags", []):
        score -= 2
    if "avoid_learning" in avoid and "growth" in career.get("tags", []):
        score -= 2

    # ここが追加：叶えやすさ
    f = career.get("feasibility", "medium")
    score += FEASIBILITY_BONUS.get(f, 1)

    return score

def pick_top_careers(profile: dict, k: int = 3) -> list[dict]:
    careers = load_careers()
    if not careers:
       return []

    def _tie_key(c: dict):
        # 同点なら「叶えやすい」→「安定(stable)タグ」→「id」で決める
        f = c.get("feasibility", "medium")
        f_rank = {"easy": 2, "medium": 1, "learn_required": 0}.get(f, 1)
        stable_rank = 1 if "stable" in c.get("tags", []) else 0
        return (f_rank, stable_rank, c.get("id", ""))

    scored = [(score_career(profile, c), c) for c in careers]
    scored.sort(key=lambda x: (x[0],) + _tie_key(x[1]), reverse=True)

    return [c for s, c in scored[:k]]


def explain_match(profile: dict, career: dict) -> str:
    top = set(profile.get("top_tags", []))
    ct = set(career.get("tags", []))
    hit = [t for t in ["research", "build", "care", "planning", "structure", "logic", "communication", "execution", "stable", "growth"]
           if (t in top and t in ct)]
    if hit:
        return "相性の手がかり：" + " / ".join(hit)
    return "相性の手がかり：（今は薄くてOK。試すことで濃くなります）"


def resolve_qual_details(qual_ids: list[str]) -> list[dict]:
    by_id = load_quals()
    out = []
    for qid in qual_ids:
        q = by_id.get(qid)
        if q:
            out.append(q)
        else:
            # IDがない場合でも落ちないように
            out.append({"id": qid, "name": qid, "tags": [], "why": "（資格詳細が未登録）", "trend_note": "", "entry_task": ""})
    return out

# 逆引き関数

def build_qual_to_careers_index() -> dict[str, list[dict]]:
    """
    資格ID -> その資格が quals に含まれている職業リスト（career dict）の辞書を作る
    """
    careers = load_careers()
    index: dict[str, list[dict]] = {}

    for c in careers:
        for qid in c.get("quals", []):
            index.setdefault(qid, []).append(c)

    return index


def get_careers_by_qualification(
    qual_id: str,
    profile: dict | None = None,
    limit: int = 10,
) -> list[dict]:
    """
    1つの資格IDから、その資格で行ける（関連する）職業一覧を返す。
    profile があれば「相性スコア」も加味して並べる。
    """
    index = build_qual_to_careers_index()
    careers = index.get(qual_id, [])

    def _rank_key(c: dict):
        # 叶えやすさを優先（easy > medium > learn_required）
        f = c.get("feasibility", "medium")
        f_rank = {"easy": 2, "medium": 1, "learn_required": 0}.get(f, 1)

        # stable タグがあれば少し優先
        stable_rank = 1 if "stable" in c.get("tags", []) else 0

        # profile があるなら相性スコアも加味
        match = score_career(profile, c) if profile else 0

        # 安定した順序にするため id も入れる
        return (match, f_rank, stable_rank, c.get("id", ""))

    careers_sorted = sorted(careers, key=_rank_key, reverse=True)
    return careers_sorted[:limit]
