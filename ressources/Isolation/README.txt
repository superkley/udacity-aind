Alden Quimby
adq2101
CS 4701 Assignment 3 - Isolation

---------------------
TO RUN MY CODE
---------------------
	- To run a client, double click "Isolation.exe" on any windows machine
	- It will ask you which player it is and what the timeout is
	- Warning: the program may use up a good chunk of your CPU :)

---------------------
QUICK NOTE ON RUNNING MY CODE
---------------------
	I set the initial depth limit for my alpha-beta search based on practicing
	with my laptop, to optimize for the tournament. If the client appears to be
	running out of time and making suboptimal moves to start when you test this 
	on your laptop, you can change the starting depth limit when asked for a 
	timeout on startup. Specifically if you enter:
	   		
	   		"Enter timeout in seconds: 45,4"
   	
   	this will set a move timeout of 45 seconds and an initial search depth
   	of 4 plys. That said, my program will recognize a timeout and decrease the 
   	search depth appropriately so that it doesn't time out on the next move.

---------------------
TO READ MY CODE (brief description of important files)
---------------------
	AlphaBeta.cs    --> my primary alpha-beta method
	Board.cs        --> a game state, includes my move generator and validator
	GameRunner.cs   --> manages a game and any IO
	Heuristics.cs   --> all of my heuristic evaluation functions
	MoveTimer.cs    --> make sure I don't timeout
	SearchConfig.cs --> configurable fields for searching (timeout, depth, etc.)
	Searcher.cs     --> manages searching for my move and game state

---------------------
EVALUATION FUNCTIONS
---------------------
	- I implemented multiple heuristics, one for the beginning of the game,
	  one for the middle, and one for the end
	- Beginning game heuristic (NumberOfMoves):
		- Number of moves I can make minus number of moves opponent can make
		- This provides a VERY rough approxiamation of the "goodness" of a board,
		  but it is VERY fast and enables a deeper search
		- I chose search depth over heuristic quality for the beginning of the
		  game because the board is very open - I basically want to make sure
		  I'm in a half-decent position for middle game, and that's it, I don't
		  need the heuristic to be perfect at this point
	- Middle game heursitic (OpenArea)
		- Number of empty spaces in reachable area around me minus number of empty
		  spaces in reachable area around opponent
		- Think of this evaluation function in terms of water. Imagine that I dropped a
		  bucket of water on my player, and that all filled spaces are walls. After the
		  water spread out and filled all empty spaces it could, how many did it fill?
		- This is a much better heuristic than NumberOfMoves, and helps to find
		  situations where opponents are completely walled off from each other
		- This is slower than NumberOfMoves, but because it is only used in middle
		  game, the board has fewer empty spaces, so it is not terrible
		- Note that if players are walled off, the heuristic returns a win for
		  the player with a larger area
	- End game heuristic (LongestPath)
		- Length of longest path I can walk minus length of longest path opponent can
		  walk
		- This heuristic is perfectly accurate if the players are walled off from
		  another, because whoever can make more moves will win
		- This is an expensive heuristic that would fail for any reasonable depth
		  in the beginning or middle game
		- Please see notes below on alpha-beta additions and the end game
	- Note: I decide when to switch between beginning/middle/end game based on the 
	  number of empty spaces remaining on the board, with a few tweaks that are
	  explained by comments in code
	- How did I determine these were good evaluation functions?
	    - LongestPath was an obvious end game heuristic because you just want
	      to make sure you use up all possible moves
	    - OpenArea was explained above (water spreading) and came from tweaking
	      the NumberOfMoves heuristic to capture the idea of "walling off"
		- I instrumented my alpha beta code with many statistics and played games
		  against myself for a long time
		- Please see AlphaBetaWithStats.cs for how I recorded statistics

---------------------
ADDITIONS TO ALPHA BETA
---------------------
	1. Quiessence Search
		For every node that I expand, I check to see if it is "interesting",
		which should help if any moves run in to the horizon effect.
		Basically, if the heuristic evaluation goes from a large positive to
		a large negative or a large negative to a large positive, the move
		is "interesting". If this happens, I extend the search for that node
		by NOT decreasing the depth limit of it's children. I also set a max
		number of allowable quiessence node expansions based on the depth limit
		so that I don't have an infinite quiessence search and don't use up
		too much of the allowable time.
	2. Variable Depth
		Searcher.cs manages my move searching, and it increases the depth limit
		for alpha beta the previous search was faster than a configured threshhold
		(as a percentage of the move time limit). Additionally, if a search times
		out - ideally this won't happen but if it does the alpha-beta just breaks
		out and returns its best result so far - the depth limit is decremented
		so that we don't time out next time.
	3. Handling Game State
		Searcher.cs manages the current state of the game. After ~20 moves (I may
		tweak this before submitting, but it's roughly 20), it switches from
		Beginning Game to Middle Game, which changes the heuristic. When in Middle
		Game, there is some complicated logic to decide if we should switch to End
		Game. Additionally, if we detect that we are gaurenteed to lose (alpha is
		negative infinity), Searcher tries to find an optimal move instead of using
		the result of alpha-beta, which will basically be a random move.
	3.1 End Game
		When Searcher.cs decides we are in End Game, we do NOT necessarily do an 
		alpha-beta search. Specifically, if my player is walled off from my opponent,
		I simply calculate the longest possible path I can take before dying and begin
		walking down that path, completely ignoring anything my opponent does. If we
		are not yet walled off, we still do an alpha-beta search and we evaluate the
		entire remaining game tree by setting depth limit to be greater than the 
		remaining empty spaces.
	4. Multi-threading and pre-computing
		After I send my move to the opponent, I start pre-computing my next move for
		every possible move the opponent could choose. Each of these searches are
		computed on a new thread. When the opponent enters a move, I kill all 
		threads that were computing my move for a different opponent move, and
		continue the execution of the correct thread. I decided to do this by thinking
		about how I play chess, and realized that while my opponent is figuring out
		his/her move, I begin thinking about how I will respond. It would probably
		be more optimal to "guess" where my opponent would move instead of starting
		a thread for every possible move they could make, but I did not implement this.
	5. Move Order
		To improve alpha-beta pruning, I evaluate all child states and order them before
		expanding. Specifically, order descending during the "max turn" stages and
		order ascending during the "min turn" stages. This should theoretically increase
		pruning, and in my testing it drastically reduced the amount of nodes my
		alpha-beta generates.
