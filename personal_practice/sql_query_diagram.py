import uuid
from copy import deepcopy
from typing import Optional

import graphviz
from sqlglot import exp, parse_one


class DML:
    def __init__(self, expression: exp.Expression, cte_alias: Optional[str] = None):
        self.expression: exp.Expression = expression
        self._cte_alias = cte_alias
        self.key: str = uuid.uuid4().hex

    @property
    def cte_alias(self) -> str:
        if self._cte_alias:
            return self._cte_alias
        return ""

    def __repr__(self):
        return self.expression.__repr__()


def extract_cte_dict(ast):
    cte_dict = {}

    for cte in ast.ctes:
        cte_dict[cte.alias] = []

    return cte_dict


def extract_dml_dict(ast):
    dml_dict = {}
    ctes = ast.ctes

    for cte in ctes:
        cte_alias = cte.alias
        dml = DML(cte.this, cte_alias)
        dml_dict[dml.key] = dml

    copied_ast = deepcopy(ast)
    if isinstance(copied_ast, exp.Select) and ast.args.get("with"):
        # Remove the WITH clause
        copied_ast.set("with", None)

    dml = DML(copied_ast)
    dml_dict[dml.key] = dml
    return dml_dict


def extract_table_set(ast):
    print(str(ast))
    tables = set()

    if hasattr(ast, "left"):
        tables.update(extract_table_set(ast.left))

    if hasattr(ast, "right"):
        tables.update(extract_table_set(ast.right))

    if from_table := ast.args.get("from"):
        tables.add(from_table.alias_or_name)

    if "joins" in ast.args:
        for join in ast.args["joins"]:
            tables.add(join.alias_or_name)

    return tables


def draw_dag(cte_dict, dml_dict):
    """Draw the DAG using graphviz."""
    dot = graphviz.Digraph(comment="CTE and Table DAG", node_attr={"shape": "box"})

    alias_key_dict = {}

    for key, dml in dml_dict.items():
        dot.node(dml.key, dml.cte_alias + "\n" + dml.expression.sql(pretty=True))
        if dml.cte_alias:
            alias_key_dict[dml.cte_alias] = dml.key

    for cte_alias, keys in cte_dict.items():
        for key in keys:
            dot.edge(alias_key_dict[cte_alias], key)

    dot.render("cte_dag", format="png", cleanup=True)
    return dot


if __name__ == "__main__":
    # Example SQL Query
    sql = """
    WITH cte1 AS (
        SELECT a, b FROM mytable
    ),
    cte2 AS (
        SELECT c FROM table2
    ),
    cte3 AS (
        SELECT cte1.a, cte2.c FROM cte1 INNER JOIN cte2 ON cte1.b = cte2.c
    ),
    final_result AS (
        SELECT cte1.a, cte3.c FROM cte1 INNER JOIN cte3 ON cte1.a = cte3.a
    )
    SELECT * FROM final_result;
    """

    sql2 = """
    WITH cte1 AS (
        SELECT a, b, COUNT(*) OVER (PARTITION BY a) AS count_a
        FROM mytable
    ),
    cte2 AS (
        SELECT c, d, ROW_NUMBER() OVER (PARTITION BY c ORDER BY d DESC) AS row_num
        FROM table2
        WHERE d > 10
    ),
    cte3 AS (
        SELECT cte1.a, cte2.c, cte1.b
        FROM cte1
        INNER JOIN cte2 ON cte1.b = cte2.c
        WHERE cte1.count_a > 1
    ),
    cte4 AS (
        SELECT a, b, c, SUM(b) OVER (PARTITION BY a) AS sum_b
        FROM (
            SELECT cte3.a, cte3.b, cte3.c
            FROM cte3
            WHERE cte3.c IS NOT NULL
        ) AS filtered_cte3
    ),
    cte5 AS (
        SELECT cte4.a, cte4.c,
               CASE 
                   WHEN cte4.sum_b > 100 THEN 'High'
                   ELSE 'Low'
               END AS category
        FROM cte4
    ),
    final_result AS (
        SELECT cte1.a, cte5.c, cte5.category, COALESCE(cte1.b, 0) AS b
        FROM cte1
        LEFT JOIN cte5 ON cte1.a = cte5.a
        WHERE cte1.count_a < 2
        UNION ALL
        SELECT a, c, category, b
        FROM cte5
        WHERE category = 'High'
        UNION ALL
        SELECT a, c, category, b
        FROM cte5
        WHERE category = 'Low'
    )
    SELECT *
    FROM final_result
    ORDER BY a, c
    """

    # Parse the SQL query
    this_ast = parse_one(sql2)
    this_cte_dict = extract_cte_dict(this_ast)
    this_dml_dict = extract_dml_dict(this_ast)

    for key, dml in this_dml_dict.items():
        tables = extract_table_set(dml.expression)
        for table in tables:
            if table in this_cte_dict:
                this_cte_dict[table].append(dml.key)

    draw_dag(this_cte_dict, this_dml_dict)

    from graphviz import Digraph

    # Initialize the main graph with 'fdp' layout
    dot = Digraph(name="graph A", engine="fdp")
    dot.attr(
        label="Outer Cluster Graph", fontsize="20"
    )  # Set a label for the main graph

    # Define the outer box (subgraph) "cluster A"
    with dot.subgraph(name="cluster_A") as outer_cluster:
        outer_cluster.attr(
            label="Outer Box", color="lightgrey", style="filled", fontsize="16"
        )

        # Define an inner box (subgraph) "cluster B" inside "cluster A"
        with outer_cluster.subgraph(name="cluster_B") as inner_cluster_b:
            inner_cluster_b.attr(
                label="Inner Box B", color="lightblue", style="filled", fontsize="14"
            )
            inner_cluster_b.node("B1", "Node B1")
            inner_cluster_b.node("B2", "Node B2")
            inner_cluster_b.edge("B1", "B2")  # Connect nodes within inner box B

        # Define another inner box (subgraph) "cluster C" inside "cluster A"
        with outer_cluster.subgraph(name="cluster_C") as inner_cluster_c:
            inner_cluster_c.attr(
                label="Inner Box C", color="lightgreen", style="filled", fontsize="14"
            )
            inner_cluster_c.node("C1", "Node C1")
            inner_cluster_c.node("C2", "Node C2")
            inner_cluster_c.edge("C1", "C2")  # Connect nodes within inner box C

        # Connect nodes from different inner boxes within the outer box
        outer_cluster.edge("B1", "C1")

    # Add an external node and connect it to the outer box
    dot.node("D", "External Node D", shape="ellipse")
    dot.edge("D", "B1")  # Edge from the external node to a node in the inner box
    dot.edge("cluster_B", "cluster_C")  # Edge between inner boxes B and C

    # Render the graph
    dot.render("output_graph_fdp_nested_boxes", format="png", cleanup=True)
