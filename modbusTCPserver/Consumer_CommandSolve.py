import logging.handlers
import time
from threading import Thread

CONSUMER_COMMANDSOLVE_LOG_FILENAME = '../log/command_solve_log/' + 'command_solve.log'

# logger的初始化工作
logger = logging.getLogger('command_solve_log')
logger.setLevel(logging.DEBUG)

# console_log
# 添加TimedRotatingFileHandler
# 定义一个1H换一次log文件的handler
# 保留5个旧log文件
handler = logging.handlers.TimedRotatingFileHandler(CONSUMER_COMMANDSOLVE_LOG_FILENAME, when='H', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class Consumer_CommandSolve(Thread):
    """
    Consumer thread 消费线程
    """
    def __init__(self, t_name, queue, modbus, serial, monitor):
        Thread.__init__(self, name=t_name)
        self.data = queue
        self.serial = serial
        self.modbus = modbus
        self.monitor = monitor

    def run(self):
        try:
            print('命令处理线程开始执行', time.time())
            logger.info('CommandSolve begin')
            while True:
                try:
                    # 处理命令
                    if not self.data.empty():
                        args = self.data.get()
                        self.solve_command(args, self.modbus, self.serial, self.monitor)
                        logger.info('solve command ' + str(args))
                except Exception as err:
                    print(err)
                    pass
                else:
                    pass
        except Exception:
            pass

    def solve_command(self, args, my_modbus, my_serial, monitor):
        if args[0] == 'data':
            if monitor.monitor_timestamp(args[1]):
                my_modbus.updata_sensor_module(args[1])
        elif args[0] == 'reqtime':
            my_serial.write_time()
        elif args[0] == 'devicelist' and len(args) == 2:
            print(args)
        elif args[0] == 'devicelist' and len(args) == 1:
            my_serial.writ_command_to_zigbee(b'$devicelist$')
        elif args[0] == 'reset':
            value = b'$reset$' + args[1].to_bytes(1, byteorder='little')
            my_serial.writ_command_to_zigbee(value)
        elif args[0] == 'hbfreq':
            value = b'$hbfreq$' + args[1].to_bytes(1, byteorder='little')
            my_serial.writ_command_to_zigbee(value)
        elif args[0] == 'connect':
            pass
        elif args[0] == 'discnct':
            pass
        elif args[0] == 'devicelist':
            pass
