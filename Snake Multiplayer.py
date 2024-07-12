import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import turtle
import time
import random

# Game settings
DELAY = 10
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650


class GameScreen:
    def __init__(self):
        self.wn = turtle.Screen()
        self.wn.title("Snake Game by NJ Production")
        self.wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.wn.bgcolor("#FFEC94")
        self.wn.tracer(0)


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.load_music("sound/melody_bgm.mp3")

    def load_music(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound(self, path):
        sound = pygame.mixer.Sound(path)
        sound.play()


class Player:
    def __init__(self, position, color, name, align):
        self.score = -10
        self.name = name
        self.align = align
        self.display = turtle.Turtle()
        self.display.speed(0)
        self.display.hideturtle()
        self.display.penup()
        self.display.goto(position)
        self.display.pencolor(color)
        self.update_score()

    def update_score(self):
        self.score += 10
        self.display.clear()
        self.display.write(f"{self.name}: {self.score}", align=self.align, font=("ds-digital", 20, "normal"))


class Snake:
    def __init__(self, start_position, color):
        self.body = []
        self.head = self.create_segment(start_position, color)
        self.head.direction = "stop"

    def create_segment(self, position, color):
        segment = turtle.Turtle()
        segment.speed(0)
        segment.color(color)
        segment.shape("square")
        segment.shapesize(0.75, 0.75, 1)
        segment.penup()
        segment.goto(position)
        return segment

    def move(self):
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 10)
        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 10)
        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 10)
        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 10)

    def move_body(self):
        for index in range(len(self.body) - 1, 0, -1):
            x = self.body[index - 1].xcor()
            y = self.body[index - 1].ycor()
            self.body[index].goto(x, y)
        if len(self.body) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.body[0].goto(x, y)

    def add_segment(self, color):
        position = self.head.position()
        segment = self.create_segment(position, color)
        self.body.append(segment)


class Food:
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.shapesize(0.75, 0.75, 1)
        self.food.speed(2)
        self.food.color("#470808")
        self.food.shape("circle")
        self.food.penup()
        self.food.goto(0, 150)

    def generate_food(self):
        x = random.randint(-435, 435)
        y = random.randint(-300, 265)
        self.food.goto(x, y)


