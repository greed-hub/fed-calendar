let forwardButton = document.getElementById('forwardButton');
let backwardButton = document.getElementById('backwardButton');
let backToTop = document.getElementById('backTop');
let calendarContainer = document.getElementById('calendar');
let rowHeaderElement = document.getElementById('rowheader');
let dates = document.getElementById('dates');

let limit = 15; //days to render at one button click
let forwardCounter = 0; //marker for days rendered
let backwardCounter = -limit; //marker for days rendered backwards

let doubleEvents = ['0'];
let officialEvents = ['0','0'];
let communityEvents = ['0','0','0'];

let prevDoubleEvents = ['0'];
let prevOfficialEvents = ['0','0'];
let prevCommunityEvents = ['0','0','0'];

let data = {};
let modalContext = "";

//get data from /calendar/json and create calendar header and render first part when request succeeds
let request = new XMLHttpRequest();
request.overrideMimeType("application/json");
request.open('GET', "/calendar/json", true);
request.onload  = function() {
   data = JSON.parse(request.responseText);
   createRowHeader();
   renderCalendar(forwardCounter, limit);
};
request.send(null);

forwardButton.addEventListener('click', function() {
    renderCalendar(forwardCounter, limit);
});

//render calendar backwards and return scroll to position before render
backwardButton.addEventListener('click', function() {
    let prevViewportHeight = document.documentElement.scrollHeight;
    renderCalendar(backwardCounter, limit);
    scrollReturn(prevViewportHeight);
});

//separates calendar row colors
function rowColor(i) {
    return i % 2 === 0 ? 'row-gold' : 'row-lgold'
}

//separates event row colors
function colorSeparation(ii, list) {
    return ii % 2 === 0 ? `background-color: rgb(${list[1]}); border-color: rgb(${list[0]});` : `background-color: rgb(${list[2]}); border-color: rgb(${list[0]});`
}

function isZero(element) {
    return element === '0'
}

//sets key for given event type, checks if key available in currentDate then makes changes to eventList array
//and generates columns for each event accordingly or if not available generates empty columns
function buildRowContent(k, currentDate, eventList, key) {
    let eventKey = (key === 'communityEventsID' ? 'communityEvents' : 'events');
    let htmlOutput = '';

    if (key in data[currentDate]) { //checks if key found in current date if not returns empty column string
        eventList.forEach((item, index) => { //modifies event list by removing events which ended before current date
            if (!data[currentDate][key].includes(item)) {
                eventList.splice(index, 1, '0');
            }
        });

        data[currentDate][key].forEach((item, index) => {//adds new event ID to the event list
            if (!eventList.includes(item)) {
                eventList.splice(eventList.findIndex(isZero), 1, item);
            }
        });

        eventList.forEach((item, index) => { //loops through event list and builds string with html depending on event status
            let imageString = '';
            if (item === '0') { //when 0 there is no event, checks for today date to change color
                if (currentDate === new Date().toISOString().slice(0, 10)) {
                    htmlOutput += `<div class='col space event-none todayRow'> </div>`;
                } else {
                    htmlOutput += `<div class='col space event-none ${rowColor(k)}'> </div>`;
                }

            } else {
                modalContext = buildModal(data[eventKey][item]);
                styleArray = data[eventKey][item]['event_style'];

                if (data[eventKey][item]['date_start'] === currentDate) {
                    if (data[eventKey][item]['date_end'] === currentDate) { //one day event
                        htmlOutput += `<div class='col space event-oneday' style='${colorSeparation(k, styleArray)}' onclick="loadmodal(this)" context="${modalContext}"
                        headerContext="${data[eventKey][item]['name']}">
                        <div class="startBorder" style="text-align: center; ${colorSeparation(k, styleArray)}">One day</div><div class="centerEvent">${data[eventKey][item]['name']}</div>
                        </div>`;
                    } else { //event is starting
                        htmlOutput += `<div class='col space event-start' style='${colorSeparation(k, styleArray)}' onclick="loadmodal(this)" context="${modalContext}"
                        headerContext="${data[eventKey][item]['name']}">
                        <div class="startBorder" style="text-align: center; ${colorSeparation(k, styleArray)}">Start</div><div class="centerEvent">${data[eventKey][item]['name']}</div>
                        </div>`;
                    }
                } else if (data[eventKey][item]['date_end'] === currentDate) { //event is ending
                    htmlOutput += `<div class='col space event-end' style='${colorSeparation(k, styleArray)}' onclick="loadmodal(this)" context="${modalContext}"
                    headerContext="${data[eventKey][item]['name']}">
                    <div class="endBorder" style="text-align: center; margin: auto;${colorSeparation(k, styleArray)}">End</div><div class="centerEvent">${data[eventKey][item]['name']}</div>
                    </div>`;
                } else { //event is ongoing

                    if (data[eventKey][item]['image']) { //adds image on event second row if image available
                        day = currentDate.split("-")
                        if (new Date(day[0],day[1]-1,day[2]).toISOString().slice(0,10) === data[eventKey][item]['date_start']) {
                            imageString = `<img src=${data[eventKey][item]['image']} class='img-fluid rounded p-0 m-0'></img>`;
                        } else {
                            imageString = '';
                        }
                    }

                    htmlOutput += `<div class='col space event-continue' style='${colorSeparation(k, styleArray)}' onclick="loadmodal(this)" context="${modalContext}"
                    headerContext="${data[eventKey][item]['name']}">${(imageString !== '') ? imageString : ''}</div>`;
                }
            }
        });

    } else { //adds empty column when key not found in current date, checks for today date to change color
        eventList.forEach((item, index) => {
            if (currentDate === new Date().toISOString().slice(0, 10)) {
                htmlOutput += `<div class='col space event-none todayRow'> </div>`;
            } else {
                htmlOutput += `<div class='col space event-none ${rowColor(k)}'> </div>`;
            }
        });
    }

    return htmlOutput
}

