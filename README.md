Productionizing ML: build your own search engine

# Build your own search engine
There are many ways to put your data science work into production. But there is one thing they all have in common. It never comes easy. Every now and then you come across a pragmatic approach that is simple and works in standard occasions. I’m about to explain one of these. The use case we’re covering is building a private google like search engine and interface to query news articles about Covid-19. The dataset contains 550K articles scraped from the web. The dataset was provided by [Aylien](https://aylien.com/coronavirus-news-dataset/).

![](img/covid-19-search.gif)

To get to this point we need an **analytics engine** to rank the documents we want to search through. We will use [Azure Cognitive Search](https://pypi.org/project/azure-search-documents/), but you could also choose alternatives such as [Elasticsearch](https://elasticsearch-py.readthedocs.io/en/master/). Also we must have a **user interface** to interact with the search engine, and to display results. We choose [Streamlit](https://www.streamlit.io/).Eventually we need to deploy the solution somewhere, and possibly limit access to it with some **access management**. We decided to go with docker, as it is cloud agnostic. In this example however, we deploy the docker image with Azure App Services. With Azure Active Directory your can limit access to people within your network for example. 

The infrastructure will look something like this:
![](img/infra.png)

## Dependencies
To build your own search enging you must have an [Azure subscription](https://azure.microsoft.com/en-us/free/) and create an [Azure Cognitive Search service](https://docs.microsoft.com/en-us/azure/search/search-create-service-portal). Follow the links to get set up.
Additionally you need to install [Docker](https://docs.docker.com/get-docker/) to run your solution on your machinie.

## Setting up the API
* Follow the [Manual](https://docs.microsoft.com/en-us/azure/search/search-create-service-portal) to create the service

* Read the [API documentation](https://pypi.org/project/azure-search-documents/#adding-documents-to-your-index) better understand the search engine.

## Setting up environment variables
To make sure your credentials do not end up in your code repositories, add your endpoint and secret from the search service to your environment variables (get them from the [azure portal](https://portal.azure.com/) or [Azure CLI](https://docs.microsoft.com/en-gb/cli/azure/install-azure-cli?view=azure-cli-latest))

I work on mac and added the following lines to my .bash_profile file. 
```
export ACS_API_KEY=<admin-key>
export ACI_ENDPOINT=<service url>
```
To make sure that they're loaded in your terminal run:
```
source ~/.bash_profile
```
If you work on a different Operating System, adding the environment variables might be different.


## The code
In ten steps, we will explain how to get your search engine running. The code can also be found in the Clone this example from the [repository](https://github.com/godatadriven/build-your-own-search-engine).

### Step 1: Create your environment file
Before we write any code, we will specify our dependencies in an environment file. We will use this file to let conda install the required dependencies in our Docker image later. Add the following to the #demo-environment.yml

## NEEDS REWRITE

### Step 2: Create your documents file
We want our search index to help us find relevant documents. For this tutorial, we are going to index information about hotels, but this can be any type of information.

## NEEDS REWRITE

### Step 3: Create your index file
The search API requires a predefined index. In this index you specify which fields can be inspected in the documents that you will upload. You can also state the data types, how text fields should be analyzed and many more optios. We must define the index based on the documents that we want to index. For now, just create the hotel_index.py with the following code:
## NEEDS REWRITE

### Step 4: Create your initialization script
Uptil now, the search API does not know about the index and the documents yet. Therefore it must be initialized. We will first initalize the index, and then upload our documents to the search engine. It will then index the documents according to the index that you provided. Create the initialize_acs.py as follows:

## NEEDS REWRITE

To initialize the API, run the file
```
python my-search-engine-demo/search.py
```

### Step 5: Create your user interface script
For the user interface, we want a search bar, and a list with tanked results. We will create them with Streamlit. To connect the interface with the API, we will connect to the search API and send the search query to it. The results that come back will be rendered as a dataframe. To replicate the UI, create the user_interface.py as follows: 

To test if everything is working, you can run the app locally:
```
conda env create -f environment.yml
conda activate my-search-engine-demo
streamlit run my-search-engine-demo/user_interface.py
```
### Step 6: Create your Dockerfile
Now we've tested our app locally and verified that everything is working it's time to make it deployable. We will create a docker image where we install the dependencies and our app. 

## NEEDS REWRITE

### Step 7: Run your application
To build the docker image run:

```
docker build --build-arg BUILDTIME_ACS_API_KEY=${ACS_API_KEY} --build-arg BUILDTIME_ACS_ENDPOINT=${ACS_ENDPOINT} --build-arg BUILDTIME_SA_CONN_STR=${SA_CONN_STR} -t my-search-engine-demo:latest .
```

To run the image in a docker container:
```
docker run -p 80:80 my-search-engine-demo:latest
```




### Step 8: Test your application
Your application should now be running on localhost:8501. When you navigate there you should see something like this:
![user interface](img/user_interface.png)

You can enter queries in the search bar, and the results will be returned in the interface.


### Step 9: Deployment
[Deploy and run a container app service](https://docs.microsoft.com/en-us/learn/modules/deploy-run-container-app-service/)
Add the image to Azure container registry
Create a web app based on the image
Put it behind active directory.

Create an [azure container registry](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal):

tag your image with the login server/image name:tag

```
docker tag SOURCE_IMAGE[:TAG] {login server}/{image name}:{tag}
```

```
docker build --build-arg BUILDTIME_ACS_API_KEY=${ACS_API_KEY} --build-arg BUILDTIME_ACS_ENDPOINT=${ACS_ENDPOINT} --build-arg BUILDTIME_SA_CONN_STR=${SA_CONN_STR} -t markplayground.azurecr.io/covid-19-search:latest .
```

```
docker push markplayground.azurecr.io/covid-19-search:latest
```

```
docker run -p 8080:8080 markplayground.azurecr.io/covid-19-search:latest
```

docker tag SOURCE_IMAGE[:TAG] {login server}/{image name}:{tag}

at access keys: 
1) enable admin
2) Get the username and password

login in your terminal
```
docker login <<servername>> 
```

Now push your image to the container registry:
```
docker push server/image name:tag
```



### Limitations
* The functionality of your app is limited to the functionality that streamlit provides.
* The solution is intended for a limited audience and limited loads. Scalability is therefore limited.
* There is no monitoring in place 


### Do it yourself!
Obviously, with three documents, this is only the start. Clone this example from the [repository](https://github.com/godatadriven/build-your-own-search-engine) and adjust the index and documents to match your requirements. Play around with the search api to finetune your results and you should have your own search engine up and running in no time!

Also, when we look at our approach from a higher level, you might notice that you could replace the analytics engine with something else. A different python package for example. At GoDataDriven we often build specific python packages for our clients, making this approach applicable to multiple use cases.
The same is true for the interface. For now we used Streamlit, but you can replace this with different interfaces when your requirments demand so. 

# Conclusion
In this tutorial, we've showed that it is possible to build a simple analytics engine with and interface with python. We've also shown that deploying it as a minimal viable product is not too complex when we use Azure App Services. In the process we've seen to use Azure Cognitive Search to build your own search engine. You can change the analytics engine, with any python package or API

I hope that you will put this tutorial to creative use in the future!

Good luck!


