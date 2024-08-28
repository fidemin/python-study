import uuid
from collections import defaultdict
from typing import Optional

from sqlglot import exp, parse_one
from copy import deepcopy

import graphviz


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
    table_name = ast.args["from"].alias_or_name
    tables = {table_name}

    if "joins" in ast.args:
        for join in ast.args["joins"]:
            tables.add(join.alias_or_name)

    return tables


def draw_dag(cte_dict, dml_dict):
    """Draw the DAG using graphviz."""
    dot = graphviz.Digraph(comment="CTE and Table DAG")

    alias_key_dict = {}

    for key, dml in dml_dict.items():
        dot.node(
            dml.key,
            f"""<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD><B>CTE: {dml.cte_alias}</B></TD>
        </TR>
        <TR>
            <TD>{dml.expression.sql()}</TD>
        </TR>
    </TABLE>>""",
        )
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

    # sql = """
    # SELECT b FROM mytable
    # """

    # Parse the SQL query
    this_ast = parse_one(sql)
    this_cte_dict = extract_cte_dict(this_ast)
    this_dml_dict = extract_dml_dict(this_ast)

    for key, dml in this_dml_dict.items():
        tables = extract_table_set(dml.expression)
        for table in tables:
            if table in this_cte_dict:
                this_cte_dict[table].append(dml.key)

    draw_dag(this_cte_dict, this_dml_dict)
    pass

    # Draw the DAG
    # dag = draw_dag("")
