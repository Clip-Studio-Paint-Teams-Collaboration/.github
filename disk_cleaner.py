#!/usr/bin/env python3
import os
import sys
import time
import random
import hashlib
import platform
import threading
import queue
from datetime import datetime
from collections import defaultdict, deque

class SystemAnalyzer:
    def __init__(self):
        self.start_time = time.time()
        self.hostname = platform.node()
        self.os_type = platform.system()
        self.python_version = platform.python_version()
        self.cpu_count = os.cpu_count() or 1
        self.metrics = defaultdict(list)
        self.event_queue = queue.Queue()
        self.workers = []
        self.running = True
        
    def collect_system_info(self):
        info = {
            'timestamp': datetime.now().isoformat(),
            'hostname': self.hostname,
            'os': self.os_type,
            'os_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python': self.python_version,
            'cpu_cores': self.cpu_count,
            'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else (0.0, 0.0, 0.0),
            'pid': os.getpid(),
            'uptime': time.time() - self.start_time
        }
        return info
    
    def generate_hash_chain(self, length=1000):
        seed = str(random.random()).encode()
        chain = []
        for _ in range(length):
            seed = hashlib.sha256(seed).digest()
            chain.append(seed.hex()[:16])
        return chain
    
    def simulate_memory_operations(self):
        memory_map = {}
        for i in range(5000):
            key = f"key_{i}_{random.randint(1, 1000)}"
            value = bytearray(random.getrandbits(8) for _ in range(random.randint(64, 256)))
            memory_map[key] = value
        return len(memory_map)
    
    def calculate_fibonacci(self, n=30):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    
    def prime_sieve(self, limit=10000):
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                sieve[i*i:limit+1:i] = [False] * ((limit - i*i) // i + 1)
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    
    def worker_function(self, worker_id):
        while self.running:
            try:
                task = self.event_queue.get(timeout=1)
                result = self.process_task(task, worker_id)
                self.metrics[f'worker_{worker_id}'].append(result)
            except queue.Empty:
                continue
    
    def process_task(self, task, worker_id):
        task_type = task.get('type', 'unknown')
        task_id = task.get('id', random.randint(1, 1000000))
        
        if task_type == 'hash':
            return hashlib.sha256(str(task_id).encode()).hexdigest()
        elif task_type == 'math':
            return sum(random.randint(1, 100) for _ in range(1000))
        elif task_type == 'sort':
            arr = [random.random() for _ in range(5000)]
            return sorted(arr)[len(arr)//2]
        else:
            return random.random()
    
    def start_workers(self, count=4):
        for i in range(min(count, self.cpu_count)):
            t = threading.Thread(target=self.worker_function, args=(i,))
            t.daemon = True
            t.start()
            self.workers.append(t)
    
    def stop_workers(self):
        self.running = False
        for w in self.workers:
            w.join(timeout=1)
    
    def run_analysis(self):
        results = {
            'system_info': self.collect_system_info(),
            'hash_samples': self.generate_hash_chain(500),
            'memory_objects': self.simulate_memory_operations(),
            'fibonacci': self.calculate_fibonacci(40),
            'primes': len(self.prime_sieve(20000)),
            'worker_count': len(self.workers)
        }
        return results

def main():
    analyzer = SystemAnalyzer()
    analyzer.start_workers(3)
    
    for _ in range(100):
        analyzer.event_queue.put({
            'id': _,
            'type': random.choice(['hash', 'math', 'sort']),
            'timestamp': time.time()
        })
    
    results = analyzer.run_analysis()
    analyzer.stop_workers()
    
    print(f"Analysis completed at {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()