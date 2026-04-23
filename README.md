

Access Tracker is built to print users information on a sticker or similar document during their visit to an organization. A user can be a visitor, vendor or employee. The system will work differently for new and old users. There will be separate custom admin side where they can view all details of user and host and edit data when necessary. 
INCASE OF NEW USER: They will have to fill up form about their info and  take a photo then proceed to printing
INCASE OF OLD USER: They will use their name and contact number to retrieve their previous info then proceed to printing

//INFRASTRUCTURE

There are 5 applications:

core: admin homepage, users homepage, choosing type of visit, choosing type of user

visitors: new user add, old user lookup, old user details, old user edit, capture photo [user details database, user history database]

access: access list is created, host list is accessed
printing: print preview handled, print function [host database, access list database]

admins: view user analytics, view admin analytics, view host analytics, view host details, add host details, edit host details, delete host, view user details, add user details, edit user details 
