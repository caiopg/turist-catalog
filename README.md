# Tourist Catalog
This repository is the source code for a website which catalogs tourist attraction points in different countries. Users may login using Google and add new countries and attractions, as well as remove countries and attractions created by them.

## Preparing the environment
1. Install VirtualBox.
2. Install Vagrant.
3. Clone https://github.com/udacity/fullstack-nanodegree-vm
4. Using terminal, move to directory called vagrant found in the cloned repository.
5. Run command ```vagrant up```.
6. Pull github code from this repository.
7. Save code in vagrant directory in cloned repository.

## Usage
1. Using terminal, move to directory called vagrant found in the cloned repository.
2. Run command ```vagrant ssh``` from vagrant folder inside the cloned repository.
3. Move to /vagrant in virtual machine.
4. Run ```python3 dbsetup.py```.
5. (Optional!) Run ```python3 populatedb.py```. This step is done only if user wants to populate the server's database with some countries and attractions.
6. Run ```python3 webserver.py```.
7. Open your browser of preference and go to localhost:8000/ .
8. Have fun!
