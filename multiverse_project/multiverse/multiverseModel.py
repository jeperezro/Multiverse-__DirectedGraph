import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import math
import time

from multiverse_project.data_structures.dictionary import Dictionary
from multiverse_project.data_structures.dynamicArray import Dynamic_Array
from multiverse_project.multiverse.multiverse import Multiverse
from multiverse_project.multiverse.zn_verse import Zn_verse

class Multiverse_Model:
    def __init__(self):
        """Setup"""
        self.root = ttk.Window(themename="darkly")
        self.root.title("THE ZN-VERSE")
        
        self.canvas = ttk.Canvas(self.root, bg="black", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        """Procedure to align window to screen's center"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 1050
        window_height = 850

        _x = (screen_width - window_width) // 2
        _y = (screen_height - window_height - 70) // 2

        self.root.geometry(f"{window_width}x{window_height}+{_x}+{_y}")
        
        """Data and Data Structures required"""
        self.multiverse = Multiverse()
        self.universe_objects = Dictionary()
        self.orbits = Dictionary()
        self.labels = Dictionary()
        self.base_radii = Dictionary()
        self.base_periods = Dictionary()
        self.start_times = Dictionary()
        self.scale_factor = 1.0

        """Clock"""
        self.start_time = time.time()
        
        """Sun of the Multiverse Model"""
        self.mod_uno = self.canvas.create_oval(390, 290, 410, 310, fill="white", outline="white")
        
        """Canvas Events"""
        self.canvas.bind("<ButtonPress-1>", self.start_pan) # To Pan
        self.canvas.bind("<B1-Motion>", self.pan)

        self.canvas.bind("<MouseWheel>", self.zoom) # To Zoom
        
        """UI"""
        # To find connections between universes
        self.universe_connection_finder_frame = ttk.Frame(self.root)
        self.universe_connection_finder_frame.pack(side=tk.LEFT, fill=tk.Y, padx=50)
        ttk.Label(self.universe_connection_finder_frame, text="Universe connections:", font=("Courier New", 16)).pack()
        ttk.Label(self.universe_connection_finder_frame, text="Insert universe to find connections:").pack()
        
        self.connection_entry_frame = ttk.Frame(self.universe_connection_finder_frame)
        self.connection_entry_frame.pack()

        ttk.Label(self.connection_entry_frame).pack(side="left", padx=10)
        ttk.Label(self.connection_entry_frame, text="[").pack(side="left")
        self.universe_a_entry = ttk.Entry(self.connection_entry_frame)
        self.universe_a_entry.pack(side="left", pady=4)
        ttk.Label(self.connection_entry_frame, text="]").pack(side="left")
        ttk.Label(self.connection_entry_frame, text="ℤ").pack(side="left")
        self.universe_zn_entry = ttk.Entry(self.connection_entry_frame)
        self.universe_zn_entry.pack(side="left", pady=4)
        ttk.Label(self.connection_entry_frame).pack(side="left", padx=10)
        self.find_connection_btn = ttk.Button(self.universe_connection_finder_frame, text="Find connections", command=self.get_universe_on_entry)
        self.find_connection_btn.pack(pady=6)
        self.reset_connection_btn = ttk.Button(self.universe_connection_finder_frame, text="Reset connections", command=self.reset_connections)
        self.reset_connection_btn.pack(pady=6)
        
        
        # To manage the multiverse
        self.multiverse_manager_frame = ttk.Frame(self.root)
        self.multiverse_manager_frame.pack(side=tk.LEFT, fill=tk.Y, padx=50)
        
        ttk.Label(self.multiverse_manager_frame, text="Multiverse Management:", font=("Courier New", 16)).pack()
        
        self.orbit_frame = ttk.Frame(self.multiverse_manager_frame)
        self.orbit_frame.pack()
        self.orbit_label = ttk.Label(self.orbit_frame, text="Insert value for universe's orbit (modulo) -->")
        self.orbit_label.pack(side="left")
        self.orbit_entry = ttk.Entry(self.orbit_frame)
        self.orbit_entry.pack(side="right")
        
        self.universe_frame = ttk.Frame(self.multiverse_manager_frame)
        self.universe_frame.pack()
        self.universe_label = ttk.Label(self.universe_frame, text="Insert value for universe's (equivalence class)")
        self.universe_label.pack(side="left")
        self.universe_entry = ttk.Entry(self.universe_frame)
        self.universe_entry.pack(side="right")
        
        self.add_universe_btn = ttk.Button(self.multiverse_manager_frame, text="Add Universe", command=self.add_universe)
        self.add_universe_btn.pack(pady=6)
        self.remove_planet_btn = ttk.Button(self.multiverse_manager_frame, text="Remove Universe", command=self.remove_universe)
        self.remove_planet_btn.pack(pady=3)

        self.remove_orbit_btn = ttk.Button(self.multiverse_manager_frame, text="Remove Orbit", command=self.remove_orbit)
        self.remove_orbit_btn.pack(pady=6)
        
        self.last_update_time = time.time()

        self.initialize_universes()
        self.update_universes()

        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.bind("<Escape>", lambda event: self.on_close())

        self.selected_universes = Dynamic_Array()  # Track selected universes
        self.original_colors = {}  # Store original colors of universes


    def initialize_universes(self):
        """Draws all universes stored in My_Multiverse at startup."""
        
        for universe in self.multiverse.graph.get_vertices():  
            self.draw_universe(universe.a, universe.n)  # Just draw, don't re-add

    def find_universe_connections(self, universe):
        self.multiverse._create_connections()
        # Get all related universes
        related_universes = self.multiverse.get_related_universes(universe)
        print(related_universes)

        # Ensure the universe exists in the canvas
        n, a = universe.n, universe.a
        if (n in self.universe_objects) and (a in self.universe_objects[n]):
            # Store the original color
            self.original_colors[(n, a)] = self.canvas.itemcget(self.universe_objects[n][a], "fill")
            # Highlight selected universe in dark turquoise
            self.canvas.itemconfig(self.universe_objects[n][a], fill="dark turquoise")
            self.selected_universes.append(Zn_verse(a, n))
        else:
            print(f"Warning: Universe {universe} not found in universe_objects.")

        # Highlight related universes in red
        for related_universe in related_universes:
            rn, ra = related_universe.n, related_universe.a
            if (rn in self.universe_objects) and (ra in self.universe_objects[rn]):
                # Store the original color
                self.original_colors[(rn, ra)] = self.canvas.itemcget(self.universe_objects[rn][ra], "fill")
                # Change to cyan
                self.canvas.itemconfig(self.universe_objects[rn][ra], fill="red")
                self.selected_universes.append(Zn_verse(ra, rn))
            else:
                print(f"Warning: Related universe {related_universe} not found in universe_objects.")

        # Get and display connections
        the_message = self.multiverse.graph.display_vertex_connections(universe)
        messagebox.showinfo(title=f"{repr(universe)} connections:", message=the_message)


    def reset_connections(self):
        # Reset previously selected universes to their original colors
        print(self.selected_universes)
        for universe in self.selected_universes:
            self.canvas.itemconfig(self.universe_objects[universe.n][universe.a], 
                                   fill=self.original_colors[(universe.n, universe.a)])

        # Clear selection tracking
        self.selected_universes.clear()
        self.original_colors.clear()

    def get_universe_on_entry(self):
        try:
            a = int(self.universe_a_entry.get())
            n = int(self.universe_zn_entry.get())
            universe = Zn_verse(a, n)

            if universe not in self.multiverse.graph.get_vertices():
                messagebox.showerror(title="Error", message=f"Universe [{a}]ℤ{n} does not exist in Multiverse.")
                return

            # Get all related universes
            self.find_universe_connections(universe)

        except ValueError:
            messagebox.showerror(title="Value Error", message="Please enter valid integer values for a and n.")


    def add_universe(self):
        try:
            n = int(self.orbit_entry.get())
            a = int(self.universe_entry.get())

            if not (0 <= a < n and n > 1):
                messagebox.showerror(
                    title="Entry Error", 
                    message="Value for orbit should be greater than 1.\nValue for planet should range from 0 to n-1."
                )
                return

            universe = Zn_verse(a, n)

            # Explicit duplicate check using custom list iteration
            is_duplicate = False
            for existing_universe in self.multiverse.graph.get_vertices():
                if existing_universe == universe:
                    is_duplicate = True
                    break

            if is_duplicate:
                messagebox.showerror(
                    title="Entry Error", 
                    message=f"Universe {repr(universe)} already exists."
                )
                return  

            # Add the universe to My_Multiverse
            self.multiverse.add_universe(a, n)

            # Update connections for ALL universes
            self.multiverse._create_connections()
            
            # Draw the universe
            self.draw_universe(a, n)


        except ValueError:
            messagebox.showerror(title="Value Error", message="Inserted value type is not allowed.\nAn integer is expected.")

    def remove_universe(self):
        try:
            n = int(self.orbit_entry.get())
            a = int(self.universe_entry.get())
            universe = Zn_verse(a, n)

            # Ensure the universe exists
            if universe in self.multiverse.graph.get_vertices():
                if n in self.universe_objects and a in self.universe_objects[n]:
                    self.canvas.delete(self.universe_objects[n].pop(a))

                if n in self.labels and a in self.labels[n]:
                    self.canvas.delete(self.labels[n].pop(a))

            if universe in self.selected_universes:
                self.selected_universes.remove(universe)

                # Remove the universe from My_Multiverse
                self.multiverse.remove_universe(a, n)

                # Carefully remove edges, preventing duplicates
                vertices = self.multiverse.graph.get_vertices()
                for existing_universe in vertices:
                    # Create a new filtered list of neighbors
                    new_neighbors = Dynamic_Array()
                    for neighbor in self.multiverse.graph.graph[existing_universe]:
                        if neighbor != universe:
                            new_neighbors.append(neighbor)
                    
                    # Update the graph's adjacency list
                    self.multiverse.graph.graph[existing_universe] = new_neighbors

                # Recreate connections to ensure clean state
                self.multiverse._create_connections()

            else:
                messagebox.showerror(title="Universe Not Found", message="The specified universe does not exist.")

        except ValueError:
            messagebox.showerror(title="Value Error", message="Inserted value is not allowed.\nAn integer is expected.")

    def draw_universe(self, a, n):
        """Draws a universe on the canvas without modifying My_Multiverse."""
        if n not in self.base_radii:
            self.base_radii[n] = 60 * n
            self.base_periods[n] = max(1.0, n*5)
            self.orbits[n] = self.canvas.create_oval(-self.base_radii[n],
                                                    -self.base_radii[n],
                                                    self.base_radii[n],
                                                    self.base_radii[n],
                                                    outline="gray25", dash=(5, 2))
            self.universe_objects[n] = Dictionary()
            self.labels[n] = Dictionary()
            self.start_times[n] = Dictionary()

        color = ["LightSteelBlue1", "light goldenrod", "seashell2", "pale goldenrod", "NavajoWhite2"][n % 5]
        universe = {"size": 7, "color": color}

        if n % 2 == 1:
            initial_angle = (a * 2 * math.pi) / n  
            self.start_times[n][a] = self.start_time - (initial_angle * self.base_periods[n]) / (2 * math.pi)
        else:
            initial_angle = math.pi / n  
            self.start_times[n][a] = self.start_time - (initial_angle * self.base_periods[n])

        coord_x = 500 + self.base_radii[n] * math.cos(initial_angle)
        coord_y = 300 + self.base_radii[n] * math.sin(initial_angle)
        
        universe_obj = self.canvas.create_oval(coord_x - 10, coord_y - 10, coord_x + 20, coord_y + 20, fill=universe["color"])
        self.universe_objects[n][a] = universe_obj

        label = self.canvas.create_text(coord_x + 10, coord_y - 10, text=f"[{a}]ℤ{n}", fill="white", font=("Arial", 9))
        self.labels[n][a] = label

    def remove_orbit(self):
        try:
            n = int(self.orbit_entry.get())
            vertices_to_remove = [v for v in self.multiverse.graph.get_vertices() if v.n == n]

            for v in vertices_to_remove:
                a = v.a
                self.canvas.delete(self.universe_objects[n].pop(a))
                self.canvas.delete(self.labels[n].pop(a))
                self.multiverse.remove_universe(a, n)

            self.canvas.delete(self.orbits.pop(n))
            self.base_radii.pop(n)
            self.base_periods.pop(n)
            self.universe_objects.pop(n)
            self.labels.pop(n)
        except ValueError:
            messagebox.showerror(title="Value Error", message="Inserted value is not allowed.\nAn integer is expected.")

        except KeyError:
            messagebox.showerror(title="Key Error", message=f"There is no orbit ℤ{n} stored in the multiverse.")

    def update_universes(self):
        current_time = time.time()
        self.last_update_time = current_time

        for n in self.base_radii:
            scaled_radius = self.scale_factor * self.base_radii[n]

            for a in self.start_times.get(n, {}):
                elapsed_time = current_time - self.start_times[n][a]
                angle = (2 * math.pi * elapsed_time) / self.base_periods[n] + (a * 2 * math.pi / n)

                x = 400 + scaled_radius * math.cos(angle)
                y = 300 + scaled_radius * math.sin(angle)
                size = self.scale_factor * 7

                if n in self.universe_objects and a in self.universe_objects[n]:
                    self.canvas.coords(self.universe_objects[n][a], x - size, y - size, x + size, y + size)

                if n in self.labels and a in self.labels[n]:
                    self.canvas.coords(self.labels[n][a], x + 10, y - 10)

                if n in self.orbits:
                    self.canvas.coords(self.orbits[n], 400 - scaled_radius, 300 - scaled_radius, 
                                    400 + scaled_radius, 300 + scaled_radius)

        self.root.after(30, self.update_universes)
        
    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)
        
    def pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale_factor *= factor

    def on_close(self):
        result = messagebox.askokcancel('Confirm', 'Ready to go?\nUnsaved changes will be deleted.')
        if result:
            self.root.destroy()

    def run(self):
        self.root.mainloop()
