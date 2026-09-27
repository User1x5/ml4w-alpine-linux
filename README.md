# ml4w-alpine-linux
A Python script which installs ml4w libraries into alpine linux and the ml4w dotfiles since the ml4w devs didnt
This script as said, installs the needed files to install ml4w in alpine linux, Since it uses musl

Please check [the disclaimer](#disclaimer) before executing the script (i had to fix this 2 or 3 times now)

# Requirements
A Working alpine linux edge install
At least 4 gb of ram

install git and python3, Since you have to clone this

`apk add git python3`

# Instructions
Clone the repo:

`git clone https://github.com/User1x5/ml4w-alpine-linux.git`

Run the script:

`python3 ml4w-alpine.py`

# Disclaimer!
Please but **PLEASE** have at least **4gb of ram** and report the bugs, i developed everything in an arch linux machine, So contribute by reporting anything that goes wrong

This script might break your instalation as it is intended to run on fresh alpine linux edge install



# Credits & Licensing

This project modifies and extends the original dotfiles created by **ML4W**. It is an independent project and is **not affiliated with, endorsed by, or associated with ML4W** in any way.

### License & Attribution
* **Original Work:** [ML4W Dotfiles](https://github.com/mylinuxforwork/dotfiles)
* **License:** This project is distributed under the **GNU General Public License v3.0 (GPL-3.0)** in compliance with the original upstream license. 

### How it Works
This script functions by cloning the official ML4W dotfiles and safely merging them into the user's `/home/` directory alongside their personal configurations.

### Contact
For any copyright inquiries, licensing questions, or removal requests, please contact me directly at **user2xemail@gmail.com**.
