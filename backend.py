from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

app = FastAPI()

TEMPERATURE = 0.2
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=TEMPERATURE, openai_api_key=api_key)



def generate_plot_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


@app.get("/query/")
def query_titanic(question: str):
    """Handles user queries about the Titanic dataset."""
    response = ""
    image_data = None

    if "percentage of passengers were male" in question.lower():
        male_percentage = (df['Sex'].str.lower() == 'male').mean() * 100
        response = f"{male_percentage:.2f}% of the passengers were male."

    elif "histogram of passenger ages" in question.lower():
        fig, ax = plt.subplots()
        sns.histplot(df['Age'].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title("Histogram of Passenger Ages")
        image_data = generate_plot_image(fig)

    elif "average ticket fare" in question.lower():
        avg_fare = df['Fare'].mean()
        response = f"The average ticket fare was ${avg_fare:.2f}."

    elif "passengers embarked from each port" in question.lower():
        fig, ax = plt.subplots()
        sns.countplot(x=df['Embarked'].dropna(), ax=ax)
        ax.set_title("Passengers by Embarkation Port")
        image_data = generate_plot_image(fig)

    else:
        response = llm([HumanMessage(content=question)]).content

    return {"response": response, "image": image_data}

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running!"}
