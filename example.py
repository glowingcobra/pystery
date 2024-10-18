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

        office_scene = Scene(img='assets/bg/office.jpg')
        computer_scene = Scene(img='assets/bg/computer.jpg')
        bookshelf_scene = Scene(img='assets/bg/bookshelf.jpg')
        hallway_scene = Scene(img='assets/bg/hallway.jpg')
        hallway_with_broken_door = load_image('assets/bg/hallway_broken.jpg')
        outside_scene = Scene(img='assets/bg/outside.jpg')

        muppet_entity = ImageEntity(img='assets/entity/muppet.png')
        muppet_in_computer_scene = computer_scene.place_entity(muppet_entity, pos=(640, 345))
        muppet_in_computer_scene.hide()

        muppet_in_office_scene = office_scene.place_entity(muppet_entity, pos=(605, 360), scale=0.45)
        muppet_in_office_scene.hide()

        sledgehammer_entity = ImageEntity(img='assets/entity/sledgehammer.png')
        sledgehammer_on_bookshelf = bookshelf_scene.place_entity(sledgehammer_entity, pos=(350, 550), scale=1)
        self.add_to_inventory_upon_click(sledgehammer_on_bookshelf)

        office_computer_region = RectRegion(left=450, top=280, width=320, height=220)
        office_computer_region.link_to_scene(computer_scene)
        office_scene.add_region(office_computer_region)

        computer_scene.add_dir_link(Dir.DOWN, office_scene)

        def clicked_computer():
            if muppet_in_computer_scene.is_hidden():
                muppet_in_computer_scene.show()
                muppet_in_office_scene.show()
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

init()
while True:
    # run the game until quit or restart
    run_result = ExampleGame().run()

    # if run_result is False, the game should quit. otherwise, we loop and restart it
    if not run_result:
        break
quit()
