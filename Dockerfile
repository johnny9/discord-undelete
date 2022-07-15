FROM python:3
RUN pip install git+https://github.com/Rapptz/discord.py
ADD bot.py /opt/bot.py
CMD ["python", "/opt/bot.py"]
