from typing import List
from lavoro_library.model.message_schemas import ApplicantProfileToMatch, JobPostToMatch
from lavoro_library.model.shared import Point


def calculate_match(job_post_to_match: JobPostToMatch, applicant_profile_to_match: ApplicantProfileToMatch) -> float:
    position_match = _calculate_position_match(job_post_to_match.position_id, applicant_profile_to_match.position_id)
    education_level_match = _calculate_education_level_match(
        job_post_to_match.education_level_id, applicant_profile_to_match.education_level_id
    )
    skill_match = _calculate_skill_match(job_post_to_match.skill_ids, applicant_profile_to_match.skill_ids)
    work_type_match = _calculate_work_type_match(
        job_post_to_match.work_type_id, applicant_profile_to_match.work_type_id
    )
    work_location_match = _calculate_work_location_match(
        job_post_to_match.work_location,
        applicant_profile_to_match.home_location,
        applicant_profile_to_match.work_location_max_distance,
    )
    contract_type_match = _calculate_contract_type_match(
        job_post_to_match.contract_type_id, applicant_profile_to_match.contract_type_id
    )
    salary_match = _calculate_salary_match(
        job_post_to_match.salary_min, job_post_to_match.salary_max, applicant_profile_to_match.min_salary
    )
    seniority_level_match = _calculate_seniority_level_match(
        job_post_to_match.seniority_level,
        applicant_profile_to_match.seniority_level,
        applicant_profile_to_match.experience_years,
    )

    total_match = (
        position_match
        + education_level_match
        + skill_match
        + work_type_match
        + work_location_match
        + contract_type_match
        + salary_match
        + seniority_level_match
    )
    return total_match / 8


def _calculate_position_match(job_post_position_id: int, applicant_profile_position_id: int) -> float:
    if job_post_position_id == applicant_profile_position_id:
        return 1.0
    else:
        return 0.0


def _calculate_education_level_match(
    job_post_education_level_id: int, applicant_profile_education_level_id: int
) -> float:
    if job_post_education_level_id <= applicant_profile_education_level_id:
        return 1.0
    else:
        return 0.0


def _calculate_skill_match(job_post_skill_ids: List[int], applicant_profile_skill_ids: List[int]) -> float:
    overlap = set(job_post_skill_ids).intersection(set(applicant_profile_skill_ids))
    return len(overlap) / len(job_post_skill_ids)


def _calculate_work_type_match(job_post_work_type_id: int, applicant_profile_work_type_id: int) -> float:
    if job_post_work_type_id == applicant_profile_work_type_id:
        return 1.0
    else:
        return 0.0


def _calculate_work_location_match(
    job_post_work_location: Point,
    applicant_profile_home_location: Point,
    applicant_profile_work_location_max_distance: int,
) -> float:
    x_distance = job_post_work_location.longitude - applicant_profile_home_location.longitude
    y_distance = job_post_work_location.latitude - applicant_profile_home_location.latitude
    distance = (x_distance**2 + y_distance**2) ** 0.5
    if distance <= applicant_profile_work_location_max_distance:
        return 1.0
    else:
        return 0.0


def _calculate_contract_type_match(job_post_contract_type_id: int, applicant_profile_contract_type_id: int) -> float:
    if job_post_contract_type_id == applicant_profile_contract_type_id:
        return 1.0
    else:
        return 0.0


def _calculate_salary_match(
    job_post_salary_min: int, job_post_salary_max: int, applicant_profile_min_salary: int
) -> float:
    if job_post_salary_min <= applicant_profile_min_salary <= job_post_salary_max:
        return 1.0
    else:
        return 0.0


def _calculate_seniority_level_match(
    job_post_seniority_level: int, applicant_profile_seniority_level: int, applicant_profile_experience_years: int
) -> float:
    seniority_level_score = 0.0
    if job_post_seniority_level == applicant_profile_seniority_level:
        seniority_level_score = 1.0
    elif job_post_seniority_level < applicant_profile_seniority_level:
        seniority_level_score = 0.5
    else:
        seniority_level_score = 0.0

    experience_years_score = 0.0
    # assume seniority level goes up by 1 every 2 years
    if applicant_profile_experience_years >= 2 * job_post_seniority_level:
        experience_years_score = 1.0
    elif applicant_profile_experience_years >= job_post_seniority_level:
        experience_years_score = 0.5
    else:
        experience_years_score = 0.0

    return seniority_level_score * experience_years_score
