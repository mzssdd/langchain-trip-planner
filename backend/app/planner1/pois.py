"""Planner POI 关键词、规范化、过滤和排序逻辑。"""

from typing import Any, Dict, List, Optional

from ..models.schemas import TripRequest

CLASSIC_SCENIC_KEYWORDS = [
    "必游景点",
    "著名景点",
    "热门景点",
    "博物馆",
    "历史文化",
    "公园",
]

POI_NOISE_KEYWORDS = [
    "培训",
    "留学",
    "考研",
    "四六级",
    "教育",
    "学校",
    "公司",
    "产业园",
    "批发",
    "市场",
    "建材",
    "房产",
    "维修",
    "物流",
]
EXPERIENCE_ALLOWED_TYPE_KEYWORDS = [
    "风景名胜",
    "博物馆",
    "美术馆",
    "展览馆",
    "科技馆",
    "文化场所",
    "剧场",
    "影剧院",
    "休闲场所",
    "娱乐场所",
    "体育休闲",
]
SCENIC_ALLOWED_TYPE_KEYWORDS = [
    "风景名胜",
    "博物馆",
    "美术馆",
    "展览馆",
    "科技馆",
    "公园",
    "广场",
    "特色商业街",
    "商业街",
    "纪念馆",
    "寺庙",
    "文化场所",
]
ATTRACTION_BUDGET_UPGRADE_KEYWORDS = {
    "comfortable": ["主题公园", "海洋馆", "游船", "夜游", "温泉景区"],
    "premium": ["主题公园", "海洋馆", "旅游度假区", "大型景区", "索道", "游船", "夜游"],
    "luxury": ["主题公园", "旅游度假区", "高端景区", "索道", "游船", "夜游", "滑雪场"],
}
ATTRACTION_PREFERENCE_KEYWORD_MAP = {
    "美食": ["美食街", "小吃街", "特色商业街"],
    "本地美食": ["美食街", "小吃街", "老街"],
    "本地菜": ["老街", "美食街"],
    "特色餐厅": ["美食街", "特色商业街"],
    "老字号": ["老街", "历史街区", "非遗街区"],
    "夜市": ["夜市", "夜市街区", "步行街"],
    "夜市夜景": ["夜市", "夜景街区", "步行街"],
    "城市漫步": ["步行街", "历史街区", "老街", "滨江步道"],
    "购物": ["步行街", "商业街", "特色商业街"],
    "购物商圈": ["步行街", "商业街", "特色商业街"],
}
FOOD_AVOID_KEYWORDS = ["海鲜", "牛肉", "羊肉", "猪肉", "辣", "酒", "生冷"]
FOOD_AVOID_MARKERS = ["过敏", "不吃", "不要", "避免", "忌", "禁忌", "不能吃", "不想吃", "别吃"]
DIET_PREFERENCE_KEYWORDS = ["素食", "清真", "少辣", "本地菜", "海鲜"]
FOOD_BREAKFAST_KEYWORDS = ["早餐", "早点", "早茶", "包子", "粥", "面馆", "糕点", "咖啡"]
FOOD_BASE_KEYWORDS = ["本地菜", "特色餐厅", "老字号", "小吃", "早餐", "简餐"]
FOOD_COMPANION_KEYWORDS = {
    "family_with_children": ["亲子餐厅", "家常菜"],
    "family_with_elders": ["家常菜", "清淡餐厅"],
    "business": ["商务餐厅", "商务宴请", "高端餐厅"],
}
FOOD_BUDGET_KEYWORDS = {
    "limited": ["小吃", "快餐", "简餐"],
    "standard": ["本地菜", "特色餐厅", "老字号"],
    "comfortable": ["精致餐厅", "创意菜", "品质餐厅"],
    "premium": ["高端餐厅", "精致餐厅", "黑珍珠餐厅", "商务餐厅", "品质餐厅"],
    "luxury": ["黑珍珠餐厅", "米其林餐厅", "高端餐厅", "omakase", "法餐"],
}
FOOD_BUDGET_UPGRADE_KEYWORDS = {
    "comfortable": ["精致餐厅", "创意菜", "品质餐厅", "高端餐厅", "私房菜", "融合菜", "商务餐厅"],
    "premium": [
        "高端餐厅",
        "精致餐厅",
        "黑珍珠餐厅",
        "创意菜",
        "私房菜",
        "商务宴请",
        "商务餐厅",
        "品质餐厅",
        "融合菜",
        "高档餐厅",
        "酒店餐厅",
        "宴请餐厅",
    ],
    "luxury": [
        "黑珍珠餐厅",
        "米其林餐厅",
        "高端餐厅",
        "私房菜",
        "omakase",
        "法餐",
        "商务宴请",
        "酒店餐厅",
        "融合菜",
    ],
}
FOOD_BUDGET_SUPPLEMENT_KEYWORDS = {
    "comfortable": ["品质餐厅", "商务餐厅", "融合菜", "私房菜", "酒楼", "中餐厅", "酒店中餐厅"],
    "premium": [
        "商务餐厅",
        "品质餐厅",
        "融合菜",
        "私房菜",
        "酒楼",
        "中餐厅",
        "酒店中餐厅",
        "海鲜餐厅",
        "日料",
        "牛排",
        "西餐厅",
        "火锅",
    ],
    "luxury": [
        "黑珍珠餐厅",
        "米其林餐厅",
        "高端餐厅",
        "酒店中餐厅",
        "海鲜餐厅",
        "日料",
        "牛排",
        "西餐厅",
        "法餐",
        "omakase",
    ],
}
HOTEL_BUDGET_UPGRADE_KEYWORDS = {
    "premium": ["高端酒店", "五星级酒店", "豪华酒店", "度假酒店"],
    "luxury": ["奢华酒店", "五星级酒店", "豪华酒店", "度假酒店"],
}
EXPERIENCE_BUDGET_UPGRADE_KEYWORDS = {
    "comfortable": ["演出", "游船", "夜游", "温泉", "剧场"],
    "premium": ["主题公园", "演出", "实景演出", "沉浸式剧场", "游船", "夜游", "温泉", "滑雪场"],
    "luxury": ["高端体验", "实景演出", "沉浸式剧场", "游船", "夜游", "温泉度假村", "滑雪场"],
}
FOOD_PREFERENCE_KEYWORD_MAP = {
    "美食": ["本地菜", "特色餐厅", "小吃"],
    "本地菜": ["本地菜", "老字号"],
    "特色餐厅": ["特色餐厅", "老字号"],
    "老字号": ["老字号"],
    "夜市": ["夜市", "小吃"],
    "咖啡": ["咖啡"],
    "购物": ["商场餐厅", "特色餐厅"],
    "亲子": ["亲子餐厅", "家常菜"],
    "老人友好": ["家常菜", "清淡餐厅"],
}
FOOD_TAG_KEYWORDS = [
    "本地菜",
    "特色餐厅",
    "老字号",
    "小吃",
    "早餐",
    "早点",
    "早茶",
    "包子",
    "粥",
    "面馆",
    "糕点",
    "简餐",
    "快餐",
    "咖啡",
    "夜市",
    "亲子餐厅",
    "家常菜",
    "清淡餐厅",
    "高端餐厅",
    "精致餐厅",
    "品质餐厅",
    "商务餐厅",
    "商务宴请",
    "黑珍珠",
    "米其林",
    "创意菜",
    "私房菜",
    "法餐",
    "omakase",
    "清真",
    "素食",
    "海鲜",
]
NEGATIVE_PREFERENCE_MARKERS = [
    "过敏",
    "不吃",
    "不要",
    "避免",
    "避开",
    "忌",
    "禁忌",
    "不能",
    "不想",
    "别",
    "少走路",
]


