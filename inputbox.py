""" by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to
"""

import string
import pygame
import pygame.font
import pygame.event
import pygame.draw

def get_key():
    """
    Returns which key got pressed
    """
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass

def display_box(screen, message):
    """
    Print a message in a box in the middle of the screen
    """
    fontobject = pygame.font.Font(None, 25)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)

    if len(message) != 0:
        screen.fill((0, 0, 0))
        label = fontobject.render(message, 1, (255, 255, 255))
        screen.blit(label, (((screen.get_width() - label.get_rect().width) / 2),
                            ((screen.get_height() - label.get_rect().height) / 2)))
    pygame.display.flip()

def ask(screen, question):
    """
    Asks a questions and captures the answer
    """
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + string.join(current_string, ""))
    while 1:
        inkey = get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey == pygame.K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + string.join(current_string, ""))
    return string.join(current_string, "")
