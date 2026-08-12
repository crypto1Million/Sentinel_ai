class SocialStrengthScorer:

    def calculate(
        self,
        telegram_members: int,
        twitter_mentions: int,
        j7_signals: int,
        engagement_rate: float
    ):

        score = 0

        score += min(
            telegram_members / 100,
            30
        )

        score += min(
            twitter_mentions / 10,
            25
        )

        score += min(
            j7_signals * 10,
            30
        )

        score += min(
            engagement_rate,
            15
        )

        return max(
            0,
            min(score, 100)
        )