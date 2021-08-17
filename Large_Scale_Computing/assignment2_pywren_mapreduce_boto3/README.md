# Question 1
`(a)`

[see code in Q1.jpynb]

The original serial version takes 1606.04 seconds (around 27 minutes) to scrape the books, my parrallel version (with batch size from 5-145) takes 19.53 - 38.05 seconds to finish the task. The best performance, 19.53s, is achieved by using a batch size of 35 books and is around 85 times faster than the original code.

![Figure 1](https://github.com/lsc4ss-s21/assignment-2-YileC928/blob/main/plot_Q1.png)

Potential bottle necks:
- There is still a serial portion of the code (e.g., write data to SQL database) that cannnot be effectively paralellized.
- Currently, the maximum timeout window for each AWS Lambda function is 15 minutes, and the maximum number of concurrent workers 3000. If we are dealing with much larger size of book dataset, it may be a problem. [source: https://aws.amazon.com/about-aws/whats-new/2018/10/aws-lambda-supports-functions-that-can-run-up-to-15-minutes/#:~:text=You%20can%20now%20configure%20your,Lambda%20function%20was%205%20minutes.]
- AWS Lambda does not offer GPU backends. The Pywren  solution may not work most effective with utterly computationaly intensive tasks.

`(b)`

We would want to scale up the SQLite relational books database to one of the large-scale database solutions on AWS when:
- The database size is too large for local storage and needed to be stored and scaled in cloud.
- Multiple collaberators and readers of the project would like to update and access the database simultaneously. The 'availability' and 'consistency' of large-scale database would help to do that. 
- If we want to ensure disaster recovery (which is made possible by 'partitions')

For this application, I would recommend my group to use **DynamoDB**:
- The project scrapes books every 24 hours: DynamoDB is scalable ('infinite' storage) and flexible.
- The project is collaberative, colleagues may need to access the data at any time: DynamoDB has high through put and  performs well on availability. 
- Books scraping is based on the book ids stored in the database, which requires fast access: DynamoDB could do fast lookups because of its key-value pair hash table structure. 
- Nevertheless, DynamoDB also has several limitations. It takes time to sychronize updates so that consistency is not ideal, and complicated queries are normally quite expensive. I think these are not serious issues in this case, as we could perform analysis on the data collected later on, and we do not require intensive queries on the database for this task (which is mainly about storage and reads/writes).

**Relational database** (e.g., MySQL via RDS) could also be an option:
It emphasize on consistency and is ideal to perform fast light queries. We can also create read-replicas to deal with user traffic. However, RDS has limits on scalability and availability, so that if we are dealing with large size of data, RDS may not be most well-suited for the task.

Compare with other solutions:

- **S3** is good at storing large, raw and unstructured data but is difficult to perform atomic operation (as data is stored as objects instead of data points)
- **Redshift** enables big queries against big data (e.g., for analytical dashboard) but is not optimal for granular update and insertion.

# Question 2
[see code in Q2.jpynb and Q2.py]

The top ten most used words are: [2002, "with"], [2147, "that"], [2513, "her"], [3136, "is"], [4348, "in"], [6096, "to"], [7088, "a"], [7882, "of"], [8705, "and"], [13156, "the"]

# Question 3
[see code in Q3.jpynb]

Below is the printed message while running consumer.py in the EC2 command line interface.
![Figure 2](https://github.com/lsc4ss-s21/assignment-2-YileC928/blob/main/EC2_print%20message.png)

Below is the stock price alert email I received when the price went below 3.
![Figure 3](https://github.com/lsc4ss-s21/assignment-2-YileC928/blob/main/Email_Alert.png)

# Question 4

**Group members**: Boya Fu, Yile Chen, Fengyi Zheng

**Social science research problem:**

2020 is all about Covid-19. This unprecedented global pandemic has changed everyone's daily normal. We have seen that, in the United States, many governors like Andrew Cuomo of New York State published COVID related content such as policy guidelines on Twitter. For this project, we would like to explore political communications of state leaders as well as CDC on twitter during the pandemic, and perhaps also, how it is related to the change of the number of COVID infected cases and deaths. The buck of the project would be a content analysis of collected tweets.


**Role of Large-scale computing methods:**

We will collect tweets from state governors and the CDC over the period of COVID-19 pandemic, and conduct content analysis (e.g., topic modeling) and visualization (e.g., word cloud). The project will benefit from large-scale computing methods from three aspects. First, parallel solutions of the Twitter scraping process are expected to significantly improve the efficiency of data collection. With large amounts of textual data, we may also parallelize the preprocessing part (e.g. Tokenization, Stemming, and Lemmatization) and thus accelerate the data cleaning process. Finally, the high performance of large-scale methods enables us to further expand the topic with a larger scale of input data and more tuning and tests on model performance.

**Division of work & Timeline:**
- Collect Data (Week8): Fengyi
- Preprocess (Week8): Boya
- Content Analysis (Week9): Boya, Yile
- Visualization (Week9): Yile
- Presentation and report rewriting (Week10): Boya, Yile, Fengyi

Any suggestion and critiques are welcomed!
