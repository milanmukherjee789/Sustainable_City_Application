cd existing_repo
git clone https://gitlab.scss.tcd.ie/smart_city/cloud_infrastructure.git
cd cloud_infrastructure
pip install -r requirements.txt (To install dependency)
cd cloud

Run python3 file_name to run all the three files.

First run:

python3 load_balancer.py
Next 

python3 autoscaling.py

And last 

python3 manager.py (in the same machine where java server is up.)

Change the port and ip of the machines in the code file
