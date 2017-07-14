"""
A fast and reliable file patcher thats very easy to use.

This was written as a project to help me learn python and programming.

The code might not be the best or the neatest as I still have alot to learn.

Created by Jack Ackermann

"""




import tkinter as tk
import ntpath
from tkinter import Tk, ttk, Frame, FALSE, messagebox

import imp.tooltip as tt
from imp.patchfunctions import PatchFunctions


class PyFilePatcher(Frame):
    """The main Gui Class, contains mainly the GUI widgets"""
    def centre_window(self):
        w = 360
        h = 320
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        centre_title = (' '*20)  # Use spaces to center Title
        self.root.title(centre_title + '--  PyFilePatcher  -- ')
        self.root.iconbitmap('rsrc\icon.ico')
        self.centre_window()
        self.grid(column=0, row=0, sticky='nsew',  padx=5,  pady=5)
        self.create_widgets()
        
    def create_widgets(self): 
        """ Create 3 LabelFrames to store our widgets."""
        lbl_color = 'lavenderblush'
        self.m_frame = tk.LabelFrame(self.root, text='Manual Edit')
        self.m_frame.grid(column=0, row=0, sticky=tk.W)
        self.m_frame.configure(borderwidth=3, labelanchor='n',
                               bg=lbl_color)
        self.m_frame2 = tk.LabelFrame(self.root, text='Find & Replace')
        self.m_frame2.grid(column=0, row=1, sticky=tk.EW)
        self.m_frame2.configure(borderwidth=3, labelanchor='n',
                                bg=lbl_color)
        self.off_frame = tk.LabelFrame(self.root, text='Hex Location')
        self.off_frame.grid(column=0, row=2, sticky=tk.W)
        self.off_frame.configure(borderwidth=3, bg=lbl_color)

        # Label Section
        LTXT1 = 'Go to file offset: '
        LTXT2 = 'Current Hex Values: '
        LTXT3 = 'New Hex Values: '
        LTXT4 = 'Find String: '
        LTXT5 = 'Replace String: '
        LTXT6 = 'Modifying data at file offset: '

        label1 = tk.Label(self.m_frame, text=LTXT1 ,bg=lbl_color)
        label1.grid(column=0, row=1, sticky=tk.W)
        label2 = tk.Label(self.m_frame, text=LTXT2 ,bg=lbl_color)
        label2.grid(column=0, row=2, sticky=tk.W)
        label3 = tk.Label(self.m_frame, text=LTXT3 ,bg=lbl_color)
        label3.grid(column=0, row=3, sticky=tk.W)

        self.off_txt = tk.StringVar()
        self.off_lbl = tk.Label(self.off_frame, textvariable=self.off_txt,
                                 bg=lbl_color, fg='Dark Blue')
        self.off_lbl.grid(column=0, row=0, sticky=tk.W)
        self.off_txt.set(LTXT6)

        label4 = tk.Label(self.m_frame2, text=LTXT4 ,bg=lbl_color)
        label4.grid(column=0, row=0, sticky=tk.W)
        label5 = tk.Label(self.m_frame2, text=LTXT5 ,bg=lbl_color)
        label5.grid(column=0, row=1, sticky=tk.W)

        # Text Box Entry Widget section
        self.fn = tk.StringVar()
        self.f_entry = ttk.Entry(self.m_frame, width=40, textvariable=self.fn)
        self.f_entry.grid(column=0, row=0, columnspan=2, sticky=tk.E)
        self.f_entry.configure(state='readonly')

        self.txt_e = tk.StringVar()
        self.txt_e.set(0)
        self.off_ent = ttk.Entry(self.m_frame, width=15,
                                 textvariable=self.txt_e)
        self.off_ent.grid(column=1, row=1, sticky=tk.W)
        self.off_ent.configure(state='disabled')
        self.off_ent.bind("<Return>", lambda x: self.goto_callback())
        
        self.txt_cur = tk.StringVar()
        self.cur_ent = ttk.Entry(self.m_frame, width=36,
                                 textvariable=self.txt_cur)
        self.cur_ent.grid(column=1, row=2)
        self.cur_ent.configure(state='readonly')

        self.txt_new = tk.StringVar()
        self.new_ent = ttk.Entry(self.m_frame, width=36,
                                   textvariable=self.txt_new)
        self.new_ent.grid(column=1, row=3)

        # m_frame2 section
        self.find_txt = tk.StringVar()
        self.find_ent = ttk.Entry(self.m_frame2, width=36,
                                   textvariable=self.find_txt)
        self.find_ent.grid(column=1, row=0)

        self.rep_txt = tk.StringVar()
        self.rep_ent = ttk.Entry(self.m_frame2, width=36,
                                   textvariable=self.rep_txt)
        self.rep_ent.grid(column=1, row=1)
        
        # Button section
        self.go_btn = ttk.Button(self.m_frame, text='Go To',
                                 command=self.goto_callback)
        self.go_btn.grid(column=1, row=1, sticky=tk.E)
        self.go_btn.configure(state='disabled')

        self.upt_btn = ttk.Button(self.m_frame, text='Update Hex',
                                 command=self.update_callback)
        self.upt_btn.grid(column=1, row=4, sticky=tk.E)
        self.upt_btn.configure(state='disabled')

        self.file_btn = ttk.Button(self.m_frame, text='File',
                                   command=self.open_callback)
        self.file_btn.grid(column=0, row=0, sticky=tk.W)

        self.exit_btn = ttk.Button(self.root, text='Exit', command=self.on_exit)
        self.exit_btn.grid(column=0, row=2, sticky=tk.SE, pady=0)

        fr_txt = 'Find & Replace'
        self.repl_btn = ttk.Button(self.m_frame2, text=fr_txt,
                                   command=self.find_callback)
        self.repl_btn.grid(column=1, row=2, sticky=tk.NSEW)
        self.repl_btn.configure(state='disabled')

        # Place padding around frames, to improve look and feel
        for child in self.root.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # Create tooltips for some entry widgets
        tooltip_txt1 = 'Enter Offset - Hex Address not binary address'
        tooltip_txt2 = "New Hex Bytes - In form of FF, EAFF, 01FFAB, 20AB409E"
        tt.create_tooltip(self.off_ent, tooltip_txt1)
        tt.create_tooltip(self.cur_ent, 'Current Hex Values')
        tt.create_tooltip(self.new_ent, tooltip_txt2)
        tt.create_tooltip(self.find_ent, 'Find Values - Max 32 Char')
        tt.create_tooltip(self.rep_ent, 'Replace Values - Max 32 Char')
        
    # All callbacks for the buttons are stored here
    def goto_callback(self):
        # Calls the file offset function
        PatchFunctions.goto_offset(self)
 
    def open_callback(self):
        # Calls the load file function
        PatchFunctions.open_file(self)
  
    def update_callback(self):
        # Calls the Update Hex function
        self.backup_file = "Patched_" + ntpath.basename(self.name)
        if len(self.txt_new.get()) % 2 == 0:
            self.backup_file = PatchFunctions.create_backup_file(self)
            PatchFunctions.update_hex(self)
        else:
            m_txt0 = "Hex value is not one char, hex = two char"
            messagebox.showerror("Error: Invalid Hex Value", m_txt0)
     
    def find_callback(self):
        # Calls the find and repalce function
        self.backup_file = "Patched_" + ntpath.basename(self.name)
        if len(self.find_txt.get()) % 2 == 0 and self.find_txt.get() != '':
            if len(self.find_txt.get()) == len(self.rep_txt.get()):
                self.backup_file = PatchFunctions.create_backup_file(self)
                PatchFunctions.find_rep(self)
            else:
                m_txt3 = "Find and Replace values must be the same length"
                messagebox.showerror("Error: Invalid Length", m_txt3)
        else:
            m_txt4 = "Hex string format must be in FF, FFFF, ABEF10"
            messagebox.showerror("Error: Invalid Hex length", m_txt4)

    def on_exit(self):
        # Exit system
        self.root.destroy()



def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.configure(background="lavenderblush")
    PyFilePatcher(root)
    root.mainloop()

if __name__ == '__main__':
    main()
