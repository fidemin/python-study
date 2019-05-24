from collections import namedtuple

ALIVE = '*'
EMPTY = '-'

Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))

def count_neighbors(y, x):
    n_ = yield Query(y+1, x+0)
    ne = yield Query(y+1, x+1)
    e_ = yield Query(y, x+1)
    se = yield Query(y-1, x)
    s_ = yield Query(y-1, x)
    sw = yield Query(y-1, x-1)
    w_ = yield Query(y, x-1)
    nw = yield Query(y+1, x-1)

    neighber_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighber_states:
        if state == ALIVE:
            count += 1

    return count


def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE

    return state


def step_cell(y, x):
    print('step_cell start for y=%d, x=%d' % (y, x))
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


TICK = object()

def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        result = ''
        for y in range(self.height):
            for x in range(self.width):
                result += self.query(y, x)

            result += '\n'
        return result

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny


if __name__ == '__main__':
    '''
    it = step_cell(10, 5)
    q0 = next(it)
    q1 = it.send(ALIVE)
    q2 = it.send(ALIVE)
    q3 = it.send(ALIVE)
    q4 = it.send(ALIVE)
    q5 = it.send(ALIVE)
    q6 = it.send(ALIVE)
    q7 = it.send(ALIVE)
    q8 = it.send(ALIVE)
    t1 = it.send(ALIVE)
    print(t1)
    '''

    grid = Grid(3, 3)
    grid.assign(0, 1, ALIVE)
    grid.assign(1, 2, ALIVE)
    print(grid)
    sim = simulate(grid.height, grid.width)
    grid = live_a_generation(grid, sim)
    print(grid)

    grid = live_a_generation(grid, sim)
    print(grid)

