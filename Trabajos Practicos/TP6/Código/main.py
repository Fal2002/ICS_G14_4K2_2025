import tkinter as tk
from tkinter import ttk, messagebox

from models import GestorActividades, Visitante

# Paleta de colores
COLORES = {
    "muy_claro": "#E8FCCF",  # Fondo principal
    "claro": "#96E072",  # Botones principales
    "medio": "#3DA35D",  # Hover/Destacados
    "oscuro": "#3E8914",  # Textos importantes
    "muy_oscuro": "#134611",  # Textos oscuros
}


class MenuPrincipal:
    """Ventana principal del sistema de gestión de actividades"""

    def __init__(self, root, gestor):
        """
        Inicializa el menú principal.

        Args:
            root: Ventana raíz de Tkinter
            gestor: Instancia de GestorActividades
        """
        self.root = root
        self.root.title("Sistema de Gestión de Actividades")
        self.gestor = gestor

        # Configurar colores de la ventana
        self.root.configure(bg=COLORES["muy_claro"])

        # Frame principal
        main_frame = tk.Frame(root, bg=COLORES["muy_claro"], padx=40, pady=40)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        titulo = tk.Label(
            main_frame,
            text="Sistema de Gestión de Actividades",
            font=("Montserrat", 16, "bold"),
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
        )
        titulo.grid(row=0, column=0, pady=20)

        # Botón de inscripción
        btn_inscripcion = tk.Button(
            main_frame,
            text="Inscribirse a una Actividad",
            command=self.abrir_inscripcion,
            width=30,
            height=2,
            bg=COLORES["claro"],
            fg=COLORES["muy_oscuro"],
            font=("Montserrat", 10, "bold"),
            activebackground=COLORES["medio"],
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
        )
        btn_inscripcion.grid(row=1, column=0, pady=10)

        # Botón de listado
        btn_listado = tk.Button(
            main_frame,
            text="Ver Listado de Actividades",
            command=self.abrir_listado,
            width=30,
            height=2,
            bg=COLORES["claro"],
            fg=COLORES["muy_oscuro"],
            font=("Montserrat", 10, "bold"),
            activebackground=COLORES["medio"],
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
        )
        btn_listado.grid(row=2, column=0, pady=10)

        # Botón de salir
        btn_salir = tk.Button(
            main_frame,
            text="Salir",
            command=root.quit,
            width=30,
            height=2,
            bg=COLORES["oscuro"],
            fg="white",
            font=("Montserrat", 10, "bold"),
            activebackground=COLORES["muy_oscuro"],
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
        )
        btn_salir.grid(row=3, column=0, pady=10)

    def abrir_inscripcion(self):
        """Abre la ventana de inscripción a actividades"""
        ventana_inscripcion = tk.Toplevel(self.root)
        InscripcionApp(ventana_inscripcion, self.gestor)

    def abrir_listado(self):
        """Abre la ventana de listado de actividades"""
        ventana_listado = tk.Toplevel(self.root)
        ListadoApp(ventana_listado, self.gestor)


