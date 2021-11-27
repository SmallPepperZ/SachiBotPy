from . import ping, react, suggest, whatis, whois



def setup(bot):
    ping.setup(bot)
    react.setup(bot)
    suggest.setup(bot)
    whatis.setup(bot)
    whois.setup(bot)