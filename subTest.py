# -*- coding: utf-8 -*-
import subprocess

baziExe = "D:\\Work_Space\\My\\BaziEval\\Release\\Bazi.exe"
revCommand = " -e " + "戊戌乙丑甲寅壬申"

out_code = 0
try:
    out_bytes = subprocess.check_output(baziExe + revCommand)
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    out_code  = e.returncode   # Return code

out_text = out_bytes.decode('gbk',errors='replace')
print(out_text)