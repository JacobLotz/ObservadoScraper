# Edit crontab job using
# crontab -e
# service cron restart


rm results.txt
rm results.png

cd scripts
python3 updateranking.py
cd ..

pango-view --font=mono -qo results.png results.txt --dpi 150

cp results.png /home/jelotz/Documents/owncloud/Prive/competitie_resultaten/.
