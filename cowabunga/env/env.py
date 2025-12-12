import numpy as np
import cowabunga.env.settings as settings
from cowabunga.env.actions import Action
from cowabunga.env.objects.cow import Cow
from cowabunga.env.objects.paddle import Paddle
from cowabunga.env.objects.cliff import RightCliff, LeftCliff

class CowabungaEnv():
    """Environment for cowabunga game."""
    def __init__(self, seed: int|None=None):
        """Instantiates the class.
        Args:
            seed: seed for random cow generation.
        """
        self.seed = seed
        if self.seed is not None:
            np.random.seed(self.seed)

        self.new_cow_prob = settings.NEW_COW_PROB
        self.max_cows_on_screen = settings.MAX_COWS_ON_SCREEN
        self.reset()

    def reset(self):
        """Resets env to initial state."""
        self.lives = settings.LIVES
        self.score = 0
        self.done = False

        self.cows:list[Cow] = []
        self.cow_id = 0 # needed in pygame to update cow sprites. gets updated at every new cow
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
        # update cows
        self.update_cows()
        # generate new cows
        self.generate_new_cows()
        # update state
        obs = [] #TODO: implement
        info = {}

        # check if game is finished
        if self.lives < 1:
            self.done = True

        return obs, self.done, info

    def check_collisions(self):
        """Checks collisions for all the cows."""
        paddle_hitbox = self.paddle.get_hitbox()
        cliffs_hitboxes = [cliff.get_hitbox() for cliff in self.cliffs]
        for cow in self.cows:
            # check collision with paddle
            if cow.check_landing_collision(paddle_hitbox):
                cow.bounce(paddle_hitbox[1])
            #check collision with cliff
            landed = False
            for cliff_hitbox in cliffs_hitboxes:
                cliff_top = cliff_hitbox[1]
                if cow.check_landing_collision(cliff_hitbox):
                    cow.land(cliff_top)
                    landed = True
                    break
            if not landed:
                cow.freefall()

    def update_cows(self):
        """Moves all cows according to their current velocity, and update score and lives."""
        for cow in self.cows:
            cow.move()
            if cow.is_dead() and self.lives > 0:
                self.lives -= 1
            if cow.is_safe():
                self.score += 1

        # remove safe and dead cows from env
        self.cows = [cow for cow in self.cows if not cow.is_dead() and not cow.is_safe()]


    def generate_new_cows(self):
        """Evaluates cows on the screen and decides wether to generate a new one."""
        n_cows = len(self.cows)
        if n_cows < self.max_cows_on_screen:
            if n_cows == 0 or np.random.random() < self.new_cow_prob:
                new_cow = Cow()
                new_cow.id = self.cow_id
                self.cow_id += 1
                self.cows.append(new_cow)