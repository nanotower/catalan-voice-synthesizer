import redis

class Db:
  def __init__(self, conf):
    self.r = redis.Redis(host=conf["redis_host"], port=conf["redis_port"], db=conf["redis_db"], decode_responses=True)

  def exists(self, phrase):
    return self.r.exists(phrase)

  def get(self, phrase):
    return self.r.get(phrase)

  def set(self, phrase, audio_as_b64):
    return self.r.set(phrase, audio_as_b64)

  def get_dbuser(self, id):
    return self.r.hget("users_db", id)

  def dbuser_exists(self, id):
    return self.r.hexists("users_db", id)
   
