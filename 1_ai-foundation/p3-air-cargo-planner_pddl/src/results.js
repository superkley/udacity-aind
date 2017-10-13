Search	Type	Expansions	Goal	Tests	New	Nodes	Length	Time	(s)	Optimal

1. Air Cargo Problem 1
    1. breadth_first_search, 6, 0.025, 43, 56, 180
    2. breadth_first_tree_search 6, 0.753, 1458, 1459, 5960
    3. depth_first_graph_search 12, 0.007, 12, 13, 48
    4. depth_limited_search 50, 0.080, 101, 271, 414
    5. uniform_cost_search 6, 0.031, 55, 57, 224
    6. recursive_best_first_search h_1 6, 2.296, 4229, 4230, 17029
    7. greedy_best_first_graph_search h_1 6, 0.004, 7, 9, 28
    8. astar_search h_1 6, 0.032, 55, 57, 224
    9. astar_search h_ignore_preconditions 6, 0.034, 41, 43, 170
    10. astar_search h_pg_levelsum 6 plan lengths, 1.163s time elapsed, 55 expansions, 57 goal tests, 224 new nodes
    
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, JFK)
Fly(P2, JFK, SFO)
Unload(C1, P1, JFK)
Unload(C2, P2, SFO)



2. Air Cargo Problem 2
    1. breadth_first_search, 9, 14.051, 3343, 4609, 30509
    2. breadth_first_tree_search -
    3. depth_first_graph_search, 575, 4.575, 582, 583, 5211
    4. depth_limited_search, -
    5. uniform_cost_search, 9, 15.075, 4853, 4855, 44041
    6. recursive_best_first_search h_1, -
    7. greedy_best_first_graph_search h_1 , 15, 2.441, 998, 1000, 8982
    8. astar_search h_1 9, 13.389, 4853, 4855, 44041
    9. astar_search h_ignore_preconditions 9, 4.126, 1450, 1452, 13303
    10. astar_search h_pg_levelsum -

9:    
Load(C3, P3, ATL)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)



3. Air Cargo Problem 3
    1. breadth_first_search, 12, 199, 14663, 18098, 129631
    2. breadth_first_tree_search, -
    3. depth_first_graph_search, 596, 4.961, 627, 628, 6176
    4. depth_limited_search, -
    5. uniform_cost_search, 12, 81.81, 18223, 18225, 159618
    6. recursive_best_first_search h_1, -
    7. greedy_best_first_graph_search h_1 , 22, 28.01, 5578, 5580, 49150
    8. astar_search h_1, 12, 78.40, 18223, 18225, 159618
    9. astar_search h_ignore_preconditions, 12, 28.00, 5040, 5042, 44944
    10. astar_search h_pg_levelsum -
Load(C2, P2, JFK)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P2, ORD, SFO)
Unload(C4, P2, SFO)
Load(C1, P1, SFO)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P1, ATL, JFK)
Unload(C3, P1, JFK)
Unload(C2, P2, SFO)
Unload(C1, P1, JFK)