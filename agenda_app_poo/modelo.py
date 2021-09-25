import sqlite3
from tkinter import messagebox
from tkinter import ttk
import re


class Crud:
    def __init__(self):
        pass

# Funcion para crear conexion base de datos y cursor
    def crear_tabla(self):
        try:
            con = sqlite3.connect("db_agendaapp.db")
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS datoscontactos (
        id        INTEGER PRIMARY KEY
                        NOT NULL,
        nombre    VARCHAR NOT NULL,
        apellido  VARCHAR NOT NULL,
        numero    VARCHAR NOT NULL,
        direccion VARCHAR NOT NULL,
        email     VARCHAR NOT NULL
    )"""
                        )
            con.commit()
            print("La tabla se creo")
            con.close()
        except:
            print("Fallo")
            con.close()

        # Actualiza  los datos de la BBDD al Treeview
        self.refresh()

    def guardar(self, nm, ln, nb, ad, ml):
        nombre_get = nm
        apellido_get = ln
        numero_get = nb
        direccion_get = ad
        mail_get = ml

        # Condicional si ingresa datos en todos los campos se guarda el contacto avisando con un alerta sino alerta de completar datos
        if len(nombre_get) < 1 or len(apellido_get) < 1 or len(numero_get) < 1:
            messagebox.showerror(
                "Agenda de Contactos",
                "Complete todos los campos obligatorios.",
            )
        else:
            get_mail = ml
            # Validacion para el entry mail que sea un correo electronico
            patron_val_mail = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+.[a-zA-Z]+$"

            if re.match(patron_val_mail, get_mail):
                con = sqlite3.connect("db_agendaapp.db")
                cur = con.cursor()
                datos = (nombre_get, apellido_get,
                         numero_get, direccion_get, mail_get)
                cur.execute(
                    "INSERT INTO datoscontactos (nombre, apellido, numero, direccion, email) VALUES (?, ?, ?, ?, ?)", datos)
                con.commit()
                messagebox.showinfo("Agenda de Contactos",
                                    "El contacto ha sido registrado")

                # Funcion limpiar campos de los entrys
                # self.limpieza_entrys()
                # Actualiza los registros del Treeview
                self.refresh()
            else:
                messagebox.showerror(
                    "Agenda de Contactos",
                    "Error en la validacion del mail. \nIngrese nuevamente el mail.")

    # Funcion para traer los datos de la base de datos y actualizar la vista del Treeview
    def refresh(self):

        # Coneccion a la base de datos creada
        con = sqlite3.connect("db_agendaapp.db")
        cur = con.cursor()
        # Traer los datos de la tabla
        cur.execute("SELECT * FROM datoscontactos")
        # Lista de todos los registros de la tabla
        self.datos_select = cur.fetchall()

    # Funcion para borrar los datos de la base de datos y del Treeview
    def borrar(self, entry_id):
        # Caja de Mensajes preguntado si desea elimar el contacto
        mbox = messagebox.askquestion(
            "Agenda de Contactos",
            "¿Esta seguro de que quiere eliminar definitivamente este contacto?",
        )
        # Condicinal para eliminar el contacto en caso de que toque Si
        if mbox == "yes":
            id_get = entry_id
            con = sqlite3.connect("db_agendaapp.db")
            cur = con.cursor()
            cur.execute(
                f"""DELETE FROM `datoscontactos` WHERE `datoscontactos`.`id` = '{id_get}' """)
            con.commit()
            con.close()

            # Caja de mensaje avisando que se realizo la eliminacion del contacto.
            messagebox.showinfo("Agenda de Contactos",
                                "El contacto ha sido eliminado.")
        else:
            # En caso de que se presione no, se muestra el cartel de que no se elimino el contacto
            messagebox.showinfo("Agenda de Contactos",
                                "El contacto no se elimino.")

    def modificar(self, iid, nm, ln, nb, ad, ml):
        mes_box = messagebox.askquestion(
            "Agenda de contactos", "¿Esta seguro de querer modificar este contacto?"
        )
        if mes_box == "yes":
            nombre_get = nm
            apellido_get = ln
            numero_get = nb
            direccion_get = ad
            mail_get = ml
            id_get = iid

            if len(nombre_get) < 1 or len(apellido_get) < 1 or len(numero_get) < 1:
                messagebox.showerror(
                    "Agenda de Contactos",
                    "Complete todos los campos obligatorios.",
                )
            else:
                get_mail = ml
                # Validacion para el entry mail que sea un correo electronico
                patron_val_mail = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+.[a-zA-Z]+$"

                if re.match(patron_val_mail, get_mail):
                    con = sqlite3.connect("db_agendaapp.db")
                    cur = con.cursor()
                    cur.execute(
                        f"""UPDATE `datoscontactos` SET
                `nombre` = '{nombre_get}', 
                `apellido` = '{apellido_get}',
                `numero` = '{numero_get}' ,
                `direccion` = '{direccion_get}',
                `email` = '{mail_get}' 
                WHERE ID = '{id_get}' """
                    )
                    con.commit()
                    messagebox.showinfo("Agenda de Contactos",
                                        "El contacto se modifico con exito.")
                else:
                    messagebox.showerror("Agenda de Contactos",
                                         "El contacto no pudo ser modificado.")
            self.refresh()

    def buscar_nombre(self, val_buscar):
        val_get = val_buscar
        # Coneccion a la base de datos creada
        con = sqlite3.connect("db_agendaapp.db")
        cur = con.cursor()
        # Traer los datos de la tablaS
        cur.execute(
            f"""SELECT * FROM `datoscontactos` WHERE `datoscontactos`.`nombre` LIKE '{val_get}%' """)
        # Lista de todos los registros de la tabla
        self.busqueda_select = cur.fetchall()

    def buscar_apellido(self, val_buscar):
        val_get = val_buscar
        # Coneccion a la base de datos creada
        con = sqlite3.connect("db_agendaapp.db")
        cur = con.cursor()
        # Traer los datos de la tablaS
        cur.execute(
            f"""SELECT * FROM `datoscontactos` WHERE `datoscontactos`.`apellido` LIKE '{val_get}%' """)
        # Lista de todos los registros de la tabla
        self.busqueda_select = cur.fetchall()

    def buscar_direccion(self, val_buscar):
        val_get = val_buscar
        # Coneccion a la base de datos creada
        con = sqlite3.connect("db_agendaapp.db")
        cur = con.cursor()
        # Traer los datos de la tablaS
        cur.execute(
            f"""SELECT * FROM `datoscontactos` WHERE `datoscontactos`.`direccion` LIKE '{val_get}%' """)
        # Lista de todos los registros de la tabla
        self.busqueda_select = cur.fetchall()

    def buscar_numero(self, val_buscar):
        val_get = val_buscar
        # Coneccion a la base de datos creada
        con = sqlite3.connect("db_agendaapp.db")
        cur = con.cursor()
        # Traer los datos de la tablaS
        cur.execute(
            f"""SELECT * FROM `datoscontactos` WHERE `datoscontactos`.`numero` LIKE '%{val_get}%' """)
        # Lista de todos los registros de la tabla
        self.busqueda_select = cur.fetchall()

    def buscar_mail(self, val_buscar):
        val_get = val_buscar
        # Coneccion a la base de datos creada
        con = sqlite3.connect("db_agendaapp.db")
        cur = con.cursor()
        # Traer los datos de la tablaS
        cur.execute(
            f"""SELECT * FROM `datoscontactos` WHERE `datoscontactos`.`email` LIKE '{val_get}%' """)
        # Lista de todos los registros de la tabla
        self.busqueda_select = cur.fetchall()
