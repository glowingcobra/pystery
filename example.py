import pygame
from pystery import init, quit, load_image, Game, Scene, ImageEntity, RectRegion, Dir

class ExampleGame(Game):
    def __init__(self):
        super().__init__()

        ################################
        # SET UP YOUR GAME STARTING HERE
        ################################
        
        typing_sound = self.load_sound('assets/audio/typing.mp3')

        text_scene1 = Scene(img='assets/bg/Text1.png')
        text_scene2 = Scene(img='assets/bg/Text2.png')
        text_scene3 = Scene(img='assets/bg/Text3.png')
        text_scene4 = Scene(img='assets/bg/Text4.png')
        text_scene5 = Scene(img='assets/bg/Text5.png')
        text_scene6 = Scene(img='assets/bg/Text6.png')
        text_scene7 = Scene(img='assets/bg/Text7.png')
        outside_scene = Scene(img='assets/bg/outside.png')
        living_room_scene = Scene(img='assets/bg/living_room.png')
        computer_scene1 = Scene(img='assets/bg/computer_scene1.jpg')
        computer_scene2 = Scene(img='assets/bg/computer_scene2.jpg')
        dining_room_scene = Scene(img='assets/bg/dining_room.png')
        glass_scene = Scene(img='assets/bg/glass.jpeg')
        bedroom_scene = Scene(img='assets/bg/bedroom.jpg')
        attic_scene = Scene(img='assets/bg/attic.png')
        accusation_scene = Scene(img='assets/bg/living_room.jpg')

        def click_file():
            typing_sound.play()
            living_room_scene.remove_region(living_room_click_region1)
            living_room_click_region1.link_to_scene(computer_scene2)
            living_room_scene.add_region(living_room_click_region1)
            computer_scene2.add_dir_link(Dir.UP, living_room_scene)

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
        text_click_region6.link_to_scene(outside_scene)
        text_scene6.add_region(text_click_region6)
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
        bedroom_scene.add_dir_link(Dir.RIGHT, attic_scene)
        attic_scene.add_dir_link(Dir.LEFT, bedroom_scene)
        attic_scene.add_dir_link(Dir.RIGHT, text_scene7)
        text_scene7.add_dir_link(Dir.LEFT, attic_scene)
        text_scene7.add_dir_link(Dir.RIGHT, accusation_scene)

        self.set_start_scene(text_scene1)
init()
while True:
    # run the game until quit or restart
    run_result = ExampleGame().run()

    # if run_result is False, the game should quit. otherwise, we loop and restart it
    if not run_result:
        break
quit()
