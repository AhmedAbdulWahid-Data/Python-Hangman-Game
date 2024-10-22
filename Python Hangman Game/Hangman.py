import pygame
import random

# initialize pygame
pygame.init()

# setup display
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 50)

# load images
images = []
for i in range(7):
    image = pygame.image.load(f"images/hangman{i}.png")
    images.append(image)

# game variables
hangman_status = 0
words = ["PYTHON", "SQL", "HTML", "CSS", "JAVASCRIPT"]
word = random.choice(words)
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# setup game loop
FPS = 60
clock = pygame.time.Clock()
start_game = False  # Variable to check if the game has started

def draw():
    win.fill(WHITE)

    if not start_game:
        # display 'Click to Play' before the game starts
        text = TITLE_FONT.render("Click to Play", 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        return

    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
        else:
            pygame.draw.circle(win, RED if ltr not in word else GREEN, (x, y), RADIUS, 0)

    # draw hangman
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def reset_game():
    global hangman_status, word, guessed, start_game
    hangman_status = 0
    word = random.choice(words)
    guessed = []
    start_game = False  # Reset to show 'Click to Play'
    for letter in letters:
        letter[3] = True

def check_game_status():
    won = all(letter in guessed for letter in word)
    if won:
        display_message("You WON! Play Again?")
        return True
    if hangman_status == 6:
        display_message(f"You LOST! The word was {word}.")
        return True
    return False

def main():
    global hangman_status, start_game

    run = True
    while run:
        clock.tick(FPS)

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not start_game:  # Check if the player needs to click to start the game
                    start_game = True
                else:
                    pos = pygame.mouse.get_pos()
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible:
                            dis = pygame.math.Vector2(pos).distance_to((x, y))
                            if dis < RADIUS:
                                letter[3] = False
                                if ltr in word:
                                    guessed.append(ltr)
                                else:
                                    hangman_status += 1

        if start_game and check_game_status():
            reset_game()

    pygame.quit()

main()