//checks if season is starting/ending in currentDate and generates matching information
function checkSeasonStartEnd(currentDate) {
    if ('endingSeason' in data[currentDate] && 'startingSeason' in data[currentDate]) {
        return `<div class='row seasonStartEnd'>
        ${(data[currentDate]['endingSeason']['attributes']['endingText'] !== null ?
        data[currentDate]['endingSeason']['attributes']['endingText'] : data[currentDate]['endingSeason']['attributes']['name'] + ' Concludes')}<br>
        ${data[currentDate]['startingSeason']['attributes']['name']} Starts</div>`
    } else if ('endingSeason' in data[currentDate]) {
        return `<div class='row seasonStartEnd'>
        ${(data[currentDate]['endingSeason']['attributes']['endingText'] !== null ?
        data[currentDate]['endingSeason']['attributes']['endingText'] : data[currentDate]['endingSeason']['attributes']['name'] + ' Concludes')}</div>`
    } else if ('startingSeason' in data[currentDate]) {
        return `<div class='row seasonStartEnd'>${data[currentDate]['startingSeason']['attributes']['name']} Starts</div>`
    }
    return ''
}

//generates complete currentDate row content with specified level and buildRowContent function
function buildRows(kk, currentDate) {
    let rowString = colB = colC = colD = colE = rowSeasonStartEnd = ""

    rowSeasonStartEnd = checkSeasonStartEnd(currentDate);

    rowString = `<div class="row flex-nowrap p-0 m-0 text-dark ${rowColor(kk)} ">`;

    if (currentDate === new Date().toISOString().slice(0, 10)) {
        rowString = `<div class="row flex-nowrap p-0 m-0 text-dark todayRow">`;
    }

    //colB level required, colC double, colD official and colE community events
    colB = `<div class='col event-none spacex' style='max-width: 4em;'>
    <div class="centerHV">${ data[currentDate]['level'] ? '<strong style="font-size: 27px">' + data[currentDate]['level'] + '</strong>' : ''}</div></div>`;
    colC =`${buildRowContent(kk, currentDate, doubleEvents, 'doubleEventsID')}`;
    colD =`${buildRowContent(kk, currentDate, officialEvents, 'officialEventsID')}`;
    colE =`${buildRowContent(kk, currentDate, communityEvents, 'communityEventsID')}`;

    return rowSeasonStartEnd + rowString + colB + colC + colD + colE + "</div>";
}

