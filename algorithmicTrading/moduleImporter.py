import os

def moduleImporter(modules_dir):
    # List files in directory
    dirs = os.listdir(modules_dir)
    print (dirs)
    # Import all
    for the_dir in dirs:
        splt = the_dir.split(".")[0] # Split dir and strip file ext.
        module = splt.replace(modules_dir,"") # 
        
