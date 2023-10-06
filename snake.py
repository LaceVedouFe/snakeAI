import os
import random
import pygame
import numpy as np
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential, load_model


class App:
    def __init__(self):
        self.running = True
        pygame.init()
        self.cell = 25
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)

    def render(self):
        self.screen.fill((0, 0, 0))

        for pos in snake.body:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(pos[0], pos[1], self.cell, self.cell))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(apple.pos[0], apple.pos[1], self.cell, self.cell))

        # max_score_text = self.font.render("Max score: " + str(env.mscore), True, (255, 255, 255))
        # score_text = self.font.render("Score: " + str(env.score), True, (255, 255, 255))
        # gen_text = self.font.render("Gen: " + str(env.gen), True, (255, 255, 255))
        # state_text = self.font.render("State: " + str(env.state), True, (255, 255, 255))
        # action_text = self.font.render("Act: " + dirs[action], True, (255, 255, 255))
        # reward_text = self.font.render("Reward: " + str(env.reward), True, (255, 255, 255))

        # self.screen.blit(max_score_text, (10, 10))
        # self.screen.blit(score_text, (10, 46))
        # self.screen.blit(gen_text, (10, 82))
        # self.screen.blit(reward_text, (10, self.height - 46))
        # self.screen.blit(state_text, (10, self.height - 82))

        pygame.display.flip()
        clock.tick(144)


class Environment:
    def __init__(self):
        self.old_distance = [0, 0]
        self.distance = [snake.head[0] - apple.pos[0], snake.head[1] - apple.pos[1]]
        self.score = self.mscore = self.reward = 0
        self.gen = 1
        self.state = []

    def get_game_state(self):
        self.state = []
        self.state.append(1) if apple.pos[1] < snake.head[1] else self.state.append(0)
        self.state.append(1) if apple.pos[0] > snake.head[0] else self.state.append(0)
        self.state.append(1) if apple.pos[1] > snake.head[1] else self.state.append(0)
        self.state.append(1) if apple.pos[0] < snake.head[0] else self.state.append(0)

        self.state.append(1) if \
            (any([k[1] + app.cell == snake.head[1] and k[0] == snake.head[0] for k in snake.body[1:]]) or
             snake.head[1] == 0) else self.state.append(0)
        self.state.append(1) if \
            (any([k[0] - app.cell == snake.head[0] and k[1] == snake.head[1] for k in snake.body[1:]]) or
             snake.head[0] == app.height - app.cell) else self.state.append(0)
        self.state.append(1) if \
            (any([k[1] - app.cell == snake.head[1] and k[0] == snake.head[0] for k in snake.body[1:]]) or
             snake.head[1] == app.width - app.cell) else self.state.append(0)
        self.state.append(1) if \
            (any([k[0] + app.cell == snake.head[0] and k[1] == snake.head[1] for k in snake.body[1:]]) or
             snake.head[0] == 0) else self.state.append(0)

        self.state.append(1) if snake.dir == 0 else self.state.append(0)
        self.state.append(1) if snake.dir == 1 else self.state.append(0)
        self.state.append(1) if snake.dir == 2 else self.state.append(0)
        self.state.append(1) if snake.dir == 3 else self.state.append(0)

    def check_new_distance(self):
        self.old_distance = self.distance
        self.distance = [snake.head[0] - apple.pos[0], snake.head[1] - apple.pos[1]]

    def is_collisison(self):
        if abs(self.distance[0]) < abs(self.old_distance[0]):
            ai.learn(1, choice)
        elif abs(self.distance[1]) < abs(self.old_distance[1]):
            ai.learn(1, choice)
        if abs(self.distance[0]) > abs(self.old_distance[0]):
            ai.learn(-1, choice)
        elif abs(self.distance[1]) > abs(self.old_distance[1]):
            ai.learn(-1, choice)

        if (snake.head in snake.body[1:]) or \
                snake.head[0] < 0 or snake.head[0] >= app.width or snake.head[1] < 0 or snake.head[1] >= app.height:
            ai.learn(-100, choice)
            self.restart()
            self.get_game_state()
            return True

        snake.body.insert(0, list(snake.head))

        if snake.head == apple.pos:
            ai.learn(10, choice)
            apple.create()
            self.score += 1
        else:
            snake.body.pop()

        return False

    def restart(self):
        snake.body = [[app.width / 2, app.height / 2]]
        snake.head = [app.width / 2, app.height / 2]
        apple.create()
        snake.dir = 0
        if self.score > self.mscore:
            self.mscore = self.score
        self.score = 0
        self.gen += 1


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False


class Model:
    def __init__(self):
        self.model = None

    def create_model(self):
        if user_input == 'n':
            self.model = Sequential()
            self.model.add(Dense(128, input_dim=12, activation='relu'))
            self.model.add(Dense(128, activation='relu'))
            self.model.add(Dense(128, activation='relu'))
            self.model.add(Dense(4, activation='softmax'))
            self.model.compile(loss='mse', optimizer=Adam(learning_rate=0.00025))
        else:
            self.model = load_model(user_input)

    def learn(self, n, target):
        env.reward = n
        target[action] = n
        self.model.fit(np.array([env.state]), np.array([target]), epochs=1, verbose=0)


class Apple:
    def __init__(self):
        self.pos = []
        self.create()

    def create(self):
        while True:
            self.pos = [random.randrange(1, app.width // app.cell) * app.cell,
                        random.randrange(1, app.height // app.cell) * app.cell]
            if self.pos not in snake.body:
                break


class Snake:
    def __init__(self, body):
        self.body = body
        self.head = body[0]
        self.dirs = {
            0: 'up',
            1: 'right',
            2: 'down',
            3: 'left'
        }
        self.dir = 0

    def move(self):
        if action == 0 and self.dir != 2:
            self.dir = 0
        elif action == 2 and self.dir != 0:
            self.dir = 2
        elif action == 3 and self.dir != 1:
            self.dir = 3
        elif action == 1 and self.dir != 3:
            self.dir = 1

        if self.dir == 0:
            self.head[1] -= app.cell
        elif self.dir == 2:
            self.head[1] += app.cell
        elif self.dir == 3:
            self.head[0] -= app.cell
        elif self.dir == 1:
            self.head[0] += app.cell


while True:
    user_input = input('"n" to create a new model or name of the model to load it: ')
    if user_input.lower() == 'n':
        user_input = user_input.lower()
        break
    if os.path.exists(user_input):
        break
    user_input += '.keras'
    if os.path.exists(user_input):
        break
    print(f'File "{user_input}" does not exist')

app = App()
snake = Snake([[app.width / 2, app.height / 2]])
apple = Apple()
ai = Model()
env = Environment()

ai.create_model()


clock = pygame.time.Clock()
while app.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                direction = 0
            elif event.key == pygame.K_d:
                direction = 1
            elif event.key == pygame.K_s:
                direction = 2
            elif event.key == pygame.K_a:
                direction = 3
            elif event.key == pygame.K_SPACE:
                ai.model.save(f'models/{input("Название модели: ")}.keras')

    env.check_new_distance()
    env.get_game_state()

    choice = ai.model.predict(np.array([env.state]))[0]
    action = np.argmax(choice)

    snake.move()
    if env.is_collisison():
        continue

    app.render()

pygame.quit()
