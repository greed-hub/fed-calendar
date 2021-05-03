from django.shortcuts import render
from datetime import date, timedelta, datetime
from django.http import JsonResponse
from calendar76.models import Season, Event, CommunityEvent
from django.template import Context
from apscheduler.schedulers.background import BackgroundScheduler

globalcalendar = {}
today = {}
modal = {}

#loops through today events list and generates string with html to display in modal
def getModal():
    modaltext = ''

    for currentEvent in getTodayEvents():
        htmlDescription = ''

        if currentEvent['html_content']:
            htmlDescription = f"""<div>{currentEvent['html_content']}</div>"""
        elif currentEvent['description']:
            htmlDescription = currentEvent['description']

        modaltext += f"""
        <div class='container-fluid mb-5 p-5' style=' box-shadow: 0 16px 48px rgb(2 2 1 / 31%);'>
            <div class='row'>
                <div class='col m-3 p-1 rounded' style='border: 1px solid #c7974b; color: #2b2a29; text-align: center; background-color: #c7974b;'>
                    <h2>{currentEvent['name']}</h2>
                </div>
            </div>
            <div class='row'>
                <div class='col-sm-6'>
                    <img src='{currentEvent['image_modal'] if currentEvent['image_modal'] is not None else ''}' class='img-fluid rounded' style='box-shadow: 0 0 6px #c7974b;'></img>
                </div>
                    <div class='col-sm-6 justify-content-center'>
                        <div class=''>
                        {'<b>Platform:</b> ' + currentEvent['platform'].upper() + '<br>' if currentEvent['platform'] != '' else ''}
                        <b>Date start:</b> {currentEvent['date_start']}<br>
                        {'<b>Time start: </b>' + currentEvent['time_start'] + ' ' + currentEvent['timezone'] + '<br>' if 'time_start' in currentEvent and 'timezone' in currentEvent else ''}
                        <b>Date end:</b> {currentEvent['date_end']}<br>
                        {'<b>Link:</b> <a href=' + currentEvent['external_link'] + '>Click here</a> 👈<br><br>' if currentEvent['external_link'] is not None else ''}
                        {htmlDescription}
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

    return modaltext

#creates modal with current season information
def seasonModal():
    try: seasonMod = f"""
        <div class="container-fluid">
        <div class='row'>
            <div class='col-sm-6'>
                <img src='{today['season']['image_modal'] if today['season']['image_modal'] else '' }' class='img-fluid rounded' style='box-shadow: 0 0 6px #c7974b;'></img>
            </div>
                <div class='col-sm-6 justify-content-center'>
                    <div class=''>
                    <b>Date start:</b> {today['season']['date_start']}<br>
                    <b>Date end:</b> {today['season']['date_end']}<br>
                    {'<b>Link:</b> <a href=' + today['season']['external_link'] + '>Click here</a> 👈<br>' if today['season']['external_link'] else '' }<br>
                    {today['season']['description']}
                    </div>
                </div>
        </div>
        </div>
        """
    except:
        seasonMod = ""
    return seasonMod

#checks for events in given date and if found returns event ID array depending on event type
def eventsID(argDay):
    doubleofficial = []
    official = []
    community = []
    for event in Event.objects.filter(date_start__lte=argDay, date_end__gte=argDay):
        if event.get_event_type_display() == 'double':
            doubleofficial.append(event.pk)
        if event.get_event_type_display() == 'official':
            official.append(event.pk)
    for event in CommunityEvent.objects.filter(date_start__lte=argDay, date_end__gte=argDay):
        community.append(event.pk)

    out = {}

    if doubleofficial != []:
        out['doubleEventsID'] = doubleofficial
    if official != []:
        out['officialEventsID'] = official
    if community != []:
        out['communityEventsID'] = community

    return out

#sets calendar range given season/event earliest and latest date, creates calendar and fills it with eventsID arrays
def calendarRange():
    newCalendar = {}

    firstDay = date.today()
    lastDay = date.today()

    try:
        if Season.objects.earliest('date_start').date_start < firstDay:
            firstDay = Season.objects.earliest('date_start').date_start
        if Season.objects.latest('date_end').date_end > lastDay:
            lastDay = Season.objects.latest('date_end').date_end
        if Event.objects.earliest('date_start').date_start < firstDay:
            firstDay = Event.objects.earliest('date_start').date_start
        if Event.objects.latest('date_end').date_end > lastDay:
            lastDay = Event.objects.latest('date_end').date_end
        if CommunityEvent.objects.earliest('date_start').date_start < firstDay:
            firstDay = CommunityEvent.objects.earliest('date_start').date_start
        if CommunityEvent.objects.earliest('date_end').date_end > lastDay:
            lastDay = CommunityEvent.objects.latest('date_end').date_end
    except:
        pass

    days_count = (lastDay - firstDay).days + 1

    for day in [firstDay + timedelta(n) for n in range(0, days_count)]:
        newCalendar[day.strftime('%Y-%m-%d')] = eventsID(day)

    return newCalendar


def fillSeasonAttributes(season):
    return {    'name' : season.name,
                'title' : season.title,
                'endingText' : season.endingText,
                'date_start' : season.date_start.strftime('%Y-%m-%d'),
                'date_end' : season.date_end.strftime('%Y-%m-%d'),
                'totalexp' : season.totalexp,
                'expression' : season.expression,
                'description' : season.description,
                'image' : season.image,
                'image_modal' : season.image_modal,
                'external_link' : season.external_link,
            }

#fills calendar with season attributes and starting/ending dates
def fillSeasonDates(calendar):
    for season in Season.objects.all():
        calendar[season.date_start.strftime('%Y-%m-%d')]['startingSeason'] = {'attributes' : fillSeasonAttributes(season)}
        calendar[season.date_end.strftime('%Y-%m-%d')]['endingSeason'] = {'attributes' : fillSeasonAttributes(season)}
    return calendar

#generates level requirements for each day during given season based on given starting/ending date and total experience to obtain
def getSeasonLevels():
    calendar = calendarRange()
    calendar = fillSeasonDates(calendar)

    for current_season in Season.objects.all():

        required_exp = current_season.totalexp
        days_count = (current_season.date_end - current_season.date_start).days + 1
        help_index = 0
        level_exp = [12.5*n*n + 962.5*n - 975 for n in range(1, 101)] #ingame formula to define experience required at certain level
        level_sum_exp = [sum(level_exp[:i]) for i in range(len(level_exp))] #array with calculated total experience per level, level as index + 1

        for single_date in [current_season.date_start + timedelta(n) for n in range(0, days_count-1)]: #looping through season days

            season_day = (single_date - current_season.date_start).days
            today_exp = ((season_day + 1)/days_count)*required_exp
            for lvl in level_sum_exp: #obtains level from array based on experience calculated for specific day
                if today_exp > lvl:
                    help_index = level_sum_exp.index(lvl)
                    calendar[single_date.strftime('%Y-%m-%d')]['level'] = help_index + 1

    return calendar


def getEventStyleAttributes(event):
    return [event.border_color, event.rowA_color, event.rowB_color]

#returns given event available information
def fillEventAttributes(event):
    eventStyle = ''
    try:
        eventStyle = getEventStyleAttributes(event.event_style)
    except:
        pass


    attr = {    'name' : event.name,
                'date_start' : event.date_start.strftime('%Y-%m-%d'),
                'date_end' : event.date_end.strftime('%Y-%m-%d'),
                'type' : event.get_event_type_display() if hasattr(event, 'event_type') else "community",
                'platform' : event.get_event_platform_display() if hasattr(event, 'event_platform') else '',
                'description' : event.description,
                'image' : event.image,
                'image_modal' : event.image_modal,
                'html_content' : event.html_content,
                'external_link' : event.external_link,
                'event_style' : eventStyle,
           }

    if hasattr(event, 'timezone') and event.timezone:
        attr['timezone'] = event.get_timezone_display()
    if hasattr(event, 'time_start') and event.time_start:
        attr['time_start'] = event.time_start.strftime("%H:%M:%S")
    if hasattr(event, 'event_platform') and event.event_platform:
        attr['platform'] = event.get_event_platform_display()

    return attr


def currentSeason():
    return Season.objects.get(date_start__lte=date.today(), date_end__gt=date.today())

#returns events dictionary
def addEvents():
    events = {}
    for event in Event.objects.all():
        events[event.pk] = fillEventAttributes(event)
    return events

#returns community events dictionary
def addCommunityEvents():
    communityEvents = {}
    for event in CommunityEvent.objects.all():
        communityEvents[event.pk] = fillEventAttributes(event)
    return communityEvents

#returns today dictionary with available information
def getToday(calend):
    seasonAttr = '' #current season attributes if available
    lvl = '' #current level requirement if available
    nextSeason = '' #next season if information available
    daysnext = '' #days till next season if information available

    try:
        seasonAttr = fillSeasonAttributes(currentSeason())
    except:
        pass

    try:
        lvl = calend['level']
    except:
        pass

    try:
        nextSeason = Season.objects.get(date_start__gt=date.today()).name
        daysnext = (Season.objects.get(date_start__gt=date.today()).date_start - date.today()).days
    except:
        pass

    today = {
        'date' : [date.today().strftime('%Y-%m-%d'), date.today().strftime('%d/%m'), date.today().strftime('%Y')],
        'last_update' : datetime.now(),
        'season' : seasonAttr,
        'events' : getTodayEvents(),
        'level' : lvl,
        'next_season' : nextSeason,
        'days_to_next_season' : daysnext,
    }
    return today

#returns list with today events
def getTodayEvents():
    event_list = []

    for event in Event.objects.filter(date_start__lte=date.today(),
                                date_end__gte=date.today(), ):

        event_list.append(fillEventAttributes(event))

    for communityevent in CommunityEvent.objects.filter(date_start__lte=date.today(),
                                    date_end__gte=date.today(), ):
        event_list.append(fillEventAttributes(communityevent))

    return event_list

#generates dictionary with calendar, specifics about today and all events attributes, then sets up modal context information
def setToday():
    global globalcalendar
    globalcalendar = getSeasonLevels()
    keyDate = date.today() + timedelta(0)
    global today
    today = getToday(globalcalendar[keyDate.strftime('%Y-%m-%d')])
    globalcalendar['today'] = today
    globalcalendar['events'] = addEvents()
    globalcalendar['communityEvents'] = addCommunityEvents()
    global modal
    modal = {'events' : getModal(), 'season' : seasonModal()}


setToday()

#runs setToday function every day at specified hours using APScheduler
def job_function():
    setToday()
sched = BackgroundScheduler()
sched.add_job(job_function, 'cron', second ='10', hour='0,1,12,23')
sched.start()


#sends json under /json path
def getJson(request):
    return JsonResponse(globalcalendar)

def index(request):
    return render(request, 'en/calendar/index.html', {'today' : today, "modal" : modal})
