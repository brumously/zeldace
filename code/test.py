import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("NPC Dialogue Interaction")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_SIZE = 30
dialogue_font = pygame.font.Font(None, FONT_SIZE)

# Define the NPC's dialogue
npc_dialogue = [
    "Hello adventurer",
    "This land is overrun with enemies. You shouldn't be here",
    "If you insist on your quest, I cannot stop you",
    "Although I may provide you with a little help",
    "Let me get a closer look at you",
    "Good luck, and no matter what you do, DO NOT GIVE UP",
]

# Define the NPC's position
npc_pos = (400, 300)

# Define the main character's position and movement speed
character_pos = pygame.math.Vector2(100, 100)
character_speed = 0.5
character_radius = 100

# Game state variables
npc_talk = False
show_talk_prompt = False
dialogue_open = False
current_dialogue = 0
dialogue_timer = 0
dialogue_index = 0
dialogue_finished = False

# Function to display the dialogue box
def display_dialogue_box(text):
    dialogue_box_height = FONT_SIZE + 20
    dialogue_box_rect = pygame.Rect(20, screen_height - dialogue_box_height - 10, screen_width - 40, dialogue_box_height)
    border_rect = pygame.Rect(dialogue_box_rect.left - 2, dialogue_box_rect.top - 2, dialogue_box_rect.width + 4, dialogue_box_rect.height + 4)

    pygame.draw.rect(screen, WHITE, border_rect)
    pygame.draw.rect(screen, BLACK, dialogue_box_rect)

    dialogue_text = dialogue_font.render(text, True, WHITE)
    screen.blit(dialogue_text, (dialogue_box_rect.x + 5, dialogue_box_rect.y + 5))

# Game loop
running = True
show_first_line = True
dialogue_text = ""

line_finished=False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t and npc_talk and not dialogue_finished:
                if not dialogue_open:
                    dialogue_open = True
                    dialogue_timer = 0
                    show_first_line = False
                else:
                    if current_dialogue + 1 < len(npc_dialogue):
                            current_dialogue += 1
                            show_first_line = True
                            line_finished=False
                    else:
                        dialogue_finished = True
                        current_dialogue=0
                        #line_finished=True
            elif event.key == pygame.K_RETURN and dialogue_open:
                if dialogue_finished:
                    dialogue_open = False
                    dialogue_index = 0
                

    keys = pygame.key.get_pressed()

    # Reset the character's movement vector
    movement = pygame.math.Vector2(0, 0)

    if keys[pygame.K_LEFT]:
        movement.x -= character_speed
    if keys[pygame.K_RIGHT]:
        movement.x += character_speed
    if keys[pygame.K_UP]:
        movement.y -= character_speed
    if keys[pygame.K_DOWN]:
        movement.y += character_speed

    # Normalize the movement vector if necessary to maintain consistent speed in diagonal movement
    if movement.length() > 0:
        movement.normalize_ip()
        movement *= character_speed

    # Update the character's position
    character_pos += movement

    # Clear the screen
    screen.fill(BLACK)

    # Check if the main character is within the NPC's radius
    distance = character_pos - pygame.math.Vector2(npc_pos)
    if distance.length() <= character_radius:
        npc_talk = True
        show_talk_prompt = True
    else:
        npc_talk = False
        show_talk_prompt = False

    # Draw the main character
    pygame.draw.circle(screen, WHITE, character_pos, 20)

    # Draw the NPC
    pygame.draw.circle(screen, WHITE, npc_pos, 20)

    # Display the talk prompt if the main character is near the NPC
    if show_talk_prompt and not dialogue_finished:
        prompt_text = dialogue_font.render("Press T to talk", True, WHITE)
        screen.blit(prompt_text, (npc_pos[0] - prompt_text.get_width() // 2, npc_pos[1] - 40))

    # Display the dialogue box if it is open
    if dialogue_open:
        if dialogue_finished:
            display_dialogue_box("Press Enter to close")
        else:
            dialogue_text = npc_dialogue[current_dialogue][:dialogue_index]
            if not show_first_line:
                display_dialogue_box(dialogue_text)
            
    # Update the dialogue timer
    if dialogue_open and not dialogue_finished and not line_finished:
        dialogue_timer += 0.3
        if dialogue_timer >= 10:
            dialogue_timer = 0
            if not show_first_line:
                dialogue_index += 1
                if dialogue_index >= len(npc_dialogue[current_dialogue]):
                    dialogue_index = 0
                    show_first_line = True
                    line_finished=True
            else:
                show_first_line = False
                dialogue_index =0  # Set the index to the end of the dialogue
    elif line_finished and not dialogue_finished:
        display_dialogue_box(npc_dialogue[current_dialogue])

    # ...

    # Update the display
    pygame.display.flip()