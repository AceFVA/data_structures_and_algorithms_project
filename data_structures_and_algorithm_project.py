# Program 1: Parking Garage using Stacks
    # In this program, the user will be able to simulate a parking garage using stack data structure.

# Program 2: Parking Garage using Queues
    # In this program, the user will be able to simulate a parking garage using queue data structure.

# Program 3: Binary Tree 
    # In this program, the user will be able to create a binary tree by inserting nodes.
    # 1. Ask the user to input how many levels they want in the binary tree.
    # 2. For each level, prompt the user to enter the value of the nodes.
    # 3. Insert the nodes into the binary tree accordingly.
    # 4. Generate the created binary tree and display it along with its traversals (in-order, pre-order, post-order). 

import tkinter as tk

class BinaryTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree")
        self.root.geometry("1920x1080")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 20)

        self.canvas = tk.Canvas(self.main_frame, width = 1300, height = 500, bg = "white")
        self.canvas.pack(side = tk.LEFT, padx = 10, pady = 20)

        self.button_frame = tk.Frame(self.main_frame, width = 200)
        self.button_frame.pack(side = tk.RIGHT, pady = 20)

        self.control_buttons()

root = tk.Tk()
app = BinaryTreeGUI(root)
root.mainloop()

# Program 4: Binary Search Tree
    # In this program, the user will input numbers to create a binary search tree (BST).
    # 1. Ask the user to input specific number of digits they want to insert into the BST.
    # 2. For each digit, prompt the user to enter the number.
    # 3. Insert the numbers into the BST accordingly.
    # 4. Generate the created BST and display it along with its traversals (in-order, pre-order, post-order).

# Program 5: Tower of Hanoi using Recursion
    # In this program, the user will be able to play the Tower of Hanoi game using recursion.