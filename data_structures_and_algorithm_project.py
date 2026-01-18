# Program: Binary Tree 
    # In this program, the user will be able to create a binary tree by inserting nodes.
    # 1. Ask the user to input how many levels they want in the binary tree.
    # 2. For each level, prompt the user to enter the value of the nodes.
    # 3. Insert the nodes into the binary tree accordingly.
    # 4. Generate the created binary tree and display it along with its traversals (in-order, pre-order, post-order). 

import tkinter as tk
from tkinter import ttk

#------------------- Binary Tree Application -------------------#
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
        self.info_color = "black"
        self.node_forced_off = []

        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 0)
        self.root.grid_rowconfigure(2, weight = 0)
        self.root.grid_columnconfigure(0, weight = 1)

#------------------- Customizations -------------------#
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("DrawTree.TButton", foreground = "white", background = "green")
        style.map("DrawTree.TButton", background = [("active", "dark green")])

        style.configure("Preorder.TButton", foreground = "white", background = "blue")
        style.map("Preorder.TButton", background = [("active", "lime")])
        style.configure("Inorder.TButton", foreground = "white", background = "orange")
        style.map("Inorder.TButton", background = [("active", "lime")])
        style.configure("Postorder.TButton", foreground = "white", background = "purple")
        style.map("Postorder.TButton", background = [("active", "lime")])
        style.configure("Instructions.TButton", font = ("Segoe", 9, "underline"), relief = "flat", foreground = "blue", background = "white")
        style.configure("OffedNode.TEntry", fieldbackground = "lightgray", foreground = "gray")

#------------------- Main Frame -------------------#
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 10)
        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(1, weight = 0)

#------------------- Canvas for Binary Tree Visualization -------------------#
        self.binary_tree_canvas = tk.Canvas(self.main_frame, bg = "white", borderwidth = 2, relief = tk.RIDGE)
        self.binary_tree_canvas.configure(width = 900, height = 600)
        self.binary_tree_canvas.grid(row = 0, column = 0, sticky = tk.NSEW, padx = (0, 5))

        # For adjusting window size
        self.levels = 0
        self.binary_tree_canvas.bind("<Configure>", self.on_tree_resize)

        # for Instructions display
        self.app_instructions = ttk.Button(self.binary_tree_canvas, text = "Help?", width = 5, style = "Instructions.TButton", command = self.show_instructions)
        self.instructions_id = self.binary_tree_canvas.create_window(0, 0, window = self.app_instructions, anchor = tk.SE)
        self.root.update_idletasks()
        self.binary_tree_canvas.coords(self.instructions_id, self.binary_tree_canvas.winfo_width() - 10, self.binary_tree_canvas.winfo_height() -10)

#------------------- Control Buttons Frame -------------------#
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.config(width = 320)
        self.button_frame.grid(row = 0, column = 1, sticky = tk.NSEW, padx = (5, 0))
        self.button_frame.grid_propagate(0)

        for row in range(3):
            self.button_frame.grid_rowconfigure(row, weight = 1)

        self.button_frame.grid_columnconfigure(0, weight = 1)

        self.selecting_level_box = ttk.LabelFrame(self.button_frame, text = "Select a level:")
        self.selecting_level_box.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 15, pady = (10, 5))

        self.selecting_traversal_box = ttk.LabelFrame(self.button_frame, text = "Select a traversal method:")
        self.selecting_traversal_box.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 15, pady = 5)
        self.selecting_traversal_box.columnconfigure(0, weight = 1)

        self.displaying_selected_node_info = ttk.LabelFrame(self.button_frame, text = "Selected Node:")
        self.displaying_selected_node_info.grid(row = 2, column = 0, sticky = tk.NSEW, padx = 15, pady = (5, 10))
        self.displaying_selected_node_info.grid_columnconfigure(0, weight = 1)
        self.displaying_selected_node_info.grid_columnconfigure(1, weight = 2)

        for row in range(6):
            self.displaying_selected_node_info.grid_rowconfigure(row, weight = 1)

        self.control_buttons()

