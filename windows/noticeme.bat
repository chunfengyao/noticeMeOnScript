@echo off
set title=�ű���ʾ
set content=%*
mshta vbscript:msgbox("Notice��%content%",262208,"%title%")(window.close)