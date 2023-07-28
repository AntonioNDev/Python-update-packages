from tkinter import *
import subprocess
import threading
import re

window = Tk()
window.title("Python update - packages")

appWidth = 500
appHeight = 500

screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

x = (screen_w / 2) - (appWidth) + 250
y = (screen_h / 2) - (appHeight) + 250

window.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

outdated_packages = []

def get_outdated_packages():
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
               thread = threading.Thread(target=update_package, args=(package,)).start()
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


def setupGUI():
   global dataTopFrame, checkUpdates, updateAll

   dataTopFrame = Frame(window, relief='sunken', height=400, width=500, border=3)
   dataTopFrame.pack(side=TOP)

   optionsButtomFrame = Frame(window, relief='groove', height=250, width=500, border=2)
   optionsButtomFrame.pack(side=BOTTOM)

   buttonsGrid = Frame(optionsButtomFrame, relief='raised', height=125, width=500, border=3)
   buttonsGrid.grid(row=0, column=0)

   checkUpdates = Button(buttonsGrid, text='Check for updates', border=4, relief='sunken', cursor='hand2', font=('San Serif', 13), fg='black', bg='grey', command=get_outdated_packages)
   updateAll = Button(buttonsGrid, text='Update All', border=4,relief='sunken', cursor='hand2', font=('San Serif', 13), fg='black', bg='grey' , command=update_packages)

   checkUpdates.grid(row=0, column=0, pady='10', padx='80')
   updateAll.grid(row=0, column=1, pady='10', padx='10')

   dataTopFrame.pack_propagate(False)
   optionsButtomFrame.pack_propagate(False)
   buttonsGrid.grid_propagate(False)



def main():
   setupGUI()
   window.bind('<Button>', lambda event: event.widget.focus_set())
   window.resizable(False, False)
   window.mainloop()

if __name__ == "__main__":
   main()
