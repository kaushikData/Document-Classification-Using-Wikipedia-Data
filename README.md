

# Document-Classification-Using-Wikipedia-Data

Note: Step1 and Step2 involve Data Collection and Data Preprocessing and they take a lot of time to process. Skip Step1 and Step2, if you want to run results immediately.

### Get Data: https://drive.google.com/drive/folders/1VIJYdcrYwBsicdyf3pbUIzSxjJFpwSGS?usp=sharing 
The data size is huge and please access the preprocessed wiki data from the google drive 

### Step 1:

Run preprocessing.py to use wiki API to access the wiki tree. Wiki tree is nothing but a tree data structure where the immediate children are 27 file categories.

### Step 2:

The final step in preprocessing requires cleaning wiki dump files to plain text. The last line in preprocessing.py runs wikiextractor.py.

Step2 is a mirror repo for the script by Giuseppe Attardi.
Please refer to the official repo if there any issues: https://github.com/attardi/wikiextractor

### Step3:

![categories Logo](/images/Distribution.png)

Now we have 27 categories and relevant 10k articles for each category. It becomes a classification problem. However, I used topic modeling (without categories/labels) and have run multiple supervised algorithms with different types of word embeddings.

The code is in Jupiter notebooks (Location: notebook folder).

It is difficult to come up by a high accuracy model which classifies all 27 labels.  

1. Base Supervised Wiki Model (For all 27 categories) - Model Accuracy is about 50 % (Low)
    - Multiniomial Naive Bayes
    
2. Multiple Supervised Models with different word embeddings (for randomly selected 10 categories of 27 categories)
    - Multinomial Naive Bayes
    - Support Vector Machine
    - Logistic Regression
    - Logistic Regression + Word2Vec 
    - Deep Neural Network with Cross Entropy Loss and Adam Optimizer
    
3. Topic Modelling

Final model gave below result for IMDB profile of Actor Jackie Chan.

![categories Logo](/images/JC.png)
