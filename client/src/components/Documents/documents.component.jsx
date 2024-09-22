import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import "./documents.Styles.scss"; // Assume you will create this SCSS file for styling
import { get_Documents } from "../../utils/GetDocuments";
import { organisationSelector } from "../../store/Organisation/organisation.selector";

export const DocumentUploads = () => {
  const [showModal, setShowModal] = useState(false);
  const [documentDetails, setDocumentDetails] = useState([]);
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const org = useSelector(organisationSelector);
  const [loading, setLoading] = useState(false); // Add loading state

  useEffect(() => {
    getDocs();
  }, []);

  async function getDocs() {
    setUploadedDocuments(await get_Documents(org.organisation_id));
  }

  // Handle input change for form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setDocumentDetails({
      ...documentDetails,
      [name]: value,
    });
  };

  // Handle file upload
  const handleFileChange = (e) => {
    setDocumentDetails({
      ...documentDetails,
      file: e.target.files[0],
    });
  };

  // Handle form submission (Upload document)
  const handleUpload = async () => {
    if (
      documentDetails.name &&
      documentDetails.description &&
      documentDetails.file
    ) {
      const formData = new FormData();
      formData.append("name", documentDetails.name);
      formData.append("description", documentDetails.description);
      formData.append("file", documentDetails.file);
      formData.append("org_id", org.organisation_id);
      try {
        setLoading(true); // Start loading
        const response = await axios.post(
          "http://127.0.0.1:5000/uploadDocuments",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          },
        );

        // If upload is successful, update the uploaded documents list
        if (response.status === 200) {
          getDocs();
          setShowModal(false); // Close the modal
          setDocumentDetails({ name: "", description: "", file: null }); // Reset form
        }
      } catch (error) {
        console.error("Error uploading document:", error);
        // You can handle error notifications here (e.g., showing an error message)
      } finally {
        setLoading(false); // Stop loading
      }
    } else {
      console.log("All fields are required!");
      // Optionally, show a validation error message here
    }
  };

  // Toggle modal visibility
  const toggleModal = () => setShowModal(!showModal);

  return (
    <div className="document-uploads">
      <h2>Uploaded Documents</h2>

      {/* Upload Button */}
      <button onClick={toggleModal} className="upload-btn">
        Upload Documents
      </button>

      {/* Modal Popup */}
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Upload New Document</h3>

            <label htmlFor="name">Document Name</label>
            <input
              name="name"
              type="text"
              value={documentDetails.name}
              onChange={handleInputChange}
              placeholder="Enter document name"
              required
            />

            <label htmlFor="description">Document Description</label>
            <textarea
              name="description"
              value={documentDetails.description}
              onChange={handleInputChange}
              placeholder="Enter document description"
              required
            />

            <label htmlFor="file">Upload File</label>
            <input
              type="file"
              name="file"
              onChange={handleFileChange}
              required
            />

            <button
              onClick={handleUpload}
              className="submit-btn"
              disabled={loading}
            >
              {loading ? "Uploading..." : "Upload"}
            </button>
            <button
              onClick={toggleModal}
              className="cancel-btn"
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Display Uploaded Documents */}
      <div className="uploaded-docs-list">
        {uploadedDocuments ? (
          uploadedDocuments.map((doc, index) => (
            <div key={index} className="document-item">
              <p>
                <strong>Document Name:</strong> {doc.document_name}
              </p>
              <p>
                <strong>Description:</strong> {doc.document_description}
              </p>
            </div>
          ))
        ) : (
          <p>No documents uploaded yet.</p>
        )}
      </div>
    </div>
  );
};
