import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# ================= WINDOW =================
WIDTH, HEIGHT = 400, 600
GROUND_Y = 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

# ================= FONTS =================
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 25)

# ================= ASSETS =================
bird_img = pygame.image.load("assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (80, 80))
PIPE_WIDTH, PIPE_HEIGHT, PIPE_GAP = 110, 300, 250
pipe_img = pygame.image.load("assets/pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))
pipe_img_flip = pygame.transform.flip(pipe_img, False, True)

jump_sound = pygame.mixer.Sound("assets/jump.wav")
gameover_sound = pygame.mixer.Sound("assets/gameover.wav")
pygame.mixer.music.load("assets/bg.ogg")
pygame.mixer.music.set_volume(0.4)

# ================= FLAGS =================
click_sound_enabled = True
jump_enabled = True
gameover_enabled = True
bg_music_enabled = True

# ================= HIGH SCORE =================
highscore_file = "highscore.txt"
if not os.path.exists(highscore_file):
    with open(highscore_file, "w") as f:
        f.write("0")

def load_highscore():
    with open(highscore_file, "r") as f:
        return int(f.read())

def save_highscore(score):
    with open(highscore_file, "w") as f:
        f.write(str(score))

highscore = load_highscore()

# ================= CLOUDS =================
clouds = [{"x": random.randint(0,WIDTH), "y": random.randint(20,150), "speed": random.uniform(0.2,0.5)} for _ in range(5)]

# ================= BUTTONS =================
def draw_3d_button(rect, text, base_color, hover_color, pressed=False):
    # 3D effect: draw shadow / depth
    shadow_offset = 5 if not pressed else 2
    pygame.draw.rect(screen, (50,50,50), (rect.x, rect.y+shadow_offset, rect.width, rect.height), border_radius=10)
    color = hover_color if rect.collidepoint(pygame.mouse.get_pos()) else base_color
    top_offset = 0 if pressed else -shadow_offset
    pygame.draw.rect(screen, color, (rect.x, rect.y+top_offset, rect.width, rect.height), border_radius=10)
    txt = font.render(text, True, (255,255,255))
    screen.blit(txt, txt.get_rect(center=rect.center))

# ================= HEADPHONES QUESTIONS =================
def ask_headphones():
    global jump_enabled, gameover_enabled, bg_music_enabled
    asking = True
    stage = 0
    both_yes = False
    button_w, button_h = 100, 50

    while asking:
        screen.fill((135, 206, 235))
        for c in clouds:  # animate clouds
            c["x"] += c["speed"]
            if c["x"]>WIDTH+50: c["x"]=-50
            pygame.draw.ellipse(screen,(255,255,255),(c["x"],c["y"],80,50))
        question = "Are you wearing headphones?" if stage==0 else "Are you sure?"
        screen.blit(font.render(question, True, (0,0,0)), (WIDTH//2-180, HEIGHT//2-100))

        yes_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, button_w, button_h)
        no_rect = pygame.Rect(WIDTH//2 + 50, HEIGHT//2, button_w, button_h)
        draw_3d_button(yes_rect,"Yes",(0,200,0),(0,255,0))
        draw_3d_button(no_rect,"No",(200,0,0),(255,0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if yes_rect.collidepoint(mx,my):
                    if stage==0:
                        stage=1
                        both_yes=True
                    else:
                        asking=False
                        both_yes=both_yes
                if no_rect.collidepoint(mx,my):
                    asking=False
                    both_yes=False

    if both_yes:
        jump_enabled, gameover_enabled, bg_music_enabled = True, True, False
    else:
        jump_enabled, gameover_enabled, bg_music_enabled = False, False, True

ask_headphones()

# ================= START SCREEN =================
def show_start_screen():
    waiting=True
    while waiting:
        screen.fill((135,206,235))
        for c in clouds:  # animate clouds
            c["x"] += c["speed"]
            if c["x"]>WIDTH+50: c["x"]=-50
            pygame.draw.ellipse(screen,(255,255,255),(c["x"],c["y"],80,50))
        screen.blit(font.render("Flappy Bird Clone", True,(0,0,0)), (WIDTH//2-110, HEIGHT//2-50))
        screen.blit(small_font.render("Tap or press SPACE to start", True,(0,0,0)), (WIDTH//2-120, HEIGHT-50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE) or event.type==pygame.MOUSEBUTTONDOWN:
                waiting=False

show_start_screen()

# ================= RESET GAME =================
def reset_game():
    global score
    if bg_music_enabled:
        pygame.mixer.music.play(-1)
    bird_x, bird_y, bird_velocity = 50, 250, 0
    pipe_x, pipe_center_y = WIDTH, random.randint(200,350)
    game_over, sound_played, score = False, False, 0
    return bird_x, bird_y, bird_velocity, pipe_x, pipe_center_y, game_over, sound_played

bird_x, bird_y, bird_velocity, pipe_x, pipe_center_y, game_over, sound_played = reset_game()

# ================= PHYSICS =================
gravity, jump_strength, pipe_speed = 0.25, -7, 3

# ================= GAME LOOP =================
running = True
while running:
    screen.fill((135,206,235))
    for c in clouds:
        c["x"] += c["speed"]
        if c["x"]>WIDTH+50: c["x"]=-50
        pygame.draw.ellipse(screen,(255,255,255),(c["x"],c["y"],80,50))
    pygame.draw.rect(screen,(0,200,0),(0,GROUND_Y,WIDTH,50))

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if not game_over:
            if (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE) or (event.type==pygame.MOUSEBUTTONDOWN):
                bird_velocity=jump_strength
                if jump_enabled: jump_sound.play()
        else:
            if event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if restart_rect.collidepoint((mx,my)):
                    bird_x, bird_y, bird_velocity, pipe_x, pipe_center_y, game_over, sound_played = reset_game()
                if home_rect.collidepoint((mx,my)):
                    ask_headphones()
                    show_start_screen()
                    bird_x, bird_y, bird_velocity, pipe_x, pipe_center_y, game_over, sound_played = reset_game()

    # ================= GAME LOGIC =================
    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity
        pipe_x -= pipe_speed

        if pipe_x<-PIPE_WIDTH:
            pipe_x=WIDTH
            pipe_center_y=random.randint(200,350)
            score = score + 1
            if score>highscore:
                highscore=score
                save_highscore(highscore)

        top_pipe_y=pipe_center_y-PIPE_GAP//2-PIPE_HEIGHT
        bottom_pipe_y=pipe_center_y+PIPE_GAP//2

        bird_rect = pygame.Rect(bird_x,bird_y,80,80)
        top_pipe_rect = pygame.Rect(pipe_x,top_pipe_y,PIPE_WIDTH,PIPE_HEIGHT)
        bottom_pipe_rect = pygame.Rect(pipe_x,bottom_pipe_y,PIPE_WIDTH,PIPE_HEIGHT)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect) or bird_y+80>=GROUND_Y:
            game_over=True
            if bg_music_enabled: pygame.mixer.music.stop()

    if game_over and not sound_played:
        if gameover_enabled: gameover_sound.play()
        sound_played=True

    # ================= DRAW =================
    screen.blit(pipe_img_flip,(pipe_x,top_pipe_y))
    screen.blit(pipe_img,(pipe_x,bottom_pipe_y))
    # Bird rotation + bobbing
    angle = -bird_velocity*3
    bob = 3*random.uniform(-1,1)
    rotated_bird = pygame.transform.rotate(bird_img, angle)
    screen.blit(rotated_bird, (bird_x, bird_y+bob))

    # ================= SCORE =================
    score_text = font.render(f"Score: {score}", True,(0,0,0))
    screen.blit(score_text,(10,10))
    high_text = font.render(f"Highscore: {highscore}", True,(0,0,0))
    screen.blit(high_text,(10,40))

    # ================= GAME OVER BUTTONS =================
    if game_over:
        restart_rect=pygame.Rect(130,260,140,50)
        home_rect=pygame.Rect(WIDTH-120,20,100,40)
        draw_3d_button(restart_rect,"RESTART",(0,0,0),(50,50,50))
        draw_3d_button(home_rect,"HOME",(0,0,200),(0,0,255))
        screen.blit(font.render("GAME OVER",True,(255,0,0)),(110,200))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