class SnakeGame:
    def __init__(self):
        self.screen = GameScreen()
        self.sound_manager = SoundManager()
        self.player1 = Player((-400, 285), "#2A4A1A", "PLAYER 1", "left")
        self.player2 = Player((400, 285), "#2A4A1A", "PLAYER 2", "right")
        self.snake1 = Snake((-200, 0), "#263A29")
        self.snake2 = Snake((200, 0), "#001C30")
        self.food = Food()
        self.delay = DELAY
        self.count1 = 1
        self.count2 = 1
        self.setup_controls()
        self.main_loop()

    def setup_controls(self):
        self.screen.wn.listen()
        self.screen.wn.onkeypress(self.snake1_go_up, "w")
        self.screen.wn.onkeypress(self.snake1_go_down, "s")
        self.screen.wn.onkeypress(self.snake1_go_left, "a")
        self.screen.wn.onkeypress(self.snake1_go_right, "d")
        self.screen.wn.onkeypress(self.snake2_go_up, "Up")
        self.screen.wn.onkeypress(self.snake2_go_down, "Down")
        self.screen.wn.onkeypress(self.snake2_go_left, "Left")
        self.screen.wn.onkeypress(self.snake2_go_right, "Right")

    def snake1_go_up(self):
        if self.snake1.head.direction != "down":
            self.snake1.head.direction = "up"

    def snake1_go_down(self):
        if self.snake1.head.direction != "up":
            self.snake1.head.direction = "down"

    def snake1_go_left(self):
        if self.snake1.head.direction != "right":
            self.snake1.head.direction = "left"

    def snake1_go_right(self):
        if self.snake1.head.direction != "left":
            self.snake1.head.direction = "right"

    def snake2_go_up(self):
        if self.snake2.head.direction != "down":
            self.snake2.head.direction = "up"

    def snake2_go_down(self):
        if self.snake2.head.direction != "up":
            self.snake2.head.direction = "down"

    def snake2_go_left(self):
        if self.snake2.head.direction != "right":
            self.snake2.head.direction = "left"

    def snake2_go_right(self):
        if self.snake2.head.direction != "left":
            self.snake2.head.direction = "right"

    def border_collision(self, snake):
        if (snake.head.xcor() > 435 or snake.head.xcor() < -435 or
                snake.head.ycor() > 275 or snake.head.ycor() < -300):
            self.game_over(snake)

    def body_collision(self, snake):
        for part in snake.body:
            if snake.head.distance(part) < 10:
                self.game_over(snake)

    def snake_collision(self, snake1, snake2):
        if snake1.head.distance(snake2.head) < 10:
            self.game_over(snake1)
        for part in snake2.body:
            if snake1.head.distance(part) < 10:
                self.game_over(snake1)

    def eating_food(self, snake, player, color):
        if snake.head.distance(self.food.food) < 10:
            self.sound_manager.play_sound("sound\generating_food.wav")
            self.food.generate_food()
            snake.add_segment(color)
            player.update_score()
            self.delay += 1

    def game_over(self, snake):
        if snake == self.snake1:
            self.count1 = 0
        else:
            self.count2 = 0
        snake.head.goto(1000, 1000)
        snake.head.direction = "stop"
        for part in snake.body:
            part.goto(1000, 1000)
        snake.body.clear()
        self.sound_manager.play_sound("sound/lose_or_failure.wav")
        time.sleep(2)
        self.sound_manager.load_music("sound/melody_bgm.mp3")

    def clear_display(self, snake, player):
        self.food.food.goto(1000, 1000)
        self.food.food.clear()
        snake.head.goto(1000, 1000)
        snake.head.direction = "stop"
        for parts in snake.body:
            parts.goto(1000, 1000)
        snake.body.clear()
        player.display.clear()
        
    def display_winner(self):
        self.sound_manager.stop_music()
        self.clear_display(self.snake1, self.player1)
        self.clear_display(self.snake2, self.player2)
        self.screen.wn.update()
        time.sleep(1)
        self.screen.wn.bgcolor("#C4D15B")
        self.sound_manager.play_sound("sound\game_over.wav")
        
        message = turtle.Turtle()
        message.speed(0)
        message.hideturtle()
        message.penup()
        message.pencolor("#2B2A4C")
        message.write("GAME OVER", align="center", font=("Jokerman", 80, "normal"))
        self.screen.wn.update()
        time.sleep(4)
        message.clear()
        
        self.sound_manager.play_sound("sound/winner.wav")
        if self.player1.score > self.player2.score:
            message.write("PLAYER 1 WINS!", align="center", font=("Jokerman", 60, "normal"))
        elif self.player2.score > self.player1.score:
            message.write("PLAYER 2 WINS!", align="center", font=("Jokerman", 60, "normal"))
        else:
            message.write("IT'S A DRAW!", align="center", font=("Jokerman", 60, "normal"))
        self.screen.wn.update()
        time.sleep(5)
        message.clear()

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.wn.update()
            if self.count1 == 1:
                self.border_collision(self.snake1)
                self.body_collision(self.snake1)
                self.snake_collision(self.snake1, self.snake2)
                self.eating_food(self.snake1, self.player1, "#224E43")
                self.snake1.move_body()
                self.snake1.move()
            if self.count2 == 1:
                self.border_collision(self.snake2)
                self.body_collision(self.snake2)
                self.snake_collision(self.snake2, self.snake1)
                self.eating_food(self.snake2, self.player2, "#606C5D")
                self.snake2.move_body()
                self.snake2.move()
            if (self.count1 == 0 and self.count2 == 0) or (self.count1 == 0 and self.player1.score < self.player2.score) or (self.count2 == 0 and self.player2.score < self.player1.score):
                self.display_winner()
                break
            clock.tick(self.delay)


if __name__ == "__main__":
    SnakeGame()