#------------------- Traversal Result Frame -------------------#
        self.top_separating_line = ttk.Separator(self.root, orient = "horizontal")
        self.top_separating_line.grid(row = 1, column = 0, sticky = tk.EW, padx = 10, pady = (6, 4))

        self.traversal_result_frame = ttk.Frame(self.root)
        self.traversal_result_frame.configure(height = 160)
        self.traversal_result_frame.grid(row = 2, column = 0, sticky = tk.EW, padx = 10, pady = (0, 10))
        self.traversal_result_frame.grid_propagate(0)

        self.traversal_title_label = ttk.Label(self.traversal_result_frame, text = "Traversal Result", font = ("Segoe UI", 14), anchor = "center", justify = "center")
        self.traversal_title_label.pack(pady = (5, 0), fill = tk.X)
        self.traversal_warning_label = ttk.Label(self.traversal_result_frame, text = "\n", foreground = "red", anchor = "center", justify = "center")
        self.traversal_warning_label.pack(pady = (0, 5), fill = tk.X)

        self.traversal_result_label = ttk.Label(self.traversal_result_frame, text = "", font = ("Segoe", 28), anchor = "center", justify = "center")
        self.traversal_result_label.pack(pady = 5)

        self.traversal_method_label = ttk.Label(self.traversal_result_frame, text = "", font = ("Segoe", 12), anchor = "center", justify = "center")
        self.traversal_method_label.pack(pady = 5)

#------------------- Instructions -------------------#
    # Shows the instructions when the user clicked the button
    def show_instructions(self):
        if hasattr(self, "instruction_window") and self.instruction_window.winfo_exists():
            self.instruction_window.lift()
            return

        self.instruction_window = tk.Toplevel(self.root)
        window = self.instruction_window
        window.title("How To Use")
        window.geometry("425x350")
        window.resizable(False, False)

        tk.Label(window, text = "Instructions", font = ("Segoe", 11)).pack(pady = (20, 0))
        tk.Label(
            window, 
            text = (
                "1.  Select your desired level of Binary Tree.\n"
                "2.  Click 'Draw Tree' button to display the Binary Tree template.\n"
                "3.  Enter any value you want on each node.\n"
                "4.  Select a traversal method of you want.\n"
                "5.  You can select any node to display its information.\n"                    
                "6.  Wait for the traversal result and you're done!"
            ), 
            justify = "left",
            font = ("Segoe", 10)
        ).pack(padx = 20, pady = 10, anchor = tk.W)

        tk.Label(window, text = "Reminders", font = ("Segoe", 11)).pack(pady = (5, 0))
        tk.Label(
            window,
            text = (
                "1.  The maximum number of level is 5.\n"
                "2.  Click the 'Reset' button to clear the entries in all nodes.\n"
                "3.  No node must be empty.\n"
                "4.  Enter '?' on any node that you want to switch off.\n"
                "5.  Switched off nodes will not be able to show its details."
            ),
            justify = "left",
            font = ("Segoe", 10)
        ).pack(padx = 20, pady = 10, anchor = tk.W)

        tk.Button(window, text = "Okay", command = lambda: (window.destroy(), setattr(self, "instruction_window", None))).pack(pady = 10)
        window.protocol("WM_DELETE_WINDOW", lambda: setattr(self, "instruction_window", None))

