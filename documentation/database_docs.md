stat# /
* Uses classes to define tables within SQLAlchemy

# Users
* Users are saved when anyone enters the page 
* Fields:
    * unique id 
    * name
    * email

# Workers
* Workers are those who manage the prints and projects with the 3D printers
* Fields:
    * unique id
    * name
    * email
    * is_Admin
    * is_Active

# Project
* Details stored on the print project needed by a User
* Fields:
    * unique id
    * name
    * description
    * general_Link
    * for_Who
    * deadline
    * status
    * primary_Person

# Model
* Details stored on the specific model for a print project
* Fields:
    * unique id
    * project_ID (references project table)
    * status
    * count_Needed

# Print
* Details stored on the specific print needed by a User
* Fields:
    * unique id
    * name
    * base_Settings
    * core1
    * core2
    * material1
    * material2
    * est_Time
    * est_Material

# Print_Events
* Details stored on print events
* Fields:
    * unique id
    * type
    * when
    * who

# Print_Settings
* Details on settings set for specific prints
* Fields:
    * unique id
    * print_ID (references print table)
    * model_ID (references model table)
    * setting_ID (references settings table)
    * core
    * value

# Print_Models
* Details stored on the print models
* Fields:
    * unique id
    * print_ID (references print table)
    * model_ID (references model table)

# Settings
* Details stored on different settings
* Fields:
    * unique id
    * name

# Print_Comments
* Comments stored by workers made on the different prints
* Fields:
    * unique id
    * print_ID (references print table)
    * workers_ID (references workers table)
    * when
    * message

# Project_Comments
* Comments stored by workers on different projects
* Fields:
    * unique id
    * project_ID (references project table)
    * workers_ID (references workers table)
    * when
    * message

# Project_Comments
* Comments stored by workers on different models
* Fields:
    * unique id
    * model_ID (references model table)
    * workers_ID (references workers table)
    * when
    * message