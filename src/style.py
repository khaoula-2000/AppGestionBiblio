import tkinter as tk
from tkinter import ttk

def configureStyles(root):
    style = ttk.Style()
    style.theme_use('clam')

    
    bg_color = "#f5f8fb"         
    fg_color = "#2d2d2d"         
    accent_color = "#005792"     
    button_color = "#0074b7"     
    highlight_color = "#cce7ff" 
    entry_bg = "#ffffff"
    gray_text = "#666666"

    root.configure(background=bg_color)

    
    style.configure('.', 
                    background=bg_color, 
                    foreground=fg_color,
                    font=('Segoe UI', 10))

    
    style.configure('TNotebook', background=bg_color, borderwidth=0)
    style.configure('TNotebook.Tab',
                    font=('Segoe UI', 10, 'bold'),
                    padding=[12, 6],
                    background=bg_color,
                    foreground=fg_color)
    style.map('TNotebook.Tab',
              background=[('selected', accent_color)],
              foreground=[('selected', 'white')])

    
    style.configure('TButton',
                    background=button_color,
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'),
                    padding=8,
                    borderwidth=0)
    style.map('TButton',
              background=[('active', '#005792'), ('pressed', '#003f63')])

    
    style.configure('TLabel',
                    background=bg_color,
                    foreground=fg_color,
                    font=('Segoe UI', 10),
                    padding=4)

    
    style.configure('TEntry',
                    font=('Segoe UI', 10),
                    padding=6,
                    fieldbackground=entry_bg,
                    foreground=fg_color,
                    relief='solid',
                    borderwidth=1)
    
    
    style.configure('TCombobox',
                    font=('Segoe UI', 10),
                    padding=6,
                    fieldbackground=entry_bg,
                    foreground=fg_color)


    style.configure('Treeview',
                    background='white',
                    foreground=fg_color,
                    rowheight=28,
                    fieldbackground='white',
                    font=('Segoe UI', 10))
    style.configure('Treeview.Heading',
                    background=accent_color,
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'),
                    padding=6)
    style.map('Treeview',
              background=[('selected', highlight_color)],
              foreground=[('selected', fg_color)])

    
    style.configure('TLabelframe',
                    background=bg_color,
                    foreground=accent_color,
                    borderwidth=1,
                    relief='solid')
    style.configure('TLabelframe.Label',
                    background=bg_color,
                    foreground=accent_color,
                    font=('Segoe UI', 10, 'bold'))

    
    style.configure('Title.TLabel',
                    font=('Segoe UI', 12, 'bold'),
                    foreground=accent_color,
                    padding=10)
    
    style.configure('Status.TLabel',
                    font=('Segoe UI', 9),
                    foreground=gray_text,
                    padding=5)

    return style
