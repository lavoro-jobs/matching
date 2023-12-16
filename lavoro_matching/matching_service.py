import os
import jsonpickle
from lavoro_library.amqp import RabbitMQConsumer
from lavoro_library.model.message_schemas import MatchToCalculate
from lavoro_matching.database import queries
from lavoro_matching.matching import calculate_match


class MatchingService:
    def __init__(self):
        self.match_to_calculate_consumer = RabbitMQConsumer(os.environ["AMQP_URL"], "match_to_calculate")

    def start(self):
        self.match_to_calculate_consumer.consume(self._message_inflow_callback)

    def _message_inflow_callback(self, channel, method, properties, body):
        message: MatchToCalculate = MatchToCalculate(**jsonpickle.decode(body))
        match_score = calculate_match(message.job_post_to_match, message.applicant_profile_to_match)
        print("Match calculated: ", match_score)
        self._save_match_to_db(
            message.applicant_profile_to_match.applicant_account_id,
            message.job_post_to_match.job_post_id,
            match_score,
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)
        pass

    def _save_match_to_db(self, applicant_profile_id, job_post_id, match_score):
        if match_score > 0.1:
            queries.create_match(applicant_profile_id, job_post_id, match_score)


if __name__ == "__main__":
    service = MatchingService()
    service.start()
