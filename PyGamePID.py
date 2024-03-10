import pygame
import sys
import math

# Pygame başlat
pygame.init()

# Ekran boyutları
WIDTH = 1000
HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

# PID Denetleyici parametreleri
kp = 0.1
ki = 0.001
kd = 0.1
setpoint = WIDTH // 2  # Hedef çizgi pozisyonu

# PID Denetleyici
class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0
    
    def calculate(self, current_value):
        error = self.setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output

# Araba sınıfı
class Car:
    def __init__(self):
        self.angle = 0
        self.radius = 100  # Dairenin yarıçapı
        self.speed = 2
        self.x = WIDTH // 2 + self.radius
        self.y = HEIGHT // 2
    
    def move(self, error):
        # Hata ve PID çıktısını kullanarak aracın hareketini güncelle
        self.angle += self.speed / self.radius
        self.x = WIDTH // 2 + self.radius * math.cos(self.angle) + error
        self.y = HEIGHT // 2 + self.radius * math.sin(self.angle) + error
    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 10)

pid_controller = PIDController(kp, ki, kd, setpoint)
car = Car()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PID Kontrollü Araç")
clock = pygame.time.Clock()

# Kullanıcı arayüzü elemanları
font = pygame.font.Font(None, 36)
text_color = BLACK
button_color = (100, 100, 100)
hover_color = (150, 150, 150)

def draw_text(screen, text, rect):
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, rect)

def draw_button(screen, rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    draw_text(screen, text, (rect.x + 20, rect.y + 10))

def button_hover(rect, pos):
    return rect.collidepoint(pos)

while True:
    screen.fill(WHITE)
    
    # Kullanıcı arayüzünü çiz
    draw_text(screen, f"kp: {kp}", (50, 50))
    draw_button(screen, pygame.Rect(180, 50, 50, 50), "+")
    draw_button(screen, pygame.Rect(250, 50, 50, 50), "-")
    
    draw_text(screen, f"ki: {ki}", (50, 150))
    draw_button(screen, pygame.Rect(180, 150, 50, 50), "+")
    draw_button(screen, pygame.Rect(250, 150, 50, 50), "-")
    
    draw_text(screen, f"kd: {kd}", (50, 250))
    draw_button(screen, pygame.Rect(180, 250, 50, 50), "+")
    draw_button(screen, pygame.Rect(250, 250, 50, 50), "-")

    # Hedef pozisyonu al
    error = pid_controller.calculate(car.x)
    
    # Arabayı hareket ettir
    car.move(error)
    
    # Arabayı çiz
    car.draw(screen)
    
    # Çizgiyi çiz
    pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), car.radius, 1)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fare tıklamasının kontrolü
            pos = pygame.mouse.get_pos()
            if button_hover(pygame.Rect(180, 50, 50, 50), pos):
                kp += 0.001
                pid_controller.kp = kp  # PID denetleyici parametresini güncelle
            elif button_hover(pygame.Rect(250, 50, 50, 50), pos):
                kp -= 0.001
                pid_controller.kp = kp  # PID denetleyici parametresini güncelle
            elif button_hover(pygame.Rect(180, 150, 50, 50), pos):
                ki += 0.0001
                pid_controller.ki = ki  # PID denetleyici parametresini güncelle
            elif button_hover(pygame.Rect(250, 150, 50, 50), pos):
                ki -= 0.0001
                pid_controller.ki = ki  # PID denetleyici parametresini güncelle
            elif button_hover(pygame.Rect(180, 250, 50, 50), pos):
                kd += 0.001
                pid_controller.kd = kd  # PID denetleyici parametresini güncelle
            elif button_hover(pygame.Rect(250, 250, 50, 50), pos):
                kd -= 0.001
                pid_controller.kd = kd  # PID denetleyici parametresini güncelle

    clock.tick(60)
