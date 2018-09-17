from collections import deque
import sys, time, resource
from heapq import heappush, heappop
MOVES = ("Up", "Down", "Left", "Right")#order in " UDLR "
MOVEBY = [-3, 3, -1, 1]
GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)
ACTION = [(1, 3), (1, 2, 3), (1, 2),(0, 1, 3), (0, 1, 2, 3), (0, 1, 2),(0, 3), (0, 2, 3), (0, 2)]
M_Distance = [0,1,2,1,2,3,2,3,4]
class TreeNode(object):
    def __init__(self,state,parent,by,manhattan_distance):
        self.state = state #current positions
        self.parent = parent#the former node
        self.by = by #the former action
        self.depth = parent.depth + 1 if parent else 0 #the current depth
        self.cost = parent.cost +1 if parent else 0 #the current cost
        self.zero = self.state.index(0) #index of zero
        self.action = ACTION[self.zero] #next valid actions
        self.reward = manhattan_distance+self.depth #in A*
def manhattan_distance(node):#A* Manhattan priority function of the node
    distance = 0
    curpos = -1
    for num in node.state: #num is the number as well as the goal position
        curpos+=1        #curpos is the current position
        if num != 0:
            distance += M_Distance[abs(curpos - num)]
    return distance
def get_history(node):#get the path from head to current node
    path = []
    while node.parent:
        path = [node.by] + path
        node = node.parent
    return path
def generate_next(node,A):#get the valid child nodes
    Next = []
    reward = manhattan_distance(node) if A else 0
    for a in list(node.action):
        target = node.zero + MOVEBY[a] #the target to switch
        newstate = list(node.state) #newstate to return
        newstate[node.zero],newstate[target] = newstate[target],newstate[node.zero]#switch
        Next.append(TreeNode(tuple(newstate), node, a, reward))#new node with parent and action
    return Next
def bfs(state):
    #things to return
    result = {'path_to_goal' : deque(), #return the path to goal node
    'cost_of_path' : 0, #return the goal node cost
    'search_depth' : 0, #return the goal node depth
    'nodes_expanded' : 0,#sum the total number of nodes visited
    'max_search_depth' : 0, #by max(every visited nodes' search depth)
    'running_time' : 0, #calculate the end_time - begin_time
    'max_ram_usage' : 0} #
    #things to return
    frontier = deque([TreeNode(state,None,None,0)])
    explored = set([state])
    timenow = time.time() #the begin_time
    while frontier:
        CurNode = frontier.popleft()#pop off results in UDLR order.
        if CurNode.state == GOAL:
            result['search_depth'] = CurNode.depth
            result['path_to_goal'] = get_history(CurNode)
            result['running_time'] = time.time()- timenow
            return result
        deeper = False
        for child in generate_next(CurNode, False):#Push onto the queue in UDLR order;
            if child.state not in explored:
                frontier.append(child)
                explored.add(child.state)
                deeper = True
        result['nodes_expanded']+=1
        result['max_search_depth']= max(result['max_search_depth'],CurNode.depth+1) if deeper==True else result['max_search_depth']
        result['max_ram_usage'] = max(result['max_ram_usage'], resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000.0)
    return None
def dfs(state):
    #things to return
    result = {'path_to_goal' : deque(), #return the path to goal node
    'cost_of_path' : 0, #return the goal node cost
    'search_depth' : 0, #return the goal node depth
    'nodes_expanded' : 0,#sum the total number of nodes visited
    'max_search_depth' : 0, #by max(every visited nodes' search depth)
    'running_time' : 0, #calculate the end_time - begin_time
    'max_ram_usage' : 0} #
    #things to return
    frontier = deque([TreeNode(state,None,None,0)])
    explored = set([state])
    timenow = time.time() #the begin_time
    while frontier:
        CurNode = frontier.pop()#pop off results in UDLR order.
        if CurNode.state == GOAL:
            result['search_depth']= CurNode.depth
            result['path_to_goal'] = get_history(CurNode)
            result['running_time'] = time.time()- timenow
            return result
        deeper = False
        for child in reversed(generate_next(CurNode, False)):#Push onto the stack in reverse-UDLR order;
            if child.state not in explored:
                frontier.append(child)
                explored.add(child.state)
                deeper = True
        result['max_search_depth']= max(result['max_search_depth'],CurNode.depth+1) if deeper==True else result['max_search_depth']
        result['nodes_expanded'] += 1
        result['max_ram_usage'] = max(result['max_ram_usage'], resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000.0)
    return None

def ast(state):
    #things to return
    result = {'path_to_goal' : deque(), #return the path to goal node
    'cost_of_path' : 0, #return the goal node cost
    'search_depth' : 0, #return the goal node depth
    'nodes_expanded' : 0,#sum the total number of nodes visited
    'max_search_depth' : 0, #by max(every visited nodes' search depth)
    'running_time' : 0, #calculate the end_time - begin_time
    'max_ram_usage' : 0} #
    #things to return
    timenow = time.time() #the begin_time
    Root = TreeNode(state,None,None,0) #Root node
    frontier = [[manhattan_distance(Root),Root]] #nodes to be explored
    explored = set([state]) #state explored
    minimum_distance_of_state = {Root.state:manhattan_distance(Root)}#remember the minimum distance
    while frontier:
        distance, CurNode = heappop(frontier) #pop off results in UDLR order.
        if distance>minimum_distance_of_state[CurNode.state]:
            continue
        explored.add(CurNode.state)
        result['max_search_depth'] = max(result['max_search_depth'],CurNode.depth)
        if CurNode.state == GOAL:
            result['search_depth'] = CurNode.depth
            result['path_to_goal'] = get_history(CurNode)
            result['running_time'] = time.time()- timenow
            return result
        deeper = False
        for child in generate_next(CurNode,True):
            state = child.state
            if state not in explored:
                distance = manhattan_distance(child)+child.depth
                heappush(frontier,[distance,child])
                if state in minimum_distance_of_state:
                    if distance<minimum_distance_of_state[state]:
                        minimum_distance_of_state[state] = distance
                else:
                    minimum_distance_of_state[state] = distance
                deeper = True
        result['max_search_depth']= max(result['max_search_depth'],CurNode.depth+1) if deeper==True else result['max_search_depth']
        result['nodes_expanded']+=1
        result['max_ram_usage'] = max(result['max_ram_usage'], resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000.0)
    return None







if __name__ == '__main__':
    sys.stdout = open("output.txt", "w")
    init_state = tuple([int(i) for i in sys.argv[2].split(',')])
    result = []
    if sys.argv[1] == 'bfs':
        result=bfs(init_state)
    elif sys.argv[1] == 'dfs':
        result=dfs(init_state)
    elif sys.argv[1] == 'ast':
        result=ast(init_state)
    path = [MOVES[m] for m in result['path_to_goal']]
    print 'path_to_goal:', path
    print "cost_of_path:", len(path)
    print "nodes_expanded:", result['nodes_expanded']
    print "search_depth:", result['search_depth']
    print "max_search_depth:", result['max_search_depth']
    print "running_time: %.8f" %(result['running_time'])
    print "max_ram_usage: %.8f"  %(result['max_ram_usage'])
    sys.stdout.close()
