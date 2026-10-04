import pygame
import math
import random

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Lander")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 55)

# =========================================================
# WORLD
# =========================================================

GROUND = 620

PAD_WIDTH = 180
PAD_X = WIDTH // 2 - PAD_WIDTH // 2
PAD_Y = GROUND

# =========================================================
# ROCKET
# =========================================================

ROCKET_WIDTH = 50
ROCKET_HEIGHT = 90

gravity = 0.13
thrust_power = 0.30
rotation_power = 0.06

# =========================================================
# GAME VARIABLES
# =========================================================

x = WIDTH / 2
y = 100

vx = 0
vy = 0

angle = 0
angular_velocity = 0

fuel = 100

game_state = "flying"

# Can be:
#
# "flying"
# "landed"
# "crashed"

explosion_particles = []

shake_timer = 0


# =========================================================
# RESET FUNCTION
# =========================================================

def reset_game():

    global x, y
    global vx, vy
    global angle, angular_velocity
    global fuel
    global game_state
    global explosion_particles
    global shake_timer

    x = WIDTH / 2
    y = 100

    vx = 0
    vy = 0

    angle = 0
    angular_velocity = 0

    fuel = 100

    game_state = "flying"

    explosion_particles = []

    shake_timer = 0


# =========================================================
# EXPLOSION
# =========================================================

def create_explosion(x, y):

    particles = []

    for i in range(80):

        particle_angle = random.uniform(0, math.pi * 2)

        speed = random.uniform(1, 7)

        particle = {

            "x": x,
            "y": y,

            "vx": math.cos(particle_angle) * speed,
            "vy": math.sin(particle_angle) * speed,

            "life": random.randint(30, 70),

            "size": random.randint(2, 7)

        }

        particles.append(particle)

    return particles


# =========================================================
# DRAW ROCKET
# =========================================================

def draw_rocket(x, y, angle, engine_on):

    rocket_surface = pygame.Surface(
        (70, 120),
        pygame.SRCALPHA
    )

    # -----------------------------------------------------
    # MAIN BODY
    # -----------------------------------------------------

    pygame.draw.rect(
        rocket_surface,
        (225, 225, 230),
        (25, 25, 20, 55),
        border_radius=5
    )

    # -----------------------------------------------------
    # NOSE CONE
    # -----------------------------------------------------

    pygame.draw.polygon(
        rocket_surface,
        (240, 240, 245),
        [
            (25, 25),
            (35, 5),
            (45, 25)
        ]
    )

    # -----------------------------------------------------
    # WINDOW
    # -----------------------------------------------------

    pygame.draw.circle(
        rocket_surface,
        (80, 170, 220),
        (35, 43),
        6
    )

    pygame.draw.circle(
        rocket_surface,
        (180, 220, 255),
        (33, 41),
        2
    )

    # -----------------------------------------------------
    # FINS
    # -----------------------------------------------------

    pygame.draw.polygon(
        rocket_surface,
        (190, 60, 60),
        [
            (25, 65),
            (13, 85),
            (25, 80)
        ]
    )

    pygame.draw.polygon(
        rocket_surface,
        (190, 60, 60),
        [
            (45, 65),
            (57, 85),
            (45, 80)
        ]
    )

    # -----------------------------------------------------
    # ENGINE
    # -----------------------------------------------------

    pygame.draw.rect(
        rocket_surface,
        (100, 100, 110),
        (28, 80, 14, 7)
    )

    # -----------------------------------------------------
    # FLAME
    # -----------------------------------------------------

    if engine_on:

        flame_length = random.randint(18, 32)

        pygame.draw.polygon(
            rocket_surface,
            (255, 110, 20),
            [
                (28, 87),
                (35, 87 + flame_length),
                (42, 87)
            ]
        )

        pygame.draw.polygon(
            rocket_surface,
            (255, 230, 80),
            [
                (31, 87),
                (35, 87 + flame_length - 8),
                (39, 87)
            ]
        )

    # -----------------------------------------------------
    # ROTATE ROCKET
    # -----------------------------------------------------

    rotated = pygame.transform.rotate(
        rocket_surface,
        -angle
    )

    rect = rotated.get_rect(
        center=(x, y)
    )

    screen.blit(
        rotated,
        rect
    )


# =========================================================
# DRAW EXPLOSION
# =========================================================

