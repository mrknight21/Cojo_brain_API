import queue
import threading
import time


# MultiThreaded Downloading
class MultiThreader(object):

    def __init__(self, command, num_threads=5):

        self.num_threads = num_threads
        self.exitFlag = False
        self.command = command

    class MyThread(threading.Thread):

        def __init__(self, parent, thread_id, name, my_queue, queue_lock):
            threading.Thread.__init__(self)
            self.threadID = thread_id
            self.name = name
            self.queue = my_queue
            self.queueLock = queue_lock
            self.parent = parent

        def run(self):
            print("Started " + self.name)
            while not self.parent.exitFlag:
                self.queueLock.acquire()
                if not self.queue.empty():
                    job = self.queue.get()
                    self.queueLock.release()
                    self.parent.command(*job)
                else:
                    self.queueLock.release()
                time.sleep(1)
            print("Exiting " + self.name)

    def start(self, command_list):

        work_queue = queue.Queue(len(command_list))
        queue_lock = threading.Lock()

        threads = []
        thread_id = 1
        self.exitFlag = False

        # Fill the queue
        queue_lock.acquire()
        for job in command_list:
            work_queue.put(job)
        queue_lock.release()
        print("Queue Filled")

        # Create new threads
        for i in range(1, self.num_threads + 1):
            thread_name = "Thread-" + str(i)
            thread = self.MyThread(self, thread_id, thread_name, work_queue, queue_lock)
            thread.start()
            threads.append(thread)
            thread_id += 1

        # Wait for queue to empty
        while not work_queue.empty():
            time.sleep(1)

        # Notify threads it's time to exit
        self.exitFlag = True

        # Wait for all threads to complete
        for t in threads:
            t.join()
        print("Exiting Main Thread")

    def __del__(self):
        self.exitFlag = True
