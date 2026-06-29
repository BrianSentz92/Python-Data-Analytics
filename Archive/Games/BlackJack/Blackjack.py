import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random

# Card data
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
          '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.card_images = self.generate_card_images()
        self.player_score = 0
        self.dealer_score = 0
        self.game_over = False

        self.score_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)

        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack(pady=10)

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.reset_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.status_label.pack()

        self.new_game()

    def create_deck(self):
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def generate_card_images(self):
        images = {}
        for rank in ranks:
            for suit in suits:
                img = Image.new("RGB", (70, 100), "white")
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()

                symbol = symbols[suit]
                color = "red" if suit in ['Hearts', 'Diamonds'] else "black"
                draw.rectangle([0, 0, 69, 99], outline="black", width=2)
                draw.text((10, 10), f"{rank}", fill=color, font=font)
                draw.text((10, 50), symbol, fill=color, font=font)
                images[(rank, suit)] = ImageTk.PhotoImage(img)
        return images

    def deal_card(self):
        return self.deck.pop()

    def calculate_score(self, hand):
        score = sum(values[rank] for rank, _ in hand)
        ace_count = sum(1 for rank, _ in hand if rank == 'A')
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def update_ui(self):
        for frame in [self.player_frame, self.dealer_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        for card in self.player_hand:
            tk.Label(self.player_frame, image=self.card_images[card]).pack(side=tk.LEFT)

        for card in self.dealer_hand:
            tk.Label(self.dealer_frame, image=self.card_images[card]).pack(side=tk.LEFT)

        self.player_score = self.calculate_score(self.player_hand)
        self.dealer_score = self.calculate_score(self.dealer_hand)
        self.score_label.config(text=f"Player: {self.player_score} | Dealer: {self.dealer_score}")

    def hit(self):
        if self.game_over:
            return
        self.player_hand.append(self.deal_card())
        self.update_ui()
        if self.player_score > 21:
            self.end_game("Player busts! Dealer wins.")

    def stand(self):
        if self.game_over:
            return
        while self.dealer_score < 17:
            self.dealer_hand.append(self.deal_card())
            self.dealer_score = self.calculate_score(self.dealer_hand)
        self.update_ui()
        if self.dealer_score > 21:
            self.end_game("Dealer busts! Player wins.")
        elif self.dealer_score >= self.player_score:
            self.end_game("Dealer wins.")
        else:
            self.end_game("Player wins.")

    def end_game(self, result):
        self.status_label.config(text=result)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.game_over = True

    def new_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.status_label.config(text="")
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.game_over = False
        self.update_ui()


root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()
