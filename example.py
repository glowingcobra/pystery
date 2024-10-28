import pygame
from pystery import init, quit, load_image, Game, Scene, ImageEntity, RectRegion, Dir

class ExampleGame(Game):
    def __init__(self):
        super().__init__()

        ################################
        # SET UP YOUR GAME STARTING HERE
        ################################

        typing_sound = self.load_sound('assets/audio/typing.mp3')
        smash_sound = self.load_sound('assets/audio/smash.mp3')
        locked_door_sound = self.load_sound('assets/audio/locked_door.mp3')

        text_scene1 = Scene(img='assets/bg/Text1.png')
        text_scene2 = Scene(img='assets/bg/Text2.png')
        living_room_scene = Scene(img='assets/bg/living_room.jpg')
        computer_scene = Scene(img='assets/bg/computer_scene.jpeg')

        office_scene = Scene(img='assets/bg/office.jpg')
        computer_scene = Scene(img='assets/bg/computer.jpg')
        bookshelf_scene = Scene(img='assets/bg/bookshelf.jpg')
        hallway_scene = Scene(img='assets/bg/hallway.jpg')
        hallway_with_broken_door = load_image('assets/bg/hallway_broken.jpg')
        outside_scene = Scene(img='assets/bg/outside.jpg')

        muppet_entity = ImageEntity(img='assets/entity/muppet.png')
        muppet_in_computer_scene = computer_scene.place_entity(muppet_entity, pos=(640, 345))
        muppet_entity.size = 1
        muppet_in_computer_scene.hide()

        muppet_in_office_scene = office_scene.place_entity(muppet_entity, pos=(605, 360), scale=0.45)
        muppet_in_office_scene.hide()

        sledgehammer_entity = ImageEntity(img='assets/entity/sledgehammer.png')
        sledgehammer_on_bookshelf = bookshelf_scene.place_entity(sledgehammer_entity, pos=(350, 550), scale=1)
        self.add_to_inventory_upon_click(sledgehammer_on_bookshelf)

        apple_entity = ImageEntity(img='assets/entity/apple.png')

        office_computer_region = RectRegion(left=450, top=280, width=320, height=220)
        office_computer_region.link_to_scene(computer_scene)
        office_scene.add_region(office_computer_region)
        
        text_click_region1 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region1.link_to_scene(text_scene2)
        text_scene1.add_region(text_click_region1)
        text_click_region2 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region2.link_to_scene(living_room_scene)
        text_scene2.add_region(text_click_region2)

        office_apple_1 = office_scene.place_entity(apple_entity, pos=(1140, 620))
        self.add_to_inventory_upon_click(office_apple_1)
        office_apple_2 = office_scene.place_entity(apple_entity, pos=(1050, 480))
        self.add_to_inventory_upon_click(office_apple_2)

        computer_scene.add_dir_link(Dir.DOWN, office_scene)

        def clicked_computer():
            if muppet_in_computer_scene.is_hidden():
                muppet_in_computer_scene.show()
                muppet_in_office_scene.show()
                computer_scene.remove_region(computer_scene_screen_region)
                typing_sound.play()

        computer_scene_screen_region = RectRegion(left=515, top=258, width=248, height=175)
        computer_scene_screen_region.on_click(clicked_computer)
        computer_scene.add_region(computer_scene_screen_region)

        office_scene.add_dir_link(Dir.LEFT, bookshelf_scene)
        bookshelf_scene.add_dir_link(Dir.RIGHT, office_scene)

        office_scene.add_dir_link(Dir.DOWN, hallway_scene)
        hallway_scene.add_dir_link(Dir.DOWN, office_scene)

        bookshelf_scene.add_dir_link(Dir.LEFT, hallway_scene)
        hallway_scene.add_dir_link(Dir.RIGHT, bookshelf_scene)
        outside_scene.add_dir_link(Dir.DOWN, hallway_scene)

        def click_hallway_door():
            if not hallway_scene.has_dir_link(Dir.UP):
                if self.get_selected_inventory_entity() == sledgehammer_entity:
                    hallway_scene.add_dir_link(Dir.UP, outside_scene)
                    hallway_scene.set_img(hallway_with_broken_door)
                    hallway_scene.remove_region(hallway_scene_door_region)
                    smash_sound.play()
                else:
                    locked_door_sound.play()

        hallway_scene_door_region = RectRegion(left=527, top=96, width=220, height=470)
        hallway_scene_door_region.on_click(click_hallway_door)
        hallway_scene.add_region(hallway_scene_door_region)

        self.set_start_scene(office_scene)
        self.set_start_scene(text_scene1)
init()
while True:
    # run the game until quit or restart
    run_result = ExampleGame().run()

    # if run_result is False, the game should quit. otherwise, we loop and restart it
    if not run_result:
        break
quit()