def update_and_draw_explosion():

    global explosion_particles

    for particle in explosion_particles:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["vy"] += 0.08

        particle["vx"] *= 0.98
        particle["vy"] *= 0.98

        particle["life"] -= 1

        if particle["life"] > 40:

            color = (255, 240, 80)

        elif particle["life"] > 20:

            color = (255, 120, 30)

        else:

            color = (120, 120, 120)

        pygame.draw.circle(
            screen,
            color,
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )

    explosion_particles = [
        p
        for p in explosion_particles
        if p["life"] > 0
    ]


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                if game_state != "flying":

                    reset_game()

    keys = pygame.key.get_pressed()

    engine_on = False

    # =====================================================
    # PHYSICS
    # =====================================================

    if game_state == "flying":

        # -------------------------------------------------
        # MAIN ENGINE
        # -------------------------------------------------

        if keys[pygame.K_SPACE] and fuel > 0:

            engine_on = True

            thrust_x = (
                math.sin(math.radians(angle))
                * thrust_power
            )

            thrust_y = (
                -math.cos(math.radians(angle))
                * thrust_power
            )

            vx += thrust_x
            vy += thrust_y

            fuel -= 0.08

            if fuel < 0:

                fuel = 0

        # -------------------------------------------------
        # ROTATION
        # -------------------------------------------------

        if keys[pygame.K_a]:

            angular_velocity -= rotation_power

        if keys[pygame.K_d]:

            angular_velocity += rotation_power

        # -------------------------------------------------
        # GRAVITY
        # -------------------------------------------------

        vy += gravity

        # -------------------------------------------------
        # POSITION UPDATE
        # -------------------------------------------------

        x += vx
        y += vy

        angle += angular_velocity

        # rotational damping
        angular_velocity *= 0.985

        # -------------------------------------------------
        # KEEP ANGLE READABLE
        # -------------------------------------------------

        if angle > 180:

            angle -= 360

        if angle < -180:

            angle += 360

        # =================================================
        # GROUND COLLISION
        # =================================================

        rocket_bottom = y + 40

        if rocket_bottom >= GROUND:

            # Is rocket over landing pad?

            on_pad = (
                x > PAD_X
                and
                x < PAD_X + PAD_WIDTH
            )

            safe_vertical_speed = abs(vy) < 1.8

            safe_horizontal_speed = abs(vx) < 1.2

            safe_angle = abs(angle) < 8

            if (
                on_pad
                and safe_vertical_speed
                and safe_horizontal_speed
                and safe_angle
            ):

                game_state = "landed"

                y = GROUND - 40

                vx = 0
                vy = 0

                angular_velocity = 0

            else:

                game_state = "crashed"

                explosion_particles = create_explosion(
                    x,
                    y
                )

                shake_timer = 20

    # =====================================================
    # SCREEN SHAKE
    # =====================================================

    shake_x = 0
    shake_y = 0

    if shake_timer > 0:

        shake_x = random.randint(-6, 6)
        shake_y = random.randint(-6, 6)

        shake_timer -= 1

    # =====================================================
    # DRAW BACKGROUND
    # =====================================================

    screen.fill(
        (10, 12, 25)
    )

    # Stars

    random.seed(42)

    for i in range(80):

        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, 500)

        pygame.draw.circle(
            screen,
            (180, 180, 200),
            (
                star_x + shake_x,
                star_y + shake_y
            ),
            1
        )

    random.seed()

    # =====================================================
    # DRAW GROUND
    # =====================================================

    pygame.draw.rect(
        screen,
        (45, 45, 55),
        (
            0,
            GROUND + shake_y,
            WIDTH,
            HEIGHT - GROUND
        )
    )

    # =====================================================
    # LANDING PAD
    # =====================================================

    pygame.draw.rect(
        screen,
        (200, 200, 210),
        (
            PAD_X + shake_x,
            PAD_Y + shake_y,
            PAD_WIDTH,
            8
        )
    )

    pygame.draw.line(
        screen,
        (255, 200, 50),
        (
            PAD_X + shake_x,
            PAD_Y + 8 + shake_y
        ),
        (
            PAD_X + PAD_WIDTH + shake_x,
            PAD_Y + 8 + shake_y
        ),
        3
    )

    # =====================================================
    # DRAW ROCKET
    # =====================================================

    if game_state != "crashed":

        draw_rocket(
            x + shake_x,
            y + shake_y,
            angle,
            engine_on
        )

    # =====================================================
    # EXPLOSION
    # =====================================================

    if game_state == "crashed":

        update_and_draw_explosion()

    # =====================================================
    # INFORMATION
    # =====================================================

    speed_text = font.render(
        f"Vertical speed: {vy:.2f}",
        True,
        (240, 240, 240)
    )

    horizontal_text = font.render(
        f"Horizontal speed: {vx:.2f}",
        True,
        (240, 240, 240)
    )

    angle_text = font.render(
        f"Angle: {angle:.1f}°",
        True,
        (240, 240, 240)
    )

    fuel_text = font.render(
        f"Fuel: {fuel:.0f}%",
        True,
        (240, 240, 240)
    )

    screen.blit(
        speed_text,
        (20, 20)
    )

    screen.blit(
        horizontal_text,
        (20, 50)
    )

    screen.blit(
        angle_text,
        (20, 80)
    )

    screen.blit(
        fuel_text,
        (20, 110)
    )

    # =====================================================
    # LANDING
    # =====================================================

    if game_state == "landed":

        message = big_font.render(
            "SUCCESSFUL LANDING!",
            True,
            (100, 255, 130)
        )

        restart = font.render(
            "Press R to launch again",
            True,
            (230, 230, 230)
        )

        screen.blit(
            message,
            message.get_rect(
                center=(WIDTH / 2, 300)
            )
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH / 2, 350)
            )
        )

    # =====================================================
    # CRASH
    # =====================================================

    if game_state == "crashed":

        message = big_font.render(
            "ROCKET DESTROYED",
            True,
            (255, 80, 80)
        )

        restart = font.render(
            "Press R to try again",
            True,
            (230, 230, 230)
        )

        screen.blit(
            message,
            message.get_rect(
                center=(WIDTH / 2, 280)
            )
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH / 2, 335)
            )
        )

    # =====================================================
    # CONTROLS
    # =====================================================

    controls = font.render(
        "SPACE: engine     A / D: rotate",
        True,
        (150, 150, 165)
    )

    screen.blit(
        controls,
        (
            WIDTH - controls.get_width() - 20,
            20
        )
    )

    # =====================================================
    # SHOW FRAME
    # =====================================================

    pygame.display.flip()

    clock.tick(60)


pygame.quit()