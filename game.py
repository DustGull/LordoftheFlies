import sys, pygame, math

#Making a Lord of the Flies inspired game.

def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frame_counts

# The main loop handles most of the game
def main():

    # Initialize pygame
    pygame.init()

    screen_size = height, width = (700, 500)
    screen = pygame.display.set_mode(screen_size)

    # create player
    player = load_piskell_sprite("player",21) #Load player sprite
    player_rect = player[0].get_rect()
    player_rect.center = (350,250) #location

    # adding characters
    #Simon
    simon = pygame.image.load("simon.png").convert_alpha() #load simon image
    simon_rect = simon.get_rect()
    simon_rect.center = 100, 200

    #Piggy
    piggy = pygame.image.load("piggy,png").convert_alpha() #load piggy's image
    piggy_rect = piggy.get()
    piggy_rect.center = (150, 200)

    #Jack is the kid who becomes wild and barbaric

    jack = pygame.image.load("jack.png").convert_alpha() #loan Jack's image
    jack_rect = jack.get()
    jack_rect.center = (180, 180)

    #That makes a total of 4 players
    #just in case I am adding an extra
    #I am commenting it out

    #Ralph

    #ralph = pygame.image.load("ralph.png").convert_alpha()
    #ralph_rect = ralph.get(0
    #ralph_rect.center = (150, 150)


    # adding inventory items

    spear = pygame.image.load("spear.png").convert_alpha()
    spear_rect = spear.get_rect()
    spear_rect.center = 750,400

    rock = pygame.image.load("rock.png").convert_alpha()
    #rock = pygame.transform.scale(rock, (200, 200)) Use this line as a reference to scale an image
    rock_rect = rock.get_rect()
    rock_rect.center = 540, 200

    torch = pygame.image.load("torch.png").convert_alpha()
    torch_rect = torch.get_rect()
    torch_rect.center = 300, 200

    glasses = pygame.image.load("glasses.png").convert_alpha()
    glasses_rect = glasses.get_rect()
    glasses_rect.center = 150, 300

    bag = pygame.image.load("sleeping_bag.png").convert_alpha()
    bag_rect = bag.get_rect()
    bag_rect.center = 400, 300

    # Clock starts
    clock = pygame.time.Clock()

    frame_count = 0;
    playing = True
    is_facing_left = True #player

    # Variable to track text on the screen. If you set the dialog string to something and set the position and the
    # counter, the text will show on the screen for dialog_counter number of frames.
    dialog_counter = 0
    dialog = ''
    dialog_position = (300, 200)

    # Load font
    pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)


    # create the inventory and make it empty
    inventory = {}

    # This list should hold all the sprite rectangles that get shifted with a key press.
    rect_list = [spear_rect, rock_rect, torch_rect, bag_rect]

    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((170,190,190))

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        # check for keys that are pressed
        # Note the indent makes it part of the while playing but not part of the for event loop.
        keys = pygame.key.get_pressed()
        # check for specific keys
        # movement says how the world should shift. Pressing keys changes the value in the movement variables.
        movement_x = 0
        movement_y = 0
        if keys[pygame.K_LEFT]:
            is_facing_left = True
            movement_x += 5
        if keys[pygame.K_RIGHT]:
            is_facing_left = False
            movement_x -= 5
        if keys[pygame.K_UP]:
            movement_y += 5
        if keys[pygame.K_DOWN]:
            movement_y -= 5

        # Move all the sprites in the scene by movement amount.
        # You can still move the rect of an individual sprite to make
        # it move around the landscape.
        for rect in rect_list:
            rect.move_ip(movement_x, movement_y)

        # Check for touching boar.
        if hero_rect.colliderect(ghost_rect):
            # Respond differently depending on gold status
            if "gold" in inventory and "sword" in inventory:
                dialog = "GO Manny!"
            elif "gold" in inventory:
                dialog = "Welcome rich friend!"
            elif "sword" in inventory:
                dialog = "Oh no. don't hurt me!"
            else:
                dialog = "Go away loser!"
            # These say where and for how long the dialog prints on the screen
            dialog_counter = 50
            dialog_position = (100, 100)

        # Check for touching spear .
        if hero_rect.colliderect(treasure_rect) and "gold" not in inventory:
            inventory["gold"] = True
            dialog = "Gold added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        if hero_rect.colliderect(sword_rect) and "sword" not in inventory:
            inventory["sword"] = True
            dialog = "Sword added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        # Draw the characters
        screen.blit(ghost, ghost_rect)
        pygame.draw.rect(screen, (0,255,0), ghost_rect, 3)

        # Only draw the gold if it hasn't been picked up
        if "gold" not in inventory:
            screen.blit(treasure, treasure_rect)

        if "sword" not in inventory:
            screen.blit(sword, sword_rect)

        # Pick the sprite frame to draw
        hero_sprite = hero[frame_count%len(hero)]
        # Flip the sprite depending on direction
        if not is_facing_left:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)
        screen.blit(hero_sprite, hero_rect)
        pygame.draw.rect(screen, (0,255,0), hero_rect, 3)

        # draw any dialog
        if dialog:
            pygame.draw.rect(screen, (200, 220, 220), (50, 425, 600, 50))
            textsurface = myfont.render(dialog, False, (0, 0, 0))
            screen.blit(textsurface, (75, 430))
            # Track how long the dialog is on screen
            dialog_counter -= 1
            if dialog_counter == 0:
                dialog = ''



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
