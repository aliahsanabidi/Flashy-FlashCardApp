from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

#---------------------------- Reading relevant files through Pandas -----------------------#
try:
    data = pandas.read_csv("data/data_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/quranic_words.csv")
    # data = pandas.read_csv("data/french_words.csv")

data_dict = data.to_dict(orient="records")
current_card = {}

#---------------------------------- Moving to next card -----------------------------#

def next_card():
    global current_card, flip_timer, data_dict
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(card_background, image=front_card)
    canvas.itemconfig(card_title, text="Arabic", fill="black")
    canvas.itemconfig(card_word, text=current_card["Arabic"], fill="black")
    flip_timer = window.after(3000, func=flip_card)

#---------------------------------- If user knows the answer -----------------------------#
def is_known():
    global data_dict, current_card
    data_dict.remove(current_card)
    data_to_learn = pandas.DataFrame(data_dict)
    data_to_learn.to_csv("data/data_to_learn.csv", index=False)
    next_card()

#---------------------------- Flipping the card to show the answer --------------------------#
def flip_card():
    global data
    global current_card
    canvas.itemconfig(card_background, image=back_card)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

#----------------------------------------- Creating UI -------------------------------------#

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


canvas = Canvas()
canvas.config(bg=BACKGROUND_COLOR, height=526, width=800, highlightthickness=0)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 125, text="Title", font=("Ariel", 45, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

tick_image = PhotoImage(file="images/right.png")
known_button = Button(image=tick_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()


window.mainloop()


