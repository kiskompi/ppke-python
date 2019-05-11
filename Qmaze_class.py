from parameters import *
import numpy as np

# maze is a 2d Numpy array of floats between 0.0 to 1.0
# 1.0 corresponds to a free cell, and 0.0 an occupied cell
# agent = (row, col) initial agent position (defaults to (0,0))

class Qmaze(object):
    def __init__(self, maze, agent=(0,0)):
        self.m_maze = np.array(maze)
        nrows, ncols = self.m_maze.shape
        self.target = (nrows-1, ncols-1)   # target cell where the "cheese" is
        self.free_cells = [(r,c) for r in range(nrows) for c in range(ncols) if self.m_maze[r,c] == 1.0]
        self.free_cells.remove(self.target)
        if self.m_maze[self.target] == 0.0:
            raise Exception("Invalid maze: target cell cannot be blocked!")
        if not agent in self.free_cells:
            raise Exception("Invalid agent Location: must sit on a free cell")
        self.reset(agent)

    def reset(self, agent):
        self.m_agent = agent
        self.m_maze = np.copy(self.m_maze)
        nrows, ncols = self.m_maze.shape
        row, col = agent
        self.m_maze[row, col] = agent_mark
        self.m_state = (row, col, 'start')
        self.m_min_reward = -0.5 * self.m_maze.size
        self.m_total_reward = 0
        self.m_visited = set()

    def update_state(self, action):
        nrows, ncols = self.m_maze.shape
        nrow, ncol, nmode = agent_row, agent_col, mode = self.m_state

        if self.m_maze[agent_row, agent_col] > 0.0:
            self.m_visited.add((agent_row, agent_col))  # mark visited cell

        valid_actions = self.valid_actions()
                
        if not valid_actions:
            nmode = 'blocked'
        elif action in valid_actions:
            nmode = 'valid'
            if action == LEFT:
                ncol -= 1
            elif action == UP:
                nrow -= 1
            if action == RIGHT:
                ncol += 1
            elif action == DOWN:
                nrow += 1
        else:                  # invalid action, no change in agent position
            mode = 'invalid'

        # new state
        self.m_state = (nrow, ncol, nmode)

    def get_reward(self):
        agent_row, agent_col, mode = self.m_state
        nrows, ncols = self.m_maze.shape
        if agent_row == nrows-1 and agent_col == ncols-1:
            return 1.0
        if mode == 'blocked':
            return self.m_min_reward - 1
        if (agent_row, agent_col) in self.m_visited:
            return -0.25
        if mode == 'invalid':
            return -0.75
        if mode == 'valid':
            return -0.04

    def act(self, action):
        self.update_state(action)
        reward = self.get_reward()
        self.m_total_reward += reward
        status = self.game_status()
        envstate = self.observe()
        return envstate, reward, status

    def observe(self):
        canvas = self.draw_env()
        envstate = canvas.reshape((1, -1))
        return envstate

    def draw_env(self):
        canvas = np.copy(self.m_maze)
        nrows, ncols = self.m_maze.shape
        # clear all visual marks
        for r in range(nrows):
            for c in range(ncols):
                if canvas[r,c] > 0.0:
                    canvas[r,c] = 1.0
        # draw the agent
        row, col, valid = self.m_state
        canvas[row, col] = agent_mark
        return canvas

    def game_status(self):
        if self.m_total_reward < self.m_min_reward:
            return 'lose'
        agent_row, agent_col, mode = self.m_state
        nrows, ncols = self.m_maze.shape
        if agent_row == nrows-1 and agent_col == ncols-1:
            return 'win'

        return 'not_over'

    def valid_actions(self, cell=None):
        if cell is None:
            row, col, mode = self.m_state
        else:
            row, col = cell
        actions = [0, 1, 2, 3]
        nrows, ncols = self.m_maze.shape
        if row == 0:
            actions.remove(1)
        elif row == nrows-1:
            actions.remove(3)

        if col == 0:
            actions.remove(0)
        elif col == ncols-1:
            actions.remove(2)

        if row>0 and self.m_maze[row-1,col] == 0.0:
            actions.remove(1)
        if row<nrows-1 and self.m_maze[row+1,col] == 0.0:
            actions.remove(3)

        if col>0 and self.m_maze[row,col-1] == 0.0:
            actions.remove(0)
        if col<ncols-1 and self.m_maze[row,col+1] == 0.0:
            actions.remove(2)

        return actions