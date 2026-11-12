# usage: run.sh script.py article.html group "names"
cd /c/Users/s30se/Desktop/blog-workspace
python -X utf8 tools/_tv1115/$1 || exit 1
python -X utf8 tools/honorific.py fix articles/$2 --group $3 --names "$4" >/dev/null
python -X utf8 tools/easy_read.py fix articles/$2 >/dev/null
python -X utf8 tools/easy_read.py check articles/$2
python -X utf8 tools/honorific.py check articles/$2 --group $3 --names "$4" | tail -3