#------------------- Control Buttons -------------------#
    def control_buttons(self):
        # Select a level tab
        self.level_entry = ttk.Spinbox(self.selecting_level_box, from_= 1, to = 5, state = "readonly", width = 20, justify = "center")
        self.level_entry.pack(pady = (5, 5))

        self.draw_tree_button = ttk.Button(self.selecting_level_box, text = "Draw Tree", width = 20, command = self.draw_tree, style = "DrawTree.TButton")
        self.draw_tree_button.pack(padx = 5, pady = 5)

        self.warning_label = ttk.Label(self.selecting_level_box, text = "", foreground = "red")
        self.warning_label.pack(pady = 1)

        # Select traversal method tab
        self.traversals_label = ttk.Label(self.selecting_traversal_box, text = "Traversals", font = ("Segoe UI", 11))
        self.traversals_label.grid(row = 0, column = 0, sticky = tk.NS, pady = (5, 20))
        self.preorder_traversal = ttk.Button(self.selecting_traversal_box, text = "Preorder", command = lambda: self.traversals("Preorder"), style = "Preorder.TButton")
        self.preorder_traversal.grid(row = 1, column = 0, sticky = tk.EW, padx = 20, pady = 5)
        self.inorder_traversal = ttk.Button(self.selecting_traversal_box, text = "Inorder", command = lambda: self.traversals("Inorder"), style = "Inorder.TButton")
        self.inorder_traversal.grid(row = 2, column = 0, sticky = tk.EW, padx = 20, pady = 5)
        self.postorder_traversal = ttk.Button(self.selecting_traversal_box, text = "Postorder", command = lambda: self.traversals("Postorder"), style = "Postorder.TButton")
        self.postorder_traversal.grid(row = 3, column = 0, sticky = tk.EW, padx = 20, pady = 5) 

        # disable the buttons first
        self.preorder_traversal.state(["disabled"])
        self.inorder_traversal.state(["disabled"])
        self.postorder_traversal.state(["disabled"])

        # Selected Info tab
        # Column 0
        self.node_info_title = ttk.Label(self.displaying_selected_node_info, text = "Node Information", font = ("Segoe", 11)).grid(row = 0, column = 0, columnspan = 2, sticky = tk.NS, pady=(5, 5))
        self.node_info_index = ttk.Label(self.displaying_selected_node_info, text = "Node Index:").grid(row = 1, column = 0, sticky = tk.W, padx = 10)
        self.node_info_value = ttk.Label(self.displaying_selected_node_info, text = "Node Value:").grid(row = 2, column = 0, sticky = tk.W, padx = 10)
        self.node_info_parent = ttk.Label(self.displaying_selected_node_info, text = "Parent:").grid(row = 3, column = 0, sticky = tk.W, padx = 10)
        self.node_info_left_chld = ttk.Label(self.displaying_selected_node_info, text = "Left Child:").grid(row = 4, column = 0, sticky = tk.W, padx = 10)
        self.node_info_right_chld = ttk.Label(self.displaying_selected_node_info, text = "Right Child:").grid(row = 5, column = 0, sticky = tk.W, padx = 10)

        # Column 1
        self.node_info_index_val = ttk.Label(self.displaying_selected_node_info, text = "?")
        self.node_info_index_val.grid(row = 1, column = 1, sticky = tk.W, padx = 10)
        self.node_info_value_val = ttk.Label(self.displaying_selected_node_info, text = "?")
        self.node_info_value_val.grid(row = 2, column = 1, sticky = tk.W, padx = 10)
        self.node_info_parent_val = ttk.Label(self.displaying_selected_node_info, text = "?")
        self.node_info_parent_val.grid(row = 3, column = 1, sticky = tk.W, padx = 10)
        self.node_info_left_chld_val = ttk.Label(self.displaying_selected_node_info, text = "?")
        self.node_info_left_chld_val.grid(row = 4, column = 1, sticky = tk.W, padx = 10)
        self.node_info_right_chld_val = ttk.Label(self.displaying_selected_node_info, text = "?")
        self.node_info_right_chld_val.grid(row = 5, column = 1, sticky = tk.W, padx = 10)
        
