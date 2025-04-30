# Your-Personal-Fitness-Instructor (Changhao Wang (cxw762) | Shuai Fu (sxf477) | Victor Boyd (vwb6) | Julio Perez (jjp212))
# Online link: 
https://csds393yourpersonalfitnessinstr.netlify.app/

# Project Description:
Your Personal Fitness Instructor is a web based fitness and nutrition assisant designed for anyone interested in loosing weight, dieting and/or exercising 

This application will generate personalized diet and exercis plans for users with different weight goals and track  caloric intake and exercise activity. This project combines fitness science and data analysis and provide a platfrom for all different users. The project is uploaded by netlify with frontend and render for backend api calls. 

# Architecture
Frontend: Built with Vue.js and Pinia 

Backend: Flask (Python) API providing all fitness calculations and record tracking

Database: CSV document to store food data, and exercise data

[ User Interface (Vue.js) ] <---> [ Flask API Server (Python Backend Functions) ] <---> [ Database ]

# Getting Started / Installation
Project setup
Clone the Repository
```sh
git clone <https://github.com/Oscarainbow/Your-Personal-Fitness-Instructor/branches>
cd YOUR-PERSONAL-FITNESS-INSTRUCTOR
```

Backend Setup
Create and activate a virtual environment

```sh
python -m venv venv
```
source venv/bin/activate        # Windows users: venv\Scripts\activate

Install backend dependencies

```sh
npm install flask pandas flask-cors
```

Start the Flask server
python foodfunctions.py


# Vue(Frontend) Setup
    # Recommended IDE Setup

    [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

    Customize configuration

    See [Vite Configuration Reference](https://vite.dev/config/).

    Project Setup

    ```sh
    npm install
    ```
    Install pinia

    ```sh
    npm install pinia
    ```

    ### Compile and Hot-Reload for Development

    ```sh
    npm run dev
    ```

    ### Compile and Minify for Production

    ```sh
    npm run build
    ```

# Usage / Examples
From a non-technical user's perspective:

Sign Up / Log In
Create an account or log in to track your fitness journey

Input Profile
Enter basic details like weight, height, age, gender, and fitness goal

Get Your Plan
YPFI will generate a custom diet and exercise plan based on your target weight and timeframe

Daily Tracking
Log what you eat and your exercises daily. View how your activities align with your fitness goals

Progress Reports
View monthly progress reports, including calorie surplus/deficit and estimated weight changes

# Folder Structure
```sh
Your-Personal-Fitness-Instructor/
├── .vscode/
│   └── settings.json
├── data/
│   ├── exerciseData/
│   │   └── exercise_dataset.csv
│   └── foodData/
│       └── food.csv
├── public/
│   └── _redirects
├── VueApp/
│   ├── __pycache__/                    
│   ├── .vscode/
│   │   └── extensions.json
│   ├── dist/                           
│   │   ├── index.html
│   │   └── assets/
│   ├── node_modules/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   ├── base.css
│   │   │   ├── main.css
│   │   │   └── logo.svg
│   │   ├── components/
│   │   │   ├── icons/
│   │   │   ├── BMRCalc.vue
│   │   │   ├── ExercisePlan.vue
│   │   │   ├── HelloWorld.vue
│   │   │   ├── TheWelcome.vue
│   │   │   ├── WeightChangeCalc.vue
│   │   │   └── WelcomeItem.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── stores/
│   │   │   └── profileStore.js
│   │   ├── views/
│   │   │   ├── AboutView.vue
│   │   │   ├── ExercisesView.vue
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   └── ProfileView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── README.md
├── .gitignore
├── foodfunctions.py                  
├── index.html
├── jsconfig.json
├── package.json
├── package-lock.json
├── Procfile                          
├── README.md
├── requirements.txt                  
├── test.py
├── testing.md
└── annotated-SoftwareRequirementsSpecification.pdf
```


# Tech Stack 
Frontend: Vue.js, Pinia, HTML, CSS

Backend: Flask, Python

Database: CSV file connected with Python

Testing: pytest (Unit Testing)

Others: Pandas (data processing), Flask-CORS (cross-origin access)

# Contribution
```sh
Name	        Main Role
Victor Boyd     Frontend Development (Vue Layout, BMR Calculator)
Julio Perez     Frontend Development (Search Bar, Tracker, UI Design)
Shuai Fu        Backend Development Lead (Core Backend Functions and API Functions)
Changhao Wang   Database, Backend Functions, Testing 
```

# Development Retrospective
Mistakes:

Initially struggled with GitHub version control and merge conflicts

Delays in connecting Python Flask backend to Vue frontend due to misunderstanding of CORS and API calling

Remote deployment challenges led to development being focused on localhost

Improvements:

Start Git integration training earlier

Assign a technical lead role to streamline API development and testing communication

Maintain an updated checklist for completed frontend/backend connections during milestones

# License
License – [ ]