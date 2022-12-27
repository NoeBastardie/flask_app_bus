# airflow_gcp_dbt_flask_project
Project made by Noe Bastardie in december 2022.

/!\ 

This readme describe the general approach and all the steps of the project --> This repo only contains the code of the step 3 (flask app) !


/!\ 


# Goal :
- Create a basic flask app that displays a folium map which contains real time position of bus (bus that are impacted by an incident on their route will be directly identifiable).

# Approach :


(1) Extract bus datas (JSON) and import them into BigQuery using Airflow 

(2) Create a new BQ table with all the informations needed using DBT

(3) Create the app using Flask and Folium.


# Data lifecycle :


Washington bus data (JSON) --> Airflow dag (step 1) --> Cloud Storage --> Airflow dag (step 2) --> BigQuery --> DBT --> BigQuery --> Flask app

# Data sources :
- Washington Metropolitan Area Transit Authority API : https://developer.wmata.com/docs/services/ :
  - incidents : https://developer.wmata.com/docs/services/54763641281d83086473f232/operations/54763641281d830c946a3d75
  - bus positions : https://developer.wmata.com/docs/services/54763629281d83086473f231/operations/5476362a281d830c946a3d68
  - trains datas also available there

# Stack :
- Airflow (extract, (transform), load)
- GCP (storage + BigQuery) 
- DBT (transform)
- Flask (app web)

# Languages :
- Python
- Bash
- SQL
- yaml
