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

# Binary Tree Application
class BinaryTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree")
        self.root.geometry("1920x1080")

# Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side = tk.TOP, fill = tk.Y, expand = True, padx = (20, 20), pady = (20, 200))

# Canvas for Binary Tree Visualization
        self.binary_tree_canvas = tk.Canvas(self.main_frame, width = 1200, height = 700, bg = "blue", bd = 2, relief = tk.RIDGE)
        self.binary_tree_canvas.pack(side = tk.LEFT, padx = (20, 0), pady = 20)

# Control Buttons Frame
        self.button_frame = tk.Frame(self.main_frame, width = 720, height = 700, bd = 2, relief = tk.RIDGE)
        self.button_frame.pack(side = tk.RIGHT, padx = (0, 20), pady = 20)
        self.button_frame.pack_propagate(0)

        self.control_buttons()

# Traversal Result Frame
        self.traversal_result_frame = tk.Frame(self.root, width = 1920, height = 380, bg = "lightgray", bd = 2, relief = tk.RIDGE)
        self.traversal_result_frame.pack(side = tk.BOTTOM, fill = tk.X, padx = (20, 20), pady = (0, 20))
        self.traversal_result_frame.pack_propagate(0)

        self.traversal_result_label = tk.Label(self.traversal_result_frame, text = "Traversal Result: ", font = ("Segoe UI", 14), bg = "lightgray")
        self.traversal_result_label.pack(pady = 20)

# Control Buttons
    def control_buttons(self):
        tk.Label(self.button_frame, text = "Number of Levels:", font = ("Segoe UI", 11)).pack(side = tk.TOP, pady = (5, 5))
        self.level_entry = tk.Entry(self.button_frame, width = 15, justify = "center")
        self.level_entry.insert(0, "1")
        self.level_entry.pack(pady = (0, 20))

        tk.Button(self.button_frame, text = "Draw Tree", bg = "green", fg = "white", width = 20, height = 2, command = self.draw_tree).pack(pady = 10)

        self.traversals_label = tk.Label(self.button_frame, text = "Traversals:", font = ("Segoe UI", 11))
        self.traversals_label.pack(pady = (20, 5))
        tk.Button(self.button_frame, text = "Preorder", bg = "blue", fg = "white", width = 20, command = lambda: self.traversals("Preorder")).pack(pady = 5)
        tk.Button(self.button_frame, text = "Inorder", bg = "orange", fg = "white", width = 20, command = lambda: self.traversals("Inorder")).pack(pady = 5)
        tk.Button(self.button_frame, text = "Postorder", bg = "purple", fg = "white", width = 20, command = lambda: self.traversals("Postorder")).pack(pady = 5)

# Draws Binary Tree on Canvas based on user input
    def draw_tree(self):
        self.binary_tree_canvas.delete("all")
        levels = self.level_entry.get()

# Verify if the input is a valid positive integer
        try:
            levels = int(levels)
            if levels < 1:
                raise ValueError
            
        except ValueError:
            self.binary_tree_canvas.create_text(600, 350, text = "Please enter a valid positive integer for levels.", font = ("Segoe UI", 16), fill = "red")
            return

        self.binary_tree_canvas.create_text(600, 350, text = "(Tree would be drawn here)", font = ("Segoe UI", 20), fill = "white")

# Identify traversal type and display result
    def traversals(self, mode):
        self.traversal_result_label.config(text = f"Traversal Result: ({mode} traversal)")

root = tk.Tk()
app = BinaryTreeApp(root)
root.mainloop()

# Program 4: Binary Search Tree
    # In this program, the user will input numbers to create a binary search tree (BST).
    # 1. Ask the user to input specific number of digits they want to insert into the BST.
    # 2. For each digit, prompt the user to enter the number.
    # 3. Insert the numbers into the BST accordingly.
    # 4. Generate the created BST and display it along with its traversals (in-order, pre-order, post-order).

# Program 5: Tower of Hanoi using Recursion
    # In this program, the user will be able to play the Tower of Hanoi game using recursion.