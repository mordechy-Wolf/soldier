import pygame
import os

# אתחול pygame
pygame.init()

# --- מנגנון לתיקון נתיבים ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
def get_path(relative_path):
    return os.path.join(SCRIPT_DIR, relative_path)
# -----------------------------

# הגדרות מסך
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('שיעור אנימציה - Pygame')

# שעון למסגור FPS
clock = pygame.time.Clock()
FPS = 60

# צבעים
BLACK = (0, 0, 0)

# משתני דמות
character_x = SCREEN_WIDTH // 2
character_y = SCREEN_HEIGHT // 2
character_speed = 5
character_flip = False  # False = פונה ימינה, True = פונה שמאלה

# משתני אנימציה
current_animation = 'Idle'  # 'Idle' או 'Run'
frame_index = 0
animation_timer = 0
ANIMATION_COOLDOWN = 100  # מילישניות בין פריימים

# משתני תנועה
moving_left = False
moving_right = False


def load_animation_frames(animation_name, scale=1.65):
    """
    פונקציה שטוענת את כל הפריימים של אנימציה מסוימת
    
    Parameters:
        animation_name: שם האנימציה ('Idle' או 'Run')
        scale: גודל הגדלה של התמונות
    
    Returns:
        רשימה של תמונות (pygame.Surface)
    """
    frames = []
    # הנתיב המלא לתיקיית האנימציה
    folder_path = get_path(os.path.join('img', 'player', animation_name))
    
    # ספירת מספר הקבצים בתיקייה
    num_of_frames = len(os.listdir(folder_path))
    
    # טעינת כל התמונות
    for i in range(num_of_frames):
        img_path = get_path(os.path.join('img', 'player', animation_name, f'{i}.png'))
        img = pygame.image.load(img_path).convert_alpha()
        
        # שינוי גודל התמונה
        new_width = int(img.get_width() * scale)
        new_height = int(img.get_height() * scale)
        img = pygame.transform.scale(img, (new_width, new_height))
        
        frames.append(img)
    
    return frames


def update_animation(animations, current_anim, frame_idx, anim_timer):
    """
    פונקציה שמעדכנת את האנימציה - מחליפה בין פריימים
    
    Parameters:
        animations: מילון של כל האנימציות
        current_anim: האנימציה הנוכחית
        frame_idx: אינדקס הפריים הנוכחי
        anim_timer: טיימר לבדיקה מתי להחליף פריים
    
    Returns:
        frame_idx, anim_timer מעודכנים
    """
    current_time = pygame.time.get_ticks()
    
    # בדיקה האם עבר מספיק זמן כדי להחליף פריים
    if current_time - anim_timer > ANIMATION_COOLDOWN:
        anim_timer = current_time
        frame_idx += 1
        
        # אם הגענו לסוף האנימציה, חוזרים להתחלה
        if frame_idx >= len(animations[current_anim]):
            frame_idx = 0
    
    return frame_idx, anim_timer


def draw_character(animations, current_anim, frame_idx, x, y, flip):
    """
    פונקציה שמציירת את הדמות על המסך
    
    Parameters:
        animations: מילון של כל האנימציות
        current_anim: האנימציה הנוכחית
        frame_idx: אינדקס הפריים להציג
        x, y: מיקום הדמות
        flip: האם להפוך את התמונה אופקית
    """
    current_frame = animations[current_anim][frame_idx]
    flipped_frame = pygame.transform.flip(current_frame, flip, False)
    
    # יצירת rect למיקום הדמות (מרכז התמונה במיקום x, y)
    frame_rect = flipped_frame.get_rect()
    frame_rect.center = (x, y)
    
    screen.blit(flipped_frame, frame_rect)


# טעינת האנימציות
print("טוען אנימציות...")
animations = {
    'Idle': load_animation_frames('Idle'),
    'Run': load_animation_frames('Run')
}
print(f"נטענו {len(animations['Idle'])} פריימים של Idle")
print(f"נטענו {len(animations['Run'])} פריימים של Run")

# לולאת המשחק הראשית
run = True
while run:
    clock.tick(FPS)
    
    # טיפול באירועים
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # לחיצה על מקש
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
        
        # שחרור מקש
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
    
    # עדכון תנועה
    previous_animation = current_animation  # שמירת האנימציה הקודמת
    
    if moving_left:
        character_x -= character_speed
        character_flip = True
        current_animation = 'Run'
    elif moving_right:
        character_x += character_speed
        character_flip = False
        current_animation = 'Run'
    else:
        current_animation = 'Idle'
    
    # אם החלפנו אנימציה - מאפסים את האינדקס
    if previous_animation != current_animation:
        frame_index = 0
        animation_timer = pygame.time.get_ticks()
    
    # עדכון אנימציה
    frame_index, animation_timer = update_animation(
        animations, 
        current_animation, 
        frame_index, 
        animation_timer
    )
    
    # ציור
    screen.fill(BLACK)
    draw_character(
        animations, 
        current_animation, 
        frame_index, 
        character_x, 
        character_y, 
        character_flip
    )
    
    pygame.display.update()

pygame.quit()