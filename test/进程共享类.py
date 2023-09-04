import multiprocessing

class IMessage:
    def __init__(self, content):
        self.content = content

def worker(shared_content):
    shared_content.content = "Hello from Worker Process!"

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_content = manager.Value(IMessage, IMessage("Hello from Main Process!"))

    process = multiprocessing.Process(target=worker, args=(shared_content,))
    process.start()
    process.join()

    final_message = IMessage(shared_content.content)  # 从共享属性中创建最终的消息对象
    print("Final content of shared_content:", final_message.content)
