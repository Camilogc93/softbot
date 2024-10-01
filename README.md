# System Architecture and Design Decisions

The development methodology consists of two components: the development of the DAG and its deployment.

## 1. Data and Problem Understanding

Every initial AI problem revolves around data. An online search was conducted for information related to teaching soft skills, their meanings, relevant documentation, as well as data on teaching and methodologies. The goal was to establish a knowledge base for implementing the RAG system.

## 2. Synthetic Data Generation (SGD)

Once the data on soft skills was gathered, those related to coaching and teaching were filtered out. This provided the necessary context for the chatbot's operation and created a dataset to assess the system to be implemented.

RAGAS was used as a tool to create synthetic data, generating questions and answers from a model (gpt4-mini) exposed to the context of the data.

The generation of a synthetic dataset aims to provide a quick evaluation baseline for the data, as no prior human-generated information exists for questions and answers relevant to the chatbot.

## 3. Fine-Tuning Embeddings

One of the foundations of a RAG system is embeddings. The better the representation of the data, the more effective the search and retrieval will be in the future.

Fine-tuning was performed on an open-source model that produced good results, incorporating insights drawn from PDFs on soft skills. The model was trained on questions and context to evaluate how information is retrieved, with tuning applied to all layers except the output.

## 4. Chunking Strategy

Chunking strategy description goes here.

## 5. Slack Integration Setup

### Step 1: Create a New Slack App

1. Go to [Slack API](https://api.slack.com/apps) and log in.
2. Click "Create New App," provide a name, select a workspace, and click "Create App."

### Step 2: Set up Your Bot

1. Under "Add features and functionality," select "Bots."
2. Click "Add a Bot User," set the name, and save.

### Step 3: Add Bot Permissions

1. Go to "OAuth & Permissions" in the sidebar.
2. Add bot token scopes like `app_mentions:read`, `chat:write`, and `channels:history`.

### Step 4: Install the Bot

1. In the sidebar, go to "Basic Information" and click "Install App."
2. Authorize the app.

### Step 5: Get the Bot Token

1. After installation, go to "OAuth & Permissions."
2. Copy the "Bot User OAuth Access Token" (`xoxb-...`) for use in your code.

## 6. Deploying the API

Once the API is deployed, enable the Events URL with the AppRunner URL.

### Next Steps

1. Install the app and save changes.
2. Add the bot to the desired channel.
3. Mention the bot in the channel to start interacting with it.

