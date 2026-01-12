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
        self.node_circles = []
        self.node_highlighter = None
        self.tree_warning_timer = None
        self.traversal_warning_timer = None
        self.current_color = ""
        self.current_method = ""
        self.current_values = []
        self.show_value = []

        # Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side = tk.TOP, fill = tk.Y, expand = True, padx = (20, 20))

        # Canvas for Binary Tree Visualization
        self.binary_tree_canvas = tk.Canvas(self.main_frame, width = 1200, height = 650, bg = "white", borderwidth = 3, relief = tk.RIDGE)
        self.binary_tree_canvas.pack(side = tk.LEFT, padx = (20, 0))

        # Control Buttons Frame
        self.button_frame = tk.Frame(self.main_frame, width = 720, height = 657, borderwidth = 3, relief = tk.RIDGE)
        self.button_frame.pack(side = tk.RIGHT, padx = (0, 20))
        self.button_frame.pack_propagate(0)

        self.control_buttons()

        # Traversal Result Frame
        self.traversal_result_frame = tk.Frame(self.root, width = 1920, height = 200, bg = "lightgray", borderwidth = 3,  relief = tk.RIDGE)
        self.traversal_result_frame.pack(side = tk.BOTTOM, padx = (40, 40), pady = (0, 50))
        self.traversal_result_frame.pack_propagate(0)

        self.traversal_title_label = tk.Label(self.traversal_result_frame, text = "Traversal Result:", font = ("Segoe UI", 14), bg = "lightgray")
        self.traversal_title_label.pack(pady = 5)

        self.traversal_result_label = tk.Label(self.traversal_result_frame, text = "", font = ("Segoe", 28), bg = "lightgray")
        self.traversal_result_label.pack(pady = 5)

        self.traversal_method_label = tk.Label(self.traversal_result_frame, text = "", font = ("Segoe", 9), bg = "lightgray")
        self.traversal_method_label.pack(pady = 5)

    # Control Buttons
    def control_buttons(self):
        tk.Label(self.button_frame, text = "Number of Levels:", font = ("Segoe UI", 11)).pack(side = tk.TOP, pady = (20, 5))
        self.level_entry = tk.Entry(self.button_frame, bg = "lightgray", width = 15, justify = "center", borderwidth = 1, relief = tk.SOLID)
        self.level_entry.insert(0, "5")
        self.level_entry.pack(pady = (0, 10))

        self.draw_tree_button = tk.Button(self.button_frame, text = "Draw Tree", bg = "green", fg = "white", width = 20, height = 2, command = self.draw_tree)
        self.draw_tree_button.pack(pady = 5)

        self.warning_label = tk.Label(self.button_frame, text = "", font = ("Segoe UI", 9), fg = "red")
        self.warning_label.pack(pady = 5)
        self.warning_timer = None

        self.traversals_label = tk.Label(self.button_frame, text = "Traversals:", font = ("Segoe UI", 11))
        self.traversals_label.pack(pady = (5, 5))
        self.preorder_traversal = tk.Button(self.button_frame, text = "Preorder", bg = "blue", fg = "white", width = 20, command = lambda: self.traversals("Preorder"))
        self.preorder_traversal.pack(pady = 5)
        self.inorder_traversal = tk.Button(self.button_frame, text = "Inorder", bg = "orange", fg = "white", width = 20, command = lambda: self.traversals("Inorder"))
        self.inorder_traversal.pack(pady = 5)
        self.postorder_traversal = tk.Button(self.button_frame, text = "Postorder", bg = "purple", fg = "white", width = 20, command = lambda: self.traversals("Postorder"))
        self.postorder_traversal.pack(pady = 5) 

        self.node_detail_title_label = tk.Label(self.button_frame, text = "Selected Node:", font = ("Segoe", 11))
        self.node_detail_title_label.pack(pady = (20, 5))
        self.node_detail_label = tk.Label(self.button_frame, bg = "lightgray", width = 20, height = 15, borderwidth = 1, relief = tk.SOLID)
        self.node_detail_label.pack(pady  = (5, 10))

    # Draws Binary Tree on Canvas based on user input
    def draw_tree(self):
        self.binary_tree_canvas.delete("all")
        self.node_circles.clear()
        self.show_value.clear()
        self.traversal_result_label.config(text = "")
        self.traversal_method_label.config(text = "")
        levels = self.level_entry.get()

        # Reset timers
        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None

        if self.traversal_warning_timer is not None:
            self.root.after_cancel(self.traversal_warning_timer)
            self.traversal_warning_timer = None

        # Verify if the input is a valid positive integer
        self.warning_label.config(text = "")
        if self.tree_warning_timer is not None:
            self.root.after_cancel(self.tree_warning_timer)
            self.tree_warning_timer = None

        self.traversal_title_label.config(text = "Traversal Result:", fg = "black")
        
        try: 
            if int(levels) > 5:
                self.warning_label.config(text = "Maximum level reached (5)\nPlease try again.")
                self.tree_warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
                return

            if int(levels) < 1:
                raise ValueError
            
        except ValueError:
            self.warning_label.config(text = "Invalid input.\nPlease enter a valid positive integer.")
            self.tree_warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
            return
        
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
                node_circle = self.binary_tree_canvas.create_oval(horizontal_position - node_radius, vertical_position - node_radius, horizontal_position + node_radius, vertical_position + node_radius, fill = "yellow")
                self.node_circles.append(node_circle)

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

    # This will make a text box where users can enter their input on each node
    def create_node_user_input(self, node_positions):
        for inputs in self.node_user_input:
            inputs.destroy()

        self.node_user_input.clear()

        for level_nodes in node_positions:
            for node_x, node_y in level_nodes:
                user_entry = tk.Entry(self.binary_tree_canvas, width = 2, justify = "center")
                self.binary_tree_canvas.create_window(node_x, node_y, window = user_entry)
                self.node_user_input.append(user_entry)

    # Gets the inputs in each node
    def get_node_entries(self):
        values = []
        for entry in self.node_user_input:
            value = entry.get().strip()

            try:
                if value == "":
                    raise ValueError
                
            except ValueError:
                self.warning_label.config(text = "Missing node value.\nPlease input any value first\nor '?' if its an empty node.")
                self.tree_warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
                return

            if value != "?":
                values.append(value)

            else:
                values.append(None)

        return values
    
    # This will gray out the nodes under a node with a "?" entried by the user
    def off_nodes(self, values):
        for index in range(len(values)):
            if values[index] is None:
                left = 2 * index + 1 # left child
                right = 2 * index + 2 # right child

            if left < len(values):
                values[left] = None

            if right < len(values):
                values[right] = None

        for index, value in enumerate(values):
            self.binary_tree_canvas.itemconfig(self.node_circles[index])

            if value is None:
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "lightgray")

            else: 
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "yellow")

        return values
    
    # Preorder Traversal
    def preorder(self, values):
        if not values:
            return []
        
        stack = [0]
        pop_out = []

        while stack:
            index = stack.pop()
            if index >= len(values):
                continue

            if values[index] is None:
                continue

            else:
                pop_out.append(index)

                stack.append(2 * index + 2)
                stack.append(2 * index + 1)

        return pop_out
    
    # Inorder Traversal
    def inorder(self, values):
        if not values:
            return []
        
        stack = []
        pop_out = []
        index = 0

        while stack or index < len(values):
            while index < len(values) and values[index] is not None:
                stack.append(index)
                index = 2 * index + 1

            if not stack:
                break

            index = stack.pop()
            pop_out.append(index)
            index = 2 * index + 2
        
        return pop_out

    # Postorder Traversal
    def postorder(self, values):
        if not values:
            return []
        
        stack = [(0, False)]
        pop_out = []

        while stack:
            index, visited = stack.pop()
            if index >= len(values):
                continue

            if values[index] is None:
                continue

            if visited:
                pop_out.append(index)
            
            else:
                stack.append((index, True))
                stack.append((2 * index + 2, False))
                stack.append((2 * index + 1, False))

        return pop_out
    
    def node_animation(self, order, step = 0, delay = 500):
        if step >= len(order):
            self.node_highlighter = None
            return
        
        result_index = order[step]
        get_value = self.current_values[result_index]

        if get_value is None:
            self.node_highlighter = self.root.after(delay, lambda: self.node_animation(order, step + 1, delay))
            return

        elif get_value == "":
            self.show_value.append("_")

        else:
            self.show_value.append(get_value)

        self.binary_tree_canvas.itemconfig(self.node_circles[result_index], fill = self.current_color)
        self.node_highlighter = self.root.after(delay, lambda: self.node_animation(order, step + 1, delay))
        self.traversal_result_label.config(text = " ".join(self.show_value), fg = self.current_color)

    # Identify traversal type and display result
    def traversals(self, method):
        if self.traversal_warning_timer is not None:
            self.root.after_cancel(self.traversal_warning_timer)
            self.traversal_warning_timer = None

        if not self.node_user_input:
            self.traversal_title_label.config(text = "Traversal Result:\n\nDraw the Binary Tree first.", fg = "red")
            self.traversal_warning_timer = self.root.after(1000, lambda: self.traversal_title_label.config(text = "Traversal Result: ", fg = "black"))
            self.traversal_result_label.config(text = "")
            self.traversal_method_label.config(text = "")
            return
        
        values = self.get_node_entries()
        if values is None:
            return

        self.current_values = values
        self.show_value.clear()

        if method == "Preorder":
            result = self.preorder(values)
            font_color = "blue"

        elif method == "Inorder":
            result = self.inorder(values)
            font_color = "orange"

        elif method == "Postorder":
            result = self.postorder(values)
            font_color = "purple"

        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None

        for circle in self.node_circles:
            self.binary_tree_canvas.itemconfig(circle, fill = "yellow")

        self.current_color = font_color
        self.current_method = method

        self.traversal_result_label.config(text = "", fg = self.current_color)
        self.traversal_method_label.config(text = self.current_method, fg = self.current_color)

        self.node_animation(result)

root = tk.Tk()
app = BinaryTreeApp(root)
root.mainloop()