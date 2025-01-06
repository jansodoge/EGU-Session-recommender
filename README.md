# EGU Session recommender webapp


This repository holds all necessary code and data to run a docker file for the "EGU Session recommender". A web application developed for the upcoming EGU General Assembly, a geo-science conference with more than 20,000 contributions. In order to help abstract authors find the right session (among more than thousand sessions) we worked together with the EGU and Copernicus to develop this app which uses natural language processing to recommend multiple fitting sessions based on the abstract a user pastes into the web app. 

The app works based on techniques described in greater detail [here](https://egusphere.copernicus.org/preprints/2024/egusphere-2024-3430/). It runs a Python shiny app so that embeddings for the user's abstract are directly computed with SBERT in Python on the web.
More information on the entire project are following soon.

