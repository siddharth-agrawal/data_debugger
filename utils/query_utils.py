import pandas as pd


def get_possible_mistakes(db_conn):
    """
    Get annotated examples where the model confidently disagrees with
    the annotation.
    """
    query = \
        """
        SELECT
          *
        FROM
          enriched_data
        WHERE
          complete = 1 AND
          pred_label != intent
        ORDER BY
          pred_confidence DESC
        """

    result = pd.read_sql_query(query, db_conn)
    return result


def get_labels_verify(db_conn):
    """
    Get unannotated examples where the model is at least 50% confident
    sorted by how confused it is.
    """
    query = \
        """
        SELECT
          *
        FROM
          enriched_data
        WHERE
          complete = 0 AND
          pred_confidence > 0.5
        ORDER BY
          score DESC
        """

    result = pd.read_sql_query(query, db_conn)
    return result


def update_label(row_id, label, db_conn):
    """
    Mark row as annotated with the provided label.
    """
    query = \
        f"""
        UPDATE
          enriched_data
        SET
          complete = 1,
          intent = "{label}"
        WHERE
          id = {row_id}
        """
    cur = db_conn.cursor()
    cur.execute(query)
    db_conn.commit()
