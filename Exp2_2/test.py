import threading
import requests
import time

def send_request(i):
    try:
        response = requests.get("http://localhost:12000/index.html")
        print(f"[Thread {i}] Status: {response.status_code}")
    except Exception as e:
        print(f"[Thread {i}] Error: {e}")

# 记录开始时间
start_time = time.time()

# 创建多个线程模拟并发请求
threads = []
for i in range(10):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

# 记录结束时间
end_time = time.time()

# 计算总耗时
total_time = end_time - start_time
print(f"Total time for all requests: {total_time:.2f} seconds")
