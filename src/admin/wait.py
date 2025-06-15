class WaitStates:
    waiting_for_password = {}
    failed_attempts = {}
    waiting_states = {}
    authorized_admins = set()
    
    @staticmethod
    def set_state(user_id: int, state: str, data: dict = None):
        WaitStates.waiting_states[user_id] = {'state': state, 'data': data or {}}
    
    @staticmethod
    def get_state(user_id: int):
        return WaitStates.waiting_states.get(user_id)
    
    @staticmethod
    def clear_state(user_id: int):
        if user_id in WaitStates.waiting_states:
            del WaitStates.waiting_states[user_id]

    @staticmethod
    def is_admin(user_id: int) -> bool:
        return user_id in WaitStates.authorized_admins
