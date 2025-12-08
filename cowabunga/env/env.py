import numpy as np
from cowabunga.env.actions import Action
from cowabunga.env.objects.cow import Cow
from cowabunga.env.objects.paddle import Paddle
from cowabunga.env.objects.cliff import RightCliff, LeftCliff

class CowabungaEnv():
    """Environment for cowabunga game."""
    def __init__(self, seed: int):
        """Instantiates the class.
        Args:
            seed: seed for random cow generation.
        """
        self.seed = seed
        if self.seed is not None:
            np.random.seed(self.seed)

        self.new_cow_prob = 0.01
        self.max_cows_on_screen = 100
        self.reset()

    def reset(self):
        """Resets env to initial state."""
        self.lives = 3
        self.score = 0
        self.done = False

        self.cows:list[Cow] = []
        self.cliffs:list[LeftCliff, RightCliff] = [LeftCliff(), RightCliff()]
        self.paddle = Paddle()

    def step(self, action: Action):
        """Updates the environment after one instant of time.
        Args:
            action: action taken by the player. Can be NOOP (no action).
        Returns:
            obs: observation of the game by the player, corresponding to state.
            done: whether episode is finished.
            info: additional info.
        """
        # handle action
        if action in (Action.LEFT, Action.RIGHT):
            self.paddle.move(action)
        
        ## update env
        # check collisions
        self.check_collisions()
        # move cows
        self.move_all_cows()
        # check dead cows
        # check safe cows
        # generate new cows
        self.generate_new_cows()
        # update state
        obs = [] #TODO: implement
        info = {}

        return obs, self.done, info

    def check_collisions(self):
        """Checks collisions for all the cows."""
        paddle_hitbox = self.paddle.get_hitbox()
        cliffs_hitboxes = [cliff.get_hitbox() for cliff in self.cliffs]
        for cow in self.cows:
            # check collision with paddle
            if cow.check_collision(paddle_hitbox):
                cow.bounce()
            #check collision with cliff
            landed = False
            for cliff_hitbox in cliffs_hitboxes:
                cow_bottom = cow.y + cow.height
                cliff_top = cliff_hitbox[1]
                if cow.check_collision(cliff_hitbox) and cow_bottom >= cliff_top:
                    cow.land()
                    break
            if not landed:
                cow.freefall()


    def move_all_cows(self):
        """Moves all cows according to their current velocity."""
        for cow in self.cows:
            cow.move()

    def generate_new_cows(self):
        """Evaluates cows on the screen and decides wether to generate a new one."""
        n_cows = len(self.cows)
        if n_cows < self.max_cows_on_screen:
            if n_cows == 0 or np.random.random() < self.new_cow_prob:
                self.cows.append(Cow())