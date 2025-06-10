# main.py

# import os
# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.core.audio import SoundLoader
# from kivy.core.image import Image as CoreImage
# from kivy.clock import Clock
# from kivy.graphics import Rectangle
# from kivy.config import Config
# from kivy.core.window import Window
#
# # -------------------------------------------------------------------
# # 如果要在開發階段固定解析度，可以使用下面兩行：
# Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '600')
# FONT_PATH = os.path.join("assets", "fonts", "msjh.ttf")
# # -------------------------------------------------------------------
#
# # 請將 game_logic.py 放在同一資料夾下，並確保它提供 START_ID, get_scene_data, handle_selection
# from game_logic import START_ID, get_scene_data, handle_selection
#
#
# class GameWidget(Widget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#         # 設定初始場景 ID
#         self.current_state = START_ID
#
#         # 儲存當前場景的各種物件
#         self.bg_texture = None
#         self.dialogue_labels = []   # 動態生成的對話 Label
#         self.choice_buttons = []    # 動態生成的按鈕
#         self.sound = None           # 背景音樂的 Sound 物件
#
#         # 1) 頂部：顯示場景標題（如果 JSON 有提供 title 欄位）
#         self.title_label = Label(
#             text="",
#             font_size='24sp',
#             bold=True,
#             color=(1, 1, 0.5, 1),
#             size_hint=(None, None),
#             size=(Window.width, 30),
#             pos=(0, Window.height - 40),
#             halign='center',
#             valign='middle',
#             font_name=FONT_PATH
#         )
#         self.title_label.text_size = (Window.width, None)
#         self.add_widget(self.title_label)
#
#         # 2) 最底部：TextInput 讓使用者可以輸入文字
#         # self.text_input = TextInput(
#         #     multiline=False,
#         #     size_hint=(None, None),
#         #     size=(Window.width * 0.8, 40),
#         #     pos=((Window.width - Window.width * 0.8) / 2, 5),
#         #     font_size='18sp',
#         #     hint_text="在此輸入文字，按下 Enter 提交",
#         #     font_name=FONT_PATH
#         # )
#         # self.text_input.bind(on_text_validate=self.on_text_entered)
#         # 先加入畫面，稍後會 bring_input_to_front()
#         # self.add_widget(self.text_input)
#
#         # 3) 把 TextInput 提到最前面，保證不會被背景或其他元件蓋住
#         # self.bring_input_to_front()
#
#         # 4) 載入第一個場景
#         self.load_scene(self.current_state)
#
#         # 5) 如果需要做動態特效或動畫，可在 update() 中處理
#         Clock.schedule_interval(self.update, 1.0 / 60.0)
#
#     def load_scene(self, state_id):
#         """
#         根據 state_id 取得場景資料並顯示：
#         1. 清除舊有的對話 Label、按鈕、以及停止音樂
#         2. 讀取新的場景資料：title, bg_image, dialogue, sound, choices
#         3. 更新頂端 title_label
#         4. 更新底層背景貼圖 (canvas.before)
#         5. 顯示新的多行對話 (Label)
#         6. 撥放新的背景音樂 (SoundLoader)
#         7. 動態產生互動按鈕 (Button)
#         """
#         # --- 1. 清除舊有物件
#         # 清除對話 Label
#         for lbl in self.dialogue_labels:
#             self.remove_widget(lbl)
#         self.dialogue_labels.clear()
#
#         # 清除互動按鈕
#         for btn in self.choice_buttons:
#             self.remove_widget(btn)
#         self.choice_buttons.clear()
#
#         # 停止舊有音樂
#         if self.sound:
#             self.sound.stop()
#             self.sound = None
#
#         # --- 2. 取得新的場景資料
#         scene = get_scene_data(state_id)
#         title_text = scene.get("title", "")
#         bg_filename = scene.get("bg_image", "")
#         dialogue_lines = scene.get("dialogue", [])
#         bgm_filename = scene.get("sound", "")
#         choices = scene.get("choices", [])
#
#         # --- 3. 更新頂部場景標題
#         self.title_label.text = title_text
#
#         # --- 4. 載入並更新背景貼圖到 canvas.before
#         bg_path = os.path.join("assets", "images", bg_filename)
#         if os.path.isfile(bg_path):
#             self.bg_texture = CoreImage(bg_path).texture
#         else:
#             self.bg_texture = None
#
#         # 先清空 canvas.before
#         self.canvas.before.clear()
#         if self.bg_texture:
#             with self.canvas.before:
#                 # 使用全螢幕大小來繪製背景
#                 Rectangle(texture=self.bg_texture,
#                           pos=self.pos,
#                           size=self.size)
#
#         # --- 5. 顯示多行對話 (Label)
#         base_y = Window.height * 0.5
#         line_height = 100
#         for idx, line in enumerate(dialogue_lines):
#             lbl = Label(
#                 text=line,
#                 font_size='20sp',
#                 color=(1, 1, 1, 1),
#                 size_hint=(None, None),
#                 size=(Window.width - 100, line_height),
#                 pos=(50, base_y + line_height * (len(dialogue_lines) - 1 - idx)),
#                 text_size=(Window.width - 100, None),
#                 halign='left',
#                 valign='middle',
#                 font_name=FONT_PATH
#             )
#             lbl.text_size = (lbl.width, lbl.height)
#             self.add_widget(lbl)
#             self.dialogue_labels.append(lbl)
#
#         # --- 6. 撥放背景音樂 (如果有指定)
#         if bgm_filename:
#             sound_path = os.path.join("assets", "sounds", bgm_filename)
#             if os.path.isfile(sound_path):
#                 self.sound = SoundLoader.load(sound_path)
#                 if self.sound:
#                     self.sound.loop = True
#                     self.sound.play()
#
#         # --- 7. 動態產生互動按鈕 (Button)
#         btn_width = Window.width * 0.8
#         btn_height = 40
#         spacing = 10
#
#         current_y = base_y - 100
#         for choice in choices:
#             next_id = choice.get("next_id")
#             pattern = choice.get("pattern", "")
#             response = choice.get("response", "")
#
#             btn = Button(
#                 text=pattern,
#                 size_hint=(None, None),
#                 size=(btn_width, btn_height),
#                 pos=((Window.width - btn_width) / 2, current_y),
#                 font_size='18sp',
#                 font_name=FONT_PATH
#
#             )
#             btn.next_id = next_id
#             btn.response = response
#             btn.bind(on_press=self.on_choice_pressed)
#
#             self.add_widget(btn)
#             self.choice_buttons.append(btn)
#
#             current_y -= (btn_height + spacing)
#
#         # 確保 TextInput 永遠在最前面
#         # self.bring_input_to_front()
#
#     # def bring_input_to_front(self):
#         """
#         把 TextInput 提到最前面，確保它不會被 Label 或 Button 蓋住
#         """
#         # self.remove_widget(self.text_input)
#         # self.add_widget(self.text_input)
#         # self.text_input.focus = False
#         # self.text_input.canvas.ask_update()
#
#     def on_choice_pressed(self, instance):
#         """
#         處理使用者按下某個選項時的邏輯：
#         1. 先移除目前所有對話 Label
#         2. 顯示該選項的 response（如果不為空）
#         3. 停掉目前音樂
#         4. 延遲 0.5 秒後再切換到下個場景
#         """
#         # 1. 清除目前所有對話 Label
#         for lbl in self.dialogue_labels:
#             self.remove_widget(lbl)
#         self.dialogue_labels.clear()
#
#         # 2. 顯示 response (如果有)
#         response_text = instance.response or ""
#         if response_text:
#             lbl = Label(
#                 text=response_text,
#                 font_size='20sp',
#                 color=(1, 1, 1, 1),
#                 size_hint=(None, None),
#                 size=(Window.width - 100, 30),
#                 pos=(50, Window.height * 0.5),
#                 text_size=(Window.width - 100, None),
#                 halign='left',
#                 valign='middle',
#                 font_name=FONT_PATH
#             )
#             lbl.text_size = (lbl.width, lbl.height)
#             self.add_widget(lbl)
#             self.dialogue_labels.append(lbl)
#
#         # 3. 停止目前音樂
#         if self.sound:
#             self.sound.stop()
#             self.sound = None
#
#         # 4. 延遲 0.5 秒切換場景
#         next_scene_id = instance.next_id
#         Clock.schedule_once(lambda dt: self.load_scene(next_scene_id), 0.5)
#
#     def on_text_entered(self, instance):
#         """
#         處理使用者在 TextInput 中按下 Enter 時的邏輯：
#         1. 讀取 instance.text
#         2. 將文字顯示到畫面上 (中間位置)
#         3. 清空 TextInput
#         4. 如果需要，將文字送回 game_logic 處理 (可自行擴充)
#         """
#         user_text = instance.text.strip()
#         if not user_text:
#             return True
#
#         # 清除舊有的對話 Label
#         for lbl in self.dialogue_labels:
#             self.remove_widget(lbl)
#         self.dialogue_labels.clear()
#
#         # 顯示使用者輸入的文字
#         lbl = Label(
#             text=f"你輸入：{user_text}",
#             font_size='20sp',
#             color=(0.8, 0.8, 1, 1),
#             size_hint=(None, None),
#             size=(Window.width - 100, 30),
#             pos=(50, Window.height * 0.5),
#             text_size=(Window.width - 100, None),
#             halign='left',
#             valign='middle',
#             font_name=FONT_PATH
#         )
#         lbl.text_size = (lbl.width, lbl.height)
#         self.add_widget(lbl)
#         self.dialogue_labels.append(lbl)
#
#         # 清空文字輸入框
#         instance.text = ""
#
#         # 若要把 user_text 傳給遊戲邏輯，可在這裡呼叫自訂函式：
#         # new_state = handle_selection_with_text(self.current_state, user_text)
#         # self.current_state = new_state
#         # self.load_scene(new_state)
#
#         return True  # 阻止事件繼續傳遞
#
#     def update(self, dt):
#         """
#         每一幀更新 (如果需要動畫或特效，可在此處加入)。
#         目前不需重繪背景，因為背景已放到 canvas.before。
#         """
#         pass
#
#
# class MyZombieApp(App):
#     def build(self):
#         return GameWidget()
#
#
# if __name__ == '__main__':
#     MyZombieApp().run()


