import os
from tkinter import *
from tkinter import filedialog
import shutil
from pathlib import Path
import time


root = Tk()
root.title('ULTIMATOR 6000')

Label(root, width=40, text='Inserisci il path della cartella', font=('Arial', 12)).pack()
e = Entry(root, width=50, borderwidth=3)
e.pack()

def apri():
    root.filename = filedialog.askdirectory(initialdir=os.getcwd(), title="Seleziona una cartella")
    e.insert(0, root.filename)


Button(root, text="Select Folder", command=apri).pack()


Label(root, width=40, text='Inserisci il suffisso', font=('Arial', 12)).pack()
div = Entry(root, width=50, borderwidth=3)
div.pack()

var1 = IntVar()
c1 = Checkbutton(root, text='Copiare in nuova cartella',variable=var1, onvalue=1, offvalue=0, font=('Arial', 12))
c1.pack()

EXCLUDE = {'COPIONE', 'BACKUPS'}

def foo():
    path = Path(e.get())
    suffisso = div.get()
    main_dir_list = os.listdir(path)

    if e.get() :
        bkp_dir = path / 'BACKUPS'
        if not os.path.exists(bkp_dir):
            os.mkdir(bkp_dir)
        os.chdir(bkp_dir)
        now = time.localtime(time.time())
        f_name = f'backup_{now.tm_year}_{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}_{now.tm_sec}.txt'
        with open(f_name, 'w') as bkp:
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    if d not in EXCLUDE:
                        d_path = Path(root) / d
                        bkp.write(f'{d_path}\n')
                        # print(d_path)
                for f in files:
                    if not 'COPIONE' in root and not 'BACKUPS' in root:
                        f_path = Path(root) / f
                        bkp.write(f'{f_path}\n')
                        # print(f_path)

    for sub_dir in main_dir_list:
        if sub_dir not in EXCLUDE and not sub_dir.startswith('.'):
            sub_path = path / sub_dir
            sub_dir_list = os.listdir(sub_path)
            os.chdir(sub_path)
            for sub_sub_dir in sub_dir_list:
                if not sub_sub_dir.startswith('.'):
                    sub_sub_path = sub_path / sub_sub_dir
                    sub_sub_list = os.listdir(sub_sub_path)
                    os.chdir(sub_sub_path)
                    count = 1
                    for f in sub_sub_list:
                        file_path = sub_sub_path / f
                        # print('file path:', file_path)
                        extension = f.split('.')[-1]
                        new_name = f'{sub_dir}-{sub_sub_dir}-{count}-{suffisso}.{extension}'
                        os.rename(file_path, new_name)
                        count += 1

    print('\nRenaming effettuato con successo!')
    if var1.get() == 1:
        new_dir = path / 'COPIONE'
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        # print(dir_list)
        for sub_dir in main_dir_list:
            # print(sub_dir)
            if sub_dir not in EXCLUDE and not sub_dir.startswith('.'):
                sub_path = path / sub_dir
                sub_sub_list = os.listdir(sub_path)
                os.chdir(sub_path)
                for sub_sub_dir in sub_sub_list:
                    if not sub_sub_dir.startswith('.'):
                        for sub_sub_dir in sub_sub_list:
                            sub_sub_path = sub_path / sub_sub_dir
                            # print('\n\n')
                            # print('sub_path', sub_path)
                            # print('new_path', new_dir)
                            shutil.copytree(sub_sub_path, new_dir, dirs_exist_ok=True)
        print('\nCopia effettuata con successo!')

Button(root, text="Esegui", padx=20, pady=4, command=foo).pack()


# def tree_printer():
#     root = Path(e.get())
#     bkp_dir = root / 'BACKUPS'
#     if not os.path.exists(bkp_dir):
#         os.mkdir(bkp_dir)
#     os.chdir(bkp_dir)
#     now = time.localtime(time.time())
#     f_name = f'backup_{now.tm_year}_{now.tm_mon}_{now.tm_mday}_{now.tm_hour}_{now.tm_min}_{now.tm_sec}.txt'
#     # print(f_name)
#     with open(f_name, 'w') as bkp:
#         for root, dirs, files in os.walk(root):
#             for d in dirs:
#                 d_path = Path(root) / d
#                 bkp.write(f'{d_path}\n')
#                 # print(d_path)
#             for f in files:
#                 f_path = Path(root) / f
#                 bkp.write(f'{f_path}\n')
#                 # print(f_path)


# Button(root, text="Tree", padx=20, pady=4, command=tree_printer).pack()

root.mainloop()
