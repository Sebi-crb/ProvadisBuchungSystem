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

export default function Calendar(props: { termine: any; gruppen: any }) {
  const [showInfoPopup, setShowInfoPopup] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const [showAddPopup, setShowAddPopup] = useState(false);

  const [events, setEvents] = useState<EventSourceInput>(props.termine);

  useEffect(() => {
    let finishedEvents: any = [];
    fetch("/api/kurs")
      .then((res) => res.json())
      .then((kurse) => {
        sessionStorage.setItem("kurse", JSON.stringify(kurse))
        for (const kurs of kurse) {
          const start = new Date(kurs?.startDate);
          start.setHours(8, 0, 0, 0);

          const end = new Date(kurs?.endDate);
          end.setHours(16, 30, 0, 0);

          const formattedEvent = {
            title: kurs?.titel,
            start: start,
            end: end,
            extendedProps: {
              trainerId: kurs?.trainerId,
              groupId: kurs?.gruppenId,
              raum: kurs?.raum,
              moduleId: kurs?.moduleId,
              id: kurs?.id,
            },
          };

          finishedEvents.push(formattedEvent);
        }
        setEvents(finishedEvents);
      });
  }, []);

  function handleNewEvent(event: any) {
    event.start = new Date(event.start);
    event.end = new Date(event.end);
    setEvents((prev: any) => [...prev, event]);
  }

  function openEventDetails(info: any) {
    console.log("info", info);
    setSelectedEvent(info.event);
    setShowInfoPopup(true);
  }

  function addNewEvent() {
    setShowAddPopup(true);
  }



  const getCustomButtons = {
    addEvent: {
      text: "+",
      click: () => addNewEvent(),
      hint: "Neuen Kurs eintragen",
    }
  }


  const isAdmin = sessionStorage.getItem("role") === "admin";

  const headerToolbar = {
  left: "prev,next today",
  center: "title",
  right: isAdmin
    ? "addEvent timeGridDay,timeGridWeek,dayGridMonth"
    : "timeGridDay,timeGridWeek,dayGridMonth",
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
      <Box sx={{ width: "70vw", float: "left", padding: 2 }}>
      <FullCalendar
  plugins={[timeGridPlugin, dayGridPlugin]}
  initialView="dayGridMonth"
  locale={deLocale}
  weekends={false}
  height="70vh"
  headerToolbar={headerToolbar}
  {...(isAdmin && { customButtons: getCustomButtons })}
  views={{
    dayGridMonth: { weekends: false },
  }}
  events={events}
  eventClick={(info) => openEventDetails(info)}
/>
      </Box>
    </>
  );
}
