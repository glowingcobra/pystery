import pygame
import time
import math
from enum import Enum

DIR_TRIANGLE_SIZE = 30
INVENTORY_SIZE = 4
INVENTORY_WIDTH_FRAC = 0 # what fraction of the screen width the inventory should take up
INVENTORY_PADDING_FRAC = 0.05 # what fraction of the inventory width should be padding between items

global screen

def init(width=1408, height=720):
    global screen

    pygame.init()
    screen = pygame.display.set_mode((width, height))

    pygame.mixer.init()

def quit():
    pygame.quit()

def load_image(fn):
    return pygame.image.load(fn).convert_alpha()

# A Region is an area of a single scene that can be clicked on.
class Region(object):
    def __init__(self):
        self.click_fn = None
        self.linked_scene = None

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

    def render_outline(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.left, self.top, self.width, self.height), 2)

# An Entity is a visual object that can be rendered and hit-test against.
# A single entity instance can have multiple placements in different scenes and in the inventory.
class Entity(object):
    pass

# An ImageEntity is an entity that is rendered using an image (as opposed to directly drawing shapes).
# The anchor is the point on the image that is placed at the position specified when rendering.
class ImageEntity(Entity):
    def __init__(self, img, *, anchor=None):
        super().__init__()

        self.loaded_img = load_image(img)
        if anchor is None:
            self.anchor = (self.loaded_img.get_width() / 2, self.loaded_img.get_height() / 2)
        else:
            self.anchor = anchor

    def render(self, *, surface, pos, scale=1):
        adjusted_pos = (pos[0] - self.anchor[0]*scale, pos[1] - self.anchor[1]*scale)
        scaled_img = pygame.transform.scale(self.loaded_img, (int(self.loaded_img.get_width() * scale), int(self.loaded_img.get_height() * scale)))
        surface.blit(scaled_img, adjusted_pos)

    def render_to_fit(self, target, rect):
        blit_to_fit(self.loaded_img, target, rect)

    def hit_test(self, *, click_pos, pos, scale=1):
        img_click_pos = ((click_pos[0] - pos[0])/scale + self.anchor[0], (click_pos[1] - pos[1])/scale + self.anchor[1])
        return (0 <= img_click_pos[0] < self.loaded_img.get_width()) and (0 <= img_click_pos[1] < self.loaded_img.get_height())

    def render_outline(self, surface, pos, scale):
        pygame.draw.rect(surface, (255, 0, 0), (pos[0] - self.anchor[0]*scale, pos[1] - self.anchor[1]*scale, self.loaded_img.get_width()*scale, self.loaded_img.get_height()*scale), 2)

class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Placement(object):
    def __init__(self, *, scene, entity, pos, scale=1, hidden=False, on_click=None):
        self.entity = entity
        self.pos = pos
        self.scale = scale
        self.hidden = hidden
        self.on_click = on_click

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def set_hidden(self, hidden):
        self.hidden = hidden

    def is_hidden(self):
        return self.hidden

    def on_click(self, fn):
        self.on_click = fn

    def render_outline(self, surface):
        self.entity.render_outline(surface, self.pos, self.scale)

