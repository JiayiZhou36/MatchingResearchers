# MatchingResearchers
Prototyping ways to promote interdisciplinary research through author matching.

The project uses Duke Scholars’ data to build a model that provides pair matching for successful interdisciplinary research, and to draft a proposal for the design of experiments once the matching model is finished.


## Data Source
"Scholars@Duke is a research discovery system featuring the research, scholarship, and activities of Duke faculty, graduate students, and academic staff."

[https://scholars.duke.edu/](https://scholars.duke.edu/)

Duke Scholars GraphQL API
https://oit.duke.edu/service/streamer/

## Two Modeling Approaches
Once both teams have reached their results, a research proposal for the experimental design will be drafted, with the potential to proceed on to platform development.

### Observational Network Analysis Team:
This team will focus on cleaning and feature engineering the data, studying the network, and observing factors that may lead to successful interdisciplinary research.

We plan to use data from individuals, including information on citations, co-authorship, paper abstracts, and departmental collaborations. 

From studying the abstracts, each person can have their own embedding space. We can tokenize text chunks, calculate word frequencies, or use methods such as PCA or cosine similarity to analyze relationships between people in the network. Once the data is cleaned and processed, we can utilize social network analysis to identify communities, cluster faculty members, and predict potential connections based on the network model.

### Machine Learning Team:
This team will also focus on data cleaning and feature engineering, using features such as the frequency of interdisciplinary collaboration and citation counts. 

A predictive model will be designed and trained to study the factors that lead to successful interdisciplinary research. Based on this model, we can estimate the likelihood of collaboration and develop a matching tool to suggest potential researcher pairs in interdisciplinary fields.


## GraphQL Query
[Link to Duke GraphQL workspace](https://graphql.scholars.duke.edu/graphiql)

```
query PeopleWithTheirPublications {
  people(pageSize: 50, startPage: 1) {
    count
     pagingInfo {
 totalPages
 pageNumber
 }
    results {
      firstName
      lastName
      email
      primaryAppointment{
        title
      }

      publications(pageSize: 100, startPage: 1) {
        count
        results {
          id
          publication{
            title
            abstract
            allAuthors {
              fullList
            }
          }
      }
    }
    }}
}
```

## How to reproduce

1. Run [`Data_Design_withdate_1125_new.ipynb`](https://github.com/JiayiZhou36/MatchingResearchers/blob/main/Data_Design_withdate_1125_new.ipynb) That should create several .rds files on the main directory.
2. Run [`Embedding.ipynb`](https://github.com/JiayiZhou36/MatchingResearchers/blob/main/Embedding/Embedding.ipynb). This creates a similarity matrix inside the Embedding folder.
3. Run [`css_project_network_code.qmd`](https://github.com/JiayiZhou36/MatchingResearchers/blob/main/css_project_network_code.qmd) 
