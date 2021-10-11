### AIAgents

Repository containing all code related to my pass time project of building AI Agents

Its just me having fun and learning some stuff in the process

Basically a continuation of a past [project](https://github.com/nilansaha/TicTacToeAI) of mine but hopefully at a bigger and more serious scale. A 3 X 3 board was not the best way to go because the search space is very limited and it's difficult to actually implement smarter agents and see them perform better than a naive rollout agent.

The idea is to start from simple things and my very very basic knowledge of agents that are intuitive and novel to my brain (not the outside world) and keep improving from there. I have found coming to solutions on my own (sometimes possibly with small hints i.e. reading a high level blog) that already exists is always fun for me and pushes me to think harder. 

#### What we have

- A N X N TicTacToe board environment that an agent can interact with
- Sample player class that can be inherit to build an agent(player)
- Game class that makes it easier to play games among two players
- Implement a tree based smart player (does extremely well against humans or random players)
- A neural net that can predict when a game has been won for a 3 X 3 board


#### To Do

- Try out the neural net with much bigger boards and validate and improve based on how well it does on those by keeping the size of game dataset same
- Implement a ValueNet to predict the the value of a board for any given instance (can be a new model with same architecture or addition of the same model with another loss and frozen layers and this could actually help because it could help in learning the semantics of the board)