#------------------- Draws Binary Tree on Canvas based on user input -------------------#
    def draw_tree(self):
        self.binary_tree_canvas.delete("tree")
        self.node_circles.clear()
        self.node_texts.clear()
        self.show_value.clear()
        self.traversal_result_label.config(text = "")
        self.traversal_method_label.config(text = "")
        self.traversal_warning_label.config(text = "\n")
        
        levels = int(self.level_entry.get())
        self.levels = levels

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

        self.traversal_title_label.config(text = "Traversal Result:", foreground = "black")
        
        # Parameters for making the binary tree
        self.root.update_idletasks()
        canvas_width = self.binary_tree_canvas.winfo_width()
        canvas_height = self.binary_tree_canvas.winfo_height()

        node_radius = 20
        top_margin = max(50, canvas_height // (levels + 1) // 2)
        vertical_spacing = max(60, min(100, (canvas_height - (top_margin + 40)) // max(1, levels))) 

        node_positions = [] # To store positions of nodes for drawing connections

        # Draw nodes level by level
        for level in range(levels):
            node_count = 2 ** level
            vertical_position = top_margin + level * vertical_spacing
            level_node_positions = []

            for node in range(node_count):
                horizontal_spacing = canvas_width / (node_count + 1)
                horizontal_position = int((node + 1) * horizontal_spacing)
                level_node_positions.append((horizontal_position, vertical_position))

                # Drawing circle for node
                node_circle = self.binary_tree_canvas.create_oval(horizontal_position - node_radius, vertical_position - node_radius, horizontal_position + node_radius, vertical_position + node_radius, fill = "yellow", outline = "black", width = 2,tags = ("tree", "node"))
                self.node_circles.append(node_circle)

                node_text = self.binary_tree_canvas.create_text(horizontal_position, vertical_position, text = "", font = ("Segoe UI", 10, "bold"), tags = ("tree",))
                self.node_texts.append(node_text)

                index = len(self.node_circles) - 1
                self.binary_tree_canvas.tag_bind(node_circle, "<Button-1>", lambda event, i = index: self.show_node_details(i))
                self.binary_tree_canvas.tag_bind(node_text, "<Button-1>", lambda event, i = index: self.show_node_details(i))

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
                    self.binary_tree_canvas.create_line(parent_x, parent_y, children_x, children_y, width = 1, tags = ("tree", "line"))

                if right_child < len(children_nodes):
                    children_x, children_y = children_nodes[right_child]
                    self.binary_tree_canvas.create_line(parent_x, parent_y, children_x, children_y, width = 1, tags = ("tree", "line"))

            self.binary_tree_canvas.tag_lower("line")
        
        self.create_node_user_input(node_positions)

        self.draw_tree_button.config(text = "Reset", command = self.reset_tree)

        self.preorder_traversal.state(["!disabled"])
        self.inorder_traversal.state(["!disabled"])
        self.postorder_traversal.state(["!disabled"])

#------------------- Lets the user have a choice to reset the tree after creating one -------------------#
    def reset_tree(self):
        self.binary_tree_canvas.delete("tree")

        for entry in self.node_user_input:
            entry.destroy()

        self.node_circles.clear()
        self.node_user_input.clear()
        self.show_value.clear()
        self.current_values = []
        self.current_color = ""
        self.current_method = ""
        self.traversal_result_label.config(text = "")
        self.traversal_method_label.config(text = "")
        self.node_info_index_val.config(text = "?")
        self.node_info_value_val.config(text = "?")
        self.node_info_parent_val.config(text = "?")
        self.node_info_left_chld_val.config(text = "?")
        self.node_info_right_chld_val.config(text = "?")

        if self.traversal_warning_timer is not None:
            self.root.after_cancel(self.traversal_warning_timer)
            self.traversal_warning_timer = None

        self.traversal_warning_label.config(text = "\n")

        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None

        self.warning_label.config(text = "")

        self.draw_tree_button.config(text = "Draw Tree", command = self.draw_tree)

        self.preorder_traversal.state(["disabled"])
        self.inorder_traversal.state(["disabled"])
        self.postorder_traversal.state(["disabled"])

#------------------- Resizing Tree when window size changes -------------------#
    def on_tree_resize(self, event):
        self.binary_tree_canvas.coords(self.instructions_id, event.width - 10, event.height - 10)

        # Checck if the tree exists first
        if not self.node_user_input:
            return

        values = []
        for entry in self.node_user_input:
            values.append(entry.get())

        self.draw_tree()
        
        for entry, value in zip(self.node_user_input, values):
            entry.insert(0, value)

#------------------- displays the information about the clicked node -------------------#
    def show_node_details(self, index):
        if self.node_forced_off and index < len(self.node_forced_off) and  self.node_forced_off[index]:
            return

        if self.current_color:
            self.info_color = self.current_color

        else:
            self.info_color = "black"

        if self.node_highlighter is not None and self.current_values:
            values = self.current_values

        else:
            if not self.node_user_input:
                return
        
            values = self.get_node_entries(warning = False)
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
                if values[index] is None:
                    return "Empty"
                
                if values[index] == "":
                    return "Empty"
                
                return values[index]
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

        if index == 0:
            self.node_info_index_val.config(text = "Root", foreground = self.info_color)
            self.node_info_parent_val.config(text = "None", foreground = self.info_color)

        else: 
            self.node_info_index_val.config(text = str(index + 1), foreground = self.info_color)
            self.node_info_parent_val.config(text = parent_text, foreground = self.info_color)

        if node_value is None or node_value == "":
            self.node_info_value_val.config(text = "Empty", foreground = self.info_color)
            self.node_info_left_chld_val.config(text = child_value(left_child_index), foreground = self.info_color)
            self.node_info_right_chld_val.config(text = child_value(right_child_index), foreground = self.info_color)

        else:
            self.node_info_value_val.config(text = node_value, foreground = self.info_color)
            self.node_info_left_chld_val.config(text = child_value(left_child_index), foreground = self.info_color)
            self.node_info_right_chld_val.config(text = child_value(right_child_index), foreground = self.info_color)

#------------------- This will make a text box where users can enter their input on each node -------------------#
    def create_node_user_input(self, node_positions):
        for inputs in self.node_user_input:
            inputs.destroy()

        self.node_user_input.clear()

        for level_nodes in node_positions:
            for node_x, node_y in level_nodes:
                user_entry = ttk.Entry(self.binary_tree_canvas, width = 3, justify = "center")  
                self.binary_tree_canvas.create_window(node_x, node_y, window = user_entry)
                user_entry.bind("<KeyRelease>", lambda event: self.update_off_nodes())
                self.node_user_input.append(user_entry)

#------------------- Gets the inputs in each node -------------------#
    def get_node_entries(self, warning = True):
        values = []

        for index, entry in enumerate(self.node_user_input):
            if self.node_forced_off and index < len(self.node_forced_off) and self.node_forced_off[index]:
                values.append(None)
                continue

            value = entry.get().strip()

            if value == "?":
                values.append(None)
                continue

            if value == "":
                if warning:
                    self.warning_label.config(text = "Missing node value. Please input any\nvalue first or '?' if its an empty node.")
                    self.tree_warning_timer = self.root.after(3000, lambda: self.warning_label.config(text = ""))
                    
                    return None
                values.append("")
                continue

            values.append(value)

        return values
    
#------------------- This will gray out the nodes under a node with a "?" entried by the user -------------------#
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

                    self.node_user_input[index].delete(0, tk.END)
                    self.node_user_input[index].state(["disabled"])

                else: 
                    self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "yellow")
                    self.binary_tree_canvas.itemconfig(self.node_texts[index], text = value)

                    self.node_user_input[index].state(["!disabled"])
        
        return values
    
    def update_off_nodes(self):
        num = len(self.node_user_input)
        forced = [False] * num
        qmarked_node = [False] * num # question marked nodes

        for index, entry in enumerate(self.node_user_input):
            if entry.get().strip() == "?":
                qmarked_node[index] = True

        stack = []
        for index, is_qmarked in enumerate(qmarked_node):
            if is_qmarked:
                for child in (2 * index + 1, 2 * index + 2):
                    if child < num and not forced[child]:
                        forced[child] = True
                        stack.append(child)

        while stack:
            index = stack.pop()
            for child in (2 * index + 1, 2 * index + 2):
                if child < num and not forced[child]:
                    forced[child] = True
                    stack.append(child)

        self.node_forced_off = forced

        # Updating entry nodes based on conditions:
        for index in range(num):
            entry = self.node_user_input[index]

            # if node is "?", grayed but editable for reactivating the nodes
            if qmarked_node[index]:
                entry.state(["!disabled"])
                entry.configure(style = "OffedNode.TEntry")
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "lightgray")
                self.binary_tree_canvas.itemconfig(self.node_texts[index], text = "?")

            # if its a descendant of the "?" node, grayed and disabled
            elif forced[index]:
                entry.delete(0, tk.END)
                entry.state(["disabled"])
                entry.configure(style = "OffedNode.TEntry")
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "lightgray")
                self.binary_tree_canvas.itemconfig(self.node_texts[index], text = "?")

            else:
                entry.state(["!disabled"])
                entry.configure(style = "TEntry")
                value = entry.get().strip()
                self.binary_tree_canvas.itemconfig(self.node_circles[index], fill = "yellow")
                self.binary_tree_canvas.itemconfig(self.node_texts[index], text = "" if value == "" else value)
        
