# Database Design___content (2).pdf

## Page 1

 Image Banner-Slider Management
This section includes banners or sliders with images and captions.
Table: banners
Column Name Data Type
Description
id
int (Primary key) unique identiﬁer for each banner
image_url
varchar(255)
url of the banner image
title
varchar(150) 
Title or heading of the banner
description
text
Short Description or tagline on the banner
Order
int
Display Order for the slider.
Status
boolean
Active/Inactive status of the banner
Vision and Mission Section Management
Table name: vision_mission
Column Name
Data Type
Description
id
int (Primary key) unique identiﬁer for the section
vision_title
varchar(150)
Title for the Vision Section
vision_description
varchar(200)
Detailed Description of the Vision
mission_title
varchar(150)
Title for the mission  Section
mission_description varchar(200)
Detailed Description of the mission
last_updated
timestamp
Timestamp of the last update.
Statistic Management 
Table Name: statistic
Column Name Data Type
Description
id
int (Primary key) unique identiﬁer for the Statistic
label
varchar(100)
Title or Label for the statics (e.g Total number of student educated)
value
varchar(50)
Value of the Statics
order
varchar(150)
Display order of statistic.
status
varchar(50)
Active/inactive status of  Statistic [This is used to implement soft delete] 
 
Our Initiative Management
This section highlights the NGO’s initiatives or projects.
Table: initiatives
Column Name Data Type
Description
id
int (Primary key) unique identiﬁer for the Statistic
title
varchar(100)
Title or Label for the statics (e.g Total number of student educated)


## Page 2

description
varchar(200)
Value of the Statics
image_url
varchar(150)
Store the url of the image to be displayed in initiative.
order
int
Display order for Initiative
status
text
Active/inactive status of  Statistic [This is used to implement soft delete] 
Above tables are as per the Home designed in the Front end section. It is not mandatory for
the learner to use the same database table design, they may have diﬀerent number of
columns , diﬀerent number of tables as per the total number of sections taken on the home
page.
Intention of providing these table structures, is to provide knowledge of database tables to
the learner.


