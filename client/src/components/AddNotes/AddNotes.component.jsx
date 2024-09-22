import { useState } from "react";
import "./AddNotes.Styles.scss";
import axios from "axios";

const AddNotes = () => {
  const [notes, setNotes] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [noteName, setNoteName] = useState("");
  const [noteDescription, setNoteDescription] = useState("");

  const handleAddNoteClick = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setNoteName("");
    setNoteDescription("");
  };

  const handleCreateNote = async () => {
    const newNote = {
      name: noteName,
      description: noteDescription,
      Org_id: "30001",
    };

    try {
      await axios.post("http://127.0.0.1:5000/AddNotes", { newNote });
      setNotes([...notes, newNote]);
      handleCloseModal();
    } catch (error) {
      console.error("Error creating note:", error);
    }
  };

  return (
    <div className="add-notes-container">
      <h2>Notes</h2>
      <button className="add-note-btn" onClick={handleAddNoteClick}>
        Add Note
      </button>

      {/* Notes List */}
      <ul className="notes-list">
        {notes.map((note, index) => (
          <li key={index}>
            <h3>{note.name}</h3>
            <p>{note.description}</p>
          </li>
        ))}
      </ul>

      {/* Modal for adding a note */}
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <span className="close-btn" onClick={handleCloseModal}>
              &times;
            </span>
            <h2>Add a New Note</h2>
            <div className="form-group">
              <label>Note Name:</label>
              <input
                type="text"
                value={noteName}
                onChange={(e) => setNoteName(e.target.value)}
                placeholder="Enter note name"
              />
            </div>
            <div className="form-group">
              <label>Description:</label>
              <textarea
                value={noteDescription}
                onChange={(e) => setNoteDescription(e.target.value)}
                placeholder="Enter note description"
              />
            </div>
            <button className="create-note-btn" onClick={handleCreateNote}>
              Create Note
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AddNotes;
