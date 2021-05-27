Running this program requires **Python 3** installed (developed using Python 3.8).

There are two different ways to run the program, either using a GUI or a CLI.

### Using the GUI

To run the program using the GUI, you will also need to install the **PyQt5** library. To do so, type this command:

`pip install pyqt5`

To run the program, use the following command:

`python game_ui.py <agents>`

where parameter `agents` corresponds to the number of agents that will play the game.

In the GUI, pressing the "Step" button will make all agents perform one turn and pressing the "Run" button will make all agents play the entirety of the game.
To play again, simply close the window and run the previous command again.

### Using the CLI

To run the program using the CLI, use command:

`python game_cli.py <agents>`

where parameter `agents` corresponds to the number of agents that will play the game.

#### Playing the game

The CLI version can also be played by one human player (against computer-controlled agents). To do so, use the following command:

`python game_cli.py <total_participants> [players]`

where parameter `total_participants` corresponds to the number of game participants (including the human player) and the parameter `players` corresponds to the number of human players (can be either 0 or 1).
