import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Request
from functions import assintan_bot
import uvicorn

# Load environment variables from .env file
from dotenv import find_dotenv, load_dotenv
load_dotenv()
# Set Slack API credentials
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SE)RET")
SLACK_BOT_USER_ID = os.getenv("SLACK_BOT_USER_I")

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize FastAPI app
fastapi_app = FastAPI()
handler = SlackRequestHandler(app)



def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.getenv["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        print(response["user_id"])
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")


def my_function(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    response = text.upper()
    return response


@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("Sure, I'll get right on that!")
    response = assintan_bot(text)
    say(response)


@fastapi_app.post("/slack/events")
async def slack_events(request: Request):
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return await handler.handle(request)


# Run the FastAPI app
# if __name__ == "__main__":
   
#     uvicorn.run("main:fastapi_app", host="127.0.0.1", port=5000, reload=True)
