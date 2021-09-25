from tkinter import Label, StringVar
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import ttk
from tkinter import CENTER, NO, Scrollbar, Canvas, YES, BOTH
from modelo import Crud


class VistaApp:
    def __init__(self, window):

        self.myparent = window
        self.myparent.geometry("880x415")
        self.myparent.config(bg="wheat1")

        self.label_title = Label(
            self.myparent, text="Agenda de Contactos", bg="wheat1")
        self.label_title.grid(row=1, column=1)

        # Creacion de Labels indicadores para sus respectivos entrys
        self.label_name = Label(self.myparent, text="Nombre: *", bg="wheat1")
        self.label_lastname = Label(
            self.myparent, text="Apellido: *", bg="wheat1")
        self.label_number = Label(self.myparent, text="Numero: *", bg="wheat1")
        self.label_name.grid(row=2, column=0)
        self.label_lastname.grid(row=3, column=0)
        self.label_number.grid(row=4, column=0)
        self.label_adress = Label(self.myparent, text="Direccion", bg="wheat1")
        self.label_adress.grid(row=5, column=0)
        self.label_mail = Label(self.myparent, text="E-mail *", bg="wheat1")
        self.label_mail.grid(row=6, column=0)

        # Variables de Entrys
        self.name_val = StringVar()
        self.lastname_val = StringVar()
        self.number_val = StringVar()
        self.adress_val = StringVar()
        self.mail_val = StringVar()
        self.id_val = StringVar()
        # Variables de Entry del Buscador
        self.buscador_val = StringVar()

        # Creacion de casilleros para enviar informacion
        self.entry_name = Entry(self.myparent, textvariable=self.name_val)
        self.entry_lastname = Entry(
            self.myparent, textvariable=self.lastname_val)
        self.entry_number = Entry(self.myparent, textvariable=self.number_val)
        self.entry_adress = Entry(self.myparent, textvariable=self.adress_val)
        self.entry_mail = Entry(self.myparent, textvariable=self.mail_val)
        self.entry_id = Entry(self.myparent, textvariable=self.id_val)
        self.entry_name.grid(row=2, column=1)
        self.entry_lastname.grid(row=3, column=1)
        self.entry_number.grid(row=4, column=1)
        self.entry_adress.grid(row=5, column=1)
        self.entry_mail.grid(row=6, column=1)
        self.entry_id.grid_forget()

        # ////   SECCION TREEVIEW    \\\\
        # Creacion del Treeview para visualizar los datos de la tabla.
        self.frame_pantalla = Frame(
            self.myparent, width=10).grid(row=2, column=2)
        self.pantalla = ttk.Treeview(self.myparent)
        # Estilo del encabezado de las columnas del Treeview
        self.estilo = ttk.Style(self.myparent)
        self.estilo.theme_use("clam")

        # Generacion de columnas y configuracion para el treeview
        self.pantalla["columns"] = ("id", "name", "lastname",
                                    "number", "adress", "mail")
        self.pantalla.column("#0", width=0, stretch=NO)
        self.pantalla.column("id", anchor=CENTER, width=30)
        self.pantalla.column("name", anchor=CENTER, width=100)
        self.pantalla.column("lastname", anchor=CENTER, width=100)
        self.pantalla.column("number", anchor=CENTER, width=80)
        self.pantalla.column("adress", anchor=CENTER, width=130)
        self.pantalla.column("mail", anchor=CENTER, width=150)
        # Generacion de encabezados del Treeview
        self.pantalla.heading("#0", text="", anchor=CENTER)
        self.pantalla.heading("id", text="ID", anchor=CENTER)
        self.pantalla.heading("name", text="Nombre", anchor=CENTER)
        self.pantalla.heading("lastname", text="Apellido", anchor=CENTER)
        self.pantalla.heading("number", text="Numero", anchor=CENTER)
        self.pantalla.heading("adress", text="Direccion", anchor=CENTER)
        self.pantalla.heading("mail", text="E-mail", anchor=CENTER)

        # Barra de desplazamiento para el Treeview
        self.barra_des = Scrollbar(self.frame_pantalla,
                                   orient="vertical", command=self.pantalla.yview)
        self.barra_des.grid(row=2, rowspan=8, column=7,
                            sticky="ns")
        self.pantalla.configure(yscrollcommand=self.barra_des.set)
        self.pantalla.grid(row=2, rowspan=8, column=2, padx=5, columnspan=5)
        # ////   FIN SECCION TREEVIEW    \\\\

        # ////   SECCION BOTONES    \\\\
        # Boton para iniciar la funcion de guardar datos del entry en la base de datos.
        self.button_send = Button(
            self.myparent,
            text="Guardar",
            command=lambda: self.para_guardar(
                self.name_val, self.lastname_val, self.number_val, self.adress_val, self.mail_val),
            bg="LightSalmon2",
            width=14,
            padx=3,
            pady=3,
        ).grid(row=8, column=0)

        # Boton para limpiar casilleros
        self.button_clean = Button(
            self.myparent,
            text="Limpiar Casilleros",
            command=self.para_limpiar,
            bg="LightSalmon2",
            width=14,
            padx=3,
            pady=3,
        ).grid(row=8, column=1)

        # Boton para BORRAR el contacto seleccionado
        self.button_clear = Button(
            self.myparent,
            text="Borrar",
            bg="LightSalmon2",
            command=lambda: self.para_borrar(
                self.id_val, self.name_val, self.lastname_val, self.number_val, self.adress_val, self.mail_val),
            width=14,
            padx=3,
            pady=3,
        ).grid(row=9, column=0)

        # Boton para MODIFICAR datos de algun contacto existente
        self.button_update = Button(
            self.myparent,
            text="Modificar",
            bg="LightSalmon2",
            command=lambda: self.para_modificar(
                self.id_val, self.name_val, self.lastname_val, self.number_val, self.adress_val, self.mail_val),
            width=14,
            padx=3,
            pady=3,
        ).grid(row=9, column=1)

        # Indicaodr de campos obligatorios
        self.label_obligatorio = Label(
            self.myparent, text="* Campos de llenado obligatorio", bg="wheat1"
        )
        self.label_obligatorio.grid(row=10, column=0, columnspan=2)

        # ////   SECCION BUSCADOR    \\\\
        lb_buscador = Label(self.myparent, text="Buscador",
                            font=20, bg="LightSalmon2")
        lb_buscador.grid(row=10, padx=10, pady=5, column=3)
        # Casillero de Busqueda
        ent_abuscador = Entry(self.myparent, width=98,
                              textvariable=self.buscador_val)
        ent_abuscador.grid(row=11, column=2, columnspan=4, pady=5)

        # BOTONES DE ACCION DEL BUSCADOR
        bt_name = Button(self.myparent, text="Buscar Nombre",
                         width=25, bg="LightSalmon2", height=2, command=lambda: self.para_buscar_nombre(self.buscador_val))
        bt_name.grid(row=12, column=2, pady=5)
        bt_lname = Button(self.myparent, text="Buscar Apellido",
                          width=25, bg="LightSalmon2", height=2, command=lambda: self.para_buscar_apellido(self.buscador_val))
        bt_lname.grid(row=12, column=3, pady=5)
        bt_number = Button(self.myparent, text="Buscar Numero",
                           width=25, bg="LightSalmon2", height=2, command=lambda: self.para_buscar_numero(self.buscador_val))
        bt_number.grid(row=12, column=4, pady=5)
        bt_mail = Button(self.myparent, text="Buscar E-mail",
                         width=25, bg="LightSalmon2", height=2, command=lambda: self.para_buscar_mail(self.buscador_val))
        bt_mail.grid(row=13, column=2)
        bt_dir = Button(self.myparent, text="Buscar Direccion",
                        width=25, bg="LightSalmon2", height=2, command=lambda: self.para_buscar_direccion(self.buscador_val))
        bt_dir.grid(row=13, column=3)
        bt_clean = Button(self.myparent, text="Ver Lista Completa",
                          width=25, bg="LightSalmon2", height=2, command=self.para_refresh)
        bt_clean.grid(row=13, column=4)
        # ////   FIN SECCION \\\\

        # Llamada al CRUD del modelo
        self.crud = Crud()
        self.crud.crear_tabla()

        # Activa Funcion para Cargar datos al Treeview
        self.para_refresh()
        # Selecciona el dato del Treeview
        self.seleccion = self.pantalla.focus()
        # Toma el Valor del TreeView seleccionado y lo inserta en los entrys

        def seleccionar_contacto(e):
            # Limpia Casillas de los Entrys
            self.para_limpiar()
            # Apunta la seleccion del treeview
            self.seleccionar = self.pantalla.focus()
            # Guarda en Variable el Item del Treeview apuntado
            values = self.pantalla.item(self.seleccionar, "values")
            self.entry_id.insert(0, values[0])
            self.entry_name.insert(0, values[1])
            self.entry_lastname.insert(0, values[2])
            self.entry_number.insert(0, values[3])
            self.entry_adress.insert(0, values[4])
            self.entry_mail.insert(0, values[5])

        self.pantalla.bind("<ButtonRelease-1>", seleccionar_contacto)

    def para_guardar(self, name, lastname, number, adress, mail):
        # Elimina cualquier dato del Treeview para dejarlo limpio
        self.pantalla.delete(*self.pantalla.get_children())
        # Pasa los parametros de valores capturados al modelo
        self.crud.guardar(name.get(), lastname.get(),
                          number.get(), adress.get(), mail.get())

        # Activa Funcion para Cargar datos al Treeview
        self.para_refresh()
        # Activa Funcion para limpiar los campos del entry
        self.para_limpiar()

    def para_limpiar(self):
        self.entry_name.delete(0, "end")
        self.entry_lastname.delete(0, "end")
        self.entry_number.delete(0, "end")
        self.entry_adress.delete(0, "end")
        self.entry_mail.delete(0, "end")
        self.entry_id.delete(0, "end")

    def para_refresh(self):
        # Elimina cualquier dato del Treeview para dejarlo limpio
        self.pantalla.delete(*self.pantalla.get_children())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        i = 0
        for dato in self.crud.datos_select:
            self.pantalla.insert(
                "",
                i,
                text="",
                values=(dato[0], dato[1], dato[2],
                        dato[3], dato[4], dato[5]),
            )
            i += i

    def para_borrar(self, ent_id, name, lastname, number, adress, mail):
        # Envia el valor de ID hacia el modelo para que lo evalue
        self.crud.borrar(ent_id.get())
        # Elimina el contactos desde la vista del Treeview

        seleccion = self.pantalla.focus()
        self.pantalla.item(
            seleccion,
            text="",
            values=(
                name.get(), lastname.get(),
                number.get(), adress.get(), mail.get()
            ),)
        eliminado = self.pantalla.selection()[0]
        self.pantalla.delete(eliminado)
        # Activa Funcion para limpiar los campos del entry
        self.para_limpiar()

    def para_modificar(self, ent_id, name, lastname, number, adress, mail):
        self.crud.modificar(ent_id.get(), name.get(
        ), lastname.get(), number.get(), adress.get(), mail.get())

        # Activa Funcion para limpiar los campos del entry
        self.para_limpiar()
        self.para_refresh()

    # ////  SECCION FUNCIONES PARA EL BUSCADOR \\\\

    def ubicador_datos(self):
        # Funcion para Optimizar el codigo ya que se va a repetir
        # Elimina cualquier dato del Treeview para dejarlo limpio
        self.pantalla.delete(*self.pantalla.get_children())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        i = 0
        for dato in self.crud.busqueda_select:
            self.pantalla.insert(
                "",
                i,
                text="",
                values=(dato[0], dato[1], dato[2],
                        dato[3], dato[4], dato[5]),
            )
            i += i

    def para_buscar_nombre(self, name):
        self.crud.buscar_nombre(name.get())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        self.ubicador_datos()

    def para_buscar_apellido(self, lname):
        self.crud.buscar_apellido(lname.get())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        self.ubicador_datos()

    def para_buscar_direccion(self, adress):
        self.crud.buscar_direccion(adress.get())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        self.ubicador_datos()

    def para_buscar_mail(self, mail):
        self.crud.buscar_mail(mail.get())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        self.ubicador_datos()

    def para_buscar_numero(self, number):
        self.crud.buscar_numero(number.get())
        # Ubica los datos de la BBDD en cada Columna del Treeview
        self.ubicador_datos()
