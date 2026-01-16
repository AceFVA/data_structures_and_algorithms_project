# Program: Binary Tree 
    # In this program, the user will be able to create a binary tree by inserting nodes.
    # 1. Ask the user to input how many levels they want in the binary tree.
    # 2. For each level, prompt the user to enter the value of the nodes.
    # 3. Insert the nodes into the binary tree accordingly.
    # 4. Generate the created binary tree and display it along with its traversals (in-order, pre-order, post-order). 

import tkinter as tk
from tkinter import ttk

# Binary Tree Application
class BinaryTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree")
        self.root.state("zoomed")
        self.node_user_input = []
        self.node_circles = []
        self.node_highlighter = None
        self.tree_warning_timer = None
        self.traversal_warning_timer = None
        self.current_color = ""
        self.current_method = ""
        self.current_values = []
        self.show_value = []
        self.node_texts = []
        self.clicked_circle = None

        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 0)
        self.root.grid_columnconfigure(0, weight = 1)

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("DrawTree.TButton", foreground = "white", background = "green")
        style.map("DrawTree.TButton", background = [("active", "dark green")])

        style.configure("Preorder.TButton", foreground = "white", background = "blue")
        style.configure("Inorder.TButton", foreground = "white", background = "orange")
        style.configure("Postorder.TButton", foreground = "white", background = "purple")

        # Main Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 10, pady = 10)
        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(1, weight = 0)

        # Canvas for Binary Tree Visualization
        self.binary_tree_canvas = tk.Canvas(self.main_frame, bg = "white", borderwidth = 2, relief = tk.RIDGE)
        self.binary_tree_canvas.grid(row = 0, column = 0, sticky = tk.NSEW, padx = (0, 5))

        # Control Buttons Frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row = 0, column = 1, sticky = tk.NS, padx = (5, 0))
        self.button_frame.grid_propagate(0)

        self.button_frame.grid_rowconfigure(0, weight = 1)
        self.button_frame.grid_rowconfigure(1, weight = 1)
        self.button_frame.grid_rowconfigure(2, weight = 1)
        self.button_frame.grid_columnconfigure(0, weight = 1)

        self.selecting_level_box = ttk.LabelFrame(self.button_frame, text = "Select a level:")
        self.selecting_level_box.pack(fill = tk.BOTH, expand = True, padx = 15, pady = 10)

        self.selecting_traversal_box = ttk.LabelFrame(self.button_frame, text = "Select a traversal method:")
        self.selecting_traversal_box.pack(fill = tk.BOTH, expand = True, padx = 15, pady = 10)

        self.displaying_selected_node_info = ttk.LabelFrame(self.button_frame, text = "Selected Node:")
        self.displaying_selected_node_info.pack(fill = tk.BOTH, expand = True, padx = 15, pady = 10)

        self.control_buttons()

        # Traversal Result Frame
        self.traversal_result_frame = ttk.Frame(self.root)
        self.traversal_result_frame.grid(row = 1, column = 0, sticky = tk.EW, padx = 10, pady = (5, 10))
        self.traversal_result_frame.grid_propagate(0)

        self.traversal_title_label = ttk.Label(self.traversal_result_frame, text = "Traversal Result:", font = ("Segoe UI", 14))
        self.traversal_title_label.pack(pady = 5)

        self.traversal_result_label = ttk.Label(self.traversal_result_frame, text = "", font = ("Segoe", 28))
        self.traversal_result_label.pack(pady = 5)

        self.traversal_method_label = ttk.Label(self.traversal_result_frame, text = "", font = ("Segoe", 9))
        self.traversal_method_label.pack(pady = 5)

    # Control Buttons
    def control_buttons(self):
        self.level_entry = ttk.Spinbox(self.selecting_level_box, from_= 1, to = 5, state = "readonly", width = 20, justify = "center")
        self.level_entry.pack(pady = (5, 5))

        self.draw_tree_button = ttk.Button(self.selecting_level_box, text = "Draw Tree", command = self.draw_tree, style = "DrawTree.TButton")
        self.draw_tree_button.pack(padx = 5, pady = 5)

        self.warning_label = ttk.Label(self.selecting_level_box, text = "", foreground = "red")
        self.warning_label.pack(pady = 1)
        self.warning_timer = None

        self.traversals_label = ttk.Label(self.selecting_traversal_box, text = "Traversals", font = ("Segoe UI", 11))
        self.traversals_label.pack(pady = (5, 0))
        self.preorder_traversal = ttk.Button(self.selecting_traversal_box, text = "Preorder", command = lambda: self.traversals("Preorder"), style = "Preorder.TButton")
        self.preorder_traversal.pack(padx = 5, pady = 5)
        self.inorder_traversal = ttk.Button(self.selecting_traversal_box, text = "Inorder", command = lambda: self.traversals("Inorder"), style = "Inorder.TButton")
        self.inorder_traversal.pack(padx = 5, pady = 5)
        self.postorder_traversal = ttk.Button(self.selecting_traversal_box, text = "Postorder", command = lambda: self.traversals("Postorder"), style = "Postorder.TButton")
        self.postorder_traversal.pack(padx = 5, pady = 5) 

        self.node_detail_title_label = ttk.Label(self.displaying_selected_node_info, text = "Node Info", font = ("Segoe", 11))
        self.node_detail_title_label.pack(pady = (10, 5))
        self.node_detail_label = tk.Label(self.displaying_selected_node_info, fg = "red", width = 20, height = 20, font = ("Segoe", 12), relief = tk.SUNKEN)
        self.node_detail_label.pack(padx = 5, pady  = (5, 10))

    # Draws Binary Tree on Canvas based on user input
    def draw_tree(self):
        self.binary_tree_canvas.delete("all")
        self.node_circles.clear()
        self.node_texts.clear()
        self.show_value.clear()
        self.traversal_result_label.config(text = "")
        self.traversal_method_label.config(text = "")
        
        levels = int(self.level_entry.get())

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
                node_circle = self.binary_tree_canvas.create_oval(horizontal_position - node_radius, vertical_position - node_radius, horizontal_position + node_radius, vertical_position + node_radius, fill = "yellow", outline = "black", width = 2,tags = ("node",))
                self.node_circles.append(node_circle)

                node_text = self.binary_tree_canvas.create_text(horizontal_position, vertical_position, text = "", font = ("Segoe UI", 10, "bold"))
                self.node_texts.append(node_text)

                self.binary_tree_canvas.tag_bind(node_circle, "<Button-1>", lambda event, index = len(self.node_circles) - 1: self.show_node_details(index))

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

        self.draw_tree_button.config(text = "Reset", command = self.reset_tree)

    # Lets the user have a choice to reset the tree after creating one
    def reset_tree(self):
        self.binary_tree_canvas.delete("all")

        for entry in self.node_user_input:
            entry.destroy()

        self.node_circles.clear()
        self.node_user_input.clear()
        self.show_value.clear()
        self.traversal_result_label.config(text = "")
        self.traversal_method_label.config(text = "")
        self.node_detail_label.config(text = "")

        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None

        self.warning_label.config(text = "")

        self.draw_tree_button.config(text = "Draw Tree", command = self.draw_tree)

    # displays the information about the clicked node
    def show_node_details(self, index):
        if self.node_highlighter is not None and self.current_values:
            values = self.current_values

        else:
            if not self.node_user_input:
                return
        
            values = self.get_node_entries()
            if values is None:
                return
        
            values = self.off_nodes(values, re_highlight = False)
            self.current_values = values

        if self.clicked_circle is not None:
            self.binary_tree_canvas.itemconfig(self.clicked_circle, outline = "black", width = 2)

        self.clicked_circle = self.node_circles[index]
        self.binary_tree_canvas.itemconfig(self.clicked_circle, outline = "red", width = 2)

        node_value = values[index]
        
        def child_value(index):
            if 0 <= index < len(values):
                if values[index] is not None:
                    return values[index]
                
                else:
                    return "None"
            
            else:
                return "N/A"

        if index != 0:
            parent_index = (index - 1) // 2

        else:
            parent_index = None

        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        if parent_index is not None:
            parent_text = child_value(parent_index)

        else: 
            parent_text = "N/A"

        # if the node has a value "?" as an entry
        if node_value is None:
            text_detail = f"Node Index: {index + 1}\n\nNode Value: N/A\n\nConnections\n\nParent: {parent_text}\nLeft Child: N/A\nRight Child: N/A"
            self.node_detail_label.config(text = text_detail)
            return
        
        # if the node is the root
        if index == 0:
            text_detail = f"Node Index: Root\nNode Value: {node_value}\n\nConnections\n\nParent: None\nLeft Child: {child_value(left_child_index)}\nRight Child: {child_value(right_child_index)}"

        # if the node is a descendants of the root
        else:
            text_detail = (f"Node Index: {index + 1}\nNode Value: {node_value}\n\nConnections\n\nParent: {parent_text}\nLeft Child: {child_value(left_child_index)}\nRight Child: {child_value(right_child_index)}")

        self.node_detail_label.config(text = text_detail)

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
                self.warning_label.config(text = "Missing node value. Please input any\nvalue first or '?' if its an empty node.")
                self.tree_warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
                return

            if value != "?":
                values.append(value)

            else:
                values.append(None)

        return values
    
    # This will gray out the nodes under a node with a "?" entried by the user
    def off_nodes(self, values, re_highlight = True):
        for index in range(len(values)):
            if values[index] is None:
                left = 2 * index + 1 # left child
                right = 2 * index + 2 # right child

                if left < len(values):
                    values[left] = None

                if right < len(values):
                    values[right] = None

        if re_highlight:
            for index, value in enumerate(values):
                if value is None:
                    self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "lightgray")
                    self.binary_tree_canvas.itemconfig(self.node_texts[index], text = "")

                else: 
                    self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "yellow")
                    self.binary_tree_canvas.itemconfig(self.node_texts[index], text = value)
        
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
    
    # creates an animation when traversing
    def node_animation(self, order, step = 0, delay = 500):
        if step >= len(order):
            self.node_highlighter = None
            self.node_color_reset()
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
        self.binary_tree_canvas.itemconfig(self.node_texts[result_index], fill = "white")
        self.node_highlighter = self.root.after(delay, lambda: self.node_animation(order, step + 1, delay))
        self.traversal_result_label.config(text = " ".join(self.show_value), fg = self.current_color)

    def node_color_reset(self):
        if not self.current_values:
            return
        
        for index, value in enumerate(self.current_values):
            if value is None:
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "lightgray")

            else: 
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "yellow")

            self.binary_tree_canvas.itemconfig(self.node_texts[index], fill = "black")
            self.binary_tree_canvas.itemconfig(self.node_circles[index], outline = "black", width = 2)

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
        
        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None
            self.node_color_reset()
            self.show_value.clear()
            self.traversal_result_label.config(text = "")

        values = self.get_node_entries()

        if values is None:
            return
        
        values = self.off_nodes(values)

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

        self.current_color = font_color
        self.current_method = method

        self.traversal_result_label.config(text = "", fg = self.current_color)
        self.traversal_method_label.config(text = self.current_method, fg = self.current_color)

        self.node_animation(result)

root = tk.Tk()
app = BinaryTreeApp(root)
root.mainloop()