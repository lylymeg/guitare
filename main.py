import pygame
import math
import sys

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

# Dimensions de la fenêtre
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guitare Virtuelle Interactive")
clock = pygame.time.Clock()

# Couleurs (Thème Bois / Acoustique Moderne)
BG_COLOR = (25, 20, 18)
WOOD_NECK = (60, 40, 30)
WOOD_BODY = (120, 75, 45)
GOLD = (230, 180, 50)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Polices
font_large = pygame.font.SysFont("Arial", 36, bold=True)
font_medium = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 16)

# Définition des 6 cordes de la guitare (Notes de E2 à E4 en fréquences Hz)
# E2, A2, D3, G3, B3, E4
STRINGS = [
    {"name": "Mi Grave (E2)", "note": "E", "freq": 82.41, "y": 140, "color": (200, 150, 100), "plucked": 0},
    {"name": "La (A2)",        "note": "A", "freq": 110.00, "y": 190, "color": (210, 160, 110), "plucked": 0},
    {"name": "Ré (D3)",        "note": "D", "freq": 146.83, "y": 240, "color": (220, 170, 120), "plucked": 0},
    {"name": "Sol (G3)",       "note": "G", "freq": 196.00, "y": 290, "color": (230, 180, 130), "plucked": 0},
    {"name": "Si (B3)",        "note": "B", "freq": 246.94, "y": 340, "color": (240, 190, 140), "plucked": 0},
    {"name": "Mi Aigu (E4)",   "note": "E", "freq": 329.63, "y": 390, "color": (255, 210, 160), "plucked": 0}
]

def generate_sound(frequency, duration=0.6):
    """Génère un son de corde pincée synthétique (effet guitare)"""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    buffer = bytearray()
    
    for i in range(num_samples):
        t = i / sample_rate
        # Enveloppe exponentielle pour simuler l'extinction de la note (décroissance)
        envelope = math.exp(-3.5 * t)
        # Onde sinusoïdale enrichie pour un son plus chaleureux
        wave = math.sin(2 * math.pi * frequency * t) + 0.5 * math.sin(4 * math.pi * frequency * t)
        val = int(wave * envelope * 32767 * 0.3)
        val = max(-32768, min(32767, val))
        buffer.extend(val.to_bytes(2, byteorder='little', signed=True))
        
    return pygame.mixer.Sound(buffer=bytes(buffer))

# Pré-générer les sons pour chaque corde
for s in STRINGS:
    s["sound"] = generate_sound(s["freq"])

active_string_name = "Clique ou glisse la souris sur les cordes !"

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0] # Clic gauche enfoncé

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Interaction à la souris (pincer les cordes)
    for s in STRINGS:
        # Zone rectangulaire sensible autour de chaque corde
        string_rect = pygame.Rect(80, s["y"] - 12, WIDTH - 160, 24)
        if string_rect.collidepoint(mouse_pos):
            if mouse_pressed and s["plucked"] == 0:
                s["sound"].play()
                s["plucked"] = 15  # Amplitude de vibration visuelle
                active_string_name = f"Corde jouée : {s['name']} ({s['note']})"

    screen.fill(BG_COLOR)

    # 1. Dessin de la caisse / manche de la guitare
    guitar_body = pygame.Rect(60, 100, WIDTH - 120, 330)
    pygame.draw.rect(screen, WOOD_BODY, guitar_body, border_radius=20)
    pygame.draw.rect(screen, WOOD_NECK, (70, 110, WIDTH - 140, 310), border_radius=15)
    pygame.draw.rect(screen, (15, 12, 10), (70, 110, WIDTH - 140, 310), 4, border_radius=15)

    # Rosace centrale décorative
    pygame.draw.circle(screen, (35, 25, 20), (WIDTH // 2, 265), 55)
    pygame.draw.circle(screen, GOLD, (WIDTH // 2, 265), 55, 3)

    # Frettes (barrettes du manche)
    for fx in range(150, WIDTH - 100, 70):
        pygame.draw.line(screen, (180, 180, 180), (fx, 110), (fx, 420), 2)

    # 2. Dessin et animation des cordes
    for s in STRINGS:
        # Effet de vibration si la corde a été pincée
        vibration = math.sin(s["plucked"] * 1.5) * s["plucked"] if s["plucked"] > 0 else 0
        if s["plucked"] > 0:
            s["plucked"] -= 1

        start_pos = (80, s["y"])
        end_pos = (WIDTH - 80, s["y"])
        mid_pos = (WIDTH // 2, s["y"] + int(vibration))

        # Dessin de la corde courbée lors du pincement
        pygame.draw.aalines(screen, s["color"], False, [start_pos, mid_pos, end_pos], 2)

        # Affichage du nom de la note à gauche de la corde
        note_txt = font_small.render(s["note"], True, GOLD)
        screen.blit(note_txt, (45, s["y"] - 10))

    # 3. Affichage du Titre et de l'aide en haut/bas
    title_txt = font_medium.render("GUITARE VIRTUELLE INTERACTIVE", True, WHITE)
    info_txt = font_medium.render(active_string_name, True, GOLD)

    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 25))
    screen.blit(info_txt, (WIDTH // 2 - info_txt.get_width() // 2, HEIGHT - 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()