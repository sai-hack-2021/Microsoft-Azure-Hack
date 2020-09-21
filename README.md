# Health Aid Prognosis Platform

## Problem to Solve :
	1. Reduce the patients in clinic who have Low covid Risk and Low Fever and connect with doctor remotely to just give prescriptions so that there is no need to come to hospital or any nearby clinic.
	2. Remotely monitor the paitents who have medium covid risk and Low Fever during home quarantine.

## Components:
The Platform  has overall 4 components : 
1. Frontend : React JS - *Hosted over MS Azure Virtual Machine platform.*
2. Backend  : Flask and MongoDB *API exposed on the virtual Machine platform*
3. Machine Learning Module Exposed as Microservice *Over Azure Container Instances*
4. Azure Bot Service: Forms the main interaction interface between the platform and the user. *built with Microsoft Healthcare Bot service*, It carefully collects and maps symptoms from users with much ease and coordinates between the various modules

**[View PPT](https://docs.google.com/presentation/d/1sP5DyX1s9E5kvmUoth2lh8EyMEjZrIjPrn2puZU9S3c/edit?usp=sharing)** <br>
**[View Platform](http://52.172.158.219/)**<br>
**[View Use cases Design](https://youtu.be/M3MK3y83tHQ)** : <br>
**[View Platform Demo](https://www.dropbox.com/sh/43hta6wrzubek4a/AABTOjeJ_31XOQOjgj2b46Fga?dl=1)**   <br>
**[View Screenshots](https://www.dropbox.com/sh/vowilit195yyfc8/AAAGQVMBQ8nGlTzfXFbSZVOLa?dl=1)** <br>
## User Credentials : For Login

1. User1
	 email : user1@gmail.com
	 password : test159
2. User2
	 email : user2@gmail.com
	 password : test159
3. User3
     email : user3@gmail.com
	 password : test159


## Scoring Model : Covid-19 Risk

- **Scoring Binned into 3 Categories** :
	-  High 
	- Medium 
	- Low 

1. The weights have been designed by carefully talking with domain experts and doctors who were treating covid patients 
2.  The model will also take into consideration about the area percentages which are divided into 3 km radius
3.  More Details about the scoring and **Decsion Making Scenarios** along with the machine learning model is given in the [Link.](https://docs.google.com/presentation/d/1Flq2x9tR15OR8lreEV-ZRMFGkN8BENEHF9KBmWlgWIo/edit?usp=sharing) 

	
	
## Machine Learning Model : Fever Classification 

- **Multi - class : Classification** : 
	- Viral
	- Bacterial 
	- Malarial
- **Data source** : Custom collected Data across various hospitals and clincs : 

1. Takes input of the symptoms of users 
2. Considers the probability of similar patterns of the user in the same area and takes into account of the percentage of the type of fever pattern
3. Takes into account of the similar patterns of the user classified as 
4. Demographic Seasonality Variations of past 15 days 


