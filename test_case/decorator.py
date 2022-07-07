import time


from tools.base_logging import Log
log = Log("test")

def init_func(AGVManager):
    '''复位函数'''
    AGVManager.clearFault(0)  # 清除类型 bit0：复位清空运控故障（需等待1s左右） bit1：清空电机故障（很快） bit2：复位电机驱动，需等待10s左右
    AGVManager.clearFault(1)
    AGVManager.clearFault(2)
    AGVManager.cancelQuickStop()  # 软急停复位
    log.info("func_name: " + func.__name__ + "  " + "清除故障， 软复位")

def decorator_fun(*func_args):  # 接收AGVManager
    def decorator(func):
        def exec_time(*args):
            print(func_args)
            print(func)
            print(args)
            # print(func_args)
            old_time = time.time()
            print("开始时间：" + str(old_time))
            try:
                result = func(*args)
            except Exception as e:
                '''异常后清除故障复位'''
                result = ""
                init_func(func_args[0])
                raise e
            finally:
                ret = result if result else ""
                if len(args) > 1:
                    params = str(args[1]) if args[1] else ""
                else:
                    params = ""
                new_time = time.time()
                print(params)
                log.info("func_name: " + func.__name__ + "  " +
                         "params: " + params + "  " +
                         "use_time: " + str(new_time - old_time) + "  " +
                         "result: " + str(ret)
                         )
            return new_time - old_time, func.__name__
        return exec_time
    return decorator


@decorator_fun("test")
def a_function_requiring_decoration():
    time.sleep(1)
    print("I am the function which needs some decoration to remove my foul smell")
    print("over")
    return 1


if __name__ == "__main__":
    a_function_requiring_decoration()
