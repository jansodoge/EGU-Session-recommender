import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from shiny import App, render, ui
import pandas as pd





# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample queries
#queries = [
#    "What is the weather today?",
#    "How to learn Python?",
#    "Best practices for data science.",
#    "What is the capital of France?",
#    "How to cook pasta?",
    # ... (other queries)
#]

dataframe_sessions = pd.read_excel("egu_session_descriptions.xlsx")
dataframe_sessions = dataframe_sessions.dropna(subset=['ID'])
dataframe_sessions = dataframe_sessions[dataframe_sessions['Abstract'] == 1]
dataframe_sessions = dataframe_sessions.reset_index(drop=True)
print("Number of rows in filtered_sessions:", len(dataframe_sessions))

queries = dataframe_sessions.Description
titles = dataframe_sessions.Title  
ids = dataframe_sessions.ID
ids = [int(num) for num in ids]

prefix = "https://meetingorganizer.copernicus.org/EGU25/session/"

# Create a new list with the URL prefix added to each number
urls = [f"{prefix}{num}" for num in ids]


# The column to display as results
# Precompute embeddings for the queries
query_embeddings = model.encode(queries)


# Define the UI
app_ui = ui.page_fluid(
    #ui.h3("EGU25 AI-session recommender", style = "margin-bottom: 80px; color: blue; background-color: lightgrey;"),
    ui.h3(
    "EGU25 Topic Similarity Adviser: experimental tool ", 
    style="margin-bottom: 60px; color: #2A9DF4; font-weight: bold; background-color: #F2F2F2; padding: 15px; border-radius: 8px; text-align: center;"),
  ui.card(
        ui.card_header("How to use"),
        ui.HTML("This experimental tool may help you find the most suitable session to submit to for the European Geosciences Union General Assembly 2025 by analysing the content of your abstract. Using advanced Natural Language Processing (NLP), it calculates how closely your abstract text matches each available session, across all disciplines and Programme Groups. The EGU25 topic similarity adviser is available until 13 January, 2025 13:00 CET. <br>  Rest assured: your data are not stored or documented in any way. <br> Please share your feedback with us at jan.sodoge(at)ufz.de  ")),

    
    ui.input_text_area("user_input", "", placeholder="Paste abstract", width = "100%"),
    ui.input_action_button("submit", "Get Session Suggestions ",  class_="btn btn-primary"),
    ui.HTML("<hr>"),
    ui.tooltip(  
        ui.input_action_button("btn", "About the results"),
        "Here are the most similar sessions for your abstract. They’re listed in no particular order, so please explore all our recommendations—don't just pick the first one! If you see only one or even no suggestion, it may mean there are few close matches. However, don't be discouraged! Submit your research to the session you feel best fits. Your intuition is often the best guide, and our tool is here to support, not replace, that judgment.",  
        id="btn_tooltip",  
        placement="right",  
    ),
    ui.output_ui("results"),
    ui.HTML(
    """
    <div style="margin-top: 100px;">
        <footer style="text-align: center; font-size: 14px; color: #666;">
            Application developed by Jan Sodoge. Project by the Computational Extreme Events Group at the Helmholtz-Centre For Environmental Research
        </footer>
    </div>
    """
    )


)

# Define server logic
def server(input, output, session):
    @output
    @render.ui
    def results():
        if input.submit():  # Note the () to call the input
            user_text = input.user_input()  # Note the () to call the input
            if user_text:
                # Compute the embedding for the user input
                user_embedding = model.encode([user_text])
                
                # Compute cosine similarities
                similarities = cosine_similarity(user_embedding, query_embeddings).flatten()
                
                # Get the indices of the top 5 similar queries
                top_indices = np.argsort(similarities)[-5:][::-1]
                top_indices = [idx for idx in top_indices if similarities[idx] > 0.2]
                
                # Prepare the results to display
                result_boxes = [
                ui.a(
                ui.div(
                titles[idx],
                style="padding: 10px; margin: 5px; border-radius: 5px; color: white; font-weight: bold; background-color: #4682B4;"
                ),
                href=urls[idx], target="_blank"  # Open in a new tab
                )
                for idx in top_indices
                ]
                #result_boxes = [ui.div(titles[idx],   style="padding: 10px; margin: 5px; border-radius: 5px; color: white; font-weight: bold; background-color: #4682B4;") for idx in top_indices]
                return result_boxes
        return ui.div("")

# Create the Shiny app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
