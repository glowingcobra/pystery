from pystery import init, quit, Game, Scene, Entity, RectRegion, Dir

class ExampleGame(Game):
    def __init__(self):
        super().__init__()

        ################################
        # SET UP YOUR GAME STARTING HERE
        ################################

        office_scene = Scene(img='assets/bg/office.jpg')
        computer_scene = Scene(img='assets/bg/computer.jpg')
        bookshelf_scene = Scene(img='assets/bg/bookshelf.jpg')
        hallway_scene = Scene(img='assets/bg/hallway.jpg')

        muppet_entity = Entity(img='assets/entity/muppet.png', pos=(640, 345))
        muppet_entity.hide()
        computer_scene.add_entity(muppet_entity)

        muppet_small_entity = Entity(img='assets/entity/muppet_small.png', pos=(605, 360))
        muppet_small_entity.hide()
        office_scene.add_entity(muppet_small_entity)

        office_computer_region = RectRegion(left=450, top=280, width=320, height=220)
        office_computer_region.link_to_scene(computer_scene)
        office_scene.add_region(office_computer_region)

        computer_scene.add_dir_link(Dir.DOWN, office_scene)

        def show_muppets():
            muppet_entity.show()
            muppet_small_entity.show()

        computer_scene_screen_region = RectRegion(left=515, top=258, width=248, height=175)
        computer_scene_screen_region.on_click(show_muppets)
        computer_scene.add_region(computer_scene_screen_region)

        office_scene.add_dir_link(Dir.LEFT, bookshelf_scene)
        bookshelf_scene.add_dir_link(Dir.RIGHT, office_scene)

        office_scene.add_dir_link(Dir.DOWN, hallway_scene)
        hallway_scene.add_dir_link(Dir.DOWN, office_scene)

        bookshelf_scene.add_dir_link(Dir.LEFT, hallway_scene)
        hallway_scene.add_dir_link(Dir.RIGHT, bookshelf_scene)

        self.set_start_scene(office_scene)

init()
while True:
    # run the game until quit or restart
    run_result = ExampleGame().run()

    # if run_result is False, the game should quit. otherwise, we loop and restart it
    if not run_result:
        break
quit()
