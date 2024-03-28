import json

import pandas as pd
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships

import config


def load_f1_graph_data():

    # ---------------------------- Prepare data from CSV files ---------------------------- #

    # Prepare circuits data

    df_circuits = pd.read_csv(f"{config.ROOT_DIR}/data/circuits.csv")
    df_circuits = df_circuits.filter(["circuitId", "circuitRef", "name", "location", "country"])
    json_circuits = df_circuits.to_json(orient="records")
    dict_circuits = json.loads(json_circuits)

    # Prepare drivers data

    df_drivers = pd.read_csv(f"{config.ROOT_DIR}/data/drivers.csv")
    df_drivers = df_drivers.filter(["driverId", "driverRef", "number", "code", "forename", "surname", "dob",
                                    "nationality"])
    json_drivers = df_drivers.to_json(orient="records")
    dict_drivers = json.loads(json_drivers)

    # Prepare constructors data

    df_constructors = pd.read_csv(f"{config.ROOT_DIR}/data/constructors.csv")
    df_constructors = df_constructors.filter(["constructorId", "constructorRef", "name", "nationality"])
    json_constructors = df_constructors.to_json(orient="records")
    dict_constructors = json.loads(json_constructors)

    # Prepare races data

    df_races = pd.read_csv(f"{config.ROOT_DIR}/data/races.csv")
    df_races = df_races.filter(["raceId", "year", "round", "circuitId", "name", "date", "time", "quali_time"])
    json_races = df_races.to_json(orient="records")
    dict_races = json.loads(json_races)

    # Prepare qualifying data

    df_qualifying = pd.read_csv(f"{config.ROOT_DIR}/data/qualifying.csv")
    df_qualifying = df_qualifying.filter(["raceId", "driverId", "constructorId", "number", "position"])
    json_qualifying = df_qualifying.to_json(orient="records")
    dict_qualifying = json.loads(json_qualifying)

    # Prepare drivers results

    # - Merge driver results with status

    df_status = pd.read_csv(f"{config.ROOT_DIR}/data/status.csv")
    df_status = df_status.filter(["statusId", "status"])

    df_driver_results = pd.read_csv(f"{config.ROOT_DIR}/data/results.csv")
    df_driver_results = df_driver_results.filter(["raceId", "driverId", "constructorId", "number", "grid",
                                                  "position", "positionText", "positionOrder", "points", "laps", "time",
                                                  "milliseconds", "fastestLap", "rank", "fastestLapTime",
                                                  "fastestLapSpeed", "statusId"])

    df_driver_results = df_driver_results.merge(df_status, how="left", on="statusId")
    df_driver_results = df_driver_results.drop(columns=["statusId"])

    json_driver_results = df_driver_results.to_json(orient="records")
    dict_driver_results = json.loads(json_driver_results)

    # Prepare constructor results

    df_constructor_results = pd.read_csv(f"{config.ROOT_DIR}/data/constructor_results.csv")
    df_constructor_results = df_constructor_results.filter(["raceId", "constructorId", "points"])
    json_constructor_results = df_constructor_results.to_json(orient="records")
    dict_constructor_results = json.loads(json_constructor_results)

    # ---------------------------- Create nodes ---------------------------- #

    # Connect to Neo4j
    graph = Graph(config.NEO4J_URI, auth=(config.NEO4J_USERNAME, config.NEO4J_PASSWORD))

    # Create circuits nodes
    create_nodes(graph.auto(), dict_circuits, labels={"Circuit"})
    count = graph.nodes.match("Circuit").count()
    print(f"Created {count} Circuit nodes")

    # Create drivers nodes
    create_nodes(graph.auto(), dict_drivers, labels={"Driver"})
    count = graph.nodes.match("Driver").count()
    print(f"Created {count} Driver nodes")

    # Create constructors nodes
    create_nodes(graph.auto(), dict_constructors, labels={"Constructor"})
    count = graph.nodes.match("Constructor").count()
    print(f"Created {count} Constructor nodes")

    # Create race nodes
    create_nodes(graph.auto(), dict_races, labels={"Race"})
    count = graph.nodes.match("Race").count()
    print(f"Created {count} Race nodes")

    # ---------------------------- Create relationships ---------------------------- #

    # Circuit -> HOSTED -> Race

    hosted = []
    for r in dict_races:
        circuit = r.pop("circuitId")
        race = r.pop("raceId")
        year = r.pop("year")
        rel_data = {"year": year}
        hosted.append((circuit, rel_data, race))

    create_relationships(graph.auto(), hosted, "HOSTED",
                         start_node_key=("Circuit", "circuitId"),
                         end_node_key=("Race", "raceId"))

    # Driver -> QUALIFIED_FOR -> Race

    qualified_for = []
    for r in dict_qualifying:
        driver = r.pop("driverId")
        race = r.pop("raceId")
        qualified_for.append((driver, r, race))

    create_relationships(graph.auto(), qualified_for, "QUALIFIED_FOR",
                         start_node_key=("Driver", "driverId"),
                         end_node_key=("Race", "raceId"))

    # Driver -> PARTICIPATED_IN -> Race

    participated_in = []
    for r in dict_driver_results:
        driver = r.pop("driverId")
        race = r.pop("raceId")
        participated_in.append((driver, r, race))

    create_relationships(graph.auto(), participated_in, "PARTICIPATED_IN",
                         start_node_key=("Driver", "driverId"),
                         end_node_key=("Race", "raceId"))

    # Constructor -> PUNCTUATED_IN -> Race

    punctuated_in = []
    for r in dict_constructor_results:
        constructor = r.pop("constructorId")
        race = r.pop("raceId")
        punctuated_in.append((constructor, r, race))

    create_relationships(graph.auto(), punctuated_in, "PUNCTUATED_IN",
                         start_node_key=("Constructor", "constructorId"),
                         end_node_key=("Race", "raceId"))


if __name__ == '__main__':
    load_f1_graph_data()
    print('Done!')
