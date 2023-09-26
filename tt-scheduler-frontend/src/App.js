import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React, { useState } from 'react';

function App() {
  const [courseNames, setCourseNames] = useState([]);
  const [results, setResults] = useState([]);
  const [term, setTerm] = useState('1');
  const [minStartTime, setMinStartTime] = useState('');
  const [maxEndTime, setMaxEndTime] = useState('');

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

    axios.post('https://ManDag004.pythonanywhere.com/api/courses/', { search_params: criteria })
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
        <div className="results">
          <h2 className="results-title">Course Results</h2>
          <ul className="results-list">
            {results.map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        </div>
      </main>
    </div>
  );
}

export default App;
 