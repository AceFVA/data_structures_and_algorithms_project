# Program: Binary Tree 
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
        self.node_user_input = []

        # Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side = tk.TOP, fill = tk.Y, expand = True, padx = (20, 20), pady = (20, 200))

        # Canvas for Binary Tree Visualization
        self.binary_tree_canvas = tk.Canvas(self.main_frame, width = 1200, height = 700, bg = "white", bd = 2, relief = tk.RIDGE)
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

        self.traversal_result_label = tk.Label(self.traversal_result_frame, text = "Traversal Result: ", font = ("Segoe UI", 14), bg = "lightgray", fg = "blue")
        self.traversal_result_label.pack(pady = 20)

    # Control Buttons
    def control_buttons(self):
        tk.Label(self.button_frame, text = "Number of Levels:", font = ("Segoe UI", 11)).pack(side = tk.TOP, pady = (5, 5))
        self.level_entry = tk.Entry(self.button_frame, width = 15, justify = "center")
        self.level_entry.insert(0, "5")
        self.level_entry.pack(pady = (0, 20))

        self.draw_tree_button = tk.Button(self.button_frame, text = "Draw Tree", bg = "green", fg = "white", width = 20, height = 2, command = self.draw_tree)
        self.draw_tree_button.pack(pady = 10)

        self.warning_label = tk.Label(self.button_frame, text = "", font = ("Segoe UI", 9), fg = "red")
        self.warning_label.pack(pady = 5)
        self.warning_timer = None

        self.traversals_label = tk.Label(self.button_frame, text = "Traversals:", font = ("Segoe UI", 11))
        self.traversals_label.pack(pady = (20, 5))
        self.preorder_traversal = tk.Button(self.button_frame, text = "Preorder", bg = "blue", fg = "white", width = 20, command = lambda: self.traversals("Preorder"))
        self.preorder_traversal.pack(pady = 5)
        self.inorder_traversal = tk.Button(self.button_frame, text = "Inorder", bg = "orange", fg = "white", width = 20, command = lambda: self.traversals("Inorder"))
        self.inorder_traversal.pack(pady = 5)
        self.postorder_traversal = tk.Button(self.button_frame, text = "Postorder", bg = "purple", fg = "white", width = 20, command = lambda: self.traversals("Postorder"))
        self.postorder_traversal.pack(pady = 5) 

    # Draws Binary Tree on Canvas based on user input
    def draw_tree(self):
        self.binary_tree_canvas.delete("all")
        levels = self.level_entry.get()

        # Verify if the input is a valid positive integer
        self.warning_label.config(text = "")
        if self.warning_timer is not None:
            self.root.after_cancel(self.warning_timer)
            self.warning_timer = None

        try: 
            if int(levels) > 5:
                self.warning_label.config(text = "Maximum level reached (5)\nPlease try again.")
                self.warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
                return

            if int(levels) < 1:
                raise ValueError
            
        except ValueError:
            self.warning_label.config(text = "Invalid input.\nPlease enter a valid positive integer.")
            self.warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
        
        # Parameters for making the binary tree
        canvas_width = 1200
        node_radius = 20
        vertical_spacing = 100

        node_positions = [] # To store positions of nodes for drawing connections

        # Draw nodes level by level
        for level in range(int(levels)):
            node_count = 2 ** level
            vertical_position = (level + 1) * vertical_spacing
            level_node_positions = []

            for node in range(node_count):
                horizontal_spacing = canvas_width // (node_count + 1)
                horizontal_position = (node + 1) * horizontal_spacing
                level_node_positions.append((horizontal_position, vertical_position))

                # Drawing circle for node
                self.binary_tree_canvas.create_oval(horizontal_position - node_radius, vertical_position - node_radius, horizontal_position + node_radius, vertical_position + node_radius, fill = "yellow")
            
            # Store each node's position separated by its level
            node_positions.append(level_node_positions)

        for level in range(len(node_positions) - 1): # Index: 0, 1, 2, 3 (except 4 since the nodes in this level doesn't have a child)
            parent_node = node_positions[level] 
            children_nodes = node_positions[level + 1]

            for parent_index, (parent_x, parent_y) in enumerate(parent_node): # --> 0, (x-axis, y-axis)
                left_child = 2 * parent_index
                right_child = 2 * parent_index + 1

                if left_child < len(children_nodes):
                    children_x, children_y = children_nodes[left_child]
                    self.binary_tree_canvas.create_line(parent_x, parent_y, children_x, children_y, width = 1, tags = "line")

                if right_child < len(children_nodes):
                    children_x, children_y = children_nodes[right_child]
                    self.binary_tree_canvas.create_line(parent_x, parent_y, children_x, children_y, width = 1, tags = "line")

            self.binary_tree_canvas.tag_lower("line")
        
        self.create_node_user_input(node_positions)

    def create_node_user_input(self, node_positions):
        for inputs in self.node_user_input:
            inputs.destroy()

        self.node_user_input.clear()

        for level_nodes in node_positions:
            for node_x, node_y in level_nodes:
                user_entry = tk.Entry(self.binary_tree_canvas, width = 4, justify = "center")
                self.binary_tree_canvas.create_window(node_x, node_y, window = user_entry)
                self.node_user_input.append(user_entry)


    # Identify traversal type and display result
    def traversals(self, mode):
        self.traversal_result_label.config(text = f"Traversal Result: ({mode} traversal)")

root = tk.Tk()
app = BinaryTreeApp(root)
root.mainloop()