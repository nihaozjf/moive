# -*- coding: utf-8 -*-

__author__ = 'zhangjufu'
import random
from user_agents import agents

class MyUserAgentMiddleware(object):
	'''choose a user_agent'''
	def process_request(self,request,spider):
		agent=random.choice(agents)
		request.headers["User-Agent"]=agent
