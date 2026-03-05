import { useEffect, useState } from "react";
import "./Calendar.css";
import FullCalendar from "@fullcalendar/react";
import timeGridPlugin from "@fullcalendar/timegrid";
import dayGridPlugin from "@fullcalendar/daygrid";
import deLocale from "@fullcalendar/core/locales/de";
import { Box } from "@mui/material";
import InfoPopup from "./InfoPopup.tsx";
import AddPopup from "./AddPopup.tsx";
import type { EventSourceInput } from "@fullcalendar/core/index.js";

export default function Calendar(props: { termine: any, gruppen: any }) {
  const [showInfoPopup, setShowInfoPopup] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const [showAddPopup, setShowAddPopup] = useState(false);

  const emptyEvent = {
    title: "",
    start: new Date(),
    end: new Date(),
    extendedProps: {
      trainer: [],
      group: [],
      raum: "",
    },
  };
  const [newEvent, setNewEvent] = useState(emptyEvent);

  const [events, setEvents] = useState<EventSourceInput>(props.termine);

  useEffect(() => {
    let finishedEvents: any = [];
    for (const termin of props.termine) {
      const start = new Date(termin?.start);
      start.setHours(8, 0, 0, 0);

      const end = new Date(termin?.end);
      end.setHours(16, 30, 0, 0);

      console.log("gruppe", termin);

      const formattedEvent = {
        title: termin?.title,
        start: start,
        end: end,
        extendedProps: {
          trainer: termin?.trainer,
          group: termin?.gruppe,
          raum: termin?.extendedProps?.raum,
        },
      };
      finishedEvents.push(formattedEvent);
    }
    setEvents(finishedEvents);
    console.log("events", finishedEvents);
  }, [props.termine]);

  function handleNewEvent(event: any) {
    event.start = new Date(event.start);
    event.end = new Date(event.end);
    setEvents((prev: any) => [...prev, event]);
  }

  function openEventDetails(info: any) {
    console.log("info", info);
    setSelectedEvent(info.event);
    setShowInfoPopup(true);
    console.log(info.event.extendedProps);
  }

  function addNewEvent() {
    setShowAddPopup(true);
  }

  return (
    <>
      {showInfoPopup && (
        <InfoPopup
          onClose={() => setShowInfoPopup(false)}
          event={selectedEvent}
        />
      )}
      {showAddPopup && (
        <AddPopup
          onClose={() => setShowAddPopup(false)}
          event={null}
          onSend={handleNewEvent}
        />
      )}
      <Box sx={{ width: "70vw" }}>
        <FullCalendar
          plugins={[timeGridPlugin, dayGridPlugin]}
          initialView="dayGridMonth"
          locale={deLocale}
          weekends={false}
          height="70vh"
          headerToolbar={{
            left: "prev,next today",
            center: "title",
            right: "addEvent timeGridDay,timeGridWeek,dayGridMonth",
          }}
          customButtons={{
            addEvent: {
              text: "+",
              click: () => addNewEvent(),
              hint: "Neuen Kurs eintragen",
            },
          }}
          views={{
            dayGridMonth: {
              weekends: false,
            },
          }}
          events={events}
          eventClick={(info) => {
            openEventDetails(info);
          }}
        />
      </Box>
    </>
  );
}
