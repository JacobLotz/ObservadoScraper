# Edit crontab job using
# crontab -e
# service cron restart


rm results.txt
rm results.png

python3 UpdateRanking.py

pango-view --font=mono -qo results.png results.txt --dpi 150

cp results.png ../owncloud/Prive/competitie_resultaten/.
