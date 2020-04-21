from game_libs.abstract_objects import Selection, Entity
from game_libs.constants import Constants
import pygame
import sys
from random import randint

pygame.init()
pygame.mixer.init()

windowSize = Constants.WINDOW_SIZE

screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

selection = None
draw_selection = False
drawn_selections = []

# Entities:
entities = [
    Entity(screen, randint(10, Constants.WINDOW_WIDTH - 10), randint(10, Constants.WINDOW_HEIGHT - 10), 10, "random")
    for e in range(80)]
for e in entities:
    e.set_speed(2)

def draw_entities(entities_iterable):
    """
    loop through created entities and draw them on the surface
    """
    for entity in entities_iterable:
        entity.draw()
        if draw_selection:
            entity.in_selection(selection)


def draw_cursor(surface, position):
    """
    draw cursor on selected surface based on passed position
    """
    pygame.draw.rect(surface, (255, 255, 255), (position[0], position[1], 5, 5), 5)


while True:
    clock.tick(60)
    mousePosition = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if not draw_selection:
                selection = Selection(mousePosition[0], mousePosition[1])
                draw_selection = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            draw_selection = False
            drawn_selections.append(selection)
            selection = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            for e in entities:
                if e.get_selection():
                    e.set_target(mousePosition)

    screen.fill((0, 0, 0))

    draw_entities(entities)

    for e in entities:
        if e.randomized == False and e.get_selection() == True:
            e.randomize_color()
            e.randomized = True
        e.goto_position()

    if draw_selection:
        selection.update(mousePosition[0], mousePosition[1])
        selection.draw(screen)

    draw_cursor(screen, mousePosition)

    pygame.display.update()
