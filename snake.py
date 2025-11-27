# importing libraries
import pygame # ייבוא ספריית pygame למשחקים
import time # ייבוא ספריית time לשימוש בפונקציות זמן
import random # ייבוא ספריית random ליצירת מספרים ומיקומים אקראיים

snake_speed = 15 # הגדרת מהירות הנחש (כמות הפריימים לשנייה)

# Window size
window_x = 720 # רוחב חלון המשחק
window_y = 480 # גובה חלון המשחק

# defining colors
black = pygame.Color(0, 0, 0) # הגדרת צבע שחור (רקע)
white = pygame.Color(255, 255, 255) # הגדרת צבע לבן (לציור הפרי)
red = pygame.Color(255, 0, 0) # הגדרת צבע אדום (לכשלון המשחק)
green = pygame.Color(0, 255, 0) # הגדרת צבע ירוק (לנחש)
blue = pygame.Color(0, 0, 255) # הגדרת צבע כחול (לא בשימוש בקוד זה)

# Initialising pygame
pygame.init() # אתחול כל המודולים הנדרשים של pygame

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes') # הגדרת כותרת חלון המשחק
game_window = pygame.display.set_mode((window_x, window_y)) # יצירת חלון המשחק בגודל שהוגדר

# FPS (frames per second) controller
fps = pygame.time.Clock() # יצירת אובייקט Clock לבקרת קצב הפריימים

# defining snake default position
snake_position = [100, 50] # הגדרת מיקום ראשוני (קואורדינטות X, Y) של ראש הנחש

# defining first 4 blocks of snake body
snake_body = [[100, 50], # רשימה המייצגת את גוף הנחש
              [90, 50],  # כל רשימה פנימית היא בלוק בגוף הנחש
              [80, 50],
              [70, 50]
              ]

# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10,  # מיקום אקראי ראשוני של הפרי
                  random.randrange(1, (window_y//10)) * 10]  # הקואורדינטות תמיד כפולות של 10

fruit_spawn = True # דגל שמציין האם יש פרי על המסך

# setting default snake direction towards right
direction = 'RIGHT' # כיוון התנועה הנוכחי של הנחש
change_to = direction # הכיוון שאליו הנחש צריך לשנות את תנועתו (בהתאם לקלט המשתמש)

# initial score
score = 0 # ניקוד התחלתי

# displaying Score function
def show_score(choice, color, font, size):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size) # יצירת אובייקט גופן להצגת הניקוד
    
    # create the display surface object score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color) # יצירת משטח טקסט לניקוד
    
    # create a rectangular object for the text surface object
    score_rect = score_surface.get_rect() # קבלת מלבן המייצג את משטח הטקסט
    
    # displaying text
    game_window.blit(score_surface, score_rect) # ציור הניקוד על חלון המשחק

# game over function
def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50) # יצירת גופן להודעת כשלון
    
    # creating a text surface on which text will be drawn
    game_over_surface = my_font.render( # יצירת משטח טקסט עם הניקוד הסופי
        'Your Score is : ' + str(score), True, red)
    
    # create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect() # קבלת מלבן המייצג את משטח הטקסט
    
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4) # מיקום הטקסט במרכז העליון של החלון
    
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect) # ציור הודעת הכשלון על המסך
    pygame.display.flip() # עדכון כל המסך כדי להציג את ההודעה
    
    # after 2 seconds we will quit the program
    time.sleep(2) # השהיית התוכנית ל-2 שניות
    
    # deactivating pygame library
    pygame.quit() # ביטול אתחול ספריית pygame
    
    # quit the program
    quit() # יציאה מהתוכנית

# Main Function
while True: # לולאת המשחק הראשית שרצה כל עוד המשחק פעיל
    
    # handling key events
    for event in pygame.event.get(): # לולאה שעוברת על כל האירועים שהתרחשו
        if event.type == pygame.KEYDOWN: # אם התרחש אירוע של לחיצה על מקש
            if event.key == pygame.K_UP: # אם המקש הוא חץ למעלה
                change_to = 'UP' # שינוי הכיוון המבוקש למעלה
            if event.key == pygame.K_DOWN: # אם המקש הוא חץ למטה
                change_to = 'DOWN' # שינוי הכיוון המבוקש למטה
            if event.key == pygame.K_LEFT: # אם המקש הוא חץ שמאלה
                change_to = 'LEFT' # שינוי הכיוון המבוקש שמאלה
            if event.key == pygame.K_RIGHT: # אם המקש הוא חץ ימינה
                change_to = 'RIGHT' # שינוי הכיוון המבוקש ימינה

    # If two keys pressed simultaneously we don't want snake to move into two directions simultaneously
    # מניעת תנועה הפוכה מיידית (למשל ממעלה למטה מיד)
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    # עדכון מיקום ראש הנחש בהתאם לכיוון הנוכחי
    if direction == 'UP':
        snake_position[1] -= 10 # הפחתת ערך ה-Y (תזוזה למעלה)
    if direction == 'DOWN':
        snake_position[1] += 10 # הגדלת ערך ה-Y (תזוזה למטה)
    if direction == 'LEFT':
        snake_position[0] -= 10 # הפחתת ערך ה-X (תזוזה שמאלה)
    if direction == 'RIGHT':
        snake_position[0] += 10 # הגדלת ערך ה-X (תזוזה ימינה)

    # Snake body growing mechanism
    # אם הנחש אוכל פרי הניקוד גדל והגוף מתארך
    snake_body.insert(0, list(snake_position)) # הוספת מיקום הראש החדש לתחילת הגוף
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10 # אם הנחש אכל את הפרי, הגדל את הניקוד
        fruit_spawn = False # סמן שיש לייצר פרי חדש
    else:
        snake_body.pop() # אם הנחש לא אכל, הסר את הבלוק האחורי (כדי לשמור על אורך קבוע)
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,  # יצירת קואורדינטות X, Y אקראיות חדשות לפרי
                          random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True # הגדרת הדגל בחזרה ל-True (כדי לצייר את הפרי החדש)
    game_window.fill(black) # צביעת הרקע מחדש בשחור (מחיקת התצוגה הקודמת)
    
    for pos in snake_body: # לולאה שרצה על כל בלוק בגוף הנחש
        pygame.draw.rect(game_window, green, # ציור מלבן ירוק לכל בלוק בגוף הנחש
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect( # ציור הפרי (מלבן לבן)
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    # בדיקה אם הנחש נגע בקצוות המסך
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over() # הפעלת פונקציית כשלון המשחק
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over() # הפעלת פונקציית כשלון המשחק

    # Touching the snake body
    # בדיקה אם ראש הנחש נגע בגוף שלו (מתחיל מהאיבר השני ברשימה)
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over() # הפעלת פונקציית כשלון המשחק

    # displaying score continuously
    show_score(1, white, 'times new roman', 20) # קריאה לפונקציית הצגת הניקוד

    # Refresh game screen
    pygame.display.update() # עדכון כל המסך כדי להציג את כל הציורים

    # Frame Per Second / Refresh Rate
    fps.tick(snake_speed) # הגבלת לולאת המשחק ל-15 פריימים לשנייה
