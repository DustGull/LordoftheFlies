import sys, pygame, math


# Making a Lord of the Flies inspired game.

def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frame_counts


def load_tiles_and_make_dict_and_rect():
    # Load the tiles
    sand = pygame.image.load("map/Sand.png").convert_alpha() # (206, 206, 46, 255)
    tile_rect = sand.get_rect()
    plains = pygame.image.load("map/Plains.png").convert_alpha() # (126, 206, 46, 255)
    swamp = pygame.image.load("map/Jungle.png").convert_alpha() # (14,64,14,255)
    dirt = pygame.image.load("map/Dirt.png").convert_alpha() # (117,94,21,255)
    water = pygame.image.load("map/water.png").convert_alpha() # (0, 176, 255, 255)
    rocks = pygame.image.load("map/Rocky.png").convert_alpha() # (39, 39, 21, 255)

    # Make a dictionary of the tiles for easy access
    tiles = {}
    tiles[(206, 206, 46, 255)] = sand
    tiles[(126, 206, 46, 255)] = plains
    tiles[(39, 39, 21, 255)] = rocks
    tiles[(0, 176, 255, 255)] = water
    tiles[(117,94,21,255)] = dirt
    tiles[(14,64,14,255)] = swamp

    return (tiles, tile_rect)

# The main loop handles most of the game
def main():
    # Initialize pygame
    pygame.init()

    screen_size = height, width = (500, 500)
    screen = pygame.display.set_mode(screen_size)
    # background_image = pygame.image.load("New Piskel.png")

    # create player
    player = pygame.image.load("Player Character.png").convert_alpha()
    player_rect = player.get_rect()
    player_rect.center = (350, 250)  # location

    # adding characters
    # Simon
    simon = pygame.image.load("Simon.png").convert_alpha()  # load simon image
    simon_rect = simon.get_rect()
    simon_rect.center = 600, 500

    # boar
    boar = pygame.image.load("Boar.png").convert_alpha()
    boar_rect = boar.get_rect()
    boar_rect.center = 600, 600

    # Piggy
    piggy = pygame.image.load("Piggy.png").convert_alpha()
    piggy_rect = piggy.get_rect()
    piggy_rect.center = (600, 400)

    # Jack is the kid who becomes wild and barbaric

    jack = pygame.image.load("Choir Boy.png").convert_alpha()  # loan Jack's image
    jack_rect = jack.get_rect()
    jack_rect.center = (600, 300)

    # adding inventory items

    spear = pygame.image.load("Spear.png").convert_alpha()
    spear_rect = spear.get_rect()
    spear_rect.center = 400, 600

    rock = pygame.image.load("rock.png").convert_alpha()
    # rock = pygame.transform.scale(rock, (200, 200)) Use this line as a reference to scale an image
    rock_rect = rock.get_rect()
    rock_rect.center = 400, 500

    glasses = pygame.image.load("glasses.png").convert_alpha()
    glasses_rect = glasses.get_rect()
    glasses_rect.center = 400, 400

    bag = pygame.image.load("bag.png").convert_alpha()
    bag_rect = bag.get_rect()
    bag_rect.center = 400, 300


    # load mini map
    world = pygame.image.load("map/testMap.png").convert()
    world_rect = world.get_rect()
    (mapx, mapy) = (0, 0)

    # Get the tiles that define different terrain types
    tiles, tile_rect = load_tiles_and_make_dict_and_rect()

    # Calculate how many tiles fit on screen
    map_tile_width = (width // tile_rect.width) + 1
    map_tile_height = (height // tile_rect.height) + 1

    # Clock starts
    clock = pygame.time.Clock()

    frame_count = 0;

    playing = True

    is_facing_left = True  # player

    # Variable to track text on the screen. If you set the dialog string to something and set the position and the
    # counter, the text will show on the screen for dialog_counter number of frames.
    dialog_counter = 0
    dialog = ''
    dialog_position = (300, 200)

    # Load font
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    # create the inventory and make it empty
    inventory = {}

    # This list should hold all the sprite rectangles that get shifted with a key press.
    rect_list = [spear_rect, rock_rect, bag_rect, glasses_rect, piggy_rect, simon_rect, boar_rect, jack_rect]

    # This is the top left corner of the view into the minimap. You can start elsewhere on the map by
    # initializing these with a different value.
    mapx = 0
    mapy = 0

    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((170, 190, 190))

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        movement_x = 0
        movement_y = 0
        # check for keys that are pressed
        # Note the indent makes it part of the while playing but not part of the for event loop.
        keys = pygame.key.get_pressed()
        # check for specific keys
        # movement says how the world should shift. Pressing keys changes the value in the movement variables.

        if keys[pygame.K_LEFT]:
            is_facing_left = True
            movement_x -= tile_rect.width
            mapx -= 1

        if keys[pygame.K_RIGHT]:
            is_facing_left = False
            movement_x += tile_rect.width
            mapx += 1

        if keys[pygame.K_UP]:
            movement_y -= tile_rect.height
            mapy -= 1

        if keys[pygame.K_DOWN]:
            movement_y += tile_rect.height
            mapy += 1

        if mapx < 0:
            mapx = 0
            movement_x = 0

        # Keep the view of the world on valid tiles.
        if mapx < 0:
            mapx = 0
            movement_x = 0
        if mapx > world.get_width() - 1 - (map_tile_width - 1):
            mapx = world.get_width() - 1 - (map_tile_width - 1)
            movement_x = 0
        if mapy < 0:
            mapy = 0
            movement_y = 0
        if mapy > world.get_height() - 1 - (map_tile_height - 1):
            mapy = world.get_height() - 1 - (map_tile_height - 1)
            movement_y = 0

        # Move all the sprites in the scene by movement amount.
        # You can still move the rect of an individual sprite to make
        # it move around the landscape.
        for rect in rect_list:
            rect.move_ip(-movement_x, -movement_y)

        # Check for touching boar.
        if player_rect.colliderect(boar_rect):
            # Respond differently depending on spear status
            if "spear" in inventory:
                dialog = "Oh no !! you killed me!!"
            else:
                dialog = "I am going to kill you!!"
            # These say where and for how long the dialog prints on the screen
            dialog_counter = 50
            dialog_position = (100, 100)

        # Check for touching spear .
        if player_rect.colliderect(spear_rect) and "spear" not in inventory:
            inventory["spear"] = True
            dialog = "Use the spear to kill the boar"
            dialog_counter = 30
            dialog_position = (300, 200)

        # Check for touching Simon
        if player_rect.colliderect(simon_rect):
            # Respond differently depending on torch status
            if "torch" in inventory:
                dialog = "You killed me!"
            elif "sleepingbag" in inventory:
                dialog = "I died while you slept"
            elif "torch" not in inventory and "sleepingbag" not in inventory:
                dialog = "Find a torch or sleepingbag"

        # Check for touching Piggy
        if player_rect.colliderect(piggy_rect):
            # Respond differently depending on glasses status
            if "glasses" in inventory:
                dialog = "I can see again!"
                # pig_has_glasses = True

            elif "rock" in inventory:  # jack_has_glasses
                dialog = "Don't kill me"

            elif "glasses" not in inventory and "rock" not in inventory:
                dialog = "Have you seen my glasses?"

        # Check for touching glasses
        if player_rect.colliderect(glasses_rect) and "glasses" not in inventory:
            inventory["glasses"] = True
            dialog = "Give the glasses to Piggy or Jack"
            dialog_counter = 30
            dialog_position = (300, 200)

            # Check for touching Sleeping bag
        if player_rect.colliderect(bag_rect) and "bag" not in inventory:
            inventory["bag"] = True
            dialog = "sleepingbag added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        # Check for touching Jack
        if player_rect.colliderect(jack_rect):
            if "glasses" not in inventory and "rock" not in inventory:
                dialog = "Get Piggy's glasses!"
            elif "rock" in inventory:
                dialog = "Use the rock to kill Piggy!"

        # Check for touching rock
        if player_rect.colliderect(rock_rect) and "rock" not in inventory:
            inventory["rock"] = True
            dialog = "Better not drop this, someone could get hurt!"
            dialog_counter = 30
            dialog_position = (300, 200)

        # Draw the map - this has to be drawn first to be underneath the characters
        for y in range(0, map_tile_height):
            # offset y
            y_index = y + mapy
            for x in range(0, map_tile_width):
                # offset x
                x_index = x + mapx
                pixelColor = world.get_at((x_index, y_index))
                # The tile is draw at the pixel location scaled up
                tile_rect.topleft = (x * tile_rect.width, y * tile_rect.height)

                # Draw the tile that corresponds to the pixel color we found.
                screen.blit(tiles[tuple(pixelColor)], tile_rect)

        #Draw the Characters

        # Draw boar
        screen.blit(boar, boar_rect)
        pygame.draw.rect(screen, (0, 255, 0), boar_rect, 3)

        # Draw Simon
        screen.blit(simon, simon_rect)
        pygame.draw.rect(screen, (0, 60, 0), simon_rect, 3)

        # Draw Piggy
        screen.blit(piggy, piggy_rect)
        pygame.draw.rect(screen, (0, 60, 0), piggy_rect, 3)

        # Draw Jack
        screen.blit(jack, jack_rect)
        pygame.draw.rect(screen, (0, 60, 0), jack_rect, 3)

        # Only draw the gold if it hasn't been picked up
        if "rock" not in inventory:
            screen.blit(rock, rock_rect)
            pygame.draw.rect(screen, (40, 60, 0), rock_rect, 3)

        if "spear" not in inventory:
            screen.blit(spear, spear_rect)
            pygame.draw.rect(screen, (90, 90, 30), spear_rect, 3)

        if "glasses" not in inventory:
            screen.blit(glasses, glasses_rect)
            pygame.draw.rect(screen, (0, 60, 0), glasses_rect, 3)

        if "bag" not in inventory:
            screen.blit(bag, bag_rect)
            pygame.draw.rect(screen, (75, 80, 100), bag_rect, 3)

        # Pick the sprite frame to draw
        # player_sprite = player[frame_count%len(player)]
        # Flip the sprite depending on direction
        # if not is_facing_left:
        # player_sprite = pygame.transform.flip(player_sprite, True, False)
        screen.blit(player, player_rect)
        pygame.draw.rect(screen, (0, 255, 0), player_rect, 3)

        # draw any dialog
        if dialog:
            pygame.draw.rect(screen, (200, 220, 220), (50, 425, 600, 50))
            textsurface = myfont.render(dialog, False, (0, 0, 0))
            screen.blit(textsurface, (75, 430))
            # Track how long the dialog is on screen
            dialog_counter -= 1
            if dialog_counter == 0:
                dialog = ''

        # Draw the minimap - this should be last to be "over" any other drawn things. We could make
        # the screen wider and fit the minimap off to the right where it doesn't block the main view.
        screen.blit(world, world_rect)
        # Draw the current window as a rectangle on the minimap.
        pygame.draw.rect(screen, (255, 0, 0), (mapx, mapy, map_tile_width, map_tile_height), 2)


        # Bring drawn changes to the front
        pygame.display.update()

        frame_count += 1

        # 30 fps
        clock.tick(30)

    # loop is over
    pygame.quit()
    sys.exit()


# Start the program
main()