//depending on forward/backward direction set up by counter postivie/negative value it generates column with dates and given date row content
//with buildRows function, then after reaching amount of days given by limit it injects htmlString into the container
function renderCalendar(counter, limit) {
    let htmlString = ""
    let datesString = ""

    if (counter < 0) { //counter < 0 renders backwards
        for (let i = counter + limit; i > counter; i--) {
            let currentDate = new Date(new Date().setDate(new Date().getDate() + i));
            currentDate = currentDate.toISOString().slice(0,10);

            if (i === 0) {
                buildRows(i, currentDate);
                continue;
            }

            if (!(currentDate in data)) { //hides button when full content is rendered
                backwardButton.classList.add("invisible");
                break;
            } else { //generates column html string with dates
                datesString = `<div class='row p-0 m-0 flex-nowrap ${rowColor(i)}'>
                <div class="col text-dark spacex" style='border-right: 3px solid #94723b;'><div class="centerHV">${formatDate(currentDate)}</div></div></div>` + datesString;
                if ('endingSeason' in data[currentDate] && 'startingSeason' in data[currentDate]) {
                    datesString = `<div class='row p-2 m-0'>&nbsp<br>&nbsp</div>` + datesString;
                } else if ('endingSeason' in data[currentDate] || 'startingSeason' in data[currentDate]){
                    datesString = `<div class='row p-2 m-0'>&nbsp</div>` + datesString;
                }
            }
            htmlString = buildRows(i, currentDate) + htmlString;
        }

    } else { // else render forward
        for (let i = counter; i < counter + limit; i++) {
            let currentDate = new Date(new Date().setDate(new Date().getDate() + i));
            currentDate = currentDate.toISOString().slice(0,10);

            if (!(currentDate in data)) { //hides button when full content is rendered
                forwardButton.classList.add("invisible");
                break;
            } else { //generates column html string with dates
                if ('endingSeason' in data[currentDate] && 'startingSeason' in data[currentDate]) {
                    datesString += `<div class='row p-2 m-0'>&nbsp<br>&nbsp</div>`;
                } else if ('endingSeason' in data[currentDate] || 'startingSeason' in data[currentDate]){
                    datesString += `<div class='row p-2 m-0'>&nbsp</div>`;
                }

                if (currentDate === new Date().toISOString().slice(0, 10)) {
                    datesString += `<div class='row p-0 m-0 flex-nowrap ${rowColor(i)}'>
                    <div class="col text-dark spacex todayRow" style='border-right: 3px solid #94723b;'><div class="centerHV">${formatDate(currentDate)}</div></div></div>`;
                } else {
                    datesString += `<div class='row p-0 m-0 flex-nowrap ${rowColor(i)}'>
                    <div class="col text-dark spacex" style='border-right: 3px solid #94723b;'><div class="centerHV">${formatDate(currentDate)}</div></div></div>`;
                }
            }
            htmlString += buildRows(i, currentDate);
        }
    }

    if ( counter < 0 ) {
        dates.insertAdjacentHTML('afterbegin', datesString)
        calendarContainer.insertAdjacentHTML('afterbegin', htmlString);
        backwardCounter -= limit;
    } else {
        dates.insertAdjacentHTML('beforeend', datesString)
        calendarContainer.insertAdjacentHTML('beforeend', htmlString);
        forwardCounter += limit;
    }
}

