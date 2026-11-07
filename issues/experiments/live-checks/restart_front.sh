#!/bin/sh
# Kill any miminet dev server on :5000, start a fresh one from the working copy, wait until it answers.
T="C:/Users/PCyur/AppData/Local/Temp/claude/C--Users-PCyur-OneDrive-----------miminet/21426821-2124-44cb-890b-8c18cde00d1d/scratchpad"
for pid in $(netstat -ano | grep ':5000 ' | grep LISTEN | awk '{print $5}' | sort -u); do
  powershell.exe -NoProfile -Command "Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1
done
sleep 1
nohup sh "$T/tools/run_front.sh" > "$T/flask.log" 2>&1 &
for i in $(seq 1 60); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5000/)" = "200" ] && break
  sleep 1
done
echo "branch: $(git -C 'C:/Users/PCyur/OneDrive/Документы/miminet/miminet' branch --show-current) | listeners on :5000: $(netstat -ano | grep ':5000 ' | grep -c LISTEN)"
