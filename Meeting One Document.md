#### Meeting One Document

##### What is the aim of the service?

As there are various games in the Apple Store with too many parameters, it has become a problem for advertisers to choose a product that is worth to invest. Therefore, we design this service to provide the company with the app trend from the Apple Store. Through machine learning, the service can predict the number of installations of the application in the future, which is beneficial to the company's advertising.

##### What are the datasets? 

The dataset is 17K Mobile Strategy Games from kaggle. (https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games).

##### What is your communication channel? 

Slack. https://app.slack.com/client/TQ3DE5B24/CPQKRFSTC

##### What is your code repository?

We use Github repository. https://github.com/chenghao-ma/COMP9321

##### A very brief description of each member’s role in the project.

z5150150 Chenghao Ma: data processing and machine learning

z5152673 Yiwei Xue: Data cleansing and processing

z5119776 Zele Di: backend development (api)

z5196202 Shen Yan: backend development (api)

z5269658 Shoujian Dong: frontend design and development

##### Project documentation; correctly described use cases using notations, such as sequence diagrams, mock‐ups, or plain natural language; the method is optional. 

Our project will be seperated into two parts: backend and frontend. The backend api will be developed by python Flask framework and the frontend will be developed by ReactJS with Material UI. The UML graph and mock-ups can be found in our github repository.

###### User story:

In a scenario, Elijia is a manager, who is responsible for investigating the market of game planned to develop, can register his own account. After that, with entering the name and password to login the website, the Dashboard webpage will display some important attributes of the top10 17K Mobile Strategy Games currently. Additionally, this webpage will present some different diagrams of various data relationships. And then he presses the button of start engine of predictor at the left side of this page, the next webpage will ask him to provide the detail of game price, size, genre and player age range. Finally, the service will response the predicted downloads to him as the reference data at the bottom of the same page. 