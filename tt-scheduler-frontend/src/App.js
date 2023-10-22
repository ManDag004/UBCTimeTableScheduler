import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

function App() {
  const [courseNames, setCourseNames] = useState([]);
  const [results, setResults] = useState([]);
  const [term, setTerm] = useState('1');
  const [minStartTime, setMinStartTime] = useState('');
  const [maxEndTime, setMaxEndTime] = useState('');
  const localizer = momentLocalizer(moment);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    populateEvents();
  }, [results]);

  const populateEvents = () => {
    let events = [];
    for (let i = 0; i < results.length; i++) {
      let course = results[i];
      console.log(course);
      let title = course["title"];
      let days = course["days"];
      let start_time = course["start_time"];
      let end_time = course["end_time"];
      console.log("days", days);
      
      days.map((day) => {
        console.log(day);
        let event = {
          title: title,
          start: new Date(2023, 9, getDayOfWeek(day), parseInt(start_time.split(":")[0]), parseInt(start_time.split(":")[1])),
          end: new Date(2023, 9, getDayOfWeek(day), parseInt(end_time.split(":")[0]), parseInt(end_time.split(":")[1])),
        }
        events.push(event);
      });

    }
    setEvents(events);
  }

  const getDayOfWeek = (day) => {
    console.log(day);
    switch (day) {
      case "Mon":
        return 2;
      case "Tue":
        return 3;
      case "Wed":
        return 4;
      case "Thu":
        return 5;
      case "Fri":
        return 6;
      default:
        return 0;
    }
  }

  const handleAddCourse = () => {
    setCourseNames([...courseNames, '']);
  };

  const handleCourseNameChange = (index, newName) => {
    const updatedCourseNames = [...courseNames];
    updatedCourseNames[index] = newName;
    setCourseNames(updatedCourseNames);
  };

  const handleDeleteCourse = (index) => {
    const updatedCourseNames = [...courseNames];
    updatedCourseNames.splice(index, 1);
    setCourseNames(updatedCourseNames);
  };

  const handleFetchResults = () => {
    let criteria = {
      courseNames: courseNames,
      term: term,
      minStartTime: minStartTime,
      maxEndTime: maxEndTime
    }

    axios.post('http://127.0.0.1:8000/api/courses/', { search_params: criteria })
      .then(response => {
          setResults(response.data);
      })
      .catch(error => {
          console.error('Error fetching courses:', error);
      });
  };

  return (
    <div className="container">
      <header>
        <h1 className="header-title">UBC Timetable Scheduler</h1>
      </header>
      <main>
        <div className="course-inputs">
          {courseNames.map((courseName, index) => (
            <div key={index} className="input-container">
              <input
                type="text"
                placeholder="Enter course name"
                value={courseName}
                onChange={e => handleCourseNameChange(index, e.target.value)}
              />
              <button
                className="delete-button"
                onClick={() => handleDeleteCourse(index)}
              >
                Delete
              </button>
            </div>
          ))}
          <button className="add-course-button" onClick={handleAddCourse}>
            Add Course
          </button>
          <div className="term-input">
            <label htmlFor="termSelect">Select Term:</label>
            <select
              id="termSelect"
              value={term}
              onChange={(e) => setTerm(e.target.value)}
            >
              <option value="1">Term 1</option>
              <option value="2">Term 2</option>
            </select>
          </div>
          <div className="time-inputs">
            <div>
              <label>Minimum Start Time:</label>
              <input
                type="time"
                id="minStartTime"
                value={minStartTime}
                onChange={(e) => setMinStartTime(e.target.value)}
              />
            </div>
            <div>
              <label>Maximum End Time:</label>
              <input
                type="time"
                id="maxEndTime"
                value={maxEndTime}
                onChange={(e) => setMaxEndTime(e.target.value)}
              />
            </div>
          </div>
        </div>
        <button className="fetch-button" onClick={handleFetchResults}>
          Fetch Results
        </button>
        {/* <div className="results">
          <h2 className="results-title">Course Results</h2>
          <ul className="results-list">
            {results.map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        </div> */}
      </main>
      {/* default view of week*/}
      
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 750 }}
        defaultView='week'
        defaultDate={new Date(2023, 9, 1)}
        toolbar={false}
      />
    </div>
  );
}

export default App;
 