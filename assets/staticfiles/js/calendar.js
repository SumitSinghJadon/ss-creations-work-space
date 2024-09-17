class EventCalendar {
    constructor(targetId) {
        this.targetId = targetId;
        this.date = new Date();
        this.dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        this.events = [];
        this.initializeCalendar();
    }

    initializeCalendar() {
        this.render();
        this.setupEventHandlers();
    }

    render() {
        const currentYear = this.date.getFullYear();
        const currentMonth = this.date.getMonth() + 1;
        const padMonth = currentMonth.toString().padStart(2, '0');
        const currentCalendarDate = `${currentYear}-${padMonth}`;
        const daysInMonth = new Date(currentYear, currentMonth, 0).getDate();
        const firstDayOfWeek = this.date.getDay();
        const trCount = Math.ceil((daysInMonth + firstDayOfWeek) / 7);

        let currentDay = 0;
        let weekWrapper = $('<tbody>');
        // Create calendar Week & Days
        for (let week = 0; week < trCount; week++) {
            const row = $('<tr>');
            for (let weekDay = 0; weekDay < 7; weekDay++) {
                if (week === 0 && weekDay < firstDayOfWeek) {
                    row.append('<td></td>');
                } else if (currentDay < daysInMonth) {
                    currentDay++;
                    row.append(`<td>${currentDay}</td>`);
                } else {
                    row.append('<td></td>');
                }
            }
            weekWrapper.append(row);
        }

        // Create calendar Table
        const table = $('<table>', { id: 'knox-calendar' });
        table.append(
            $('<thead>').append(
                $('<tr>').append(this.dayNames.map(name => `<th>${name}</th>`).join(''))
            )
        );

        table.append(weekWrapper);
        $(`#${this.targetId}`).empty().append(table);

        $("#currentMonth").val(currentCalendarDate);

        $(`#${this.targetId} td`).css({
            width: '100px',
            height: '100px',
        });

        this.renderEvents()
    }

    addEvent(startDateTime, endDateTime, title, description) {
        this.events.push({ startDateTime, endDateTime, title, description });
        this.renderEvents();
    }

    renderEvents() {
        // Clear existing event bars
        $(`#${this.targetId} .event-bar`).remove();

        // Render events
        for (const event of this.events) {
            const startDate = new Date(event.startDateTime);
            const endDate = new Date(event.endDateTime);

            // Check if the event is in the current month
            if (startDate.getFullYear() === this.date.getFullYear() && startDate.getMonth() === this.date.getMonth()) {
                const startDay = startDate.getDate();
                const endDay = endDate.getDate();
                const startCell = startDay + this.date.getDay() - 1;
                const endCell = endDay + this.date.getDay() - 1;

                // Create event range bar element
                const eventBar = $('<div>', { class: 'bg-blue-300 px-1 rounded text-sm', text: event.title });

                // Find the table cells for the event and append the event bar
                for (let cell = startCell; cell <= endCell; cell++) {
                    const cellElement = $(`#${this.targetId} td`).eq(cell);
                    cellElement.append(eventBar.clone());
                }
            }
        }
    }

    setupEventHandlers() {
        const calendar = this;

        $("#prevMonthCal").on("click", function () {
            calendar.date.setMonth(calendar.date.getMonth() - 1);
            calendar.render();
        });

        $("#nextMonthCal").on("click", function () {
            calendar.date.setMonth(calendar.date.getMonth() + 1);
            calendar.render();
        });

        $("#currentMonth").on("change", function () {
            const date = new Date($(this).val());
            calendar.changeMonth(date);
        });
    }

    changeMonth(date) {
        this.date = date;
        this.render();
    }
}