# main.py

import os
import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.config import Config
from kivy.core.window import Window

# 固定開發解析度
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# 動態選字型：Windows 用 msjh, macOS 用系統黑體, 其他平台用預設
FONT_FILE = os.path.join("assets", "fonts", "msjh.ttf")
from game_logic import START_ID, get_scene_data


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_state = START_ID

        # 背景貼圖、文字 Label、按鈕、音樂
        self.bg_texture = None
        self.dialogue_label = None
        self.choice_buttons = []
        self.sound = None

        # 場景標題
        self.title_label = Label(
            text="",
            font_size='24sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint=(None, None),
            size=(Window.width, 30),
            pos=(0, Window.height - 40),
            halign='center',
            valign='middle',
            font_name=FONT_FILE
        )
        self.title_label.text_size = (Window.width, None)
        self.add_widget(self.title_label)

        # 載入第一個場景
        self.load_scene(self.current_state)

    def load_scene(self, state_id):
        # 1. 清除舊有按鈕、停止音樂、移除文字
        for btn in self.choice_buttons:
            self.remove_widget(btn)
        self.choice_buttons.clear()

        if self.sound:
            self.sound.stop()
            self.sound = None

        if self.dialogue_label:
            self.remove_widget(self.dialogue_label)
            self.dialogue_label = None

        # 2. 取得場景資料
        scene = get_scene_data(state_id)
        title_text = scene.get("title", "")
        bg_filename = scene.get("bg_image", "")
        dialogue_lines = scene.get("dialogue", [])
        bgm_filename = scene.get("sound", "")
        choices = scene.get("choices", [])

        # 3. 更新標題
        self.title_label.text = title_text

        # 4. 背景貼圖放到 canvas.before
        bg_path = os.path.join("assets", "images", bg_filename)
        if os.path.isfile(bg_path):
            self.bg_texture = CoreImage(bg_path).texture
        else:
            self.bg_texture = None

        self.canvas.before.clear()
        if self.bg_texture:
            with self.canvas.before:
                Rectangle(texture=self.bg_texture,
                          pos=self.pos,
                          size=self.size)

        # 5. 合併對話並自動換行
        text = "\n".join(dialogue_lines)
        if text:
            lbl = Label(
                text=text,
                font_size='20sp',
                color=(1, 1, 1, 1),
                size_hint=(None, None),
                width=Window.width - 100,            # 留 50px 邊距
                text_size=(Window.width - 100, None),# 自動換行
                halign='left',
                valign='top',
                font_name=FONT_FILE
            )
            lbl.texture_update()
            lbl.height = lbl.texture_size[1]
            lbl.pos = (50, Window.height - 80 - lbl.height)
            self.add_widget(lbl)
            self.dialogue_label = lbl

        # 6. 撥放背景音樂
        if bgm_filename:
            sound_path = os.path.join("assets", "sounds", bgm_filename)
            if os.path.isfile(sound_path):
                self.sound = SoundLoader.load(sound_path)
                if self.sound:
                    self.sound.loop = True
                    self.sound.play()

        # 7. 建立按鈕，固定放在畫面下方
        btn_w = Window.width * 0.8
        btn_h = 40
        spacing = 10
        # 按鈕從底部 y = 20 開始往上排
        current_y = 20
        for choice in choices:
            next_id = choice.get("next_id")
            pattern = choice.get("pattern", "")

            btn = Button(
                text=pattern,
                size_hint=(None, None),
                size=(btn_w, btn_h),
                pos=((Window.width - btn_w) / 2, current_y),
                font_size='18sp',
                font_name=FONT_FILE
            )
            btn.next_id = next_id
            btn.bind(on_press=self.on_choice)
            self.add_widget(btn)
            self.choice_buttons.append(btn)

            current_y += btn_h + spacing

    def on_choice(self, btn):
        # 切換到下一個場景
        self.current_state = btn.next_id
        self.load_scene(self.current_state)


class MyZombieApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    MyZombieApp().run()
