
# F1 Graph (Python + Neo4j)

Project example for building a Graph Database using the Neo4j DBMS with Python language that contains Formula 1 historical data from 1950 to 2020.

Modeled data is a sub-set of this dataset: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020/


Nodes:
- *Circuit*
- *Race*
- *Constructor*
- *Driver*

Relationships:
- *Circuit --HOSTED--> Race*
- *Driver --CUALIFIED_FOR--> Race*
- *Driver --PARTICIPATED_IN--> Race*
- *Constructor --PUNCTUATED_IN--> Race*


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`ANEO4J_URI`
`NEO4J_USERNAME`
`NEO4J_PASSWORD`
## Pre-requisites

- Python version: 3.10.7
- Have an instance of Neo4j, if don't have it, then get started here: https://console.neo4j.io/
- Virtual environment with Poetry (https://python-poetry.org/docs/basic-usage/)


## Dependencies installation

```bash
  poetry install
```


## Appendix

- https://neo4j-contrib.github.io/py2neo/ - Py2neo is a client library and toolkit for working with Neo4j from within Python applications. I have used this library for load bulk data in order to have a big database for performing queries. Note: this one is currently deprecated by the developers.

- https://neo4j.com/docs/api/python-driver/current/ - Official python driver from Neo4j. (Work in progress for inserting individual nodes and relationships in the graph database).