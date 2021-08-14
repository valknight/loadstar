from enum import Enum
from datetime import datetime

class Severity(Enum):
	CRITICAL = 'CRTICIAL'
	ERROR = 'ERROR'
	WARNING = 'WARNING'
	INFO = 'INFO'
	DEBUG = 'DEBUG'

class Log():
	def __init__(self, maxLength = 5000):
		self.maxLength = maxLength
		self.logQueue = []
		self.log("Started log!", Severity.DEBUG)
	
	def log(self, message: str, level: Severity = Severity.INFO):
		self.logQueue.append(Message(message, level = level))
	
	@property
	def output(self):
		l = []
		for m in self.logQueue:
			l.append(str(m))
		return l
	
	def __str__(self):
		return '\n'.join(self.output)


class Message():
	def __init__(self, message: str, level: Severity = Severity.INFO):
		self.level = level
		self.message = message
		self.time = datetime.now()
		
	
	def __str__(self):
		return "[{}] [{}] {}".format(self.time.strftime("%H:%M:%S"), self.level, self.message)