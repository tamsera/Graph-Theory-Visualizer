import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import random
import math

WIDTH = 800
HEIGHT = 600
MARGIN = 65


class GraphApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Gráfelméleti elemző")
        self.root.geometry("1320x690")
        self.root.minsize(1150, 650)

        self.graph = nx.Graph()
        self.positions = {}
        self.layout_number = 0

        # Fő elrendezés
        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        # BAL OLDAL - CANVAS
        left = ttk.Frame(main)
        left.pack(side="left", anchor="n", padx=(0, 12))

        self.canvas = tk.Canvas(
            left,
            width=WIDTH,
            height=HEIGHT,
            bg="white",
            highlightthickness=1,
            highlightbackground="#aaaaaa"
        )
        self.canvas.pack()

        # JOBB OLDAL
        right = ttk.Frame(main)
        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        ttk.Label(
            right,
            text="Gráf kapcsolatai",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.textbox = tk.Text(
            right,
            height=4,
            wrap="word"
        )
        self.textbox.pack(
            fill="x",
            pady=(5, 10)
        )

        self.textbox.insert(
            "1.0",
            "AB, AC, AE, BC, BD, BE, CE, CD, DE, DF, EF"
        )

        ttk.Button(
            right,
            text="START - Új elrendezés",
            command=self.start
        ).pack(fill="x", pady=(0, 10))

        # Checkboxok
        ttk.Label(
            right,
            text="Gráfelméleti vizsgálatok",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))

        checkbox_frame = ttk.Frame(right)
        checkbox_frame.pack(fill="x")

        self.options = {}

        names = [
            "Euler-kör",
            "Euler-út",
            "Hamilton-kör",
            "Hidak",
            "Artikulációs pontok",
            "Csúcsfokszámok",
            "Feszítőfa",
            "Síkgráf tartományai"
        ]

        for i, name in enumerate(names):
            var = tk.BooleanVar(value=False)
            self.options[name] = var

            ttk.Checkbutton(
                checkbox_frame,
                text=name,
                variable=var,
                command=self.draw
            ).grid(
                row=i // 2,
                column=i % 2,
                sticky="w",
                padx=5,
                pady=4
            )

        # Konzol
        ttk.Label(
            right,
            text="Konzol / Eredmények",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        console_frame = ttk.Frame(right)
        console_frame.pack(fill="both", expand=True)

        self.console = tk.Text(
            console_frame,
            wrap="word",
            bg="#171b24",
            fg="#e6edf3",
            insertbackground="white",
            font=("Consolas", 10),
            state="disabled"
        )
        self.console.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            console_frame,
            orient="vertical",
            command=self.console.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.console.configure(yscrollcommand=scrollbar.set)

        self.console.tag_configure(
            "title", foreground="#73c7ff"
        )
        self.console.tag_configure(
            "success", foreground="#7ee787"
        )
        self.console.tag_configure(
            "warning", foreground="#ffb86c"
        )

        self.write_console(
            "Add meg az éleket, majd nyomd meg a START gombot."
        )

    def write_console(self, text, tag=None):
        self.console.configure(state="normal")
        self.console.insert(tk.END, text + "\n", tag)
        self.console.configure(state="disabled")

    def clear_console(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.configure(state="disabled")

    def read_graph(self):
        text = self.textbox.get("1.0", tk.END)

        edges = [
            x.strip().upper()
            for x in text.replace("\n", ",").split(",")
            if x.strip()
        ]

        graph = nx.Graph()

        for edge in edges:
            if "-" in edge:
                parts = edge.split("-")

                if len(parts) != 2:
                    raise ValueError(f"Hibás él: {edge}")

                a, b = [x.strip() for x in parts]

            elif len(edge) == 2:
                a, b = edge

            else:
                raise ValueError(f"Hibás él: {edge}")

            if not a or not b or a == b:
                raise ValueError(f"Hibás él: {edge}")

            graph.add_edge(a, b)

        return graph

    def start(self):
        try:
            graph = self.read_graph()
        except ValueError as error:
            messagebox.showerror("Hiba", str(error))
            return

        if graph.number_of_nodes() == 0:
            messagebox.showwarning("Hiba", "Nincs megadott él!")
            return

        planar, _ = nx.check_planarity(graph)

        if not planar:
            messagebox.showwarning(
                "Nem síkgráf",
                "A gráf nem rajzolható kereszteződés nélkül!"
            )
            return

        nodes = list(graph.nodes())
        edges = list(graph.edges())

        random.shuffle(nodes)
        random.shuffle(edges)

        temp_graph = nx.Graph()
        temp_graph.add_nodes_from(nodes)
        temp_graph.add_edges_from(edges)

        pos = nx.planar_layout(temp_graph)

        angle = random.uniform(0, 2 * math.pi)
        mirror = random.choice([-1, 1])

        ca = math.cos(angle)
        sa = math.sin(angle)

        transformed = {}

        for node, (x, y) in pos.items():
            x *= mirror
            transformed[node] = (
                x * ca - y * sa,
                x * sa + y * ca
            )

        xs = [p[0] for p in transformed.values()]
        ys = [p[1] for p in transformed.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        dx = max(max_x - min_x, 0.00001)
        dy = max(max_y - min_y, 0.00001)

        scale = min(
            (WIDTH - 2 * MARGIN) / dx,
            (HEIGHT - 2 * MARGIN) / dy
        )

        offset_x = (WIDTH - dx * scale) / 2
        offset_y = (HEIGHT - dy * scale) / 2

        self.positions = {
            node: (
                offset_x + (x - min_x) * scale,
                offset_y + (y - min_y) * scale
            )
            for node, (x, y) in transformed.items()
        }

        self.graph = graph
        self.layout_number += 1
        self.draw()

    def hamilton_cycle(self):
        graph = self.graph
        nodes = list(graph.nodes())

        if not nodes or not nx.is_connected(graph):
            return None

        if len(nodes) > 12:
            return "LIMIT"

        start = nodes[0]

        def search(path, visited):
            if len(path) == len(nodes):
                if graph.has_edge(path[-1], start):
                    return path + [start]
                return None

            for neighbor in graph.neighbors(path[-1]):
                if neighbor not in visited:
                    result = search(
                        path + [neighbor],
                        visited | {neighbor}
                    )
                    if result:
                        return result

            return None

        return search([start], {start})

    def draw(self):
        self.canvas.delete("all")
        self.clear_console()

        if not self.positions:
            self.write_console("Először nyomd meg a START gombot.")
            return

        graph = self.graph
        pos = self.positions

        selected = {
            name
            for name, var in self.options.items()
            if var.get()
        }

        edge_colors = {}
        edge_widths = {}
        node_colors = {}
        degree_labels = {}

        def mark_edge(a, b, color, width=4):
            key = frozenset((a, b))
            edge_colors[key] = color
            edge_widths[key] = width

        self.write_console(
            "GRÁFELMÉLETI ELEMZÉS", "title"
        )
        self.write_console("-" * 42)
        self.write_console(
            f"Csúcsok száma: {graph.number_of_nodes()}"
        )
        self.write_console(
            f"Élek száma: {graph.number_of_edges()}"
        )
        self.write_console(
            f"Elrendezés: {self.layout_number}"
        )
        self.write_console("")

        # Euler-kör
        if "Euler-kör" in selected:
            self.write_console("EULER-KÖR", "title")

            if nx.is_eulerian(graph):
                circuit = list(nx.eulerian_circuit(graph))
                vertices = (
                    [circuit[0][0]]
                    + [b for a, b in circuit]
                )

                for a, b in circuit:
                    mark_edge(a, b, "#2563eb", 4)

                self.write_console("Létezik.", "success")
                self.write_console(
                    "Útvonal:\n" + " → ".join(vertices)
                )
                self.write_console(
                    f"Indulás: {vertices[0]}"
                )
                self.write_console(
                    f"Érkezés: {vertices[-1]}"
                )
            else:
                self.write_console("Nem létezik.", "warning")

            self.write_console("")

        # Euler-út
        if "Euler-út" in selected:
            self.write_console("EULER-ÚT", "title")

            if nx.has_eulerian_path(graph):
                path = list(nx.eulerian_path(graph))
                vertices = (
                    [path[0][0]]
                    + [b for a, b in path]
                )

                for a, b in path:
                    mark_edge(a, b, "#f59e0b", 4)

                self.write_console("Létezik.", "success")
                self.write_console(
                    "Útvonal:\n" + " → ".join(vertices)
                )
                self.write_console(
                    f"Indulás: {vertices[0]}"
                )
                self.write_console(
                    f"Érkezés: {vertices[-1]}"
                )
                self.write_console(
                    f"Bejárt élek: {len(path)}"
                )
            else:
                self.write_console("Nem létezik.", "warning")

            self.write_console("")

        # Hamilton-kör
        if "Hamilton-kör" in selected:
            self.write_console("HAMILTON-KÖR", "title")

            cycle = self.hamilton_cycle()

            if cycle == "LIMIT":
                self.write_console(
                    "12 csúcs felett a keresés kihagyva.",
                    "warning"
                )
            elif cycle:
                for a, b in zip(cycle, cycle[1:]):
                    mark_edge(a, b, "#a855f7", 5)

                self.write_console("Létezik.", "success")
                self.write_console(
                    "Útvonal:\n" + " → ".join(cycle)
                )
                self.write_console(
                    f"Érintett csúcsok: {len(cycle) - 1}"
                )
            else:
                self.write_console("Nem létezik.", "warning")

            self.write_console("")

        # Hidak
        if "Hidak" in selected:
            self.write_console("HIDAK", "title")
            bridges = list(nx.bridges(graph))

            if bridges:
                for a, b in bridges:
                    mark_edge(a, b, "#ef4444", 5)

                self.write_console(
                    "Hidak: " + ", ".join(
                        f"{a}-{b}" for a, b in bridges
                    ),
                    "success"
                )
            else:
                self.write_console("Nincsenek hidak.", "warning")

            self.write_console("")

        # Artikulációs pontok
        if "Artikulációs pontok" in selected:
            self.write_console(
                "ARTIKULÁCIÓS PONTOK", "title"
            )
            points = list(nx.articulation_points(graph))

            if points:
                for node in points:
                    node_colors[node] = "#fb923c"

                self.write_console(
                    "Csúcsok: " + ", ".join(points),
                    "success"
                )
            else:
                self.write_console(
                    "Nincsenek artikulációs pontok.",
                    "warning"
                )

            self.write_console("")

        # Csúcsfokszámok
        if "Csúcsfokszámok" in selected:
            self.write_console("CSÚCSFOKSZÁMOK", "title")

            for node, degree in graph.degree():
                degree_labels[node] = degree
                self.write_console(
                    f"{node}: {degree}"
                )

            self.write_console("")

        # Feszítőfa
        if "Feszítőfa" in selected:
            self.write_console("FESZÍTŐFA", "title")

            if nx.is_connected(graph):
                tree = nx.minimum_spanning_tree(graph)

                for a, b in tree.edges():
                    mark_edge(a, b, "#16a34a", 4)

                self.write_console("Létezik.", "success")
                self.write_console(
                    "Kiválasztott élek:"
                )

                for a, b in tree.edges():
                    self.write_console(f"{a} - {b}")

            else:
                self.write_console(
                    "Nem létezik, a gráf nem összefüggő.",
                    "warning"
                )

            self.write_console("")

        # Síkgráf tartományai
        if "Síkgráf tartományai" in selected:
            self.write_console(
                "SÍKGRÁF TARTOMÁNYAI", "title"
            )

            n = graph.number_of_nodes()
            m = graph.number_of_edges()
            c = nx.number_connected_components(graph)

            faces = m - n + c + 1

            self.write_console(
                f"Tartományok száma: {faces}",
                "success"
            )
            self.write_console(
                "A külső tartomány is beleszámít."
            )
            self.write_console("")

        if not selected:
            self.write_console(
                "Pipálj be egy vagy több vizsgálatot!"
            )

        # Háttérrács
        for x in range(0, WIDTH, 50):
            self.canvas.create_line(
                x, 0, x, HEIGHT,
                fill="#eeeeee"
            )

        for y in range(0, HEIGHT, 50):
            self.canvas.create_line(
                0, y, WIDTH, y,
                fill="#eeeeee"
            )

        # Élek
        for a, b in graph.edges():
            x1, y1 = pos[a]
            x2, y2 = pos[b]

            key = frozenset((a, b))

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=edge_colors.get(key, "#333333"),
                width=edge_widths.get(key, 2)
            )

        # Csúcsok
        for node, (x, y) in pos.items():
            r = 19

            self.canvas.create_oval(
                x-r, y-r,
                x+r, y+r,
                fill=node_colors.get(node, "#8ecaff"),
                outline="black",
                width=2
            )

            self.canvas.create_text(
                x, y,
                text=node,
                font=("Arial", 12, "bold")
            )

            if node in degree_labels:
                self.canvas.create_text(
                    x + 27,
                    y - 23,
                    text=str(degree_labels[node]),
                    fill="red",
                    font=("Arial", 11, "bold")
                )


root = tk.Tk()
app = GraphApp(root)
root.mainloop()