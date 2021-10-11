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


#### To Do

- Implement a neural network to predict when a game has been won (a network that can predict that based on the semantics of the board should be close to predicting the value of a game based on the board)