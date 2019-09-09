# Document-Classification-Using-Wikipedia-Data

Note: Step1 and Step2 involve Data Collection and Data Preprocessing and they take a lot of time to process. Skip Step1 and Step2, if you want to run results immediately.

### Step 1:

Run preprocessing.py to use wiki API to access the wiki tree. Wiki tree is nothing but a tree data structure where the immediate children are 27 file categories.

### Step 2:

The final step in preprocessing requires cleaning wiki dump files to plain text. The last line in preprocessing.py runs wikiextractor.py.

Step2 is a mirror repo for the script by Giuseppe Attardi.
Please refer to the official repo if there any issues: https://github.com/attardi/wikiextractor

### Step3:

![categories Logo](/images/Distribution.png)

Now we have 27 categories and relevant 10k articles for each category. It becomes a classification problem. However, I initially used topic modeling (without categories/labels) and have run multiple supervised algorithms with different types of word embeddings.

The code is in Jupiter notebooks (Location: notebook folder).
