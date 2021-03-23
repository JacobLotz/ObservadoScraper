rm results.txt
rm results.png

python3 UpdateRanking.py

pango-view --font=mono -qo results.png results.txt