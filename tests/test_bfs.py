from src.graph.grid import Grid
from src.graph.path_finder import bfs_shortest_path
#Test the BFS shortest path function on a simple 3x3 grid
def test_bfs_shortest_path():
    testgrid = Grid(3,3)
    start = (0,0)
    target = (2,2)

    result = bfs_shortest_path(testgrid,start,target)
    
    expected_path = [(0,0), (1,0), (1,1), (1,2), (2,2)]
    expected_length = 4

    assert result["length"] == expected_length
    
    print(result["path"])
    print(result["length"])

