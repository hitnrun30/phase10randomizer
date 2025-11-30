import os
import sys
import subprocess
import time
import phase10config

# Give Python enough time to do real work.
# You can tune this later once you see actual durations.
TIMEOUT_SECONDS = phase10config.CONFIG["HTML_TIMEOUT_SECONDS"]

def main():
    script_path = os.path.join(os.path.dirname(__file__), "phase10logic.py")

    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        # Took too long – don't hang the web server
        print("<li>Error: Python generation timed out.</li>")
        return

    duration = time.time() - start

    if result.returncode != 0:
        # phase10logic.py failed; don't dump stderr to users
        # (If you want, you can log result.stderr to a file for debugging.)
        print("<li>Error: Python generation failed.</li>")
        return

    stdout = (result.stdout or "").strip()
    if not stdout:
        print("<li>Error: no output from Python.</li>")
        return

    # Optionally, if you ever want to see timing in the page for debugging:
    # print(f"<li>DEBUG: generated in {duration:.3f}s</li>")
    # print(stdout)
    # return

    # Normal behavior: just pipe through the <li> lines from phase10logic.py
    print(stdout)


if __name__ == "__main__":
    main()
