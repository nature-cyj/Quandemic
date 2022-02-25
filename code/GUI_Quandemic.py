from tkinter import *
from tkinter.ttk import * 

import pennylane as qml
from pennylane import numpy as np

nx_qubits = 3 
ny_qubits = 3
level = 4 # int(input("level:"))

size_of_board = 600
number_of_dots = nx_qubits+1
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)

class Quandemic():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Quandemic')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        
        self.pcr_total_left = 1
        self.ini_bool = -1
        self.ini_result = self.game(nx_qubits,ny_qubits,level,self.ini_bool)
        self.progress = True
        self.can_total_survey = True
        self.game_card = {}
        
        self.can_select_swap = True
        self.can_select_hospital = False
        self.can_select_pcr_one = False
        
        #self.c2 = Canvas(self.window, width=330, height=200, bg="red")
        #self.c2.place(x=50, y=50)
        self.st = Style()
        self.st.configure('W.TButton', background='#345', foreground='black', font=('Arial', 10 ))
        
        self.btn_pcr_all = Button(self.window, text='PCR Total Inspect',style='W.TButton',
                          command=None) # self.display_pcr_total_result([1, 0, 1, 0, 1, 1, 0, 1, 1])
        self.btn_pcr_all.place(x=6.0*size_of_board/8, y=7)
        
        self.btn_pcr = Button(self.window, text='PCR 1p',style='W.TButton',
                          command=self.on_btn_pcr_click)
        self.btn_pcr.place(x=5.6*size_of_board/8, y=35)
        
        self.btn_next = Button(self.window, text='Next',style='W.TButton',
                          command=self.on_btn_next_click)
        self.btn_next.place(x=6.8*size_of_board/8, y=35)
        
        self.refresh_board()
        self.play_again()
        

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.box_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        
        # Fill city edge row and col to prevent click
        self.row_status[0,:] = 2
        self.row_status[number_of_dots-1,:] = 2
        self.col_status[:,0] = 2
        self.col_status[:,number_of_dots-1] = 2        
        
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []
        self.turntext_handle2 = []
        self.pcr_result_text_handle = []
        self.line_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()
        self.display_guide_text("Select pairs to swap and click next")
        #self.display_guide_text("Quandemic: Save the City!")
            
        
    def mainloop(self):
        #self.window.after(10, self.qml_loop)
        self.window.mainloop()

        
    # Quandemic Core
    def game(self,nx_qubits,ny_qubits,level,ini,state=[],game_card={}):
        if ini==-1:
            dev1 = qml.device("default.qubit",wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev1)
            def ini_circuit():
                n_total = nx_qubits*ny_qubits
                coords = np.random.choice(n_total,level, replace=False)
                for coord in coords:
                    qml.PauliX(wires=coord)
                return qml.state()
            return ini_circuit()
        elif ini==-2: 
            dev2 = qml.device("default.qubit",wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev2)
            def intermediate_circuit():
                qml.AmplitudeEmbedding(state, wires=range(nx_qubits*ny_qubits))
                for swap in game_card['SWAP']:
                    qml.SWAP(wires=list(map(int,swap.split(','))))
                for hospital in game_card['hospital']:
                    if int(hospital) == (nx_qubits*ny_qubits-1)/2:
                        print("Welcome to the most dangerous, but efficacious hospital.")
                        self.display_result_text("Welcome to the Pauli-X Hospital")
                        qml.PauliX(wires=hospital)
                    else:
                        print("Here, this is a medicine. But I'm not sure it may help you heal completely...")
                        self.display_result_text("Welcome to the H Hospital")
                        qml.Hadamard(wires=hospital)
                self.can_select_hospital = False
                self.can_select_pcr_one = False
                self.can_select_swap = True
                return qml.state()
            return intermediate_circuit()
        elif ini == -3:
            dev3 = qml.device("default.qubit",shots=1,wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev3)
            def end_circuit():
                qml.AmplitudeEmbedding(state, wires=range(nx_qubits*ny_qubits))
                return qml.sample()
            final_pcr = end_circuit()
            if 1 not in final_pcr:
                return 'All citizens are cured!!! YOU WIN'
            else:
                return 'Virus is not disappeared. YOU LOSE'
        elif ini == -4:
            dev6 = qml.device("default.qubit",shots=1,wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev6)
            def total_survey_circuit():
                qml.AmplitudeEmbedding(state, wires=range(nx_qubits*ny_qubits))
                return qml.sample()
            dev7 = qml.device("default.qubit",wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev7)
            def after_survey(total_survey):
                print("The entire PCR test result is:",total_survey)
                self.display_pcr_total_result(total_survey)
                qml.BasisState(total_survey, wires=range(nx_qubits*ny_qubits))
                return qml.state()
            return after_survey(total_survey_circuit())
        else:
            dev4 = qml.device("default.qubit",shots=1,wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev4)
            def measure_circuit(issample):
                qml.AmplitudeEmbedding(state, wires=range(nx_qubits*ny_qubits))
                if issample:
                    return qml.sample(wires=ini)
                else:
                    return qml.state()
            measure_out = measure_circuit(True)
            if measure_out == 1:
                print("The PCR test of person ",ini," is ","Positive.")
                self.display_result_text("The PCR test of person {} is Positive.".format(ini))
            else:
                print("The PCR test of person ",ini," is ","Negative.")
                self.display_result_text("The PCR test of person {} is Negative.".format(ini))
            states = measure_circuit(False)
            aft_meas = []
            j =nx_qubits*ny_qubits - 1 - ini
            for i, st in enumerate(states):
                indx = int((i % (2**(j+1)))/2**j)
                if measure_out == indx:
                    aft_meas.append(st)
                else :
                    aft_meas.append(0)
            dev5 = qml.device("default.qubit",wires=range(nx_qubits*ny_qubits))
            @qml.qnode(dev5)
            def re_input_circuit():
                qml.AmplitudeEmbedding(aft_meas, wires=range(nx_qubits*ny_qubits),normalize=True)
                return qml.state()
            return re_input_circuit()    
        
    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def convert_grid_to_logical_position_box(self, grid_position):
        grid_position = np.array(grid_position)
        grid_position -= distance_between_dots/4
        return np.array(grid_position // distance_between_dots, dtype=int)
    
    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = player1_color_light
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = player2_color_light
                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:
            val =- 1

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.line_handle.append(self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width))
        
    def clear_edge(self):
        for line in self.line_handle:
            self.canvas.delete(line)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif player2_score > player1_score:
            text = 'Winner: Player 2 '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)
        
           

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                '''
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)'''

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def display_guide_text(self, msg):
        color = player2_color
        self.canvas.delete(self.turntext_handle2)
        self.turntext_handle2 = self.canvas.create_text(5*len(msg)+4,
                                                       distance_between_dots/8,
                                                       font="cmr 15 bold",text=msg, fill=color)
        
    def display_result_text(self, msg):
        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(msg),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=msg, fill=player1_color)
        
    def display_pcr_total_result(self, pcr_total_result):     
        for hd in self.pcr_result_text_handle:
            self.canvas.delete(hd)
        arr = np.array(pcr_total_result, requires_grad=False)
        arr = np.reshape(arr,(-1,3))       
        for i in range(nx_qubits):
            for j in range(ny_qubits):
                start_x = (i+1)*distance_between_dots
                end_x = (j+1)*distance_between_dots
                self.pcr_result_text_handle.append(self.canvas.create_text(start_x,
                                                       end_x,
                                                       font="cmr 25 bold",text=str(arr[i][j])))
     
    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    
    def click(self, event): 
        ''' Use this function as main loop'''
        
        if self.can_select_swap:
            self.display_guide_text("Select pairs to swap and click next")
        
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                #self.mark_box()
                self.refresh_board()
                # self.player1_turn = not self.player1_turn  # change turn

                if self.is_gameover():
                    self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.display_guide_text("Select pairs to swap and click next")
                    #self.display_pcr_total_result([1, 0, 1, 0, 1, 1, 0, 1, 1])
        
        if self.can_select_hospital:
            self.can_select_swap = False
            grid_position = [event.x, event.y]
            logical_positon = self.convert_grid_to_logical_position_box(grid_position)
            self.shade_box(logical_positon)
            self.display_guide_text("Select the hospitals and click next")
            self.game_card['hospital'] = list(map(int,input("select the hospitals:").split()))
        
        '''
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False'''


    def on_btn_next_click(self):
        def row_edge_to_pair(coord):
            if np.array_equal(coord, np.array([1,0])): return [0,3]
            elif np.array_equal(coord, np.array([1,1])): return [1,4]
            elif np.array_equal(coord, np.array([1,2])): return [2,5]
            elif np.array_equal(coord, np.array([2,0])): return [3,6]
            elif np.array_equal(coord, np.array([2,1])): return [4,7]
            elif np.array_equal(coord, np.array([2,2])): return [5,8]
        
        def col_edge_to_pair(coord):
            if np.array_equal(coord, np.array([0,1])): return [0,1]
            elif np.array_equal(coord, np.array([0,2])): return [1,2]
            elif np.array_equal(coord, np.array([1,1])): return [3,4]
            elif np.array_equal(coord, np.array([1,2])): return [4,5]
            elif np.array_equal(coord, np.array([2,1])): return [6,7]
            elif np.array_equal(coord, np.array([2,2])): return [7,8]

        if self.can_select_pcr_one:
            self.display_guide_text("Who wants to get pcr?")
            self.ini_bool = int(input("Who wants to get pcr?:")) # ini_bool for index of person who gets PCR test
            self.ini_result = self.game(nx_qubits,ny_qubits,level,self.ini_bool,self.ini_result)
            self.clear_edge()
            
        if self.can_select_hospital:
            self.clear_edge()
            self.display_guide_text("Select the hospitals and click next")
            self.ini_bool = -2
            self.ini_result = self.game(nx_qubits,ny_qubits,level,self.ini_bool,self.ini_result,self.game_card)
            self.can_select_hospital = False
            self.can_select_pcr_one = True
            
        if self.can_select_swap:
            swaps_r = np.argwhere(self.row_status == 1)
            swaps_c = np.argwhere(self.col_status == 1)
            self.game_card['SWAP'] = np.concatenate((swaps_r, swaps_c))
            self.can_select_swap = False
            self.can_select_hospital = True
                                         
        return None
    
    def on_btn_pcr_click(self):
        return None
    
    def on_btn_pcr_all_click(self):
        if self.pcr_total_left == 0:
            self.display_guide_text("You already used all total PCR chance")
            return None
        self.pcr_total_left -= 1
        self.display_result_text("The Total PCR Inspection Used")
        self.ini_result = self.game(nx_qubits,ny_qubits,level,-4,self.ini_result)
        
        return None
            
game_instance = Quandemic()
game_instance.mainloop()