//generates modal content with given event information
function buildModal(currentEvent) {

    if (currentEvent['image_modal']) {
        imageModalString = `<img src=${currentEvent['image_modal']} class='img-fluid rounded' style='box-shadow: 0 0 6px #c7974b;'></img>`
    } else {
        imageModalString = ''
    }

    let htmlDescription = ''
    if (currentEvent['html_content']) {
        htmlDescription = `<div>${currentEvent['html_content']}</div>`
    } else if (currentEvent['description']) {
        htmlDescription = currentEvent['description']
    }

    return `
    <div class='container-fluid p-5' style=' box-shadow: 0 16px 48px rgb(2 2 1 / 31%);'>

        <div class='row'>
            <div class='col-sm-6'>
                ${imageModalString}
            </div>
                <div class='col-sm-6 justify-content-center'>
                    <div class=''>
                    ${currentEvent['platform'] ? '<b>Platform:</b> ' + currentEvent['platform'].toUpperCase() + '<br>' : ''}
                    <b>Date start:</b> ${currentEvent['date_start']}<br>
                    ${currentEvent['time_start'] && currentEvent['timezone'] ? '<b>Time start: </b>' + currentEvent['time_start'] + ' ' + currentEvent['timezone'] + '<br>' : ''}
                    <b>Date end:</b> ${currentEvent['date_end']}<br>
                    ${currentEvent['external_link'] ? '<b>Link:</b> <a href=' + currentEvent['external_link'] + '>Click here</a> 👈<br>' : ''}
                    <br>
                    ${htmlDescription}
                    </div>
                </div>
            </div>
        </div>

    </div>`
}

//generates calendar header with columns description
createRowHeader = () => {
    let rh =    `       <div class='row flex-nowrap p-0 m-0'>
                            <div class="col-1 topRow" style="border-right: 0; border-left: 0; min-width: 4em; max-width: 4em;">Level<span style="font-size: 15px; cursor: pointer"
                            onclick="loadmodal(this)" context="<div style='margin: 20px; text-align: center;'>level disclaimer information</div>"
                            headerContext="Level disclaimer">&nbsp🛈</span></div>
                            <div class="col p-0 m-0"><div class="container-fluid p-0 m-0"><div class="row flex-nowrap p-0 m-0">
                            <div class="col-2 topRow" style="min-width: ${6*doubleEvents.length}em;">X2</div>
                            <div class="col-4 topRow" style="min-width: ${6*officialEvents.length}em;">Official</div>
                            <div class="col-6 topRow" style="min-width: ${6*communityEvents.length}em;">Community</div></div><div><div>
                        </div>`

        rowHeaderElement.insertAdjacentHTML('afterbegin', rh);
};

function formatDate(day) {

    day = day.split("-")

    let d = new Date(day[0], day[1]-1, day[2], 12, 0, 0, 0);

    let weekday = new Array(7);
    weekday[0] = "Sun.";
    weekday[1] = "Mon.";
    weekday[2] = "Tues.";
    weekday[3] = "Wed.";
    weekday[4] = "Thurs.";
    weekday[5] = "Fri.";
    weekday[6] = "Sat.";

    let month = new Array(12);
    month[0] = "Jan.";
    month[1] = "Feb.";
    month[2] = "March";
    month[3] = "April";
    month[4] = "May";
    month[5] = "June";
    month[6] = "July";
    month[7] = "Aug.";
    month[8] = "Sept.";
    month[9] = "Oct.";
    month[10] = "Nov.";
    month[11] = "Dec.";

    return `<span class="dateCol">${weekday[d.getDay()]}</span><br>
            <strong class="dateNumber">${day[2]}</strong><br>
            <span class="dateCol">${month[day[1]-1]}</span>`
}

//when calendar renders backward it returns scroll to position when button was clicked
scrollReturn = (prev) => {
    let currentHeight = document.documentElement.scrollHeight;
    window.scrollBy(0, currentHeight-prev);
}

function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

//renders calendar forward if forwardButton is in viewport
document.addEventListener('scroll', function () {
    if (isInViewport(forwardButton)) {
            renderCalendar(forwardCounter, limit);
    }
}, {
    passive: true
});

backToTop.addEventListener('click', () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
});
