# snakeAI

## Download and Run
To run the program you will need [Python](https://www.python.org/)

### Installation
Clone the repository and install the required dependencies:

```
git clone https://github.com/LaceVedouFe/snakeAI.git
```
```
pip install tensorflow, pygame
```
## Snake
Snake is trained with reinforcement training.
### Neural Network
Snake contains a neural network. The neural network has an input layer of 12 neurons, 3 hidden layers of 128 neurons, and one output layer of 4 neurons.
### Vision
Snake receives information about the apple and obstacles (its body and the edges of the field):
|State|Possible Values|
|-----|---------------|
|Apple is above the snake|0 or 1|
|Apple is on the right of the snake|0 or 1|
|Apple is below the snake|0 or 1|
|Apple is on the left of the snake|0 or 1|
|Obstacle is above the snake|0 or 1|
|Obstacle is on the right of the snake|0 or 1|
|Obstacle is below the snake|0 or 1|
|Obstacle is on the left of the snake|0 or 1|
|Direction == UP |0 or 1|
|Direction == RIGHT |0 or 1|
|Direction == DOWN |0 or 1|
|Direction == LEFT |0 or 1|
### Rewards
- The snake moves closer to the apple +1
- The snake moves away from the apple -1
- Snake eats an apple +10
- Snake dies -100
