# Flappy Bird AI with NEAT

An AI-powered Flappy Bird game developed using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to navigate through pipes autonomously without pre-programmed strategies.

## Features

- **Classic Flappy Bird Gameplay** - Playable with spacebar
- **AI Training with NEAT** - Neural networks evolve across generations
- **Automatic Saving** - Best genome (bird) saved as `best_bird.pkl`
- **Visual Training** - Watch multiple birds learning simultaneously
- **Configurable Parameters** - Customizable NEAT settings via `config-neat.txt`

## Installation

### Prerequisites
- Python 3.12 or higher
- uv package manager

### Setup
1. Clone repository or download files
2. Navigate to project directory:
   ```bash
   cd flappy-bird
   ```
3. Install dependencies with uv:
   ```bash
   uv sync
   ```

## File Structure

```
flappy-bird/
├── main.py                 # Main training script
├── flappy_bird.py          # Manual playable version
├── flappy_bird_neat.py     # adjusted version of flappy bird for NEAT training  
├── config-neat.txt         # NEAT algorithm configuration
├── pyproject.toml          # Project dependencies
└── imgs/                   # images
    ├── bird1.png
    ├── bird2.png
    ├── bird3.png
    ├── pipe.png
    ├── base.png
    ├── bg.png
    └── message.png
```


## Usage

### Start AI Training
```bash
uv run main.py
```

Training runs automatically and displays:
- Current generation
- Best fitness of generation
- Average fitness
- Number of species

### Test Trained AI
After training completes, the best genome is automatically loaded and tested. The best genome is saved as `best_bird.pkl`.

### Manual Play
```bash
uv run flappy_bird.py
```
Use **Spacebar** to jump


## NEAT Configuration

Key settings in `config-neat.txt`:

- **Population**: 50 genomes per generation
- **Fitness Target**: 1000 points
- **Inputs**: 5 (bird Y-position, velocity, pipe positions, bird distance to pipe)
- **Outputs**: 1 (jump decision)
- **Activation Function**: tanh

## How the AI Works

### Input Data
The AI receives 5 pieces of information:
1. Current Y-position of the bird
2. Vertical velocity of the bird
3. Y-position of the upper pipe
4. Y-position of the lower pipe
5. Horizontal distance to the next pipe

### Decision Making
- Output value > 0.5 → Bird jumps
- Output value ≤ 0.5 → Bird continues falling

### Fitness Evaluation
- **+0.1** per frame alive
- **+5** for each pipe successfully passed
- **-1** upon death
- Training stops when fitness > 1000


## License

This project is created for educational purposes. Graphics assets are not included in the repository and must be obtained separately.

## References

- [NEAT-Python Documentation](https://neat-python.readthedocs.io/)
- [Original NEAT Paper](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf)
- [Pygame Documentation](https://www.pygame.org/docs/)


---