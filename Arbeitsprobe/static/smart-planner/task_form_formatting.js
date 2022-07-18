// Event fields
const deadlineDate = document.getElementById('id_deadline_date')
const deadlineTime = document.getElementById('id_deadline_time')
const duration = document.getElementById('id_duration')
const newTitleInputField = document.getElementById('id_title')
const newTitleBackground = document.getElementById('id_new-task-title')

// Buttons
const closeButton = document.getElementById('id_close-button-new-task')
const deadlineDatePrev = document.getElementById('id_deadline-date-prev')
const deadlineDateNext = document.getElementById('id_deadline-date-next')
const deadlineTimePrev = document.getElementById('id_deadline-time-prev')
const deadlineTimeNext = document.getElementById('id_deadline-time-next')
const durationHourPrev = document.getElementById('id_duration-h-prev')
const durationMinPrev = document.getElementById('id_duration-min-prev')
const durationHourNext = document.getElementById('id_duration-h-next')
const durationMinNext = document.getElementById('id_duration-min-next')
const submitButton = document.getElementById('id_submit-button-new-task')



// Onload of the template check if create or update view
$(document).ready(()=> {
    console.log('ich tue was!')
    enableSubmitIfUpdate();
})


// ----------------------- EVENT LISTENERS --------------------------
// using event listeners there is no need to use an onclick() function in the html file
// the function is called directly in the addEventListener() function

// enable title field and submit button on valid input
newTitleInputField.addEventListener('keyup', () => {
    enableSubmit();
    checkDuration();
})

// prevent default firefox datepicker from showing up
deadlineDate.addEventListener('click', function(event) {
    event.preventDefault()
}, false)

// toggle button actions
deadlineDatePrev.addEventListener('click', () => {
    deadlineDate.stepDown(1);
    checkDate();
    checkTime();
})

deadlineDateNext.addEventListener('click', () => {
    deadlineDate.stepUp(1);
    checkDate();
    checkTime();
})

deadlineTimePrev.addEventListener('click', () => {
    deadlineTime.stepDown(60);
    checkTime();
})

deadlineTimeNext.addEventListener('click', () => {
    deadlineTime.stepUp(60);
    checkTime();
})

durationHourPrev.addEventListener('click', () => {
    duration.stepDown(60);
    checkDuration();
})

durationHourNext.addEventListener('click', () => {
    duration.stepUp(60);
    checkDuration();
})

durationMinPrev.addEventListener('click', () => {
    duration.stepDown(5);
    checkDuration();
})

durationMinNext.addEventListener('click', () => {
    duration.stepUp(5);
    checkDuration();
})

// check for valid form after manual input
// use 'focusout' because with 'input' or 'change' not all dates can be entered, although they might be valid
deadlineDate.addEventListener('focusout', () => {
    checkDate();
    checkTime();
})

deadlineTime.addEventListener('focusout', () => {
    checkTime();
})
duration.addEventListener('focusout', () => {
    checkDuration();
})
// ----------------- FUNCTIONS -------------------------

// called on template load
// enables submit for the update view since there is a valid title input already
function enableSubmitIfUpdate() {
    enableSubmit();
    checkDate();
    checkTime();
}

// checks if input is valid and enables submit button and title
function enableSubmit() {

    // Spaces are not a valid input for the title
    if (newTitleInputField.value.trim() !== '') {
        newTitleBackground.classList.add('active');
        submitButton.disabled = false;
    } else {
        newTitleBackground.classList.remove('active');
        submitButton.disabled = true;
    }
}

//checks if time inputs are valid and enables the toggle buttons
function checkDate() {
    if (deadlineDate.value <= getCurDate()) {
        deadlineDate.value = getCurDate();
        deadlineDatePrev.disabled = true;
    } else {
        deadlineDatePrev.disabled = false;
    }
}

function checkTime() {
    if (deadlineDate.value <= getCurDate() && deadlineTime.value <= getCurTime()) {
        deadlineTime.value = getCurTime();
        deadlineTime.stepUp(1);
        deadlineTimePrev.disabled = true;
    } else if (deadlineTime.value === '23:59') {
        deadlineTimeNext.disabled = true;
    } else if (deadlineTime.value === '00:00') {
        deadlineTimePrev.disabled = true;
    } else {
        deadlineTimePrev.disabled = false;
        deadlineTimeNext.disabled = false;
    }
}

function checkDuration() {
    if (duration.value <= '00:05') {
        duration.value = '00:05';
        durationHourPrev.disabled = true;
        durationMinPrev.disabled = true;
    } else {
        durationHourPrev.disabled = false;
        durationMinPrev.disabled = false;
    }
}

// functions for getting current date and time
function getCurTime() {
    var date = new Date();
    return ((date.getHours() < 10)?"0":"") + date.getHours() +":"+
        ((date.getMinutes() < 10)?"0":"") + date.getMinutes();
}

function getCurDate() {
    var date = new Date();
    return date.getFullYear() +"-"+
        (((date.getMonth() + 1) < 10)?"0":"") + (date.getMonth() + 1) +"-"+
        ((date.getDate() < 10)?"0":"") + date.getDate();
}

$("#id_deadline_date").datepicker(
    {
        onSelect: function () {
            checkTime();
            checkDate();
        },
        beforeShow: function () {
            $("#id_deadline_date").datepicker("option", "minDate", getCurDate());
        },
        showOtherMonths: true,
        dayNamesMin: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
        dateFormat: 'yy-mm-dd',
        firstDay: '1'
    });
