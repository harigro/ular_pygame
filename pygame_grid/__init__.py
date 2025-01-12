# Copyright 2021 Casey Devet
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

# Load the pygame module
import pygame

def draw_grid (x_dist=100, y_dist=100, color="black", opacity=0.5, 
        thickness=3, x_minor_dist=20, y_minor_dist=20, 
        minor_color="black", minor_opacity=0.25, minor_thickness=1):
    '''
    Draw gridlines on the current pygame screen surface.
    '''

    # Get the active pygame screen and its dimensions
    screen = pygame.display.get_surface()
    if screen is None:
        raise RuntimeError("There is no pygame screen open!")
    width, height = screen.get_size()

    # Create the font to use for labels
    font = pygame.font.SysFont("Arial", 12)

    # Draw thin vertical lines
    for x in range(x_minor_dist, width, x_minor_dist):
        # Don't draw the line if it coincides with a thick line
        if x % x_dist != 0:
            # Create a thin line surface and blit it on the screen
            line_surface = pygame.Surface((minor_thickness, height), pygame.SRCALPHA)
            line_surface.fill(minor_color)
            line_surface.set_alpha(int(minor_opacity * 255))
            screen.blit(line_surface, (x - minor_thickness // 2, 0))

    # Draw thin horizontal lines
    for y in range(y_minor_dist, height, y_minor_dist):
        # Don't draw the line if it coincides with a thick line
        if y % y_dist != 0:
            # Create a thin line surface and blit it on the screen
            line_surface = pygame.Surface((width, 1), pygame.SRCALPHA)
            line_surface.fill(minor_color)
            line_surface.set_alpha(int(minor_opacity * 255))
            screen.blit(line_surface, (0, y - minor_thickness // 2))

    # Draw thick vertical lines
    for x in range(x_dist, width, x_dist):
        # Create a thick line surface and blit it on the screen
        line_surface = pygame.Surface((3, height), pygame.SRCALPHA)
        line_surface.fill(color)
        line_surface.set_alpha(int(opacity * 255))
        screen.blit(line_surface, (x - thickness // 2, 0))

        # Create a label for the thick line
        label = font.render(str(x), True, color)
        label.set_alpha(int(opacity * 255))
        label = pygame.transform.rotate(label, -90)
        screen.blit(label, (x - 13, 1))

    # Draw thick horizontal lines
    for y in range(y_dist, height, y_dist):
        # Create a thick line surface and blit it on the screen
        line_surface = pygame.Surface((width, 3), pygame.SRCALPHA)
        line_surface.fill(color)
        line_surface.set_alpha(int(opacity * 255))
        screen.blit(line_surface, (0, y - thickness // 2))

        # Create a label for the thick line
        label = font.render(str(y), True, color)
        label.set_alpha(int(opacity * 255))
        screen.blit(label, (1, y - 13))


# The function that will be imported with "import *"
__all__ = ["draw_grid"]
