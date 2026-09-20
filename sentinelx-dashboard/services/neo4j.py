from neo4j import GraphDatabase


def get_driver(uri, username, password):
    """
    Create a Neo4j driver.
    """

    return GraphDatabase.driver(
        uri,
        auth=(username, password)
    )


def test_connection(uri, username, password):
    """
    Test the Neo4j connection.
    """

    driver = get_driver(
        uri,
        username,
        password
    )

    try:

        driver.verify_connectivity()

        return True

    finally:

        driver.close()


def get_node_summary(
    uri,
    username,
    password
):
    """
    Return node labels and counts.
    """

    driver = get_driver(
        uri,
        username,
        password
    )

    try:

        with driver.session() as session:

            result = session.run(
                """
                MATCH (n)
                RETURN labels(n) AS labels,
                       count(n) AS count
                ORDER BY count DESC
                """
            )

            return [
                {
                    "labels": record["labels"],
                    "count": record["count"]
                }
                for record in result
            ]

    finally:

        driver.close()


def get_graph_data(
    uri,
    username,
    password
):
    """
    Return actual Neo4j nodes and relationships.
    """

    driver = get_driver(
        uri,
        username,
        password
    )

    try:

        with driver.session() as session:

            result = session.run(
                """
                MATCH (a)-[r]->(b)
                RETURN
                    elementId(a) AS source_id,
                    coalesce(a.name, a.id, elementId(a)) AS source,
                    labels(a) AS source_labels,

                    type(r) AS relationship,

                    elementId(b) AS target_id,
                    coalesce(b.name, b.id, elementId(b)) AS target,
                    labels(b) AS target_labels
                """
            )

            return [
                {
                    "source_id": record["source_id"],
                    "source": str(record["source"]),
                    "source_labels": record["source_labels"],

                    "relationship": record["relationship"],

                    "target_id": record["target_id"],
                    "target": str(record["target"]),
                    "target_labels": record["target_labels"]
                }
                for record in result
            ]

    finally:

        driver.close()


def get_relationship_summary(
    uri,
    username,
    password
):
    """
    Return relationship type counts.
    """

    driver = get_driver(
        uri,
        username,
        password
    )

    try:

        with driver.session() as session:

            result = session.run(
                """
                MATCH ()-[r]->()
                RETURN type(r) AS relationship,
                       count(r) AS count
                ORDER BY count DESC
                """
            )

            return [
                {
                    "relationship": record["relationship"],
                    "count": record["count"]
                }
                for record in result
            ]

    finally:

        driver.close()