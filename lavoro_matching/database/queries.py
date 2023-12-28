from lavoro_matching.database import db


def create_match(applicant_account_id, job_post_id, match_score, end_date):
    query = """
        INSERT INTO matches (applicant_account_id, job_post_id, match_score, end_date)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (applicant_account_id, job_post_id) DO UPDATE
        SET match_score = EXCLUDED.match_score, end_date = EXCLUDED.end_date;
    """

    query_tuple = (query, (applicant_account_id, job_post_id, match_score, end_date))
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1
