import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('game', Path(__file__).parent/'dist/game.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GameTests(unittest.TestCase):
    def setUp(self): self.g = module.Game()
    def test_maze_connected(self):
        self.assertTrue(all(len(r)==21 for r in module.MAZE))
        seen = {self.g.player}; todo = [self.g.player]
        while todo:
            p = todo.pop()
            for d in module.DIRECTIONS:
                q = self.g.move(p,d)
                if self.g.walkable(q) and q not in seen: seen.add(q); todo.append(q)
        self.assertTrue(set(self.g.pellets) <= seen)
        self.assertTrue(set(self.g.ghosts) <= seen)
    def test_wall_and_pause(self):
        self.g.player=(1,1); self.g.command('up'); self.g.direction='up'
        self.g.step(); self.assertEqual(self.g.player,(1,1))
        self.g.command('pause'); t=self.g.tick; self.g.step(); self.assertEqual(self.g.tick,t)
    def test_power(self):
        self.g.player=(2,1); self.g.command('left'); self.g.step()
        self.assertEqual(self.g.score,50); self.assertGreater(self.g.power,0)
        self.g.ghosts[0]=self.g.player; self.g.collision(); self.assertEqual(self.g.score,250)
    def test_lives(self):
        for expected in [2,1,0]:
            self.g.invincible=0; self.g.ghosts[0]=self.g.player; self.g.collision()
            self.assertEqual(self.g.lives,expected)
        self.assertEqual(self.g.status,'over')
    def test_level(self):
        self.g.pellets={(9,13):'.'}; self.g.command('left'); self.g.step()
        self.assertEqual(self.g.level,2); self.assertEqual(self.g.score,510)
    def test_simulation(self):
        for _ in range(1500):
            self.g.command(module.random.choice(list(module.DIRECTIONS)))
            self.g.step()
            self.assertTrue(self.g.walkable(self.g.player))
            self.assertTrue(all(self.g.walkable(p) for p in self.g.ghosts))
            if self.g.status=='over': self.g=module.Game()

if __name__=='__main__': unittest.main()
