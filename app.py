import os
from tkinter import *
from tkinter import filedialog
import shutil


root = Tk()
root.title('ULTIMATOR 6000')

Label(root, width=40, text='Inserisci il path della cartella', font=('Arial', 12)).pack()
e = Entry(root, width=50, borderwidth=3)
e.pack()

def open():
    root.filename = filedialog.askdirectory(initialdir=os.getcwd(), title="Seleziona una cartella")
    e.insert(0, root.filename)


Button(root, text="Select Folder", command=open).pack()


Label(root, width=40, text='Inserisci il suffisso', font=('Arial', 12)).pack()
div = Entry(root, width=50, borderwidth=3)
div.pack()

var1 = IntVar()
c1 = Checkbutton(root, text='Copiare in nuova cartella',variable=var1, onvalue=1, offvalue=0, font=('Arial', 12))
c1.pack()

def foo():
    path = e.get()
    suffisso = div.get()
    dir_list = os.listdir(path)

    for sub_dir in dir_list:
        if sub_dir != 'COPIONE':
            sub_path = f'{path}\\{sub_dir}'
            sub_list = os.listdir(sub_path)
            os.chdir(sub_path)
            count = 1
            for f in sub_list:
                file_path = f'{sub_path}\\{f}'
                print('file path:', file_path)
                extension = f.split('.')[-1]
                new_name = f'{sub_dir}-{count}-{suffisso}.{extension}'
                os.rename(file_path, new_name)
                count += 1

    if var1.get() == 1:
        new_dir = f'{path}\\COPIONE'
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        print(dir_list)
        for sub_dir in dir_list:
            print(sub_dir)
            if sub_dir != 'COPIONE':
                sub_path = f'{path}\\{sub_dir}'
                print('\n\n')
                print('sub_path', sub_path)
                print('new_path', new_dir)
                shutil.copytree(sub_path, new_dir, dirs_exist_ok=True)

Button(root, text="Esegui", padx=20, pady=4, command=foo).pack()

root.mainloop()