def build_poi_keywords(request: TripRequest, role: str) -> List[str]:
    """根据请求构造稳定的POI搜索关键词。"""
    preferences = positive_preference_tags(request)

    if role == "classic":
        return CLASSIC_SCENIC_KEYWORDS

    if role in {"scenic", "preference"}:
        keywords = build_attraction_preference_keywords(preferences)
        keywords.extend(["景点", "博物馆", "公园"])
        return unique_strings(keywords)[:6]

    if role == "experience":
        keywords = [f"{item}体验" for item in preferences[:2]]
        keywords.extend(["文化体验", "休闲娱乐"])
        return unique_strings(keywords)[:3]

    if role == "food":
        food_constraints = infer_food_constraints(request)
        diet = food_constraints["diet"]
        keywords = []
        if diet and diet != "无":
            keywords.append(diet)
        if any("美食" in item or "餐" in item for item in preferences):
            keywords.extend(preferences)
        keywords.extend(["特色餐厅", "本地菜"])
        return unique_strings(keywords)[:3]

    return ["景点"]

def build_budget_upgrade_keywords(request:TripRequest, role: str) -> List[str]:
    """预算较宽时额外补召回高价景点/体验/餐饮候选。"""
    budget_level = request.budget_constraint.budget_level or ""
    if role in {"scenic", "attraction", "preference"}:
        return ATTRACTION_BUDGET_UPGRADE_KEYWORDS.get(budget_level, [])
    if role == "experience":
        return EXPERIENCE_BUDGET_UPGRADE_KEYWORDS.get(budget_level, [])
    if role == "food":
        if avoids_expensive_food(request):
            return []
        return FOOD_BUDGET_UPGRADE_KEYWORDS.get(budget_level, [])
    return []



