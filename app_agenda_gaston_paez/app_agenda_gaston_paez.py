from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
import mysql.connector
from tkinter import ttk
import sys
import re

# SECCION MANEJO DE BASE DE DATOS
mysql_agendaapp = mysql.connector.connect(host="localhost", user="root", passwd="")
bdda_cursor = mysql_agendaapp.cursor()

try:
    # CREACION DE BASE DE DATOS
    bdda_cursor.execute("CREATE DATABASE if not exists agendaapp")
    # CREACION DE TABLA
    bdda_cursor.execute(
        "CREATE TABLE if not exists agendaapp.datoscontactos (`id` INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT , `nombre` VARCHAR(18) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `apellido` VARCHAR(25) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `numero` VARCHAR(15) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `direccion` VARCHAR(60) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `email` VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL )"
    )
except:
    print("Error al crear base de datos")

# -----SECCION TKINTER-----
root = Tk()
root.config(bg="wheat1")
root.title("Agenda de Contactos")
root.geometry("880x280")


label_title = Label(root, text="Agenda de Contactos", bg="wheat1")
label_title.grid(row=1, column=1)
# Creacion de Labels indicadores para sus respectivos entrys
label_name = Label(root, text="Nombre: *", bg="wheat1")
label_lastname = Label(root, text="Apellido: *", bg="wheat1")
label_number = Label(root, text="Numero: *", bg="wheat1")
label_name.grid(row=2, column=0)
label_lastname.grid(row=3, column=0)
label_number.grid(row=4, column=0)
label_adress = Label(root, text="Direccion", bg="wheat1")
label_adress.grid(row=5, column=0)
label_mail = Label(root, text="E-mail *", bg="wheat1")
label_mail.grid(row=6, column=0)

# Creacion de casilleros para enviar informacion
entry_name = Entry(root)
entry_lastname = Entry(root)
entry_number = Entry(root)
entry_name.grid(row=2, column=1)
entry_lastname.grid(row=3, column=1)
entry_number.grid(row=4, column=1)
entry_adress = Entry(root)
entry_adress.grid(row=5, column=1)
entry_mail = Entry(root)
entry_mail.grid(row=6, column=1)
entry_id = Entry(root)
entry_id.grid_forget()


# Creacion del Treeview para visualizar los datos de la tabla.
frame_pantalla = Frame(root, width=10).grid(row=2, column=2)
pantalla = ttk.Treeview(root)
# Estilo del encabezado de las columnas del Treeview
estilo = ttk.Style(root)
estilo.theme_use("clam")

# Generacion de columnas y configuracion para el treeview
pantalla["columns"] = ("id", "name", "lastname", "number", "adress", "mail")
pantalla.column("#0", width=0, stretch=NO)
pantalla.column("id", anchor=CENTER, width=30)
pantalla.column("name", anchor=CENTER, width=100)
pantalla.column("lastname", anchor=CENTER, width=100)
pantalla.column("number", anchor=CENTER, width=80)
pantalla.column("adress", anchor=CENTER, width=130)
pantalla.column("mail", anchor=CENTER, width=150)
# Generacion de encabezados del Treeview
pantalla.heading("#0", text="", anchor=CENTER)
pantalla.heading("id", text="ID", anchor=CENTER)
pantalla.heading("name", text="Nombre", anchor=CENTER)
pantalla.heading("lastname", text="Apellido", anchor=CENTER)
pantalla.heading("number", text="Numero", anchor=CENTER)
pantalla.heading("adress", text="Direccion", anchor=CENTER)
pantalla.heading("mail", text="E-mail", anchor=CENTER)

# Barra de desplazamiento para el Treeview
barra_des = Scrollbar(frame_pantalla, orient="vertical", command=pantalla.yview)
barra_des.grid(row=2, rowspan=6, column=4, sticky="ns")
pantalla.configure(yscrollcommand=barra_des.set)
pantalla.grid(row=2, rowspan=6, column=3)

# Funcion para limpiar los entrys
def limpieza_entrys():
    entry_name.delete(0, "end")
    entry_lastname.delete(0, "end")
    entry_number.delete(0, "end")
    entry_adress.delete(0, "end")
    entry_mail.delete(0, "end")
    entry_id.delete(0, "end")


