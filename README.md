# Satisfaction Observer

**How positive (or negative) are tweets that people write about different topics?**

This application performs sentiment analysis on tweets posted with respect to different categories (e.g. heads of governments). The corresponding sentiment scores range on a scale from 0 to 100. The analyzed data can be displayed in a corresponding webapp based on [express.js](https://expressjs.com).

**Visit the application at [satisfaction.observer](https://satisfaction.observer)!**

## About

### How Does It Work?

The twitter data that are used for sentiment analysis are queried from the [Twitter Search API](https://developer.twitter.com/en/docs/tweets/search/overview/standard). Up to 1000 tweets per item are obtained in one cycle.

Subsequently, the tweets are cleaned: certain text fragments such as links and twitter handles are removed. Furthermore, the names of the items are replaced with generic tokens (such as "president" for a government leader) in order to eliminate systematic bias that might be originating from the items' names.

In the next step, the cleaned tweets are put through a text classification pipeline. Concretely, we utilize the [TextClassificationPipeline](https://huggingface.co/transformers/main_classes/pipelines.html#textclassificationpipeline) from the awesome [Hugging Face Transformers](https://huggingface.co/transformers/) framework. For sentiment analysis, the deep neural natural language processing model [BERT](https://arxiv.org/abs/1810.04805) is utilized. More specifically, we use the [nlptown/bert-base-multilingual-uncased-sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) model.

The pipeline outputs sentiment labels between 1 and 5 with a respective confidence score for each tweet. We normalize labels on a scale between 0 and 100 and calculate the average among all tweets for an item weighted by the confidence scores. For this calculation, only labels with a confidence score of at least 0.65 are considered.

### What Are the Limitations?
The classification labels should be taken with a big grain of salt! For now, the results are only for educational purposes and do not claim to represent the sentiment in a realistic way. Sometimes tweets that are clearly negative are classified as positive and vice versa. This might be due to the following – non-exhaustive – set of limitations:

* The model was fine-tuned on product reviews and not tweets. Thus, there might be linguistic discrepancies between the data the model was fine-tuned on and the data that is now used for classifications. I am currently working on a labeled dataset for tweets to further fine-tune the model and to investigate whether this will improve the predictive quality
* The model is particularly bad at classifying sarcasm – a common characteristic of tweets. The identification of sarcasm has been researched into but is still in its early stages.
* A very common observation is that tweets that are conveying positive sentiment might not necessarily incorporate a positive attitude towards the item mentioned and vice versa. For example, an author might compose a happy tweet because of a potential failure of a government leader. In this case, the sentiment would be positive, however the attitude towards the leader would be negative.

## Instructions
### Setup Python Environment

```
git clone git@github.com:jonasmue/satisfaction.observer.git
cd satisfaction.observer
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Query and Classify Tweets
```
# Recent Tweets
python main.py

# 'Mixed' Tweets (Recent and Popular Tweets)
python main.py --popular
```

### Setup and Run Express Server
```
cd display
npm install
npm debug
```