from tkinter import *
from tkinter import ttk
import subprocess
import threading
import re



class AppFunc:
   outdated_packages = []

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
            statusLabel.config(entryFrame, text=f'Something went wrong: {e}', fg='crimson')

         finally:
            countPackages.config(text=f'Packages to update: {len(cls.outdated_packages)}')

            if cls.outdated_packages:
               for x in cls.outdated_packages:
                  packageName = Label(labels_frame, text=f'{x} needs an update')
                  packageName.pack(side='top', padx=15, pady=5, anchor='w')
               
               #Set the scrolling position to the latest label
               canvas.yview_moveto(1.0)   

            # Enable the "Check for updates" button after the function is done
            checkForUpdates.config(state="normal", text='Check for updates', fg='black', bg='grey')

      # Disable the "Check for updates" button before starting the thread
      checkForUpdates.config(state="disabled", fg='white', text='Searching...', bg='white')

      # Start the function in a separate thread
      threading.Thread(target=get_outdated_packages_worker).start()

   
   def update_package(self, package):
      try:
         subprocess.run(['pip3', 'install', '--upgrade', package], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
         packageName = Label(labels_frame, text=f'{package} updated successfully', fg='black')
         packageName.pack(side='top', padx=10, pady=10, anchor='w')

         outdated_packages.remove(package)
         countPackages.config(text=f'Packages to update: {len(self.outdated_packages)}')
      except Exception as e:
         statusLabel.config(entryFrame, text=f'Something went wrong: {e}', fg='crimson')

   @classmethod
   def update_packages(cls, self):
      statusLabel.config(text='')

      def update_packages_worker():
         try:
            threads = []
            for package in outdated_packages:
                  thread = threading.Thread(target=self.update_package, args=(package,))
                  threads.append(thread)
                  thread.start()

            for thread in threads:
                  thread.join()

         except Exception as e:
            statusLabel.config(entryFrame, text=f'Something went wrong: {e}', fg='crimson')

         finally:
            # Enable the "Update All" button after the function is done
            updateAll.config(state="normal", text='Update All', fg='black', bg='white')
            
      # Disable the "Update All" button before starting the thread
      updateAll.config(state="disabled", fg='white', text='Updating...', bg='grey')

      # Start the function in a separate thread
      threading.Thread(target=update_packages_worker).start()

   @classmethod
   def display_all_packages(cls, self):
      def display_all_packages_worker():
         try:
            result = subprocess.run(['pip3', 'list', 'freeze'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                  package_lines = result.stdout.strip().split('\n')[2:]
                  for line in package_lines:
                     package_name = re.match(r'^(\S+)', line)
                     if package_name:
                        cls.outdated_packages.append(package_name.group(1))

         except Exception as e:
            statusLabel.config(entryFrame, text=f'Something went wrong: {e}', fg='crimson')

         finally:
            countPackages.config(text=f'Total packages: {len(cls.outdated_packages)}')

            if cls.outdated_packages:
                  for x in cls.outdated_packages:
                     packageName = Label(labels_frame, text=f'{x}')
                     packageName.pack(side='top', padx=15, pady=5, anchor='w')

                  # Update the canvas scroll region when labels_frame size changes
                  labels_frame.update_idletasks()
                  canvas.config(scrollregion=canvas.bbox("all"))

                  # Set the scrolling position to the latest label
                  canvas.yview_moveto(1.0)

            # Enable the "Display All" button after the function is done
            displayAll.config(state="normal", text='Display All', fg='black', bg='white')

      #Disable the "Check for updates" button before starting the thread
      displayAll.config(state="disabled", fg='white', text='Processing...', bg='grey')

      #Start the function in a separate thread
      threading.Thread(target=display_all_packages_worker).start()

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
      global labels_frame, canvas, statusLabel, entryFrame, updateAll, update, checkForUpdates, displayAll, uninstall, install, countPackages

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

      #Console Frame
      consoleFrame = Frame(topMainFrame, relief=None, width=self.appWidth, bg='green')
      consoleFrame.grid(row=0, column=0, columnspan=2, sticky='nsew') 
      topMainFrame.grid_columnconfigure(0, weight=1) 
      topMainFrame.grid_columnconfigure(1, weight=0)  #Set weight for the second column to 0
      topMainFrame.grid_rowconfigure(0, weight=1)  #Responsive height for the console frame

      #Create a canvas in the consoleFrame
      canvas = Canvas(consoleFrame, bg='pink')
      canvas.grid(row=0, column=0, sticky='nsew')

      #Add a vertical scrollbar for the canvas
      canvas_scroll = Scrollbar(consoleFrame, command=canvas.yview, orient=VERTICAL)
      canvas_scroll.grid(row=0, column=1, sticky='ns')
      canvas.config(yscrollcommand=canvas_scroll.set)

      #Create a frame inside the canvas for the labels
      labels_frame = Frame(canvas, bg='pink')
      canvas.create_window((0, 0), window=labels_frame, anchor=NW)

      #Update the canvas scroll region when labels_frame size changes
      labels_frame.update_idletasks()
      canvas.config(scrollregion=canvas.bbox(ALL))

      consoleFrame.grid_rowconfigure(0, weight=1)  #Make canvas expand vertically
      consoleFrame.grid_columnconfigure(0, weight=1)  #Make canvas expand horizontally

      #Bottom buttons frame
      bottomButtonsFrame = Frame(bottomMainFrame, relief=None, width=self.appWidth * 0.7, height=200, bg='blue')
      bottomButtonsFrame.grid(row=0, column=1, sticky='nsew')
      bottomMainFrame.grid_columnconfigure(1, weight=7)
      bottomMainFrame.grid_rowconfigure(0, weight=1) 

      bottomMainFrame.grid_columnconfigure(1, weight=4)
      bottomMainFrame.grid_columnconfigure(0, weight=1)
      bottomMainFrame.grid_propagate(False)

      
      #Create buttons 3x3 grid layout
      displayAll = Button(bottomButtonsFrame, text="Display all", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2', command=lambda: AppFunc.display_all_packages(self))
      displayAll.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
      
      checkForUpdates = Button(bottomButtonsFrame, text="Check for updates", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2', command=lambda: AppFunc.get_outdated_packages(self))
      checkForUpdates.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
      
      updateAll = Button(bottomButtonsFrame, text="Update all", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2')
      updateAll.grid(row=0, column=2, sticky='ew', padx=5, pady=5)
      
      update = Button(bottomButtonsFrame, text="Update", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2')
      update.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
      
      install = Button(bottomButtonsFrame, text="Install", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2')
      install.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
      
      uninstall = Button(bottomButtonsFrame, text="Uninstall", bg="white", fg="#231942", font=('San Serif', 11), cursor='hand2')
      uninstall.grid(row=1, column=2, sticky='ew', padx=5, pady=5)

      #Make buttons expand both horizontally and vertically
      for col in range(3):
         bottomButtonsFrame.grid_columnconfigure(col, weight=1)
      for row in range(2):
         bottomButtonsFrame.grid_rowconfigure(row, weight=1)


      #Add LabelFrame and Entry in bottomMainFrame
      entryFrame = LabelFrame(bottomMainFrame, text='Package to install/uninstall/update:', font=('San Sarif', 11))
      entryFrame.grid(row=0, column=0, sticky='nsew')

      entry_package = Entry(entryFrame, bg='white', fg='black', font=('San Sarif', 11))
      entry_package.pack(padx=10, pady=5, ipady=5, anchor='nw', fill='x')

      statusLabel = Label(entryFrame, text=f'Good', fg='green', font=('San Serif', 11))
      statusLabel.pack(padx=10, pady=30, ipady=5, anchor='sw', fill='x')

      countPackages = Label(entryFrame, text='', fg='black')
      countPackages.pack()

      entryFrame.grid_rowconfigure(0, weight=1)  #LabelFrame takes the remaining vertical space


if __name__ == "__main__":
   AppGUI()
