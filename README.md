# ReScope
Rescopes policies, configuration profiles, or static groups in Jamf Pro based on information provided by the user.

To use, first edit the config file with your information then run the program using:

./ReScope.py {policy,config,group} ids \[ids ...\]

Then (when prompted) enter a comma-separated list of computer ids followed by a comma-separatred list of computer group ids (alternatively you could write a file containing the information then redirect it in).
