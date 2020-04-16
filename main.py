from game_libs.abstract_objects import Selection
import pygame
import sys

pygame.init()
pygame.mixer.init()

windowSize = (800, 600)

screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

selection = None
draw_selection = False
drawn_selections = []


def draw_cursor(surface, position):
    pygame.draw.rect(surface, (255, 255, 255), (position[0], position[1], 5, 5), 5)


while True:
    clock.tick(40)
    mousePosition = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not draw_selection:
                selection = Selection(mousePosition[0], mousePosition[1])
                draw_selection = True

        if event.type == pygame.MOUSEBUTTONUP:
            draw_selection = False
            drawn_selections.append(selection)
            selection = None

    screen.fill((0, 0, 0))
    draw_cursor(screen, mousePosition)
    if draw_selection:
        selection.update(mousePosition[0], mousePosition[1])
        selection.draw(screen)

    if drawn_selections:
        for s in drawn_selections:
            s.draw(screen)

    pygame.display.update()
