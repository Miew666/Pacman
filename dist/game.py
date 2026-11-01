"""Pure Python maze game engine, shared by CPython tests and browser Pyodide."""
import random
import json

MAZE = [
'#####################',
'#o........#........o#',
'#.###.###.#.###.###.#',
'#...................#',
'#.###.#.#####.#.###.#',
'#.....#...#...#.....#',
'#####.###.#.###.#####',
'#.....#.......#.....#',
'#.###.#.##.##.#.###.#',
'#...#...#   #...#...#',
'###.#.#.#   #.#.#.###',
'#.....#.......#.....#',
'#.###.###.#.###.###.#',
'#o..#..... .....#..o#',
'###.#.#.#####.#.#.###',
'#.....#...#...#.....#',
'#.#######.#.#######.#',
'#...................#',
'#####################',
]
DIRECTIONS = {'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}

class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.status = 'ready'
        self.tick = 0
        self.power = 0
        self.combo = 0
        self.load_level()

    def load_level(self):
        self.pellets = {(x,y): c for y,row in enumerate(MAZE) for x,c in enumerate(row) if c in '.o'}
        self.reset_positions()

    def reset_positions(self):
        self.player = (10,13)
        self.direction = 'left'
        self.wanted = 'left'
        self.ghosts = [(9,9),(10,9),(11,9),(10,10)]
        self.ghost_dirs = [None]*4
        self.power = 0
        self.invincible = 14

    def walkable(self,p):
        x,y = p
        return 0 <= y < len(MAZE) and 0 <= x < len(MAZE[0]) and MAZE[y][x] != '#'

    def move(self,p,d):
        dx,dy = DIRECTIONS[d]
        return p[0]+dx,p[1]+dy

    def command(self,d):
        if d in DIRECTIONS:
            self.wanted = d
            if self.status == 'ready': self.status = 'playing'
        elif d == 'pause' and self.status in ('playing','paused'):
            self.status = 'paused' if self.status == 'playing' else 'playing'
        elif d == 'start' and self.status == 'ready': self.status = 'playing'

    def collision(self):
        for i,g in enumerate(self.ghosts):
            if g != self.player: continue
            if self.power:
                self.combo += 1
                self.score += 200 * 2**min(self.combo-1,3)
                self.ghosts[i] = (10,9)
            elif not self.invincible:
                self.lives -= 1
                if self.lives == 0: self.status = 'over'
                else:
                    self.reset_positions()
                    self.status = 'ready'
                return True
        return False

    def step(self):
        if self.status != 'playing': return
        self.tick += 1
        self.power = max(0,self.power-1)
        self.invincible = max(0,self.invincible-1)
        if self.walkable(self.move(self.player,self.wanted)): self.direction = self.wanted
        p = self.move(self.player,self.direction)
        if self.walkable(p): self.player = p
        pellet = self.pellets.pop(self.player,None)
        if pellet:
            self.score += 50 if pellet == 'o' else 10
            if pellet == 'o': self.power = 55; self.combo = 0
        if self.collision(): return
        if self.tick % (3 if self.power else 2) == 0:
            for i,g in enumerate(self.ghosts):
                choices = [d for d in DIRECTIONS if self.walkable(self.move(g,d))]
                previous = self.ghost_dirs[i]
                forward = [d for d in choices if previous is None or DIRECTIONS[d] != tuple(-v for v in DIRECTIONS[previous])]
                choices = forward or choices
                target = self.player if i < 2 or self.tick % 50 < 30 else [(1,1),(19,1),(1,17),(19,17)][i]
                def distance(d):
                    q = self.move(g,d)
                    return abs(q[0]-target[0])+abs(q[1]-target[1])
                if choices:
                    d = random.choice(choices) if random.random()<.22 else sorted(choices,key=distance,reverse=bool(self.power))[0]
                    self.ghosts[i] = self.move(g,d)
                    self.ghost_dirs[i] = d
        if self.collision(): return
        if not self.pellets:
            self.level += 1
            self.score += 500
            self.load_level()
            self.status = 'ready'

    def snapshot(self):
        return json.dumps(dict(maze=MAZE,player=self.player,ghosts=self.ghosts,direction=self.direction,
            pellets=[[x,y,c] for (x,y),c in self.pellets.items()],score=self.score,lives=self.lives,
            level=self.level,status=self.status,power=self.power,invincible=self.invincible))

game = Game()
