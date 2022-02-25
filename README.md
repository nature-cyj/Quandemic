<div align='center'>

![Title_Image](./Logo.png)

Contributors:
[@JongheumJung](mailto://jungjh0330snu@snu.ac.kr),
[@YoonjaeChung](https://github.com/nature-cyj),
[@GyunghunKim](https://github.com/GyunghunKim) 


</div>

## Abstract

In the regime of a global pandemic, leaders around the world need to consider various possibilities
and take conscious actions to protect their citizens from the infectious virus. In the quantum world
that we model in this game, every possible situation exists as a superposed state. Nothing is
decisive at all. You, as the leader of this quantum city, need to suppress the possibility, or
amplitude of states representing bad situations. Lastly, the mandatory PCR test for every citizen is
waiting you---it 'measures' the city and will show whether your policies rescued the city or not.
Predict, act, and measure!

## The Game

### Objectives
- Obtain negative result for everyone at the last PCR test.

### Contents

- **Citizens**<br>
A quantum circuit with N by M qubits represents a city that N\*M citizens live with a deadly virus.
0's and 1's appearing on the computational basis of this system corresponds to healthy and infected
states, respectively.  Since the people live in a quantum world, the city stays in a superposition
of possible infection states!

- **Regular Action: PCR Testing (Single Person)**<br>
A PCR test corresponds to measurement on a specific qubit, or a citizen of this city. Not only
obtains a decisive result about the citizen's infection status, the test destroys possibility of the
city to be in states which counter the test result. In quantum-like words, the measurement projects
previous state into a subspace contains the measured result.

- **Special Action: PCR Testing (Total Inspection)**<br>
For sake of the player, one can measure states of all qubits at once for only one time during the
game. It will remove superposition of the city's state, but the state will quickly branch and
involve possibilities as time goes on.

- **Regular Action: Move Citizens (Swap)**<br>
In each turn, player should choose pairs of citizens to swap position. However, since the swapped
citizens interact each other, they might additionally catch the virus. The newly possible infected
state is involved to the game as superposition.  Simply, a quantum **SWAP** gate and a Kraus
operator which puts 0 to 1 at a fixed possibility successively applied for each pair of citizens
that the player selected. Players are allowed to swap 'neighboring' citizens only. 

- **Regular Action: Send Hospital**<br>
There are two hospitals in this city placed at the certain area.<br>
  - **The 'H' hospital**<br>
    The 'H' hospital is placed in every corner of the city. For example, in 3x3 city, 'H' hospital
    is placed at position 0, 2, 6, 8. The 'H' hospital works by applying Hadamard gate if player
    selects its position.  Be careful that it might increase probability of infection if it is used
    in a wrong way!
    
  - **The Pauli's X hospital**<br>
    The Pauli's X hospital is placed at the center of the city. It acts to the citizen at the center
    by applying X gate. So the hospital will cure a citizen if one is infected, but it will infect a
    healthy one at the same time!
    
In each turn, the player should select which citizens to send hospital. It is only possible to send
citizens that are placed on the hostpial area. For example, in 3x3 city, selecting 0, 4, 6 are valid
action, while selecting 1, 8 is invalid because there is no hospital at position 1.


- **The last, mandatory PCR test**<br>
This test decides whether your critical choices during the pandemic were successful or not. This
very final operation measures all qubits of the system as the total survey. Even if a single **1**
exists in your final state, it will move, copy itself and spread throughout your city again. No way!
The game's objective is to obtain the result |00...00> and to free your city from the pandemic
forever! 
