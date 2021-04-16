# social-media-analysis-to-monitor-for-potential-illegal-wildlife-trafficking
Analyzing public social media posts using natural language processing techniques to detect potential illegal wildlife trafficking.

## What's the plan?

The idea is to monitor several popular social media sites for any potential illegal wildlife trafficking. This includes a host of activities from selling illegal ivory items to the purchase of live animals. Currently, only publically available tweets are monitored, but plans to extend to other social media sites are in place. 

There are 7 different types of animals/animal products being which are being monitored. Each animal (elephants, pangolins, bears, cats, etc.) has its own dedicated MySQL database in which scanned tweets which contain keywords specific to the sale of the selected animal/animal products are stored. Tweets are then read-out, cleaned (removing invalid characters, lemmatizing, etc.), and separated into bigrams (see Xu Q, et al). Topic modelling is then applied based on these bigrams to find posts that are suspected of promoting/advertising illegal wildlife trade. Additionally, any media published with the suspected tweet is stored for further analysis. 

The end goal behind this project is to detect suspicious posts and report the posts to the relevant social media company and to the relevant authorities.

## Motivation behind the project?

This project was stronly influenced by the following paper by Xu, et al:

Citation: Xu Q, Li J, Cai M and Mackey TK (2019) Use of Machine Learning to Detect Wildlife Product Promotion and Sales on Twitter. Front. Big Data 2:28. doi: 10.3389/fdata.2019.00028

and by the follwing TRAFFIC report by Xiao Yu and Wang Jia:

Moving targets: Tracking online sales of illegal wildlife products in China, available at (https://www.traffic.org/site/assets/files/2536/moving_targets_china-monitoring-report.pdf)
