class PasswordWaitStates:
    waiting_for_password = {}
    failed_attempts = {}
    waiting_states = {}
    
    @staticmethod
    def set_state(user_id: int, state: str, data: dict = None):
        PasswordWaitStates.waiting_states[user_id] = {'state': state, 'data': data or {}}
    
    @staticmethod
    def get_state(user_id: int):
        return PasswordWaitStates.waiting_states.get(user_id)
    
    @staticmethod
    def clear_state(user_id: int):
        if user_id in PasswordWaitStates.waiting_states:
            del PasswordWaitStates.waiting_states[user_id]
