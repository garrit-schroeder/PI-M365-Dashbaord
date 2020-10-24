# PI-M365-Dashbaord
<a href="https://hub.docker.com/r/garritschroeder/pi-m365-dashbaord">
<img alt="Docker Pull Count" src="https://img.shields.io/docker/pulls/garritschroeder/pi-m365-dashbaord.svg"/>
</a>

This projects calls a Logic App in Azure to gather informatin from M365
- Get unread mails count
- Get calendar events from today
- Get Open Todos Count
- Get Planner Cards Count

Create the Logic App yourself and supply the URL to the Logic App POST trigger via the environment varialbe LOGIC_APP_URL
