from enum import Enum
from datetime import datetime

class Severity(Enum):
	CRITICAL = 'CRTICIAL'
	ERROR = 'ERROR'
	WARNING = 'WARNING'
	INFO = 'INFO'
	DEBUG = 'DEBUG'

def sevToStr(level: Severity):
	if level == Severity.CRITICAL:
		return "CRITICAL"
	if level == Severity.ERROR:
		return "ERROR"
	if level == Severity.WARNING:
		return "WARNING"
	if level == Severity.INFO:
		return "INFO"
	if level == Severity.DEBUG:
		return "DEBUG"

class Log():
	def __init__(self, maxLength = 5000):
		self.maxLength = maxLength
		self.logQueue = []
		self.log("Started log!", Severity.DEBUG)
	
	def log(self, message: str, level: Severity = Severity.INFO):
		self.logQueue.append(Message(message, level = level))
	
	def critical(self, message: str):
		self.log(message, Severity.CRITICAL)
	
	def error(self, message: str):
		self.log(message, Severity.ERROR)
	
	def warning(self, message: str):
		self.log(message, Severity.WARNING)
	
	def warn(self, message: str):
		self.warning(message)
	
	def info(self, message: str):
		self.log(message, Severity.INFO)
	
	def debug(self, message: str):
		self.log(message, Severity.DEBUG)
	
	@property
	def output(self):
		l = []
		for m in self.logQueue:
			l.append(str(m))
		return l
	
	@property
	def output_dict(self):
		l = []
		for m in self.logQueue:
			l.append(m.toDict())
		return l
	
	def __str__(self):
		return '\n'.join(self.output)


class Message():
	def __init__(self, message: str, level: Severity = Severity.INFO):
		self.level = level
		self.message = message
		self.time = datetime.now()
	
	def toDict(self):
		return {'level': sevToStr(self.level), 'message': self.message, 'time': self.time}
	
	def __str__(self):
		return "[{}] [{}] {}".format(self.time.strftime("%H:%M:%S"), sevToStr(self.level), self.message)