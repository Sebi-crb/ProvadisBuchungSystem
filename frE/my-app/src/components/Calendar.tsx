import { useState } from 'react';
import './Calendar.css';
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import deLocale from '@fullcalendar/core/locales/de'
import { Box } from '@mui/material';
import InfoPopup from './InfoPopup.tsx';
import AddPopup  from './AddPopup.tsx';


export default function Calendar(props: { termine: any }) {
    const [showInfoPopup, setShowInfoPopup] = useState(false);
    const [selectedEvent, setSelectedEvent] = useState(null);

    const [showAddPopup, setShowAddPopup] = useState(false);


    function openEventDetails(info: any) {
        console.log(info);
        setSelectedEvent(info.event);
        setShowInfoPopup(true);
        console.log(info.event.extendedProps);
    }

    function addNewEvent() {
        setShowAddPopup(true);
    }

  return (
    <>
      {showInfoPopup && <InfoPopup onClose={() => setShowInfoPopup(false)} event={selectedEvent} />}
        {showAddPopup && <AddPopup onClose={() => setShowAddPopup(false)} event={null} />}
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
            right: 'addEvent timeGridDay,timeGridWeek,dayGridMonth',
          }}
          customButtons={{
            addEvent: {
                text: "+",
                click: () => addNewEvent(),
                hint: "Neuen Kurs eintragen"
            }
          }}
          views={{
            dayGridMonth: {
              weekends: false  
            }
          }}
          events={props.termine}
          eventClick={(info) => {openEventDetails(info)}}
        />
    
      </Box>
    </>
  );
}