# Funcion para traer los datos de la base de datos y actualizar la vista del Treeview
def refresh():
    # Elimina cualquier dato del Treeview para dejarlo limpio
    pantalla.delete(*pantalla.get_children())
    # Coneccion a la base de datos creada
    connect = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="agendaapp"
    )
    conn = connect.cursor()
    # Traer los datos de la tabla
    conn.execute("SELECT * FROM datoscontactos")
    # Bucle para que tome los datos de la tabla y los asigne por valores a los encabezados del Treeview
    i = 0
    for dato in conn:
        pantalla.insert(
            "",
            i,
            text="",
            values=(dato[0], dato[1], dato[2], dato[3], dato[4], dato[5]),
        )
        i += i


refresh()
# Funcion para enviar los datos igresados en el entry a la base de datos
def guardar():
    nombre_get = entry_name.get()
    apellido_get = entry_lastname.get()
    numero_get = entry_number.get()
    direccion_get = entry_adress.get()
    mail_get = entry_mail.get()
    # Condicional si ingresa datos en todos los campos se guarda el contacto avisando con un alerta sino alerta de completar datos
    if len(nombre_get) < 1 or len(apellido_get) < 1 or len(numero_get) < 1:
        messagebox.showerror(
            "Agenda de Contactos",
            "Complete todos los campos obligatorios.",
        )
    else:
        get_mail = entry_mail.get()
        # Validacion para el entry mail que sea un correo electronico
        patron_val_mail = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+.[a-zA-Z]+$"

        if re.match(patron_val_mail, get_mail):
            base_agenda = mysql.connector.connect(
                host="localhost", user="root", passwd="", database="agendaapp"
            )

            sql_insertar = "INSERT INTO `datoscontactos` (`nombre`, `apellido`, `numero`, `direccion`, `email`) VALUES (%s, %s, %s, %s, %s)"
            datos = (nombre_get, apellido_get, numero_get, direccion_get, mail_get)
            agenda_cursor = base_agenda.cursor()
            agenda_cursor.execute(sql_insertar, datos)
            base_agenda.commit()
            messagebox.showinfo("Agenda de Contactos", "El contacto ha sido registrado")

            # Funcion limpiar campos de los entrys
            limpieza_entrys()
            # Actualiza los registros del Treeview
            refresh()
        else:
            messagebox.showerror(
                "Agenda de Contactos",
                "Error en la validacion del mail. \n Ingrese el mail nuevamente correcamente",
            )


def borrar():
    # Caja de Mensajes preguntado si desea elimar el contacto
    mbox = messagebox.askquestion(
        "Agenda de Contactos",
        "¿Esta seguro de que quiere eliminar definitivamente este contacto?",
    )
    # Condicinal para eliminar el contacto en caso de que toque Si
    if mbox == "yes":
        nombre_get = entry_name.get()
        apellido_get = entry_lastname.get()
        numero_get = entry_number.get()
        direccion_get = entry_adress.get()
        mail_get = entry_mail.get()
        id_get = entry_id.get()

        seleccion = pantalla.focus()
        pantalla.item(
            seleccion,
            text="",
            values=(
                id_get,
                nombre_get,
                apellido_get,
                numero_get,
                direccion_get,
                mail_get,
            ),
        )
        base_agenda = mysql.connector.connect(
            host="localhost", user="root", passwd="", database="agendaapp"
        )
        agenda_cursor = base_agenda.cursor()
        agenda_cursor.execute(
            f"""DELETE FROM `datoscontactos` WHERE `datoscontactos`.`id` = '{id_get}' """
        )
        base_agenda.commit()
        base_agenda.close()
        # Elimina el contactos desde la vista del Treeview
        eliminado = pantalla.selection()[0]
        pantalla.delete(eliminado)
        # Caja de mensaje avisando que se realizo la eliminacion del contacto.
        messagebox.showinfo("Agenda de Contactos", "El contacto ha sido eliminado.")
    else:
        # En caso de que se presione no, se muestra el cartel de que no se elimino el contacto
        messagebox.showinfo("Agenda de Contactos", "El contacto no se elimino.")


