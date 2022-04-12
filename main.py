import pygame
from classes import *
from vars import *
from functions import *
import random


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pong')
        # pygame.display.set_icon(icon)

        self.title_font = pygame.font.SysFont("monospace", 50)
        self.engine_font = pygame.font.SysFont("monospace", 15)
        self.game_font = pygame.font.SysFont("monospace", 35)

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.current_framerate = framerate
        self.current_timescale = timescale

        self.game_running = True  
        self.game_started = False
        self.timeElapsed = 0
        self.frame = 1 # 1st frame

        # y start coord is wrong, has to take boundaries into consideration
        self.paddle1 = Paddle('Player', goal_width - paddle_width, (screen_height - boundary_upper) / 2) 
        self.paddle2 = Paddle('Player', screen_width - goal_width, (screen_height - boundary_upper) / 2)
        self.ball = Ball(screen_width / 2, screen_height / 2, -700, 700)

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_ball(self):
        if self.game_started:
            self.ball.update_position(self.current_timescale, self.clock.get_fps(), [self.paddle1, self.paddle2])
        pygame.draw.circle(self.screen, white, (self.ball.x, self.ball.y), ball_radius) # scale is divide by 1000, arg is radius so divide by 2

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_paddles(self):
        self.paddle1.update_position()
        self.paddle2.update_position()
        pygame.draw.rect(self.screen, white, (self.paddle1.x, self.paddle1.y, paddle_width, paddle_height))
        pygame.draw.rect(self.screen, white, (self.paddle2.x, self.paddle2.y, paddle_width, paddle_height))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_pitch(self):
        pygame.draw.line(self.screen, white, (goal_width, 0), (goal_width, screen_height))
        pygame.draw.line(self.screen, white, (screen_width - goal_width, 0), (screen_width - goal_width, screen_height))
        pygame.draw.line(self.screen, white, (0, boundary_upper), (screen_width, boundary_upper))
        pygame.draw.line(self.screen, white, (0, screen_height - boundary_lower), (screen_width, screen_height - boundary_lower))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_engine_labels(self):
        # pygame.draw.line(self.screen, white, (0, screen_height - ui_height), ((screen_width, screen_height - ui_height)), 3)

        framerateLabel = self.engine_font.render(f'{round(self.clock.get_fps())} / {self.current_framerate}', 1, white)
        self.screen.blit(framerateLabel, (screen_width - 90, screen_height - 20))
        timescaleLabel = self.engine_font.render(str(round(self.current_timescale)), 1, white)
        self.screen.blit(timescaleLabel, (screen_width - 30, screen_height - 40))
        timeElapsedLabel = self.engine_font.render(f'{round(self.timeElapsed)} seconds', 1, white)
        self.screen.blit(timeElapsedLabel, (10, screen_height - 20))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def check_goal(self):  # move to ball.update_position?
        scorer = 0
        if self.ball.x + ball_radius < goal_width:
            scorer = 1
            self.paddle2.score += 1
        elif self.ball.x - ball_radius > screen_width - goal_width:
            scorer = 2
            self.paddle1.score += 1
        if scorer > 0:
            self.ball.reset()
            if self.paddle1.score >= 10:
                print('Player 1 won!\nNew game!')
                self.reset_game()
            elif self.paddle2.score >= 10:
                print('Player 2 won!\nNew game!')
                self.reset_game()

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def event_handler(self):
        keys = pygame.key.get_pressed()

        key_value = 1
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            key_value = 10

        if keys[pygame.K_SPACE] and not self.game_started:
            self.game_started = True

        if self.game_started:
            if self.paddle1.controller == 'Player':
                if keys[pygame.K_UP]:
                    self.paddle1.update_position(-5 * key_value)
                elif keys[pygame.K_DOWN]:
                    self.paddle1.update_position(5 * key_value)

            if self.paddle2.controller == 'Player':
                if keys[pygame.K_KP8]:
                    self.paddle2.update_position(-5 * key_value)
                elif keys[pygame.K_KP2]:
                    self.paddle2.update_position(5 * key_value)

        if keys[pygame.K_r]:
            self.reset_game()

        if keys[pygame.K_KP_PLUS]:
            self.current_timescale += key_value / 40
        elif keys[pygame.K_KP_MINUS]:
            self.current_timescale -= key_value / 40

        if keys[pygame.K_ESCAPE]:
            print('Quitting')
            self.game_running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Quitting')
                self.game_running = False
                

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def collision_check(self, body): 
    # sometimes it traps one body inside another
    # clipping is not smooth
        for other_body in [x for x in self.celestialBodyList if x.name != body.name]:
            body_collision_index = self.celestialBodyList.index(other_body) - 1
            other_body_collision_index = self.celestialBodyList.index(body) - 1

            d = distance(other_body, body, False)
            sum_of_radii = ((other_body.diameter / 2) / diameter_scale) + ((body.diameter / 2) / diameter_scale)
            if d <= sum_of_radii:
                # less than 4 frames of collision seems to work
                if body.collisions_in_period[body_collision_index] < 4 and other_body.collisions_in_period[other_body_collision_index] < 4:
                    dx = other_body.posX - body.posX
                    dy = other_body.posY - body.posY
                    collisionTangentAngle = math.atan2(dy, dx)

                    body.velocityAngle = 2 * collisionTangentAngle + body.velocityAngle
                    other_body.velocityAngle = 2 * collisionTangentAngle + other_body.velocityAngle

                    body.velocityModule, other_body.velocityModule = elastic_collision(body.velocityModule, body.mass, other_body.velocityModule, other_body.mass)

                    # print(f'{body.velocityModule:.3f} {body.velocityAngle:.3f}')
                    # print(f'{other_body.velocityModule:.3f} {other_body.velocityAngle:.3f}')

                    unstuck_angle = 0.5 * math.pi + collisionTangentAngle
    
                    body.posX -= math.cos(unstuck_angle)
                    body.posY += math.sin(unstuck_angle)
                    other_body.posX -= math.cos(unstuck_angle)
                    other_body.posY += math.sin(unstuck_angle)

                    body.collisions_in_period[body_collision_index] += 1
                    other_body.collisions_in_period[other_body_collision_index] += 1

                else: # destroy if velocity too low instead of collisions_in_period?
                    if other_body.mass <= body.mass and other_body.destructible:
                        body.mass += other_body.mass
                        # add volume to self, not just add radius
                        body.diameter = ((((body.diameter / 2) ** 3) + ((other_body.diameter / 2) ** 3)) ** (1/3)) * 2
                        self.to_destroy.append(other_body.destroy())
                    elif body.destructible:
                        other_body.mass += body.mass
                        # add volume to self, not just add radius
                        other_body.diameter = ((((body.diameter / 2) ** 3) + ((other_body.diameter / 2) ** 3)) ** (1/3)) * 2
                        self.to_destroy.append(body.destroy())
            else:
                body.collisions_in_period[body_collision_index] = 0
                other_body.collisions_in_period[other_body_collision_index] = 0


