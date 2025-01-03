import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk
import pygame

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("오락실 게임")
        self.root.geometry("600x650")

        pygame.mixer.init()

        # 사운드 파일 로드
        self.joystick_sound = pygame.mixer.Sound("joystick-sound.mp3")
        self.button_sound = pygame.mixer.Sound("button-sound.mp3")
        self.coin_sound = pygame.mixer.Sound("coin-sound.mp3")
        self.background_sound = "background-sound.mp3"

        # 게임 선택 버튼 클릭 횟수 저장 변수
        self.click_counts = {"game1": 0, "game2": 0, "game3": 0}

        # 뱃지 이미지 로드
        self.badge_images = [ImageTk.PhotoImage(Image.open(f"badge_{i}.png")) for i in range(1, 7)]

        # 배경 이미지 로드
        self.background_img = ImageTk.PhotoImage(Image.open("background.png"))

        # canvas 생성 및 배경 이미지 설정
        self.canvas = tk.Canvas(self.root, width=600, height=650)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_img, anchor="nw")

        # 이미지 로드
        self.game1_img = ImageTk.PhotoImage(Image.open("game1.png"))
        self.game2_img = ImageTk.PhotoImage(Image.open("game2.png"))
        self.game3_img = ImageTk.PhotoImage(Image.open("game3.png"))
        self.coin_img = ImageTk.PhotoImage(Image.open("coin.png"))
        self.joystick_img = ImageTk.PhotoImage(Image.open("joystick.png"))
        self.button_img = ImageTk.PhotoImage(Image.open("button.png"))

        # 게임 선택 버튼 생성
        self.game1_button = tk.Button(self.root, image=self.game1_img, command=lambda: self.start_game(1), width=80, height=100, bd=0, highlightthickness=0)
        self.game2_button = tk.Button(self.root, image=self.game2_img, command=lambda: self.start_game(2), width=80, height=100, bd=0, highlightthickness=0)
        self.game3_button = tk.Button(self.root, image=self.game3_img, command=lambda: self.start_game(3), width=80, height=100, bd=0, highlightthickness=0)

        # 게임 선택 버튼 초기 비활성화 상태로 설정
        self.game1_button.place_forget()
        self.game2_button.place_forget()
        self.game3_button.place_forget()

        # 코인 투입, 조이스틱, 버튼 프레임 생성
        self.coin_slot = tk.Button(self.root, image=self.coin_img, command=self.show_game_buttons, width=80, height=100, bd=0, highlightthickness=0)
        self.joystick = tk.Button(self.root, image=self.joystick_img, width=60, height=100, bd=0, highlightthickness=0, command=self.joystick_click)
        self.button = tk.Button(self.root, image=self.button_img, width=150, height=70, bd=0, highlightthickness=0, command=self.button_click)

        # canvas 위에 컨트롤 요소 배치
        middle = 250
        padding = 120
        self.canvas.create_window(120, 515, anchor="nw", window=self.coin_slot)
        self.canvas.create_window(120, 380, anchor="nw", window=self.joystick)
        self.canvas.create_window(330, 405, anchor="nw", window=self.button)

        # 클릭 횟수 표시 라벨
        self.click_text = tk.StringVar()
        self.click_text.set("핑퐁게임: 0  슈팅게임: 0  테트리스: 0")
        self.click_label = tk.Label(self.root, textvariable=self.click_text, font=("Helvetica", 12), bg="white")

        # 배지 라벨 리스트
        self.badge_labels = []

    # 게임 선택 시 호출할 함수
    def start_game(self, game_number):

            if game_number == 1:
                subprocess.Popen(["python3", "pingpong.py"])
                self.click_counts["game1"] += 1
            elif game_number == 2:
                subprocess.Popen(["python3", "shootgame.py"])
                self.click_counts["game2"] += 1
            elif game_number == 3:
                subprocess.Popen(["python3", "tetris.py"])
                self.click_counts["game3"] += 1
                
            self.update_click_counts()  # 클릭 횟수 업데이트
            self.check_click_counts()   # 클릭 횟수 체크

    # 클릭 횟수 업데이트 함수
    def update_click_counts(self):
        self.click_text.set(f"핑퐁게임: {self.click_counts['game1']}  슈팅게임: {self.click_counts['game2']}  테트리스: {self.click_counts['game3']}")

    # 클릭 횟수 체크 함수
    def check_click_counts(self):
        total_clicks = sum(self.click_counts.values())
        if total_clicks == 3:
            self.show_message_and_add_badge("게임을 총 3번 플레이 하셨습니다! - 게임 초보 뱃지 획득")
        elif total_clicks == 6: 
            self.show_message_and_add_badge("게임을 총 6번 플레이 하셨습니다! - 게임 중수 뱃지 획득")
        elif total_clicks == 9:
            self.show_message_and_add_badge("게임을 총 9번이나 플레이 하셨습니다! - 게임 고수 뱃지 획득")
        elif total_clicks == 12:
            self.show_message_and_add_badge("게임을 총 12번 플레이 하셨습니다..! - 게임 마스터 뱃지 획득")
        elif total_clicks == 15:
            self.show_message_and_add_badge("게임을 총 15번째 플레이 중이십니다... - 게임 챌린저 뱃지 획득 ")
        elif total_clicks == 20:
            self.show_message_and_add_badge("엄청나네요! 게임을 총 20번 플레이 하셨습니다! 마지막 뱃지를 받으셨습니다! 축하드립니다! - 게임 중독자 뱃지 획득")

    def show_message_and_add_badge(self, message, warning=False):
        if warning:
            messagebox.showinfo("경고", message)
        else:
            messagebox.showinfo("메시지", message)
        self.add_badge()

    # 배지 추가 함수
    def add_badge(self):
        if len(self.badge_labels) < 6:  # 최대 6개 배지
            badge_label = tk.Label(self.root, image=self.badge_images[len(self.badge_labels)])
            self.badge_labels.append(badge_label)
            self.canvas.create_window(200 + 50 * len(self.badge_labels), 520, anchor="nw", window=badge_label)

    # 코인 슬롯 버튼 클릭 시 호출할 함수
    def show_game_buttons(self):
        self.coin_sound.play()
        messagebox.showinfo("안내", "게임을 여러 번 플레이하며 뱃지를 모아보세요!")  
        self.root.after(650, self.play_background_music)  
        middle = 250
        padding = 120
        self.game1_button.place(x=middle - padding, y=150)
        self.game2_button.place(x=middle, y=150)
        self.game3_button.place(x=middle + padding, y=150)
        if not self.click_label.winfo_ismapped():
            self.canvas.create_window(210, 275, anchor="nw", window=self.click_label)

    # 배경 음악 재생 함수
    def play_background_music(self):
        pygame.mixer.music.load(self.background_sound)
        pygame.mixer.music.play(-1) 

    # 조이스틱 클릭 시 호출할 함수
    def joystick_click(self):
        self.joystick_sound.play()

    # 버튼 클릭 시 호출할 함수
    def button_click(self):
        self.button_sound.play()


# 메인 윈도우 설정
root = tk.Tk()
app = GameApp(root)
root.mainloop()