#------------------- Preorder Traversal -------------------#
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
    
#------------------- Inorder Traversal -------------------#
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

#------------------- Postorder Traversal -------------------#
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
    
#------------------- creates an animation when traversing -------------------#
    def node_animation(self, order, step = 0, delay = 300):
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

        self.binary_tree_canvas.itemconfig(self.node_circles[result_index], fill = self.info_color)
        self.binary_tree_canvas.itemconfig(self.node_texts[result_index], fill = "white")
        self.node_highlighter = self.root.after(delay, lambda: self.node_animation(order, step + 1, delay))
        self.traversal_result_label.config(text = " ".join(self.show_value), foreground = self.info_color)

#------------------- Color Resetter -------------------#
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

#------------------- Identify traversal type and display result -------------------#
    def traversals(self, method):
        if self.traversal_warning_timer is not None:
            self.root.after_cancel(self.traversal_warning_timer)
            self.traversal_warning_timer = None

        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None
            self.node_color_reset()
            self.show_value.clear()
            self.traversal_result_label.config(text = "")

        values = self.get_node_entries(warning = False)

        if values is None:
            return
        
        values = self.off_nodes(values, re_highlight = False)

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
            font_color = "violet"

        if self.node_highlighter is not None:
            self.root.after_cancel(self.node_highlighter)
            self.node_highlighter = None

        self.info_color = font_color
        self.current_method = method

        self.traversal_result_label.config(text = "", foreground = self.info_color)
        self.traversal_method_label.config(text = self.current_method, foreground = self.info_color)

        self.node_animation(result)

root = tk.Tk()
app = BinaryTreeApp(root)
root.mainloop()