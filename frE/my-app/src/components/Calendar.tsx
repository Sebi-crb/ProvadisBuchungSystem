import './Calendar.css';
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import deLocale from '@fullcalendar/core/locales/de'
import { Box } from '@mui/material';

export default function Calendar() {

    const events = [
        { title: "Kurs 1", start: "2026-03-02", end: "2026-03-02T12:00:00" },
        { title: "Kurs 2", start: "2026-03-04T14:00:00", end: "2026-03-04T16:00:00" },
        { title: "Kurs 3", start: "2026-03-05T09:00:00", end: "2026-03-15T11:00:00" },
    ];

  return (
    <>
      <Box sx={{ width: "70vw" }}>
        <FullCalendar
          plugins={[timeGridPlugin, dayGridPlugin]}
          initialView="dayGridMonth"
          locale={deLocale}
          weekends={false}
          height="70vh"
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'addEvent timeGridWeek,timeGridDay,dayGridMonth',
          }}
          customButtons={{
            addEvent: {
                text: "+",
                click: () => null,
                hint: "Neuen Kurs eintragen"
            }
          }}
          views={{
            dayGridMonth: {
              weekends: false  
            }
          }}
          events={events}
        />
    
      </Box>
    </>
  );
}