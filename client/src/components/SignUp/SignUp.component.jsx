import "./SignUp.Styles.scss";
import OrgTypes from "./../../../solid data/orgtypes.json";
import { CreateOrganisation } from "./../../utils/Organisation";
import { useState } from "react";
import { useNavigate } from "react-router";
import { useDispatch } from "react-redux";
import { updateOrg } from "../../store/Organisation/organisation.actions";

const Inital_State = {
  organisation_name: "",
  organisation_type: "",
  organisation_description: "",
  organisation_email: "",
  password: "",
};

export const SignUp = () => {
  const [organisationData, setOrganisationData] = useState(Inital_State);
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const dispatch = useDispatch();
  const HandleSubmit = async (e) => {
    e.preventDefault(); // Prevent form from refreshing the page on submit
    try {
      const response = await CreateOrganisation(organisationData);
      if (response["message"] == "organisation/@created") {
        dispatch(updateOrg(response["data"]));
        navigate("/orgDashboard");
      } else if (response["message"] == "organisation/@exists") {
        setMessage("Organisation Email Exists");
      }
      console.log(response);
    } catch (error) {
      setMessage(error);
    }
  };

  const HandleChange = (e) => {
    const { name, value } = e.target;

    setOrganisationData({
      ...organisationData,
      [name]: value,
    });
  };

  return (
    <div className="signup-container">
      <h2 className="signup-title">Create Organisation</h2>
      {message && <p>{message}</p>}
      <form className="signup-form">
        <label htmlFor="organisation_name" className="signup-label">
          Name
          <input
            name="organisation_name"
            type="text"
            className="signup-input"
            value={organisationData.organisation_name}
            onChange={(e) => HandleChange(e)}
            placeholder="Enter your name"
            required
          />
        </label>

        <label htmlFor="organisation_email" className="signup-label">
          Email
          <input
            name="organisation_email"
            type="email"
            className="signup-input"
            value={organisationData.organisation_email}
            onChange={(e) => HandleChange(e)}
            placeholder="Enter your email"
            required
          />
        </label>

        <label htmlFor="organisation_type" className="signup-label">
          Organization Type
          <select
            name="organisation_type"
            className="signup-select"
            value={organisationData.organisation_type}
            required
            onChange={(e) => HandleChange(e)}
          >
            <option value="default">Select Organization Type</option>
            {OrgTypes.map((org) => (
              <option key={org.id} value={org.industry}>
                {org.industry}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="organisation_description" className="signup-label">
          Description
          <textarea
            name="organisation_description"
            className="signup-textarea"
            placeholder="Describe your organization"
            value={organisationData.organisation_description}
            onChange={(e) => HandleChange(e)}
          ></textarea>
        </label>

        <label htmlFor="password" className="signup-label">
          Password
          <input
            name="password"
            type="password"
            className="signup-input"
            value={organisationData.password}
            onChange={(e) => HandleChange(e)}
            placeholder="Password"
            required
          />
        </label>
        <button type="submit" className="signup-button" onClick={HandleSubmit}>
          Create Organisation
        </button>
      </form>
    </div>
  );
};
