import pygame
import time
import math
from enum import Enum

DIR_TRIANGLE_SIZE = 30

global screen

def init(width=1280, height=720):
    global screen

    pygame.init()
    screen = pygame.display.set_mode((width, height))

def quit():
    pygame.quit()

class Region(object):
    def __init__(self):
        self.linked_scene = None
        self.click_fn = None

    def link_to_scene(self, scene):
        self.linked_scene = scene

    def on_click(self, fn):
        self.click_fn = fn

class RectRegion(Region):
    def __init__(self, *, left, top, width, height):
        super().__init__()

        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def contains(self, pos):
        return (self.left <= pos[0] <= (self.left + self.width)) and (self.top <= pos[1] <= (self.top + self.height))

class Entity(object):
    def __init__(self, *, pos, img=None):
        self.hidden = False

        self.pos = pos

        self.loaded_img = None
        self.anchor = None
        if img:
            self.loaded_img = pygame.image.load(img).convert_alpha()
            self.anchor = (self.loaded_img.get_width() / 2, self.loaded_img.get_height() / 2)

    def show(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def set_hidden(self, hidden):
        self.hidden = hidden

class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Scene(object):
    def __init__(self, *, img):
        self.entities = []
        self.regions = []
        self.dir_links = {}

        self.loaded_img = pygame.image.load(img).convert_alpha()

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_region(self, region):
        self.regions.append(region)

    def add_dir_link(self, dir, scene):
        assert dir in Dir, 'Invalid direction'
        self.dir_links[dir] = scene

class Transform(object):
    def __init__(self, scale, x_offset, y_offset):
        self.scale = scale
        self.x_offset = x_offset
        self.y_offset = y_offset

    def apply(self, pos):
        return (pos[0] * self.scale + self.x_offset, pos[1] * self.scale + self.y_offset)

    def apply_inverse(self, pos):
        return ((pos[0] - self.x_offset) / self.scale, (pos[1] - self.y_offset) / self.scale)

def blit_to_fit(surface, target):
    # determine factor by which we need to scale surface to fit target
    scale = min(target.get_width() / surface.get_width(), target.get_height() / surface.get_height())
    x_offset = (target.get_width() - surface.get_width() * scale) / 2
    y_offset = (target.get_height() - surface.get_height() * scale) / 2

    # now resize the surface to the size of the display
    scaled_surface = pygame.transform.scale_by(surface, scale)

    target.blit(scaled_surface, (x_offset, y_offset))

    return Transform(scale, x_offset, y_offset)

def draw_triangle(surface, color, pos, size, angle):
    # calculate the three points of the triangle
    p1 = (pos[0] + size*math.cos(angle), pos[1] + size*math.sin(angle))
    p2 = (pos[0] + size*math.cos(angle + 2*math.pi/3), pos[1] + size*math.sin(angle + 2*math.pi/3))
    p3 = (pos[0] + size*math.cos(angle + 4*math.pi/3), pos[1] + size*math.sin(angle + 4*math.pi/3))

    # draw the triangle
    pygame.draw.polygon(surface, color, [p1, p2, p3])

def get_dir_triangle_pos_angle(dims, dir):
    INSET_MULT = 2
    if dir == Dir.UP:
        return (dims[0]/2, INSET_MULT*DIR_TRIANGLE_SIZE), -math.pi/2
    elif dir == Dir.DOWN:
        return (dims[0]/2, dims[1] - INSET_MULT*DIR_TRIANGLE_SIZE), math.pi/2
    elif dir == Dir.LEFT:
        return (INSET_MULT*DIR_TRIANGLE_SIZE, dims[1]/2), math.pi
    elif dir == Dir.RIGHT:
        return (dims[0] - INSET_MULT*DIR_TRIANGLE_SIZE, dims[1]/2), 0
    else:
        assert False

class Game(object):
    def __init__(self):
        self.start_scene = None
        self.current_scene = None

    def set_start_scene(self, scene):
        self.start_scene = scene

    def run(self):
        running = True
        clock = pygame.time.Clock()
        t0 = time.time()
        t_prev = t0

        show_fps = False
        font = pygame.font.Font(None, 16)

        last_render_surface_dims = None
        last_render_xform = None

        self.current_scene = self.start_scene

        while running:
            # limit FPS to 60
            clock.tick(60)

            # track elapsed time, and time since last frame
            t = time.time() - t0
            dt = t - t_prev
            t_prev = t

            # check for any events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # user clicked window close button
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_f:
                        show_fps = not show_fps
                    elif event.key == pygame.K_r:
                        return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if last_render_xform and last_render_surface_dims:
                        if event.button == 1:
                            # left mouse button
                            mouse_pos = pygame.mouse.get_pos()
                            xformed_click_pos = last_render_xform.apply_inverse(mouse_pos)

                            print('mouse click at {}'.format((int(xformed_click_pos[0]), int(xformed_click_pos[1]))))

                            # check if the click was on any directional link triangle
                            for dir, target_scene in self.current_scene.dir_links.items():
                                pos, angle = get_dir_triangle_pos_angle(last_render_surface_dims, dir)
                                if math.hypot(pos[0] - xformed_click_pos[0], pos[1] - xformed_click_pos[1]) < DIR_TRIANGLE_SIZE:
                                    self.current_scene = target_scene
                                    break

                            # check if the click was in any region
                            for region in self.current_scene.regions:
                                if region.contains(xformed_click_pos):
                                    if region.click_fn:
                                        region.click_fn()
                                    if region.linked_scene:
                                        self.current_scene = region.linked_scene
                                        break

            # draw the current scene
            render_surface = pygame.Surface(self.current_scene.loaded_img.get_size())
            render_surface.fill((0, 0, 0))
            last_render_surface_dims = render_surface.get_size()

            # draw the background image
            render_surface.blit(self.current_scene.loaded_img, (0, 0))

            # draw the entity instances
            for ent in self.current_scene.entities:
                if ent.loaded_img and not ent.hidden:
                    assert ent.anchor, 'Entity must have an anchor point set'
                    adjusted_pos = (ent.pos[0] - ent.anchor[0], ent.pos[1] - ent.anchor[1])
                    render_surface.blit(ent.loaded_img, adjusted_pos)

            # draw any directional link arrows
            for dir, target_scene in self.current_scene.dir_links.items():
                pos, angle = get_dir_triangle_pos_angle(last_render_surface_dims, dir)
                draw_triangle(render_surface, (255, 255, 255), pos, DIR_TRIANGLE_SIZE, angle)
                draw_triangle(render_surface, (0, 0, 0), pos, 0.6*DIR_TRIANGLE_SIZE, angle)

            # render FPS
            if show_fps:
                rounded_fps = str(round(clock.get_fps(), 2))
                fps_text = font.render(rounded_fps, True, (255, 255, 255))
                render_surface.blit(fps_text, (render_surface.get_width() - fps_text.get_width(), 0))

            # clear the screen to black
            screen.fill((0, 0, 0))

            # blit the render surface to the screen
            last_render_xform = blit_to_fit(render_surface, screen)

            # show updated screen
            pygame.display.flip()

        return False
