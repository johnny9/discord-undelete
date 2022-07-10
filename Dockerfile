FROM python:3
RUN pip install discord.py
ADD bot.py /opt/bot.py
CMD ["python", "/opt/bot.py"]
