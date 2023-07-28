from tkinter import *
from tkinter import ttk
import subprocess
import threading
import re



outdated_packages = []

""" def get_outdated_packages():
   outdated_packages.clear()
   def get_outdated_packages_worker():
      global outdated_packages, countPackages

      try:
         result = subprocess.run(['pip3', 'list', '--outdated'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
         if result.returncode == 0:
            package_lines = result.stdout.strip().split('\n')[2:]
            for line in package_lines:
               package_name = re.match(r'^(\S+)', line)
               if package_name and package_name.group(1) != "pip":
                  outdated_packages.append(package_name.group(1))
                  

      except Exception as e:
         errorLabel = Label(dataTopFrame, text=f'Something went wrong: {e}', fg='red')
         errorLabel.pack()

      finally:
         countPackages = Label(dataTopFrame, text=f'Packages to update: {len(outdated_packages)}', fg='black', font=('San Serif', 10))
         countPackages.pack(side='top', padx=10, pady=10, anchor='e')

         if outdated_packages:
            for x in outdated_packages:
               packageName = Label(dataTopFrame, text=f'{x} needs an update')
               packageName.pack(side='top', padx=10, pady=5, anchor='w')

         # Enable the "Check for updates" button after the function is done
         checkUpdates.config(state="normal", text='Check for updates', fg='black', bg='grey')

   # Disable the "Check for updates" button before starting the thread
   checkUpdates.config(state="disabled", fg='white', text='Searching...', bg='white')

   # Start the function in a separate thread
   threading.Thread(target=get_outdated_packages_worker).start()

def update_package(package):
   try:
      subprocess.run(['pip3', 'install', '--upgrade', package], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
      packageName = Label(dataTopFrame, text=f'{package} updated successfully', fg='black')
      packageName.pack(side='top', padx=10, pady=10, anchor='w')

      outdated_packages.remove(package)
   except Exception as e:
      errorLabel = Label(dataTopFrame, text=f'Something went wrong: {e}', fg='red')
      errorLabel.pack()

def update_packages():
   countPackages.config(text='')
   def update_packages_worker():
      try:
         threads = []
         for package in outdated_packages:
               thread = threading.Thread(target=update_package, args=(package,))
               threads.append(thread)
               thread.start()

         for thread in threads:
               thread.join()

      except Exception as e:
         errorLabel = Label(dataTopFrame, text=f'Something went wrong: {e}', fg='red')
         errorLabel.pack()

      finally:
         # Enable the "Update All" button after the function is done
         updateAll.config(state="normal", text='Update All', fg='black', bg='grey')

   # Disable the "Update All" button before starting the thread
   updateAll.config(state="disabled", fg='white', text='Updating...', bg='white')

   # Start the function in a separate thread
   threading.Thread(target=update_packages_worker).start()
 """

class AppFunc:
   ...


class AppGUI:
   def __init__(self): 

      self.window = Tk()
      self.window.title("Python update - packages")

      self.appWidth = 950
      self.appHeight = 650
      self.screen_w = self.window.winfo_screenwidth()
      self.screen_h = self.window.winfo_screenheight()


      x = (self.screen_w / 2) - (self.appWidth / 2)
      y = (self.screen_h / 2) - (self.appHeight / 2)
      self.window.geometry(f'{self.appWidth}x{self.appHeight}+{int(x)}+{int(y)}')

      self.setupGUI()
      self.window.mainloop()
   
   def setupGUI(self):
      #Main Frame
      topMainFrame = Frame(self.window, relief=None, height=450, width=self.appWidth, bg='red')
      topMainFrame.grid(row=0, column=0, sticky='nsew')
      self.window.grid_rowconfigure(0, weight=1)
      self.window.grid_columnconfigure(0, weight=1)

      #Bottom Frame
      bottomMainFrame = Frame(self.window, relief=None, height=200, width=self.appWidth, bg='yellow')
      bottomMainFrame.grid(row=1, column=0, sticky='nsew')
      self.window.grid_rowconfigure(1, weight=0)
      self.window.grid_columnconfigure(0, weight=1)

      #Treeview frame
      tree_frame = Frame(topMainFrame)
      tree_frame.grid(row=0, column=0, sticky='nsew')
      topMainFrame.grid_columnconfigure(0, weight=1)
      topMainFrame.grid_rowconfigure(0, weight=1)

      tree_scroll = Scrollbar(tree_frame)
      tree_scroll.pack(side=RIGHT, fill=Y)
      
      style = ttk.Style()
      style.theme_use("clam")  
      style.configure("Treeview",
         background="white",
         foreground="#231942",
         rowheight=25,
         fieldbackground="white"
      )

      my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
      my_tree.pack(fill='both', expand=True)

      tree_scroll.config(command=my_tree.yview)

      my_tree['columns'] = ("Name", "Version")

      my_tree.column("#0", width=0, stretch=NO)
      my_tree.column("Name", anchor=CENTER, width=50)
      my_tree.column("Version", anchor=CENTER, width=50)
   
      my_tree.heading("#0", text='', anchor=W)
      my_tree.heading("Name", text="Name", anchor=CENTER)
      my_tree.heading("Version", text="Version", anchor=CENTER)

      #Console Frame
      consoleFrame = Frame(topMainFrame, relief=None, width=self.appWidth * 0.1, bg='green')
      consoleFrame.grid(row=0, column=1, sticky='nsew')
      topMainFrame.grid_columnconfigure(1, weight=7)  #70% width of the top frame
      topMainFrame.grid_rowconfigure(0, weight=1)     #responsive height for the console frame

      #Column configuration for topMainFrame to make consoleFrame 70% width
      topMainFrame.grid_columnconfigure(1, weight=3)
      topMainFrame.grid_columnconfigure(0, weight=1)



if __name__ == "__main__":
   AppGUI()
