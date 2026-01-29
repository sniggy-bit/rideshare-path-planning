from src.graph.grid import Grid

#Test get_neighbors function for an arbitrary node in the middle of the grid
def test_get_neighbors_middle():
    testgrid = Grid(4,4)
    neighbors = testgrid.get_neighbors((1,1))
    assert neighbors == [(0,1), (2,1), (1,0), (1,2)]
    