def build_attraction_preference_keywords(preferences: List[str]) -> List[str]:
    """把用户偏好转成景点侧关键词，避免把餐饮偏好直接搜成餐厅。"""
    primary_keywords: List[str] = []
    secondary_keywords: List[str] = []
    fallback_keywords: List[str] = []
    for item in preferences:
        mapped = attractopn_keywords_for_preference(item)
        if mapped:
            primary_keywords.append(mapped[0])
            secondary_keywords.append(mapped[1:])
        else:
            fallback_keywords.append(item)
    return unique_strings(primary_keywords + secondary_keywords + fallback_keywords)


def attractopn_keywords_for_preference(preference: str) -> List[str]:
    """返回单个偏好的景点侧搜索词；精确标签优先于包含关系。"""
    if preference in ATTRACTION_PREFERENCE_KEYWORD_MAP:
        return ATTRACTION_PREFERENCE_KEYWORD_MAP[preference]

    keywords: List[str] = []
    for key, values in ATTRACTION_PREFERENCE_KEYWORD_MAP.items():
        if key in preference:
            keywords.extend(values)
    return unique_strings(keywords)


def positive_preference_tags(request: TripRequest) -> List[str]:
    """过滤掉明显的表达，避免拿“海鲜过敏”这类词去正向搜POI。"""
    return [
        item.strip()
        for item in request.preferences
        if item and item.strip() and not is_negative_preference
    ]

def is_negative_preference(value: str) -> bool:
    """判断偏好标签是否是负向约束"""
    text = str(value or "").strip()
    return any(marker in text for marker in NEGATIVE_PREFERENCE_MARKERS)

def unique_strings(values: List[str]) -> List[str]:
    """字符串去重并过滤空值"""
    results = []
    seen = set()
    for value in values:
        value = value.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        results.append(value)
    return results

def infer_food_constraints(request: TripRequest) -> Dict[str, Any]:
    """从偏好和自由文本中拆出饮食偏好和忌口约束"""
    text = " ".join(request.preferences + [request.free_text_input or ""])

    avoid = []
    for keyword in FOOD_AVOID_KEYWORDS:
        if mentions_food_avoidance(text, keyword):
            avoid.append(keyword)

    diet = "无"
    for keyword in DIET_PREFERENCE_KEYWORDS:
        if keyword in avoid:
            continue
        if keyword in text:
            diet = keyword
            break

    return {"diet": diet, "avoid": avoid}


def mentions_food_avoidance(text: str, keyword: str) -> bool:
    """判断某个食物词是否出现在负向饮食表达中"""
    if keyword not in text:
        return False
    for marker in FOOD_AVOID_MARKERS:
        if f"{marker}{keyword}" in text or f"{keyword}{marker}" in text:
            return True
    return False
