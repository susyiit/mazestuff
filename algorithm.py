# here we go
import random
import heapq

def generating_the_maze(grid, start_x, start_y, cols, rows):
    # starts the maze and marks the first cell as "visited"
    current = grid[start_x][start_y]
    current.visit = True
    stack = [current] # it creates footsteps

    
    while stack:
        current = stack[-1] # looks at top of the cell
        surround = [] # list for the surrounding cells
        x = current.x
        y = current.y

        # checks all directions for neighbors
        # if true append the neighbor cell and the walls that gets removed
        if y > 0 and not grid[x][y-1].visit:
            surround.append((grid[x][y-1], 'top', 'bottom'))
        if x < cols - 1 and not grid[x+1][y].visit:
            surround.append((grid[x+1][y], 'right', 'left'))
        if y < rows - 1 and not grid[x][y+1].visit:
            surround.append((grid[x][y+1], 'bottom', 'top'))
        if x > 0 and not grid[x-1][y].visit:
            surround.append((grid[x-1][y], 'left', 'right'))

        # for every unvisited neighbor
        if surround:
            # pick a random neighbor to visit 
            nextcell, wall, next_wall = random.choice(surround)
            nextcell.visit = True
            # removes the walls between the current cell and the neighbor
            current.walls[wall] = False
            nextcell.walls[next_wall] = False
            # pushes the new cell to the stack to continue the path
            stack.append(nextcell)
        else:
            # if there arent any unvisited neighbors backtrack by popping from the stack
            stack.pop()

def algo1dfs(grid, start, end):
    # depth first search
    stack = [start]
    visit = {start} # these are very confusing things
    path = {} # uhhhh

    while stack:
        current = stack.pop() # 
        if current == end: # i guess bro
            break
        
        x, y = current.x, current.y
        neighbors = []
        # i honestly got all these from stackoverflow
        if not current.walls['top']: neighbors.append(grid[x][y-1])
        if not current.walls['right']: neighbors.append(grid[x+1][y])
        if not current.walls['bottom']: neighbors.append(grid[x][y+1])
        if not current.walls['left']: neighbors.append(grid[x-1][y])

        for n in neighbors:
            if n not in visit:
                visit.add(n)
                path[n] = current
                stack.append(n)
        
        # visualization
        yield visit, current, []

    # reconstruction of the start-end path
    final = []
    curr = end
    while curr in path:
        final.append(curr)
        curr = path[curr]
    final.append(start)
    yield visit, end, final 

def algo2bfs(grid, start, end):
    # breadth first search algorithm
    queue = [start]
    visit = {start}
    path = {}

    while queue:
        current = queue.pop(0) # this algorithm expands everything in 4 directions
        if current == end:
            break
        
        x, y = current.x, current.y
        neighbors = []
        if not current.walls['top']: neighbors.append(grid[x][y-1])
        if not current.walls['right']: neighbors.append(grid[x+1][y])
        if not current.walls['bottom']: neighbors.append(grid[x][y+1])
        if not current.walls['left']: neighbors.append(grid[x-1][y])

        for n in neighbors:
            if n not in visit:
                visit.add(n)
                path[n] = current
                queue.append(n)
        yield visit, current, []

    final = []
    curr = end
    while curr in path:
        final.append(curr)
        curr = path[curr]
    final.append(start)
    yield visit, end, final

def algo3dijkstra(grid, start, end):
    # dijkstras algorithm
    
    queue = [(0, id(start), start)] 
    visit = {start}
    path = {}
    g_score = {start: 0} # shortest distance from start to end

    while queue:
        # genuinely no idea
        cost, _, current = heapq.heappop(queue)
        if current == end:
            break

        x, y = current.x, current.y
        neighbors = []
        if not current.walls['top']: neighbors.append(grid[x][y-1])
        if not current.walls['right']: neighbors.append(grid[x+1][y])
        if not current.walls['bottom']: neighbors.append(grid[x][y+1])
        if not current.walls['left']: neighbors.append(grid[x-1][y])

        for n in neighbors:
            # the cost increases ????
            tentative_g = g_score[current] + 1
            # ok
            if n not in g_score or tentative_g < g_score[n]:
                g_score[n] = tentative_g
                path[n] = current
                visit.add(n)
                heapq.heappush(queue, (tentative_g, id(n), n))
        
        yield visit, current, []

    final = []
    curr = end
    while curr in path:
        final.append(curr)
        curr = path[curr]
    final.append(start)
    yield visit, end, final

def algo4astar(grid, start, end):
    # A* algorithm
    def heuristic(a, b):
        # something something manhattan
        return abs(a.x - b.x) + abs(a.y - b.y)

    queue = [(0, id(start), start)]
    visit = {start}
    path = {}
    g_score = {start: 0} # exact cost from start to node??

    while queue:
        # popping off
        _, _, current = heapq.heappop(queue)
        if current == end:
            break

        x, y = current.x, current.y
        neighbors = []
        if not current.walls['top']: neighbors.append(grid[x][y-1])
        if not current.walls['right']: neighbors.append(grid[x+1][y])
        if not current.walls['bottom']: neighbors.append(grid[x][y+1])
        if not current.walls['left']: neighbors.append(grid[x-1][y])

        for n in neighbors:
            tentative_g = g_score[current] + 1
            if n not in g_score or tentative_g < g_score[n]:
                g_score[n] = tentative_g
                f_score = tentative_g + heuristic(n, end)
                path[n] = current
                visit.add(n)
                heapq.heappush(queue, (f_score, id(n), n))
        
        yield visit, current, []

    final = []
    curr = end
    while curr in path:
        final.append(curr)
        curr = path[curr]
    final.append(start)
    yield visit, end, final