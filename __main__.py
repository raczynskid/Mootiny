import sys

import pygame

from game_libs import game_objects
from game_libs import interface
from game_libs.abstract_objects import Selection, MovementGrid
from game_libs.constants import Constants
from game_libs.entity_manager import EntityManager
from game_libs.fx import Weather
from game_libs.sprites import Grass
from game_libs.sprites import font_index

pygame.init()
pygame.mixer.init()
pygame.font.init()

windowSize = Constants.WINDOW_SIZE

screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

selection = None
draw_selection = False
drawn_selections = []
active_build = None
build_time_offset = 0
Constants.FONT = pygame.font.Font(font_index['KnowYourProduct'], 24)
pygame.display.set_caption('Mootiny')

# Entities:
MG = MovementGrid()
weather = Weather()
EM = EntityManager()
for i in range(10):
    EM.create_non_interactive(Grass())

EM.create_random_cow()
EM.create_random_cow()
EM.create_random_cow()
EM.create_random_cow()



# Interface:
bar = interface.InterfaceBar()


def draw_entities(entities_iterable):
    """
    loop through created entities and draw them on the surface
    """
    for entity in entities_iterable:
        try:
            entity.draw_sprite()
            entity.draw_selection_indicator_only()
            if draw_selection:
                entity.in_selection(selection)
        except TypeError:
            entity.draw_sprite(mousePosition)


def draw_cursor(surface, position):
    """
    draw cursor on selected surface based on passed position
    """
    pygame.draw.rect(surface, (255, 255, 255), (position[0], position[1], 5, 5), 5)


if __name__ == "__main__":

    while True:
        # tick the clock, get mouse postion, color the screen
        clock.tick(Constants.FRAMERATE)
        mousePosition = pygame.mouse.get_pos()
        screen.fill((90, 150, 92))

        # draw all non_interactive (background) entities
        EM.draw_non_interactives()

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # LEFT CLICK
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:

                # check if mouse over building, if so add unit to queue (skip if in build mode)
                if not active_build or active_build.is_active():
                    EM.check_for_new_orders(mousePosition)

                # if no selection is being drawn, start drawing new selection
                if not draw_selection:
                    selection = Selection(mousePosition[0], mousePosition[1])
                    draw_selection = True

                # check if mouse is hovering over any construction build buttons
                # if yes, add new building to entity manager and set build mode on
                if bar.check_build(mousePosition) == 'barn':
                    EM.create_building(game_objects.Barn((600, 500), 2))
                    active_build = EM.buildings[-1]
                    active_build.set_build_mode(True)


                # if active build is in progress and offset time elapsed, place building on keypress
                if active_build and active_build.is_build_mode():
                    if build_time_offset > (Constants.FRAMERATE / 3):
                        active_build.build(mousePosition)
                        nd = MG.get_row_column_by_pixel_coords(mousePosition)
                        nodes_to_close = [nd, (nd[0] + 1, nd[1]), (nd[0], nd[1] + 1), (nd[0] + 1, nd[1] + 1)]
                        print("closing ", nodes_to_close)
                        for node in nodes_to_close:
                            MG.close_square(node)
                        build_time_offset = 0



            # LEFT CLICK RELEASE
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:

                # Movement Grid
                # MG.select_square(MG.get_row_column_by_pixel_coords(mousePosition))
                # MG.deselect_square()

                # Selection drawing
                draw_selection = False
                drawn_selections.append(selection)
                selection = None
                for e in EM.entities:
                    e.hover(mousePosition)
                    if e.get_hover():
                        e.select()

            # RIGHT CLICK PRESS
            # set target for all selected entities
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                target_square = MG.get_row_column_by_pixel_coords(mousePosition)
                EM.set_group_target(MG, target_square)

            # RIGHT CLICK RELEASE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                pass

        # Collision checks for all Cow objects
        # EM.check_cow_collisions()

        # Move all entities with sprites, check for hover select
        EM.move_and_hover(mousePosition)

        # if selection drawing mode is on, draw the rectangle
        if draw_selection:
            selection.update(mousePosition[0], mousePosition[1])
            selection.draw(screen)

        # if building mode enabled increase offset counter and draw sprite at cursor
        if active_build and active_build.is_build_mode():
            build_time_offset += 1
            initiate_build = None
            active_build.is_build_collision(mousePosition, EM.buildings)
            active_build.draw_sprite(mousePosition)

        # draw entities and buildings
        draw_entities(EM.entities)
        draw_entities(EM.buildings)
        weather.weather_step()

        # check and run production for all buildings in Entity Manager
        EM.run_production_queues()

        # DEBUG MODE VISIBLE GRID
        if Constants.DEBUG_MODE:
            MG.highlight_square(mousePosition)
            MG.selection_block = False
            MG.draw_grid()

        # draw interface bar
        bar.draw_self()

        # draw cursor if not in build mode
        if not active_build or active_build.is_active():
            draw_cursor(screen, mousePosition)

        # refresh screen
        pygame.display.update()
