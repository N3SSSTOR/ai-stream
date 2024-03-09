import enum 


class Scope(enum.Enum):
	USER_SHOW = "oauth-user-show"
	DONATION_SUBSCRIBE = "oauth-donation-subscribe"
	DONATION_INDEX = "oauth-donation-index"
	CUSTOM_ALERT_STORE = "oauth-custom_alert-store"
	GOAL_SUBSCRIBE = "oauth-goal-subscribe"
	POLL_SUBSCRIBE = "oauth-poll-subscribe"