import microcontroller

# Configurations and states are stored in the microcontroller's non-volatile memory.
# byte 0: profile index


class Config:
    def __init__(self, num_profiles=256, configuring=False):
        if not (1 <= num_profiles <= 256):
            raise ValueError("Number of profiles must be between 1 and 255.")

        self.num_profiles = num_profiles
        self.configuring = configuring

        if self.get_profile_index() > num_profiles - 1:
            self.set_profile_index(num_profiles - 1)

    def get_profile_index(self):
        return microcontroller.nvm[0]

    def set_profile_index(self, index):
        if not (0 <= index <= self.num_profiles - 1):
            raise ValueError("Profile index out of bounds.")
        microcontroller.nvm[0] = index

    def inc_profile_index(self, n=1):
        current_index = self.get_profile_index()
        new_index = (current_index + n) % self.num_profiles
        self.set_profile_index(new_index)
        return new_index

    def is_configuring(self):
        return self.configuring

    def set_configuring(self, configuring):
        self.configuring = configuring
        return configuring

    def toggle_configuring(self):
        self.configuring = not self.configuring
        return self.configuring