def modificar():
    mes_box = messagebox.askquestion(
        "Agenda de contactos", "¿Esta seguro de querer modificar este contacto?"
    )
    if mes_box == "yes":
        nombre_get = entry_name.get()
        apellido_get = entry_lastname.get()
        numero_get = entry_number.get()
        direccion_get = entry_adress.get()
        mail_get = entry_mail.get()
        id_get = entry_id.get()
        # Selecciona el numero de registro
        seleccion = pantalla.focus()
        pantalla.item(
            seleccion,
            text="",
            values=(
                id_get,
                nombre_get,
                apellido_get,
                numero_get,
                direccion_get,
                mail_get,
            ),
        )
        base_agenda = mysql.connector.connect(
            host="localhost", user="root", passwd="", database="agendaapp"
        )
        agenda_cursor = base_agenda.cursor()
        agenda_cursor.execute(
            f"""UPDATE `datoscontactos` SET
            `nombre` = '{nombre_get}', 
            `apellido` = '{apellido_get}',
            `numero` = '{numero_get}' ,
            `direccion` = '{direccion_get}',
            `email` = '{mail_get}' 
            WHERE ID = '{id_get}' """
        )
        base_agenda.commit()
        base_agenda.close()
        messagebox.showinfo("Agenda de Contactos", "El contacto se modifico con exito.")
        refresh()
    else:
        messagebox.showinfo("Agenda de Contactos", "El contacto no ha sido modificado.")


def seleccionar_contacto(e):
    limpieza_entrys()

    seleccionar = pantalla.focus()
    values = pantalla.item(seleccionar, "values")
    entry_id.insert(0, values[0])
    entry_name.insert(0, values[1])
    entry_lastname.insert(0, values[2])
    entry_number.insert(0, values[3])
    entry_adress.insert(0, values[4])
    entry_mail.insert(0, values[5])


# SECCION FRAMES
frame_botonera = Frame(root, bg="wheat1", pady=15)
frame_botonera.grid(row=7, columnspan=2)

# Frame para hacer margen a los botones
frame_vertical1 = Frame(frame_botonera, width=5).grid(row=0, rowspan=2, column=0)
frame_vertical2 = Frame(frame_botonera, width=5).grid(row=0, rowspan=2, column=2)
frame_space = Frame(frame_botonera, height=5).grid(row=1)

# Boton para iniciar la funcion de guardar datos del entry en la base de datos.
button_send = Button(
    frame_botonera,
    text="Guardar",
    command=guardar,
    bg="LightSalmon2",
    width=14,
    padx=3,
    pady=3,
).grid(row=0, column=1)

# Boton para limpiar casilleros
button_clean = Button(
    frame_botonera,
    text="Limpiar Casilleros",
    command=limpieza_entrys,
    bg="LightSalmon2",
    width=14,
    padx=3,
    pady=3,
).grid(row=0, column=3)

# Boton para BORRAR el contacto seleccionado
button_clear = Button(
    frame_botonera,
    text="Borrar",
    bg="LightSalmon2",
    command=borrar,
    width=14,
    padx=3,
    pady=3,
).grid(row=2, column=1)

# Boton para MODIFICAR datos de algun contacto existente
button_update = Button(
    frame_botonera,
    text="Modificar",
    bg="LightSalmon2",
    command=modificar,
    width=14,
    padx=3,
    pady=3,
).grid(row=2, column=3)

# Indicaodr de campos obligatorios
frame_bottom = Frame(root)
frame_bottom.grid(row=9, columnspan=3)
label_obligatorio = Label(
    frame_bottom, text="* Campos de llenado obligatorio", bg="wheat1"
)
label_obligatorio.grid(row=0, column=5)

pantalla.bind("<ButtonRelease-1>", seleccionar_contacto)
root.mainloop()

# OPTIMIZACIONES
# Se modifico el orden del diseño
# Permitir solo numeros en el entry numeros.
# Se cambio el uso de registro en lista por el de base de datos.
# Se añadio una patalla con un Treeview
# Barra de desplazamiento para visualizar todos los datos del Treeview
# Validador de campo mail, solo se puede ingresar texto en formato de mail.
# E-mail es un campo obligatorio.
