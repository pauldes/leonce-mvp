
class YoutubeChannelScrapper():

    def __init__(channel_name: str):
        self.channel_name = channel_name


    @property
    def x(self):
        return self._channel_name


    @x.setter
    def channel_name(self, value):
        print("Called")
        self._channel_name = value
