import os
import sys
import time
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox


#执行下述 python 代码，流式获取代码输出并打印，代码执行超时时间为600秒

python_code = """
import time
print("hello python")
#time.sleep(2)
#print("hello python after 2 sec")
"""

RUNS = 100
for i in range(1, RUNS + 1):
    sandbox = None
    try:
        start = time.time()
        sandbox = Sandbox.create(template="code-code-vpc", timeout=3600)
        create_elapsed = time.time() - start

        run_start = time.time()
        result = sandbox.run_code(python_code, on_stdout=lambda data: print(data), timeout=60)
        run_elapsed = time.time() - run_start

        elapsed = time.time() - start
        print(result)
        print(
            f"[{i}/{RUNS}] Lifecycle: {elapsed:.2f}s "
            f"(create: {create_elapsed:.2f}s, run_code: {run_elapsed:.2f}s)"
        )
    except KeyboardInterrupt:
        print(f"\n[Interrupted at run {i}/{RUNS}], cleaning up...", flush=True)
        break
    finally:
        if sandbox is not None:
            try:
                sandbox.kill()
            except Exception as e:
                print(f"[warn] kill failed at run {i}: {e}")