#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_labels(self):
        self.screen.blit(self.title_font.render('Pong', 1, white), ((screen_width / 2) - 65, 10))            
        self.screen.blit(self.game_font.render(str(self.paddle1.score), 1, white), ((screen_width / 2) - 200, 20))            
        self.screen.blit(self.game_font.render(str(self.paddle2.score), 1, white), ((screen_width / 2) + 200, 20))            

        # DEBUG
        # self.screen.blit(self.game_font.render(f'{self.paddle1.y}', 1, blue), ((screen_width / 2), 330))            
        # self.screen.blit(self.game_font.render(f'{self.paddle2.y}', 1, blue), ((screen_width / 2), 630))  

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def reset_game(self):
        self.ball.reset()
        self.paddle1.reset()
        self.paddle2.reset()

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def main_loop(self):
        posX = 0
        posY = 0
        while self.game_running: 
            self.clock.tick(self.current_framerate)

            self.screen.fill(black)

            self.mouseX, self.mouseY = pygame.mouse.get_pos()
            
            self.draw_pitch()
            self.draw_paddles()
            self.draw_ball()
            self.check_goal()


            self.draw_labels()

            self.draw_engine_labels()

            # self.draw_buttons()
            
            self.event_handler()

            self.frame +=1
            self.timeElapsed += self.current_timescale / self.current_framerate

            pygame.display.flip()

        pygame.quit()

#—————————————————————————————————————————————————————————————————————————————————————————————————
#—————————————————————————————————————————————————————————————————————————————————————————————————

# def run_neat():
#     config = neat


if __name__=="__main__":
    game = Game()
    game.main_loop()

    # NEAT stuff
    # local_dir = os.path.dirname(__file__)
    # config_path = os.path.join(local_dir, 'neural_config.txt')
