import os
import binascii
import shutil
import re
from tkinter import filedialog, messagebox


class PatchFunctions(object):
    """
    This class contains all the funtions needed to convert binary to hex
    and convert hex back into binary.

    It also handles the patch file creation as well as the update to the
    patch file.

    The original file is untouched.

    """
    def __init__(self):
        pass
    
    def goto_offset(self): # Goes to file offset to edit
        """
        This function takes you to the required offset
        The go to offset must be a hex string

        It also updates the current hex address at the bottom of the screen 
        """
        LTXT6 = 'Modifying data at file offset: '
        self.off_txt.set(LTXT6 + self.txt_e.get())
        # read written data only
        try:
            with open (self.name, "rb") as f:
                hex_add = int(self.txt_e.get(), 16) # convert hex to int
                if hex_add < len(f.read()):
                    f.seek(hex_add)
                    self.read = f.read(16)  # Read 16 bytes
                    to_hex = binascii.hexlify(self.read) # convert bin to hex
                    self.txt_cur.set(to_hex.upper())
                else:
                    title_txt = "Out of range"
                    body_txt = "Index out of range, please correct"
                    messagebox.showerror(title_txt, body_txt)
        except ValueError:
            title_txt = "Error: Not a integer"
            body_txt = "Goto Index can only be a hex value"
            messagebox.showerror(title_txt, body_txt)
        except FileNotFoundError:
            self.txt_cur.set('')
            self.off_txt.set(LTXT6)
            messagebox.showerror("Error: File Error", "No File was Found!") 

    def open_file(self): # Loads file to edit
        """
        This function loads the file the user wants to edit.
        It enables the buttons once the file is loaded.

        If user cancels the file dialog, the buttons get disabled again

        """
        
        try:
            file_type = [("All Files","*.*")]
            title_text = "---- Please select the file to edit ----"
            self.name = filedialog.askopenfilename(filetypes=file_type,
                                                   title=title_text)
            if self.name != '':
                self.fn.set(self.name)
                self.go_btn.configure(state='enabled')
                self.upt_btn.configure(state='enabled')
                self.repl_btn.configure(state='enabled')
            else:
                self.go_btn.configure(state='disabled')
                self.upt_btn.configure(state='disabled')
                self.repl_btn.configure(state='disabled')
                self.txt_cur.set('')
                self.txt_e.set('')
                self.fn.set('')
        except:
            self.go_btn.configure(state='disabled')
            self.upt_btn.configure(state='disabled')
            self.repl_btn.configure(state='disabled')
            self.txt_cur.set('')
            self.txt_e.set('')
            self.fn.set('')
            messagebox.showerror("File Error", "File could not be opened")

    def create_backup_file(self):
        """
        Creates a copy of the original file, only the copy gets patched.
        The original file does not get touched.
        """
        try:
            f = open(self.backup_file, 'rb')
        except FileNotFoundError:
            shutil.copyfile(self.name, self.backup_file)
        else:
            f.close
        return self.backup_file
        
    def update_hex(self):
        """
        Update Hex values with new Hex values
        Write new hex data into the patch file
        """
        to_bin = binascii.unhexlify(self.txt_new.get()) # convert hex to bin
        hex_add = int(self.txt_e.get(), 16)
        try:
            with open (self.backup_file, "r+b") as fb:        
                fb.seek(hex_add)
                fb.write(to_bin)
                m_txt = "File has been successfully Patched"
                messagebox.showinfo("Success", m_txt)
        except FileNotFoundError:
            m_txt2 = "No File was Found!"
            messagebox.showerror("Error: File Error", m_txt2)
           
    def find_rep(self):
        """ Find and replace all found hex values """
        find_str = binascii.unhexlify(self.find_txt.get())
        replace_str = binascii.unhexlify(self.rep_txt.get())
        with open(self.backup_file, 'r+b') as f:
            hex_data = f.read()
            if find_str in hex_data:
                m_found = len(re.findall(find_str, hex_data))
                r_txt = "There were {0} found".format(m_found)
                r_txt += "\n\nProceed and replace all found match / matches"
                if messagebox.askyesno('Verify', r_txt):
                    rep_data = re.sub(find_str, replace_str, hex_data)
                    f.seek(0)
                    f.write(rep_data)
                    r_txt2 = "There were {0} matches replaced".format(m_found)
                    messagebox.showinfo('-- Success --', r_txt2)
                else:
                    can_txt = 'User cancelled find and replace update'
                    messagebox.showinfo('Cancelled', can_txt)
            else:
                messagebox.showerror("Not Found", "No Matches were found")

