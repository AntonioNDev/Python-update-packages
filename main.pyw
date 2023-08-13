from tkinter import *
from tkinter import ttk
import subprocess
import threading
import re



class AppFunc:
   outdated_packages = []
   all_packages = []

   @classmethod
   def get_outdated_packages(cls, self):
      cls.outdated_packages.clear() #clear the list from the items before

      def get_outdated_packages_worker():
         global outdated_packages

         try:
            result = subprocess.run(['pip3', 'list', '--outdated'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
               package_lines = result.stdout.strip().split('\n')[2:]
               for line in package_lines:
                  package_name = re.match(r'^(\S+)', line)
                  if package_name and package_name.group(1) != "pip":
                     cls.outdated_packages.append(package_name.group(1))
                     

         except Exception as e:
            statusLabel.config(text=f'Something went wrong: {e}', fg='crimson')

         finally:
            countPackages.config(text=f'Packages to update: {len(cls.outdated_packages)}')

            if cls.outdated_packages:
               for x in cls.outdated_packages:
                  packageName = Label(labels_frame, text=f'{x} needs an update', bg='#d9dadd', font=('San Serif', 11))
                  packageName.pack(side='top', padx=15, pady=5, anchor='w')
               
               #Set the scrolling position to the latest label
               canvas.yview_moveto(1.0)   

            # Enable the "Check for updates" button after the function is done
            checkForUpdates.config(state="normal", text='Check for updates', bg="#3c4442", fg="white")

      # Disable the "Check for updates" button before starting the thread
      checkForUpdates.config(state="disabled", fg='white', text='Searching...', bg='white')

      # Start the function in a separate thread
      threading.Thread(target=get_outdated_packages_worker).start()

   @classmethod
   def update_package(cls, package):
      def update_single_package(package):
            try:
               subprocess.run(['pip3', 'install', '--upgrade', package], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
               packageName = Label(labels_frame, text=f'{package} updated successfully', fg='black', bg='#d9dadd', font=('San Serif', 11))
               packageName.pack(side='top', padx=10, pady=10, anchor='w')

         
            except Exception as e:
               statusLabel.config(text=f'Something went wrong: {e}', fg='crimson')

            finally:
               update.config(state="normal", bg="#3c4442", fg="white", text='Update')

      if isinstance(package, str) and package:  #Update a single package
            thread = threading.Thread(target=update_single_package, args=(package,), daemon=True)
            thread.start()

            if package in cls.outdated_packages:
               cls.outdated_packages.remove(package)
               countPackages.config(text=f'Packages to update: {len(cls.outdated_packages)}')

            entry_package.delete(0, 'end')
            update.config(state="disabled", text='Updating', fg='white', bg='white')

      elif isinstance(package, list):  #Update multiple packages
            threads = []
            packageName = Label(labels_frame, text=f'Updating packages, this might take a while, please wait.', fg='black', bg='#d9dadd', font=('San Serif', 11))
            packageName.pack(side='top', padx=10, pady=10, anchor='w')

            for pkg in package:
               thread = threading.Thread(target=update_single_package, args=(pkg,))
               threads.append(thread)
               thread.start()

               cls.outdated_packages.remove(pkg)
               countPackages.config(text=f'Packages to update: {len(cls.outdated_packages)}')

            for thread in threads:
               thread.join()

   @classmethod
   def update_packages(cls, self):
      def update_packages_worker():
         try:
               thread = threading.Thread(target=cls.update_package, args=(cls.outdated_packages,))
               thread.start()

         except Exception as e:
               statusLabel.config(text=f'Something went wrong: {e}', fg='crimson')

         finally:
               # Enable the "Update All" button after the function is done
               updateAll.config(state="normal", text='Update All', bg="#3c4442", fg="white")

      # Disable the "Update All" button before starting the thread
      updateAll.config(state="disabled", fg='white', text='Updating all...', bg='white')

      # Start the function in a separate thread
      threading.Thread(target=update_packages_worker).start()

   @classmethod
   def display_all_packages(cls, self):
      cls.all_packages.clear() 

      def display_all_packages_worker():
         try:
            result = subprocess.run(['pip3', 'list', 'freeze'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                  package_lines = result.stdout.strip().split('\n')[2:]
                  for line in package_lines:
                     package_name = re.match(r'^(\S+)', line)
                     if package_name:
                        cls.all_packages.append(package_name.group(1))

         except Exception as e:
            statusLabel.config(text=f'Something went wrong: {e}', fg='crimson')

         finally:
            countPackages.config(text=f'Total packages: {len(cls.all_packages)}')

            if cls.all_packages:
                  for x in cls.all_packages:
                     packageName = Label(labels_frame, text=f'{x}', bg='#d9dadd', font=('San Serif', 11))
                     packageName.pack(side='top', padx=15, pady=5, anchor='w')

                  # Update the canvas scroll region when labels_frame size changes
                  labels_frame.update_idletasks()
                  canvas.config(scrollregion=canvas.bbox("all"))

                  # Set the scrolling position to the latest label
                  canvas.yview_moveto(1.0)

            # Enable the "Display All" button after the function is done
            displayAll.config(state="normal", text='Display All', bg="#3c4442", fg="white")

      #Disable the "Check for updates" button before starting the thread
      displayAll.config(state="disabled", fg='white', text='Processing...', bg='white')

      #Start the function in a separate thread
      threading.Thread(target=display_all_packages_worker).start()

   @classmethod
   def uninstall_package(cls, package):
      def uninstall_package_worker(package):
         uninstall.config(state="disabled", text='Uninstalling...', fg='white', bg='white')
         try:
            print(f"Uninstalling {package}")
            subprocess.run(['pip3', 'uninstall', '-y', package], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            packageName = Label(labels_frame, text=f'{package} uninstalled successfully', fg='black', bg='#d9dadd', font=('San Serif', 11))
            packageName.pack(side='top', padx=10, pady=10, anchor='w')

         
         except Exception as e:
            statusLabel.config(text=f'Something went wrong: {e}', fg='crimson')

         finally:
            uninstall.config(state="normal", text='Uninstall', bg="#3c4442", fg="white")

         
         entry_package.delete(0, 'end')

      if package:
         thread = threading.Thread(target=uninstall_package_worker, args=(package,), daemon=True)
         thread.start()

   @classmethod 
   def install_package(cls, package):
      def install_package_worker(package):
         install.config(state="disabled", text='Installing', fg='white', bg='white')
         try:
            subprocess.run(['pip3', 'install', package], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            packageName = Label(labels_frame, text=f'{package} installed successfully', fg='black', bg='#d9dadd', font=('San Serif', 11))
            packageName.pack(side='top', padx=10, pady=10, anchor='w')
         
         except Exception as e:
            statusLabel.config(text=f'Something went wrong: {e}', fg='crimson')

         finally:
            install.config(state="normal", text='Install', bg="#3c4442", fg="white")
         
         entry_package.delete(0, 'end')

      if package:
         thread = threading.Thread(target=install_package_worker, args=(package,), daemon=True)
         thread.start()

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
      self.window.bind('<Button>', lambda event: event.widget.focus_set())
      self.window.mainloop()


   def clear_console(self):
      for widget in labels_frame.winfo_children():
         widget.destroy()

      canvas.update_idletasks()
      canvas.config(scrollregion=canvas.bbox(ALL))
      countPackages.config(text='')

      if not labels_frame.winfo_children():
         canvas.yview_moveto(0.0)


   def setupGUI(self):
      global labels_frame, canvas, statusLabel, entryFrame, updateAll, update, checkForUpdates, displayAll, uninstall, install, countPackages, entry_package

      #Main Frame
      topMainFrame = Frame(self.window, relief=None, height=450, width=self.appWidth)
      topMainFrame.grid(row=0, column=0, sticky='nsew')
      self.window.grid_rowconfigure(0, weight=1)
      self.window.grid_columnconfigure(0, weight=1)

      #Bottom Frame
      bottomMainFrame = Frame(self.window, relief=None, height=200, width=self.appWidth)
      bottomMainFrame.grid(row=1, column=0, sticky='nsew')
      self.window.grid_rowconfigure(1, weight=0)
      self.window.grid_columnconfigure(0, weight=1)

      #Console Frame
      consoleFrame = Frame(topMainFrame, relief=None, width=self.appWidth)
      consoleFrame.grid(row=0, column=0, columnspan=2, sticky='nsew') 
      topMainFrame.grid_columnconfigure(0, weight=1) 
      topMainFrame.grid_columnconfigure(1, weight=0)  #Set weight for the second column to 0
      topMainFrame.grid_rowconfigure(0, weight=1)  #Responsive height for the console frame

      #Create a canvas in the consoleFrame
      canvas = Canvas(consoleFrame, bg='#d9dadd')
      canvas.grid(row=0, column=0, sticky='nsew')

      #Add a vertical scrollbar for the canvas
      canvas_scroll = Scrollbar(consoleFrame, command=canvas.yview, orient=VERTICAL)
      canvas_scroll.grid(row=0, column=1, sticky='ns')
      canvas.config(yscrollcommand=canvas_scroll.set)

      #Create a frame inside the canvas for the labels
      labels_frame = Frame(canvas, bg='#d9dadd')
      canvas.create_window((0, 0), window=labels_frame, anchor=NW)

      #Update the canvas scroll region when labels_frame size changes
      labels_frame.update_idletasks()
      canvas.config(scrollregion=canvas.bbox(ALL))

      consoleFrame.grid_rowconfigure(0, weight=1)  #Make canvas expand vertically
      consoleFrame.grid_columnconfigure(0, weight=1)  #Make canvas expand horizontally

      #Bottom buttons frame
      bottomButtonsFrame = Frame(bottomMainFrame, relief=None, width=self.appWidth * 0.7, height=200, bg='#d9dadd')
      bottomButtonsFrame.grid(row=0, column=1, sticky='nsew')
      bottomMainFrame.grid_columnconfigure(1, weight=7)
      bottomMainFrame.grid_rowconfigure(0, weight=1) 

      bottomMainFrame.grid_columnconfigure(1, weight=4)
      bottomMainFrame.grid_columnconfigure(0, weight=1)
      bottomMainFrame.grid_propagate(False)

      
      #Create buttons 3x3 grid layout
      displayAll = Button(bottomButtonsFrame, text="Display all", bg="#3c4442", fg="white", font=('San Serif', 12), relief='sunken', border=2,cursor='hand2', command=lambda: AppFunc.display_all_packages(self))
      displayAll.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
      
      checkForUpdates = Button(bottomButtonsFrame, text="Check for updates", bg="#3c4442", fg="white", font=('San Serif', 12), relief='sunken', border=2,cursor='hand2', command=lambda: AppFunc.get_outdated_packages(self))
      checkForUpdates.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
      
      updateAll = Button(bottomButtonsFrame, text="Update all", bg="#3c4442", fg="white", font=('San Serif', 12), relief='sunken', border=2,cursor='hand2', command=lambda: AppFunc.update_packages(self))
      updateAll.grid(row=0, column=2, sticky='ew', padx=5, pady=5)
      
      update = Button(bottomButtonsFrame, text="Update", bg="#3c4442", fg="white", font=('San Serif', 12), relief='sunken', border=2,cursor='hand2', command=lambda: AppFunc.update_package(entry_package.get()))
      update.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
      
      install = Button(bottomButtonsFrame, text="Install", bg="#3c4442", fg="white", font=('San Serif', 12), relief='sunken', border=2,cursor='hand2', command=lambda: AppFunc.install_package(entry_package.get()))
      install.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
      
      uninstall = Button(bottomButtonsFrame, text="Uninstall", bg="#3c4442", fg="white", font=('San Serif', 12), relief='sunken', border=2,cursor='hand2', command=lambda: AppFunc.uninstall_package(entry_package.get()))
      uninstall.grid(row=1, column=2, sticky='ew', padx=5, pady=5)

      #Make buttons expand both horizontally and vertically
      for col in range(3):
         bottomButtonsFrame.grid_columnconfigure(col, weight=1)
      for row in range(2):
         bottomButtonsFrame.grid_rowconfigure(row, weight=1)


      #Add LabelFrame and Entry in bottomMainFrame
      entryFrame = LabelFrame(bottomMainFrame, text='Package to install / uninstall / update:', font=('San Sarif', 11), bg='#6e7c7a', fg='white')
      entryFrame.grid(row=0, column=0, sticky='nsew')

      entry_package = Entry(entryFrame, bg='white', fg='black', font=('San Sarif', 11))
      entry_package.pack(padx=10, pady=5, ipady=5, anchor='nw', fill='x')

      statusLabel = Label(entryFrame, text=f'', fg='green', font=('San Serif', 11), bg='#6e7c7a')
      statusLabel.pack(padx=10, pady=10, ipady=5, anchor='sw', fill='x')

      countPackages = Label(entryFrame, text='', bg='#6e7c7a', fg='white', font=('San Serif', 10))
      countPackages.pack()

      clearButton = Button(entryFrame, text="Clear Console", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2', command=self.clear_console)
      clearButton.pack(pady=5)

      entryFrame.grid_rowconfigure(0, weight=1)  #LabelFrame takes the remaining vertical space


if __name__ == "__main__":
   AppGUI()
   active_threads = threading.active_count()
   print(f"Number of active threads: {active_threads}")