class InscripcionApp:
    """Ventana de inscripción a actividades"""

    def __init__(self, root, gestor):
        """
        Inicializa la ventana de inscripción.

        Args:
            root: Ventana de Tkinter
            gestor: Instancia de GestorActividades
        """
        self.root = root
        self.root.title("Inscripción a Actividades")
        self.gestor = gestor

        # Configurar colores de la ventana
        self.root.configure(bg=COLORES["muy_claro"])

        # --- Widgets ---
        # Frame principal
        main_frame = tk.Frame(root, padx=20, pady=20, bg=COLORES["muy_claro"])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Actividad
        tk.Label(
            main_frame,
            text="Actividad:",
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
            font=("Montserrat", 10, "bold"),
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.actividad_var = tk.StringVar()
        self.actividad_combo = ttk.Combobox(
            main_frame,
            textvariable=self.actividad_var,
            state="readonly",
            font=("Montserrat", 10),
        )
        self.actividad_combo["values"] = list(self.gestor.actividades.keys())
        self.actividad_combo.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))
        self.actividad_combo.bind("<<ComboboxSelected>>", self.actualizar_horarios)

        # Horario
        tk.Label(
            main_frame,
            text="Horario:",
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
            font=("Montserrat", 10, "bold"),
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.horario_var = tk.StringVar()
        self.horario_combo = ttk.Combobox(
            main_frame,
            textvariable=self.horario_var,
            state="readonly",
            font=("Montserrat", 10),
        )
        self.horario_combo.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))

        # Número de visitantes
        tk.Label(
            main_frame,
            text="Número de visitantes:",
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
            font=("Montserrat", 10, "bold"),
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_visitantes_var = tk.StringVar(value="1")
        self.num_visitantes_spinbox = ttk.Spinbox(
            main_frame,
            from_=1,
            to=100,
            textvariable=self.num_visitantes_var,
            width=10,
            command=self.actualizar_campos_visitantes,
        )
        self.num_visitantes_spinbox.grid(row=2, column=1, sticky=tk.W)
        self.num_visitantes_spinbox.bind(
            "<KeyRelease>", self.actualizar_campos_visitantes
        )

        # Frame con scroll para los visitantes
        self.canvas_frame = tk.Frame(main_frame, bg=COLORES["muy_claro"])
        self.canvas_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )

        self.canvas = tk.Canvas(
            self.canvas_frame,
            height=300,
            bg="white",
            highlightbackground=COLORES["medio"],
            highlightthickness=2,
        )
        scrollbar = tk.Scrollbar(
            self.canvas_frame,
            orient="vertical",
            command=self.canvas.yview,
            bg=COLORES["claro"],
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Lista para almacenar los campos de cada visitante
        self.visitantes_fields = []

        # Crear campos para el primer visitante
        self.actualizar_campos_visitantes()

        # Términos y condiciones
        self.acepta_terminos_var = tk.BooleanVar()
        self.terminos_check = tk.Checkbutton(
            main_frame,
            text="Acepto los términos y condiciones",
            variable=self.acepta_terminos_var,
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
            font=("Montserrat", 9),
            selectcolor=COLORES["claro"],
            activebackground=COLORES["muy_claro"],
            activeforeground=COLORES["oscuro"],
        )
        self.terminos_check.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Botón de inscripción
        self.inscribir_button = tk.Button(
            main_frame,
            text="Inscribir",
            command=self.inscribir,
            bg=COLORES["medio"],
            fg="white",
            font=("Montserrat", 11, "bold"),
            activebackground=COLORES["oscuro"],
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=5,
        )
        self.inscribir_button.grid(row=5, column=1, pady=10)

    def actualizar_horarios(self, event=None):
        """Actualiza los horarios disponibles según la actividad seleccionada"""
        nombre_actividad = self.actividad_var.get()
        if nombre_actividad:
            actividad = self.gestor.obtener_actividad(nombre_actividad)
            horarios_disponibles = [
                h
                for h, c in actividad.horarios.items()
                if actividad.obtener_cantidad_cupos_disponibles_horario(h) > 0
            ]
            self.horario_combo["values"] = horarios_disponibles
            if horarios_disponibles:
                self.horario_combo.set(horarios_disponibles[0])
            else:
                self.horario_combo.set("")
            # Actualizar campos de visitantes para mostrar u ocultar talla según la actividad
            self.actualizar_campos_visitantes()
        else:
            self.horario_combo["values"] = []
            self.horario_combo.set("")

    def actualizar_campos_visitantes(self, event=None):
        """Actualiza dinámicamente los campos de visitantes según la cantidad especificada"""
        try:
            num_visitantes = int(self.num_visitantes_var.get())
            if num_visitantes < 1:
                num_visitantes = 1
                self.num_visitantes_var.set("1")
            elif num_visitantes > 100:
                num_visitantes = 100
                self.num_visitantes_var.set("100")
        except ValueError:
            return

        # Limpiar campos existentes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.visitantes_fields = []

        # Verificar si la actividad requiere talla
        nombre_actividad = self.actividad_var.get()
        requiere_talla = False
        if nombre_actividad:
            actividad = self.gestor.obtener_actividad(nombre_actividad)
            if actividad:
                requiere_talla = actividad.requiere_talla_vestimenta()

        # Crear campos para cada visitante
        for i in range(num_visitantes):
            # Separador
            if i > 0:
                separator = tk.Frame(
                    self.scrollable_frame, height=2, bg=COLORES["claro"]
                )
                separator.grid(
                    row=i * 6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
                )

            tk.Label(
                self.scrollable_frame,
                text=f"Visitante {i+1}:",
                font=("Montserrat", 10, "bold"),
                bg="white",
                fg=COLORES["oscuro"],
            ).grid(row=i * 6 + 1, column=0, columnspan=3, sticky=tk.W, pady=5)

            tk.Label(
                self.scrollable_frame,
                text="Nombre:",
                bg="white",
                fg=COLORES["muy_oscuro"],
                font=("Montserrat", 9),
            ).grid(row=i * 6 + 2, column=0, sticky=tk.W, pady=2, padx=(10, 5))
            nombre_var = tk.StringVar()
            nombre_entry = tk.Entry(
                self.scrollable_frame,
                textvariable=nombre_var,
                width=30,
                font=("Montserrat", 9),
            )
            nombre_entry.grid(
                row=i * 6 + 2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2
            )

            tk.Label(
                self.scrollable_frame,
                text="DNI:",
                bg="white",
                fg=COLORES["muy_oscuro"],
                font=("Montserrat", 9),
            ).grid(row=i * 6 + 3, column=0, sticky=tk.W, pady=2, padx=(10, 5))
            dni_var = tk.StringVar()
            dni_entry = tk.Entry(
                self.scrollable_frame,
                textvariable=dni_var,
                width=30,
                font=("Montserrat", 9),
            )
            dni_entry.grid(
                row=i * 6 + 3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2
            )

            tk.Label(
                self.scrollable_frame,
                text="Edad:",
                bg="white",
                fg=COLORES["muy_oscuro"],
                font=("Montserrat", 9),
            ).grid(row=i * 6 + 4, column=0, sticky=tk.W, pady=2, padx=(10, 5))
            edad_var = tk.StringVar()
            edad_entry = tk.Entry(
                self.scrollable_frame,
                textvariable=edad_var,
                width=30,
                font=("Montserrat", 9),
            )
            edad_entry.grid(
                row=i * 6 + 4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2
            )

            # Solo mostrar campo de talla si la actividad lo requiere
            talla_var = tk.StringVar()
            if requiere_talla:
                talla_label = tk.Label(
                    self.scrollable_frame,
                    text="Talla:",
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                    font=("Montserrat", 9),
                )
                talla_label.grid(
                    row=i * 6 + 5, column=0, sticky=tk.W, pady=2, padx=(10, 5)
                )
                talla_combo = ttk.Combobox(
                    self.scrollable_frame,
                    textvariable=talla_var,
                    state="readonly",
                    width=28,
                    font=("Montserrat", 9),
                )
                talla_combo["values"] = ["XS", "S", "M", "L", "XL"]
                talla_combo.grid(
                    row=i * 6 + 5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2
                )

            self.visitantes_fields.append(
                {
                    "nombre": nombre_var,
                    "dni": dni_var,
                    "edad": edad_var,
                    "talla": talla_var,
                }
            )

    def inscribir(self):
        """Procesa la inscripción de visitantes a la actividad seleccionada"""
        nombre_actividad = self.actividad_var.get()
        horario = self.horario_var.get()
        acepta_terminos = self.acepta_terminos_var.get()

        # Recopilar datos de todos los visitantes
        visitantes = []
        for i, fields in enumerate(self.visitantes_fields):
            nombre = fields["nombre"].get()
            dni = fields["dni"].get()
            edad_str = fields["edad"].get()
            talla = fields["talla"].get()

            try:
                edad = int(edad_str) if edad_str else None
                dni = int(dni) if dni else dni
            except ValueError:
                edad = None

            visitante = Visitante(
                nombre=nombre,
                dni=dni,
                edad=edad,
                talla_vestimenta=talla if talla else None,
            )
            visitantes.append(visitante)

        # Llamar al gestor para registrar la inscripción
        resultado = self.gestor.registrar_inscripcion(
            nombre_actividad=nombre_actividad,
            horario=horario,
            visitantes=visitantes,
            acepta_terminos=acepta_terminos,
        )

        # Mostrar resultado
        if resultado.exitoso:
            messagebox.showinfo("Inscripción Exitosa", resultado.mensaje)
            # Limpiar campos y actualizar horarios
            self.num_visitantes_var.set("1")
            self.actualizar_campos_visitantes()
            self.actualizar_horarios()
        else:
            messagebox.showerror("Error de Inscripción", resultado.mensaje)


class ListadoApp:
    """Ventana de listado de actividades"""

    def __init__(self, root, gestor):
        """
        Inicializa la ventana de listado.

        Args:
            root: Ventana de Tkinter
            gestor: Instancia de GestorActividades
        """
        self.root = root
        self.root.title("Listado de Actividades")
        self.gestor = gestor

        # Configurar tamaño de ventana y color de fondo
        self.root.geometry("900x600")
        self.root.configure(bg=COLORES["muy_claro"])

        # Frame principal
        main_frame = tk.Frame(root, padx=20, pady=20, bg=COLORES["muy_claro"])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid para que se expanda
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        tk.Label(
            main_frame,
            text="Listado de Actividades",
            font=("Montserrat", 14, "bold"),
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
        ).grid(row=0, column=0, pady=10, sticky=tk.W)

        # Frame con scroll para el contenido
        canvas_frame = tk.Frame(main_frame, bg=COLORES["muy_claro"])
        canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        canvas = tk.Canvas(canvas_frame, bg=COLORES["muy_claro"], highlightthickness=0)
        scrollbar = tk.Scrollbar(
            canvas_frame, orient="vertical", command=canvas.yview, bg=COLORES["claro"]
        )
        scrollable_frame = tk.Frame(canvas, bg=COLORES["muy_claro"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostrar las actividades
        row = 0
        for nombre_actividad, actividad in self.gestor.actividades.items():
            # Frame para cada actividad
            actividad_frame = tk.LabelFrame(
                scrollable_frame,
                text=nombre_actividad,
                padx=10,
                pady=10,
                bg="white",
                fg=COLORES["oscuro"],
                font=("Montserrat", 11, "bold"),
                relief=tk.RIDGE,
                bd=2,
            )
            actividad_frame.grid(
                row=row, column=0, sticky=(tk.W, tk.E), pady=10, padx=10
            )

            # Información de la actividad
            info_text = f"Requiere talla: {'Sí' if actividad.requiere_talla_vestimenta() else 'No'}"
            edad_minima = actividad.obtener_edad_minima()
            if edad_minima is not None:
                info_text += f" | Edad mínima: {edad_minima} años"
            tk.Label(
                actividad_frame,
                text=info_text,
                font=("Montserrat", 9, "italic"),
                bg="white",
                fg=COLORES["medio"],
            ).grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))

            # Encabezados de horarios
            tk.Label(
                actividad_frame,
                text="Horario",
                font=("Montserrat", 9, "bold"),
                bg="white",
                fg=COLORES["muy_oscuro"],
            ).grid(row=1, column=0, padx=5, sticky=tk.W)
            tk.Label(
                actividad_frame,
                text="Cupos Totales",
                font=("Montserrat", 9, "bold"),
                bg="white",
                fg=COLORES["muy_oscuro"],
            ).grid(row=1, column=1, padx=5, sticky=tk.W)
            tk.Label(
                actividad_frame,
                text="Ocupados",
                font=("Montserrat", 9, "bold"),
                bg="white",
                fg=COLORES["muy_oscuro"],
            ).grid(row=1, column=2, padx=5, sticky=tk.W)
            tk.Label(
                actividad_frame,
                text="Disponibles",
                font=("Montserrat", 9, "bold"),
                bg="white",
                fg=COLORES["muy_oscuro"],
            ).grid(row=1, column=3, padx=5, sticky=tk.W)

            # Separador
            separator = tk.Frame(actividad_frame, height=2, bg=COLORES["claro"])
            separator.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)

            # Información de cada horario
            horario_row = 3
            for horario, cupos_totales in sorted(actividad.horarios.items()):
                ocupados = len(actividad.inscripciones_por_horario.get(horario, []))
                disponibles = actividad.obtener_cantidad_cupos_disponibles_horario(
                    horario
                )

                tk.Label(
                    actividad_frame,
                    text=f"{horario} hs",
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                ).grid(row=horario_row, column=0, padx=5, sticky=tk.W)
                tk.Label(
                    actividad_frame,
                    text=str(cupos_totales),
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                ).grid(row=horario_row, column=1, padx=5, sticky=tk.W)
                tk.Label(
                    actividad_frame,
                    text=str(ocupados),
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                ).grid(row=horario_row, column=2, padx=5, sticky=tk.W)

                # Color para disponibles
                color = COLORES["medio"] if disponibles > 0 else "#CC0000"
                label_disponibles = tk.Label(
                    actividad_frame,
                    text=str(disponibles),
                    foreground=color,
                    bg="white",
                    font=("Montserrat", 9, "bold"),
                )
                label_disponibles.grid(row=horario_row, column=3, padx=5, sticky=tk.W)

                horario_row += 1

            # Botón para ver visitantes inscritos
            if any(len(v) > 0 for v in actividad.inscripciones_por_horario.values()):
                tk.Button(
                    actividad_frame,
                    text="Ver Visitantes Inscritos",
                    command=lambda act=actividad: self.mostrar_visitantes(act),
                    bg=COLORES["claro"],
                    fg=COLORES["muy_oscuro"],
                    font=("Montserrat", 9, "bold"),
                    activebackground=COLORES["medio"],
                    activeforeground="white",
                    relief=tk.RAISED,
                    bd=2,
                ).grid(row=horario_row, column=0, columnspan=4, pady=(10, 0))

            row += 1

        # Botón cerrar
        tk.Button(
            main_frame,
            text="Cerrar",
            command=root.destroy,
            bg=COLORES["oscuro"],
            fg="white",
            font=("Montserrat", 10, "bold"),
            activebackground=COLORES["muy_oscuro"],
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=5,
        ).grid(row=2, column=0, pady=10)

    def mostrar_visitantes(self, actividad):
        """
        Muestra los visitantes inscritos en una actividad.

        Args:
            actividad: Actividad cuyos visitantes se mostrarán
        """
        ventana_visitantes = tk.Toplevel(self.root)
        ventana_visitantes.title(f"Visitantes Inscritos - {actividad.nombre}")
        ventana_visitantes.geometry("700x500")
        ventana_visitantes.configure(bg=COLORES["muy_claro"])

        # Frame principal
        main_frame = tk.Frame(
            ventana_visitantes, padx=20, pady=20, bg=COLORES["muy_claro"]
        )
        main_frame.pack(fill="both", expand=True)

        # Título
        tk.Label(
            main_frame,
            text=f"Visitantes Inscritos en {actividad.nombre}",
            font=("Montserrat", 12, "bold"),
            bg=COLORES["muy_claro"],
            fg=COLORES["muy_oscuro"],
        ).pack(pady=10)

        # Frame con scroll
        canvas_frame = tk.Frame(main_frame, bg=COLORES["muy_claro"])
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=COLORES["muy_claro"], highlightthickness=0)
        scrollbar = tk.Scrollbar(
            canvas_frame, orient="vertical", command=canvas.yview, bg=COLORES["claro"]
        )
        scrollable_frame = tk.Frame(canvas, bg=COLORES["muy_claro"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostrar visitantes por horario
        row = 0
        for horario, visitantes in sorted(actividad.inscripciones_por_horario.items()):
            if len(visitantes) > 0:
                # Frame para cada horario
                horario_frame = tk.LabelFrame(
                    scrollable_frame,
                    text=f"Horario: {horario} hs ({len(visitantes)} visitante(s))",
                    padx=10,
                    pady=10,
                    bg="white",
                    fg=COLORES["oscuro"],
                    font=("Montserrat", 10, "bold"),
                    relief=tk.RIDGE,
                    bd=2,
                )
                horario_frame.grid(
                    row=row, column=0, sticky=(tk.W, tk.E), pady=10, padx=10
                )

                # Encabezados
                tk.Label(
                    horario_frame,
                    text="Nombre",
                    font=("Montserrat", 9, "bold"),
                    width=20,
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                ).grid(row=0, column=0, padx=5, sticky=tk.W)
                tk.Label(
                    horario_frame,
                    text="DNI",
                    font=("Montserrat", 9, "bold"),
                    width=15,
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                ).grid(row=0, column=1, padx=5, sticky=tk.W)
                tk.Label(
                    horario_frame,
                    text="Edad",
                    font=("Montserrat", 9, "bold"),
                    width=10,
                    bg="white",
                    fg=COLORES["muy_oscuro"],
                ).grid(row=0, column=2, padx=5, sticky=tk.W)
                if actividad.requiere_talla_vestimenta():
                    tk.Label(
                        horario_frame,
                        text="Talla",
                        font=("Montserrat", 9, "bold"),
                        width=10,
                        bg="white",
                        fg=COLORES["muy_oscuro"],
                    ).grid(row=0, column=3, padx=5, sticky=tk.W)

                # Separador
                separator = tk.Frame(horario_frame, height=2, bg=COLORES["claro"])
                separator.grid(
                    row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5
                )

                # Datos de visitantes
                visitante_row = 2
                for visitante in visitantes:
                    tk.Label(
                        horario_frame,
                        text=visitante.nombre,
                        width=20,
                        bg="white",
                        fg=COLORES["muy_oscuro"],
                    ).grid(row=visitante_row, column=0, padx=5, sticky=tk.W)
                    tk.Label(
                        horario_frame,
                        text=visitante.dni,
                        width=15,
                        bg="white",
                        fg=COLORES["muy_oscuro"],
                    ).grid(row=visitante_row, column=1, padx=5, sticky=tk.W)
                    tk.Label(
                        horario_frame,
                        text=str(visitante.edad),
                        width=10,
                        bg="white",
                        fg=COLORES["muy_oscuro"],
                    ).grid(row=visitante_row, column=2, padx=5, sticky=tk.W)
                    if actividad.requiere_talla_vestimenta():
                        tk.Label(
                            horario_frame,
                            text=visitante.talla_vestimenta or "N/A",
                            width=10,
                            bg="white",
                            fg=COLORES["muy_oscuro"],
                        ).grid(row=visitante_row, column=3, padx=5, sticky=tk.W)
                    visitante_row += 1

                row += 1

        # Botón cerrar
        tk.Button(
            main_frame,
            text="Cerrar",
            command=ventana_visitantes.destroy,
            bg=COLORES["oscuro"],
            fg="white",
            font=("Montserrat", 10, "bold"),
            activebackground=COLORES["muy_oscuro"],
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=5,
        ).pack(pady=10)


def main():
    """Función principal que inicia la aplicación"""
    root = tk.Tk()
    gestor = GestorActividades()
    app = MenuPrincipal(root, gestor)
    root.mainloop()


if __name__ == "__main__":
    main()
