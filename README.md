#Items Catalog Project

This project was developed using Flask. Flask is a light weight web framework written in python.   The code also utilizes [material design lite](https://getmdl.io).   


##Current Features

1. CRUD  
2. Oauth2 - Google Authentication
3. Cross site
4. Image Handling using raw url

##Environment

The environment leverages a Vagrant VM.   There is a shell script written by Udacity called pg_config.sh.  I have modified the original script to create the sportsvenue database.  You can still access the original script via pg_config.sh.bak (bak - stands for backup script)

If the script does not function properly, do the following command:
`cp pg_config.sh.bak pg_config.sh`

This will restore the original script.

###How to setup the Environment

1. Clone the github repo:
`git clone https://github.com/harushimo/fullstack-nanodegree-vm.git`

2. Type this command: `cd fullstack-nanodegree-vm/vagrant directory`

3. Run the command `vagrant up`.  This command will create a Vagrant file in your directory.

4. After the Vagrant VM is setup, you must type in the command: `vagrant ssh`

5. Run `python database_setup.py`.

The data is store in postgresql database.

There is a shared folder called vagrant inside the virtual machine.  You must type this command while in the VM: `cd /vagrant`

### setup database manually(if script fails)

```
sudo su - postgres
psql
CREATE DATABASE sportsvenue;
CREATE USER vagrant WITH PASSWORD 'vagrant';
GRANT ALL PRIVILEGES ON DATABASE sportsvenue TO sports;
\q
exit
```

For the create user, you can input any password you like.

##Running the application
When inside the virtual machine, run the following commands
```
cd fullstack/vagrant/catalog
python application.py
```
This will run an local instance of the application.  Type in the browser: 'https://localhost:5000'


Main Screen:
![Main Screen](../static/images/Main_page.png "Main Page")

click the login button.

Once Login, a new screen will show up with AddVenue and Logout

![User Screen](../static/images/authenicated_user.png "User Menu")

### Adding a venue
