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
        text_scene3 = Scene(img='assets/bg/Text3.png')
        text_scene4 = Scene(img='assets/bg/Text4.png')
        text_scene5 = Scene(img='assets/bg/Text5.png')
        text_scene6 = Scene(img='assets/bg/Text6.png')
        text_scene7 = Scene(img='assets/bg/Text7.png')
        outside_scene = Scene(img='assets/bg/outside.png')
        living_room_scene = Scene(img='assets/bg/living_room.jpg')
        computer_scene1 = Scene(img='assets/bg/computer_scene1.jpg')
        computer_scene2 = Scene(img='assets/bg/computer_scene2.jpg')
        dining_room_scene = Scene(img='assets/bg/dining_room.png')
        glass_scene = Scene(img='assets/bg/glass.jpeg')
        bedroom_scene = Scene(img='assets/bg/bedroom.jpg')

        office_scene = Scene(img='assets/bg/office.jpg')
        computer_scene = Scene(img='assets/bg/computer.jpg')
        bookshelf_scene = Scene(img='assets/bg/bookshelf.jpg')
        hallway_scene = Scene(img='assets/bg/hallway.jpg')
        hallway_with_broken_door = load_image('assets/bg/hallway_broken.jpg')
        outside_scene2 = Scene(img='assets/bg/outside.jpg')

        muppet_entity = ImageEntity(img='assets/entity/muppet.png')
        muppet_in_computer_scene = computer_scene2.place_entity(muppet_entity, pos=(640, 345))
        muppet_entity.size = 1
        muppet_in_computer_scene.hide()

        muppet_in_office_scene = office_scene.place_entity(muppet_entity, pos=(605, 360), scale=0.45)
        muppet_in_office_scene.hide()

        sledgehammer_entity = ImageEntity(img='assets/entity/sledgehammer.png')
        sledgehammer_on_bookshelf = bookshelf_scene.place_entity(sledgehammer_entity, pos=(350, 550), scale=1)
        self.add_to_inventory_upon_click(sledgehammer_on_bookshelf)

        apple_entity = ImageEntity(img='assets/entity/apple.png')

        

        def clicked_computer():
            if muppet_in_computer_scene.is_hidden():
                muppet_in_computer_scene.show()
                muppet_in_office_scene.show()
                computer_scene.remove_region(computer_scene_screen_region)
                typing_sound.play()

        def click_file():
            code_found = True
            typing_sound.play()
            living_room_scene.remove_region(living_room_click_region1)
            living_room_click_region1.link_to_scene(computer_scene2)
            living_room_scene.add_region(living_room_click_region1)
            computer_scene2.add_dir_link(Dir.UP, living_room_scene)

        office_computer_region = RectRegion(left=450, top=280, width=320, height=220)
        office_computer_region.link_to_scene(computer_scene2)
        office_scene.add_region(office_computer_region)
        
        text_click_region1 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region1.link_to_scene(text_scene2)
        text_scene1.add_region(text_click_region1)
        text_click_region2 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region2.link_to_scene(text_scene3)
        text_scene2.add_region(text_click_region2)
        text_click_region3 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region3.link_to_scene(text_scene4)
        text_scene3.add_region(text_click_region3)
        text_click_region4 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region4.link_to_scene(text_scene5)
        text_scene4.add_region(text_click_region4)
        text_click_region5 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region5.link_to_scene(text_scene6)
        text_scene5.add_region(text_click_region5)
        text_click_region6 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region6.link_to_scene(text_scene7)
        text_scene6.add_region(text_click_region6)
        text_click_region7 = RectRegion(left=0, top=0, width=1280, height=720)
        text_click_region7.link_to_scene(outside_scene)
        text_scene7.add_region(text_click_region7)
        outside_scene_click_region1 = RectRegion(left=675, top=450, width=150, height=150)
        outside_scene_click_region1.link_to_scene(living_room_scene)
        outside_scene.add_region(outside_scene_click_region1)
        living_room_click_region1 = RectRegion(left=680, top=370, width=120, height=70)
        living_room_click_region1.link_to_scene(computer_scene1)
        living_room_scene.add_region(living_room_click_region1)
        living_room_scene.add_dir_link(Dir.RIGHT, dining_room_scene)
        computer_scene1.add_dir_link(Dir.UP, living_room_scene)
        computer_scene1_click_region1 = RectRegion(left= 200, top=132, width=900, height=100)
        computer_scene1_click_region1.link_to_scene(computer_scene2)
        computer_scene1_click_region1.on_click(click_file)
        computer_scene1.add_region(computer_scene1_click_region1)
        computer_scene2.add_dir_link(Dir.UP, living_room_scene)
        dining_room_scene.add_dir_link(Dir.LEFT, living_room_scene)
        dining_room_scene.add_dir_link(Dir.RIGHT, bedroom_scene)
        dining_room_scene_click_region1 = RectRegion(left= 1050, top=570, width=90, height=60)
        dining_room_scene_click_region1.link_to_scene(glass_scene)
        dining_room_scene.add_region(dining_room_scene_click_region1)
        glass_scene.add_dir_link(Dir.UP, dining_room_scene)
        bedroom_scene.add_dir_link(Dir.LEFT, dining_room_scene)

        office_apple_1 = office_scene.place_entity(apple_entity, pos=(1140, 620))
        self.add_to_inventory_upon_click(office_apple_1)
        office_apple_2 = office_scene.place_entity(apple_entity, pos=(1050, 480))
        self.add_to_inventory_upon_click(office_apple_2)

        computer_scene.add_dir_link(Dir.DOWN, office_scene)

        computer_scene_screen_region = RectRegion(left=515, top=258, width=248, height=175)
        computer_scene_screen_region.on_click(clicked_computer)
        computer_scene.add_region(computer_scene_screen_region)

        office_scene.add_dir_link(Dir.LEFT, bookshelf_scene)
        bookshelf_scene.add_dir_link(Dir.RIGHT, office_scene)

        office_scene.add_dir_link(Dir.DOWN, hallway_scene)
        hallway_scene.add_dir_link(Dir.DOWN, office_scene)

        bookshelf_scene.add_dir_link(Dir.LEFT, hallway_scene)
        hallway_scene.add_dir_link(Dir.RIGHT, bookshelf_scene)
        outside_scene2.add_dir_link(Dir.DOWN, hallway_scene)

        def click_hallway_door():
            if not hallway_scene.has_dir_link(Dir.UP):
                if self.get_selected_inventory_entity() == sledgehammer_entity:
                    hallway_scene.add_dir_link(Dir.UP, outside_scene2)
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
