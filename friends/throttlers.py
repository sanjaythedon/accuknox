from rest_framework.throttling import UserRateThrottle


class UserLevelThrottle(UserRateThrottle):
    rate = '3/min'