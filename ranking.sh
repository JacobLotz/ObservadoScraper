# Edit crontab job using
# crontab -b


rm results.txt
rm results.png

python3 UpdateRanking.py

pango-view --font=mono -qo results.png results.txt

cp results.png ../owncloud/competitie_resultaten/.