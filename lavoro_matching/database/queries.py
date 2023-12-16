from lavoro_matching.database import db


def create_match(applicant_profile_id, job_post_id, match_score):
    query = """
        INSERT INTO matches (applicant_profile_id, job_post_id, match_score)
        VALUES (%s, %s, %s)
        ON CONFLICT (applicant_profile_id, job_post_id) DO UPDATE
        SET match_score = EXCLUDED.match_score;
    """

    query_tuple = (query, (applicant_profile_id, job_post_id, match_score))
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1
