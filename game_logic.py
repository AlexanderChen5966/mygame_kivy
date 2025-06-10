# game_logic.py

import os
import json

# JSON 路徑（確保此檔案與 assets 資料夾位於同一層級）
# JSON_PATH = os.path.join("assets", "zombie_interactive_story_fully_ready.json")
JSON_PATH = os.path.join("assets", "zombie_interactive_story_fully_ready3.json")

if not os.path.isfile(JSON_PATH):
    raise FileNotFoundError(f"在 assets 資料夾中找不到 JSON 檔案：{JSON_PATH}")

# 載入整個 JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# raw_data 典型結構：
# {
#   "start_id": 1,
#   "scenes": [
#       {
#         "id": 1,
#         "title": "某個標題",
#         "image": "scene_01.jpg",
#         "sound": "bgm_01.mp3",
#         "text": "場景文字 描述…",
#         "triggers": [
#             {
#               "pattern": "選項 A 文字",
#               "next_id": 2,
#               "response": "點選後顯示的回應…",
#               "fx_image": "fx_default.png",
#               "fx_sound": "Click.ogg"
#             },
#             …
#         ]
#       },
#       …
#   ]
# }

# 建立 SCENES 字典：key = scene id（int），value = 該場景 dict
SCENES = {}
for scene in raw_data.get("scenes", []):
    scene_id = scene.get("id")
    if scene_id is not None:
        SCENES[scene_id] = scene

# 確認 start_id 在 SCENES 中
START_ID = raw_data.get("start_id")
if START_ID not in SCENES:
    raise KeyError(f"在 SCENES 中找不到 start_id={START_ID} 這個場景。")


def get_scene_data(state_id):
    """
    根據 state_id (int) 回傳該場景要用的資料：
      - bg_image: 場景背景圖檔名稱 (str)，放在 assets/images/ 下
      - dialogue: 場景主文本 (list[str])，將 scene["text"] 包成只有一行的 list
      - sound: 場景背景音樂檔名稱 (str)，放在 assets/sounds/ 下
      - choices: list[dict]，每個 dict 包含：
          {
            "next_id": 下一個場景 id (int),
            "pattern": 這個選項要顯示在按鈕上的文字 (str),
            "response": 點選此選項時要顯示的回應文字 (str, 可為空串)
          }
    如果 state_id 不存在，會拋出 KeyError。
    """
    if state_id not in SCENES:
        raise KeyError(f"在 SCENES 中找不到場景 id：{state_id}")

    scene = SCENES[state_id]

    # 背景圖片檔名 (scene["image"])
    bg_image = scene.get("image", "")

    # 將單行 "text" 包成 list，方便 main.py 一律用 list 來顯示多行文字
    # 如果你之後想讓同一場景有多行文字，就在這裡拆成多行
    text = scene.get("text", "")
    dialogue = [text] if text else []

    # 背景音樂檔名
    sound = scene.get("sound", "")

    # 互動選項 (triggers)：把原 JSON 的 triggers 內容取出並轉成適合 Kivy 端使用的結構
    # 我們只取關鍵的 next_id、pattern、response
    raw_choices = scene.get("triggers", [])
    choices = []
    for choice in raw_choices:
        next_id = choice.get("next_id")
        pattern = choice.get("pattern", "")
        response = choice.get("response", "")
        if next_id is not None:
            choices.append({
                "next_id": next_id,
                "pattern": pattern,
                "response": response
            })

    return {
        "bg_image": bg_image,
        "dialogue": dialogue,
        "sound": sound,
        "choices": choices
    }


def handle_selection(selected_id):
    """
    返回要切換到的下一個場景 id（int）。
    這裡直接把按鈕傳進來的 next_id 回傳即可，main.py 按鈕事件綁定時，
    就會呼叫這個函式，再決定下一個場景。
    """
    return selected_id


# game_logic.py

# import os
# import json

# JSON 檔放在 assets 資料夾下
# JSON_PATH = os.path.join("assets", "zombie_interactive_story_fully_ready1.json")
# JSON_PATH = os.path.join("assets", "zombie_interactive_story_fully_ready2.json")
# if not os.path.isfile(JSON_PATH):
#     raise FileNotFoundError(f"找不到 JSON：{JSON_PATH}")
#
# # 讀整個檔案為字串
# with open(JSON_PATH, "r", encoding="utf-8") as f:
#     raw_text = f.read()
#
# # 使用 raw_decode 只解析第一個完整 JSON 物件，忽略後續多餘字元
# decoder = json.JSONDecoder()
# raw, idx = decoder.raw_decode(raw_text)
#
# # raw 現在是正確載入的 dict
# START_ID = raw.get("start_id")
# if START_ID is None:
#     raise KeyError("JSON 裡缺少 start_id")
#
# # 建立以 id 為鍵的場景字典
# SCENES = {}
# for s in raw.get("scenes", []):
#     sid = s.get("id")
#     if sid is None:
#         continue
#     SCENES[sid] = s
#
# if START_ID not in SCENES:
#     raise KeyError(f"start_id={START_ID} 不存在於 scenes 裡")
#
# def get_scene_data(scene_id):
#     """
#     回傳 dict 給 main.py：
#       - title: 場景標題 (str)
#       - bg_image: 圖檔名 (str)
#       - dialogue: list[str]
#       - sound: 音樂檔名 (str)
#       - choices: list[{"pattern":str, "next_id":int}]
#     """
#     if scene_id not in SCENES:
#         raise KeyError(f"找不到場景 id={scene_id}")
#
#     s = SCENES[scene_id]
#     title = s.get("title", "")
#     img = s.get("image", "")
#     lines = s.get("dialogue_lines", [])
#     music = s.get("sound", "")
#     raw_choices = s.get("choices", [])
#
#     # 將 choices 轉成 main.py 需要的格式
#     choices = []
#     for c in raw_choices:
#         pat = c.get("pattern", "")
#         nid = c.get("next_id")
#         if nid is not None:
#             choices.append({"pattern": pat, "next_id": nid})
#
#     return {
#         "title": title,
#         "bg_image": img,
#         "dialogue": lines,
#         "sound": music,
#         "choices": choices
#     }