class Scene(object):
    def __init__(self, *, img):
        self.placements = []
        self.regions = []
        self.dir_links = {}

        self.loaded_img = load_image(img)

    def set_img(self, loaded_img):
        self.loaded_img = loaded_img

    def place_entity(self, entity, *, pos, scale=1):
        placement = Placement(scene=self, entity=entity, pos=pos, scale=scale)
        self.placements.append(placement)
        return placement

    def remove_placement(self, placement):
        self.placements.remove(placement)

    def add_region(self, region):
        self.regions.append(region)

    def remove_region(self, region):
        self.regions.remove(region)

    def add_dir_link(self, dir, scene):
        assert dir in Dir, 'Invalid direction'
        self.dir_links[dir] = scene

    def has_dir_link(self, dir):
        return dir in self.dir_links

    def handle_click(self, click_pos, game):
        # check if the click was on any directional link triangle
        for dir, target_scene in self.dir_links.items():
            pos, angle = get_dir_triangle_pos_angle(self.loaded_img.get_size(), dir)
            if math.hypot(click_pos[0] - pos[0], click_pos[1] - pos[1]) < DIR_TRIANGLE_SIZE:
                game.set_current_scene(target_scene)
                return

        # check if the click was in any region
        for region in self.regions:
            if region.contains(click_pos):
                if region.click_fn:
                    region.click_fn()
                if region.linked_scene:
                    game.set_current_scene(region.linked_scene)
                    return

        # check if the click was on any entity placement
        for placement in self.placements:
            if not placement.hidden and placement.entity.hit_test(click_pos=click_pos, pos=placement.pos, scale=placement.scale):
                if placement.on_click:
                    placement.on_click()
                return

        print('scene click did not hit anything')
        return

    # returns new surface
    def render(self, show_outlines):
        render_surface = pygame.Surface(self.loaded_img.get_size())
        render_surface.fill((0, 0, 0))

        # draw the background image
        render_surface.blit(self.loaded_img, (0, 0))

        # draw the entity placements
        for placement in self.placements:
            if not placement.hidden:
                placement.entity.render(surface=render_surface, pos=placement.pos, scale=placement.scale)

                if show_outlines:
                    placement.render_outline(render_surface)

        # draw any region outlines
        if show_outlines:
            for region in self.regions:
                region.render_outline(render_surface)

        # draw any directional link arrows
        for dir, target_scene in self.dir_links.items():
            pos, angle = get_dir_triangle_pos_angle(render_surface.get_size(), dir)
            draw_triangle(render_surface, (255, 255, 255), pos, DIR_TRIANGLE_SIZE, angle)
            draw_triangle(render_surface, (0, 0, 0), pos, 0.6*DIR_TRIANGLE_SIZE, angle)

        return render_surface

class Transform(object):
    def __init__(self, scale, x_offset, y_offset):
        self.scale = scale
        self.x_offset = x_offset
        self.y_offset = y_offset

    def apply(self, pos):
        return (pos[0] * self.scale + self.x_offset, pos[1] * self.scale + self.y_offset)

    def apply_inverse(self, pos):
        return ((pos[0] - self.x_offset) / self.scale, (pos[1] - self.y_offset) / self.scale)

