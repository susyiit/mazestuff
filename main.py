import pygame
from algorithm import generating_the_maze, algo1dfs, algo2bfs, algo3dijkstra, algo4astar

# the dimensions and the layout
WID = 800
HEI = 800
FPS = 60
CELLSIZE = 40
COL = WID // CELLSIZE # number of columns
ROW = HEI // CELLSIZE # Number of rows 
BG = (30, 30, 30) # background colour
PATHC = (200, 200, 200) # path lines colour
SLVC = (255, 100, 100) # solver colour
VISITC = (100, 255, 100) # visited nodes (not the final path)
FINALC = (100, 100, 255) # final path
MARKC = (0, 0, 255) # start and end ( the blue thingies )

class Cell: # it creates gaps in the walls ( its like mining )
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visit = False # maze generation status
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    
    def path(self, screen, nextcell, color=PATHC):
        # pixel stuff
        cx1 = self.x * CELLSIZE + CELLSIZE // 2
        cy1 = self.y * CELLSIZE + CELLSIZE // 2
        cx2 = nextcell.x * CELLSIZE + CELLSIZE // 2
        cy2 = nextcell.y * CELLSIZE + CELLSIZE // 2

        # draws rounded caps and connects the centers
        pygame.draw.circle(screen, color, (cx1, cy1), CELLSIZE // 4)
        pygame.draw.circle(screen, color, (cx2, cy2), CELLSIZE // 4)
        pygame.draw.line(screen, color, (cx1, cy1), (cx2, cy2), CELLSIZE // 2)

class okaymaze:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WID, HEI))
        self.clock = pygame.time.Clock() # controls the speed
        # this grid array holds EVERY cell instance.. freaky
        self.grid = [[Cell(x, y) for y in range(ROW)] for x in range(COL)]
        self.font = pygame.font.SysFont(None, 48) 
        self.state = "MENU" # game state ( menu or maze )
        
        # visualization
        self.solv = None
        self.viscel = set()
        self.currcel = None
        self.final = []
        
        # average thingy maths
        self.times = {1: [], 2: [], 3: [], 4: []}
        self.current_algo = None # tracks the current algorithm 
        self.start_ticks = 0 # counts the ticks

    def draw_menu(self):
        self.screen.fill(BG)
        
        # menu stuff
        s1 = f"1 - DFS, Avg Time: {(sum(self.times[1])/len(self.times[1])):.2f}s" if self.times[1] else "1 - DFS"
        s2 = f"2 - BFS, Avg Time: {(sum(self.times[2])/len(self.times[2])):.2f}s" if self.times[2] else "2 - BFS"
        s3 = f"3 - Dijkstra, Avg Time: {(sum(self.times[3])/len(self.times[3])):.2f}s" if self.times[3] else "3 - Dijkstra"
        s4 = f"4 - A*, Avg Time: {(sum(self.times[4])/len(self.times[4])):.2f}s" if self.times[4] else "4 - A*"

        # renders strings into surfaces
        t1 = self.font.render(s1, True, (255, 255, 255))
        t2 = self.font.render(s2, True, (255, 255, 255))
        t3 = self.font.render(s3, True, (255, 255, 255))
        t4 = self.font.render(s4, True, (255, 255, 255))
        t5 = self.font.render("R - Reset to Main Menu", True, (255, 255, 255))
        self.screen.blit(t1, (WID // 2 - 200, HEI // 2 - 120))
        self.screen.blit(t2, (WID // 2 - 200, HEI // 2 - 60))
        self.screen.blit(t3, (WID // 2 - 200, HEI // 2))
        self.screen.blit(t4, (WID // 2 - 200, HEI // 2 + 60))
        self.screen.blit(t5, (WID // 2 - 200, HEI // 2 + 160))
        pygame.display.flip() # updates the menu

    def draw_maze(self):
        self.screen.fill(BG)
        
        # renders the maze structure
        for x in range(COL):
            for y in range(ROW):
                cell = self.grid[x][y]
                # it begins
                if not cell.walls['right']:
                    cell.path(self.screen, self.grid[x+1][y])
                if not cell.walls['bottom']:
                    cell.path(self.screen, self.grid[x][y+1])
        
        # pixel coordinates from top left to bottom right
        scx = self.grid[0][0].x * CELLSIZE + CELLSIZE // 2
        scy = self.grid[0][0].y * CELLSIZE + CELLSIZE // 2
        ecx = self.grid[COL-1][ROW-1].x * CELLSIZE + CELLSIZE // 2
        ecy = self.grid[COL-1][ROW-1].y * CELLSIZE + CELLSIZE // 2
        
        # the blue thingies
        pygame.draw.circle(self.screen, MARKC, (scx, scy), CELLSIZE // 3)
        pygame.draw.circle(self.screen, MARKC, (ecx, ecy), CELLSIZE // 3)

        # footstep generator ( greeen )
        for cell in self.viscel:
            cx = cell.x * CELLSIZE + CELLSIZE // 2
            cy = cell.y * CELLSIZE + CELLSIZE // 2
            pygame.draw.circle(self.screen, VISITC, (cx, cy), CELLSIZE // 6)
        
        # draws the character(?) uhhh
        if self.currcel:
            cx = self.currcel.x * CELLSIZE + CELLSIZE // 2
            cy = self.currcel.y * CELLSIZE + CELLSIZE // 2
            pygame.draw.circle(self.screen, SLVC, (cx, cy), CELLSIZE // 4)

        # draws start-finish 
        for i in range(len(self.final) - 1):
            self.final[i].path(self.screen, self.final[i+1], FINALC)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                
                if event.type == pygame.KEYDOWN:
                    # r = goes to main menu
                    if event.key == pygame.K_r:
                        self.grid = [[Cell(x, y) for y in range(ROW)] for x in range(COL)]
                        self.state = "MENU"
                        self.solv = None
                        self.viscel = set()
                        self.currcel = None
                        self.final = []

                    elif self.state == "MENU":
                        # 1 2 3 4 = each have unique corresponding algorithms
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            #generates the maze ( duh )
                            generating_the_maze(self.grid, 0, 0, COL, ROW)
                            start = self.grid[0][0] # top left
                            end = self.grid[COL-1][ROW-1] # bottom right
                            
                            # gets the time ( in ms )
                            self.start_ticks = pygame.time.get_ticks()

                            # 1 2 3 4 = stuff again
                            if event.key == pygame.K_1:
                                self.current_algo = 1
                                self.solv = algo1dfs(self.grid, start, end)
                            elif event.key == pygame.K_2:
                                self.current_algo = 2
                                self.solv = algo2bfs(self.grid, start, end)
                            elif event.key == pygame.K_3:
                                self.current_algo = 3
                                self.solv = algo3dijkstra(self.grid, start, end)
                            elif event.key == pygame.K_4:
                                self.current_algo = 4
                                self.solv = algo4astar(self.grid, start, end)
                            
                            # visualization
                            self.state = "SOLVING"
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "SOLVING":
                if self.solv:
                    try:
                        # takes the next step ( as one should in life )
                        self.viscel, self.currcel, self.final = next(self.solv)
                    except StopIteration:
                        if self.start_ticks != 0:
                            # average list calculation
                            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000.0
                            self.times[self.current_algo].append(elapsed)
                            self.start_ticks = 0 
                        self.solv = None 
                self.draw_maze()
            
            # caps the loop to fps rate
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = okaymaze()
    game.run()