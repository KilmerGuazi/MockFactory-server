# MockFactory-server
造数工厂后端服务

# 使用前，搭建mysql和redis
- 在config.py中配置连接信息,包括开发、测试、生产环境，例如
  ```python
  class ProductionConfig(object):
    pass

  class TestingConfig(object):
    pass
  
  class LocalConfig(object):
    """
    本地环境配置
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    DB_SERVER = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWORD = quote_plus('')
    DB_PORT = 3306
    DATA_BASE = 'mockfactory'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DATA_BASE}"
    REDIS_HOST = ''
    REDIS_PORT = 6379
    REDIS_PASSWORD = quote_plus('')
    REDIS_DB = 10
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

  class 

  ```

  # 环境配置，
  - 请在对应服务器上设置环境变量 SPRING_PROFILES_ACTIVE，值分别是local、dev、test 、prod
 
  # 数据库的表，请根据orm\mapper.py中的models自行创建
