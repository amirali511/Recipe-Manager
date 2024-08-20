"""
Created by Amirali Rahmani Vatan Khah for CS50p 2023 final project.
A Gtk4 program for managing recipes.
Email address : amiralivatankhah3@gmail.com
"""
"""
Important note about the CSV file: 
The csv file can't be empty and MUST contain some values except the headers. 
So the default value is {"name" : "CS50", "briefExplan" : "Python"}
"""





# Importing the required libraries
import csv
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  



# Functions for working with the CSV file
## Reading Data from the file
def readData(file):
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        l = []
        for line in reader:
            l.append(line)
        return l
      
      
            
## Adding data to the csv file            
def addData(file, data):
    with open(file, "a") as f:
        writer = csv.DictWriter(f, ["name", "briefExplan"])
        writer.writerow(data)
     
     
## Removing data from the csv file        
def removeData(file, data):
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        newData = []
        for row in reader:
            if row["name"] != data:
                newData.append(row)
                
    with open(file, "w") as f:
        writer = csv.DictWriter(f, ["name", "briefExplan"])
        writer.writeheader()
        writer.writerows(newData)
        
  
  
# Main Window        
class Win(Gtk.ApplicationWindow):
    
    # Constructor
    def __init__(self, application):
        super().__init__(application=application)
        
        
        # Making the tile bar and add menu button
        header = Adw.HeaderBar()
        self.set_title("RecMan")
        self.set_titlebar(header)
        menu = Gtk.MenuButton()
        popOver = Gtk.Popover()
        menu.set_popover(popOver)
        header.pack_end(menu)
        
        
        # Add and remove buttons
        addLabel = Gtk.Label()
        addLabel.set_text("Add a recipe")
        rmLabel = Gtk.Label()
        rmLabel.set_text("Remove one of the existing recipes")
        addRecipeButton = Gtk.Button(label="+")
        addRecipeButton.connect("clicked", self.newRecipe)
        removeRecipeButton = Gtk.Button(label="-")
        removeRecipeButton.connect("clicked", self.rmRecipe)  
        Buttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        Buttons.append(addRecipeButton)
        Buttons.append(addLabel)
        Buttons.append(removeRecipeButton)
        Buttons.append(rmLabel)
        popOver.set_child(Buttons)

        
        # Reading datas from our recipe file
        datas = readData("db.csv")
        # making a grid for the data
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.set_child(grid)
        
        # Adding the frames of data to the window
        top = 0
        cnt = 0
        for data in datas:
            frame = Gtk.Frame(label=data["name"])
            description = Gtk.Label()
            description.set_text(data["briefExplan"])
            frame.set_child(description)
            frame.set_hexpand(True)
            frame.set_vexpand(True)
            grid.attach(frame, datas.index(data) % 3, top, 1, 1)
            cnt += 1
            if cnt % 3 == 0:
                top += 1
        
        
        
    # Addding a new recipe    
    def newRecipe(self, addRecipeButton):
        addRecipeWin = NewRecipeWin(self.get_application())
        addRecipeWin.present()
        return
     
     
    # Remove recipes 
    def rmRecipe(self, removeRecipeButton):
        rmRecipeWin = RemoveRecipeWin(self.get_application())
        rmRecipeWin.present()
        return       


# Adding a recipe window
class NewRecipeWin(Gtk.ApplicationWindow):
    
    # Constructor
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title("New Recipe")
        # Adding a box layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)
        
        # Addding a label for the user
        label = Gtk.Label()
        label.set_text("Relaunch the program to see your recipe!")
        box.append(label)
        label.set_margin_start(5)
        label.set_margin_end(5)
        label.set_margin_top(5)
        label.set_margin_bottom(5)
        
        
        # Adding a single line text input for the name of recipe
        recipeTitle = Gtk.Entry()
        box.append(recipeTitle)
        recipeTitle.set_placeholder_text("Name")
        recipeTitle.set_margin_start(5)
        recipeTitle.set_margin_end(5)
        recipeTitle.set_margin_top(5)
        recipeTitle.set_margin_bottom(5)


        # Description of the recipe that is multiline
        recipeDescr = Gtk.TextView()
        box.append(recipeDescr)
        recipeDescr.set_margin_start(5)
        recipeDescr.set_margin_end(5)
        recipeDescr.set_margin_top(5)
        recipeDescr.set_margin_bottom(5)
        
        
        # OK button
        OKButton =  Gtk.Button(label="OK")
        OKButton.connect("clicked", lambda _: self.completeAddition(recipeTitle, recipeDescr))
        box.append(OKButton)
        OKButton.set_margin_start(5)
        OKButton.set_margin_end(5)
        OKButton.set_margin_top(5)
        OKButton.set_margin_bottom(5)
        
        
    # Writing data to the file and closing the window    
    def completeAddition(self, name, descr):
        exName = name.get_text()
        buffer = descr.get_buffer()
        exDescr = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        exDescr = exDescr.replace('\n', '.')
        addData("db.csv", {"name" : exName, "briefExplan" : exDescr})
        self.close()
        
  
# A window for removing data
class RemoveRecipeWin(Gtk.ApplicationWindow):
    
    # Constructor
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title("Remove a Recipe")
        
        # Creating a box layout for the label and text input and button
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)
        userAtt = Gtk.Label()
        userAtt.set_text("Relaunch the program to see the effects")
        box.append(userAtt)
        name = Gtk.Entry()
        box.append(name)
        name.set_placeholder_text("Name")
        name.set_margin_start(5)
        name.set_margin_end(5)
        name.set_margin_top(5)
        name.set_margin_bottom(5)
        delBtn = Gtk.Button(label="Delete")
        box.append(delBtn)
        delBtn.set_margin_start(5)
        delBtn.set_margin_end(5)
        delBtn.set_margin_top(5)
        delBtn.set_margin_bottom(5)
        delBtn.connect("clicked", lambda _: self.removeR(name))
    
    # On 'Delete' Button clicked
    def removeR(self, ti):
        text = ti.get_text()
        
        # Removing data if possible
        removeData("db.csv", text)
        self.close()

# Main app class
class App(Gtk.Application):
    
    # Constructor
    def __init__(self):
        super().__init__()
        self.connect("activate", self.app)
    
    # The main app
    def app(self, application):
        self.win = Win(application=application)
        self.win.present()
        return
        
    
# Running the app
def main():
    Application = App()
    Application.run()

if __name__ == "__main__":  
    main()