def blit_to_fit(surface, target, rect=None):
    if rect is None:
        rect = target.get_rect()

    scale = min(rect.width / surface.get_width(), rect.height / surface.get_height())
    x_offset = rect.left + (rect.width - surface.get_width() * scale) / 2
    y_offset = rect.top + (rect.height - surface.get_height() * scale) / 2

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
        self.inventory = [None] * INVENTORY_SIZE
        self.selected_inventory_idx = None
        self.inventory_item_rects = None

    def set_start_scene(self, scene):
        self.start_scene = scene

    def load_sound(self, fn):
        return pygame.mixer.Sound(fn)

    def play_sound(self, sound):
        sound.play()

    def is_inventory_full(self):
        return all([x is not None for x in self.inventory])

    def add_to_inventory(self, entity):
        if self.is_inventory_full():
            print('Inventory is full')
            return

        for i in range(INVENTORY_SIZE):
            if self.inventory[i] is None:
                self.inventory[i] = entity
                break
        else:
            assert False, 'Should not reach here'

    def is_in_inventory(self, entity):
        return entity in self.inventory

    def get_selected_inventory_entity(self):
        if self.selected_inventory_idx is not None:
            return self.inventory[self.selected_inventory_idx]
        else:
            return None

    def add_to_inventory_upon_click(self, placement):
        def fn():
            self.add_to_inventory(placement.entity)
            self.current_scene.remove_placement(placement)
        placement.on_click = fn

    def set_current_scene(self, scene):
        self.current_scene = scene

    def calculate_inventory_item_rects(self, scene_rect):
        inventory_rect = pygame.Rect(scene_rect.right, scene_rect.top, screen.get_width()*INVENTORY_WIDTH_FRAC, scene_rect.height)
        total_squares_height = inventory_rect.width*INVENTORY_SIZE + INVENTORY_PADDING_FRAC*(INVENTORY_SIZE - 1)
        assert total_squares_height <= inventory_rect.height
        inventory_y_offset = (inventory_rect.height - total_squares_height) / 2

        self.inventory_item_rects = []
        y = inventory_y_offset
        for i in range(INVENTORY_SIZE):
            self.inventory_item_rects.append(pygame.Rect(inventory_rect.left, y, inventory_rect.width, inventory_rect.width))
            y += inventory_rect.width + INVENTORY_PADDING_FRAC*inventory_rect.width

    def render_inventory(self):
        assert len(self.inventory) == INVENTORY_SIZE
        assert len(self.inventory_item_rects) == INVENTORY_SIZE

        for i in range(INVENTORY_SIZE):
            irect = self.inventory_item_rects[i]
            pygame.draw.rect(screen, (128, 128, 128), irect)

            if i == self.selected_inventory_idx:
                pygame.draw.rect(screen, (255, 255, 255), irect, 5)

            INNER_PADDING_FRAC = 0.1
            inner_rect = pygame.Rect(irect.left + irect.width*INNER_PADDING_FRAC, irect.top + irect.height*INNER_PADDING_FRAC, irect.width*(1 - 2*INNER_PADDING_FRAC), irect.height*(1 - 2*INNER_PADDING_FRAC))

            if self.inventory[i] is not None:
                self.inventory[i].render_to_fit(screen, inner_rect)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        t0 = time.time()
        t_prev = t0

        show_fps = False
        font = pygame.font.Font(None, 32)

        show_outlines = False

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
                    elif event.key == pygame.K_o:
                        show_outlines = not show_outlines
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if last_render_xform:
                        if event.button == 1:
                            # left mouse button
                            mouse_pos = pygame.mouse.get_pos()
                            xformed_click_pos = last_render_xform.apply_inverse(mouse_pos)

                            print('mouse click at {}'.format((int(xformed_click_pos[0]), int(xformed_click_pos[1]))))

                            self.current_scene.handle_click(xformed_click_pos, self)

                            # check if the click was in the inventory
                            assert (self.inventory_item_rects is not None) and (len(self.inventory_item_rects) == INVENTORY_SIZE)
                            for i in range(INVENTORY_SIZE):
                                if self.inventory_item_rects[i].collidepoint(mouse_pos):
                                    if self.selected_inventory_idx == i:
                                        self.selected_inventory_idx = None
                                    else:
                                        self.selected_inventory_idx = i
                                    break
                            else:
                                self.selected_inventory_idx = None

            # render the current scene
            scene_render_surface = self.current_scene.render(show_outlines)

            # render FPS
            if show_fps:
                rounded_fps = str(round(clock.get_fps(), 2))
                fps_text = font.render(rounded_fps, True, (255, 255, 255))
                scene_render_surface.blit(fps_text, (scene_render_surface.get_width() - fps_text.get_width(), 0))

            # clear the screen to black
            screen.fill((0, 0, 0))

            # blit the render surface to the screen
            scene_container_rect = pygame.Rect(0, 0, screen.get_width() * (1 - INVENTORY_WIDTH_FRAC), screen.get_height())
            last_render_xform = blit_to_fit(scene_render_surface, screen, scene_container_rect)

            scene_actual_rect = pygame.Rect(last_render_xform.x_offset, last_render_xform.y_offset, scene_render_surface.get_width()*last_render_xform.scale, scene_render_surface.get_height()*last_render_xform.scale)

            # render the inventory
            self.calculate_inventory_item_rects(scene_actual_rect)
            self.render_inventory()

            # show updated screen
            pygame.display.flip()

        return False
