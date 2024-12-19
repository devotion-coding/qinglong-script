"""
    @author TJ
    @github 
    @described 获取环境变量
    觉得不错麻烦点个star谢谢
"""
import os

# 读环境变量
def read_env_variable(env_variable_map=None):

    if env_variable_map is None:
        env_variable_map = {}

    for k in env_variable_map:
        if os.getenv(k):
            v = os.getenv(k)
            env_variable_map[k] = v
